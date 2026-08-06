#!/usr/bin/env python3
"""Update Hermes Agent contribution badges + table in README.md.

v2 — Separates Issues from PRs for accurate counting.
Fetches labels for richer contribution context.
Distinguishes "Author" vs "Participant" role per entry.
"""
import json, os, re, urllib.parse, urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN", "")
USER = "vollegrewar"
REPO = "NousResearch/hermes-agent"
README = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md"
)

GRAPHQL = "https://api.github.com/graphql"
REST = "https://api.github.com"

QUERY = """\
query($cursor: String) {
  user(login: "%s") {
    issueComments(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        repository { nameWithOwner }
        issue   { number title state createdAt labels(first:5) { nodes { name } } }
        pullRequest { number title state createdAt labels(first:5) { nodes { name } } }
      }
    }
  }
}
""" % (USER,)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def api_post(payload):
    req = urllib.request.Request(GRAPHQL, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def api_get(path):
    req = urllib.request.Request(f"{REST}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fmt_labels(item):
    """Extract top-3 label names from a REST or GraphQL item node."""
    labels_node = item.get("labels")
    if not labels_node:
        return "-"
    if isinstance(labels_node, list):
        # REST format: [{"name":"P1"}, ...]
        names = [l["name"] for l in labels_node if isinstance(l, dict)]
    else:
        # GraphQL format: {"nodes":[{"name":"P1"}, ...]}
        nodes = labels_node.get("nodes", []) if isinstance(labels_node, dict) else []
        names = [n["name"] for n in nodes if isinstance(n, dict)]
    return ", ".join(names[:3]) if names else "-"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # ---- 1. GraphQL: every comment by the user (cross-repo) ---------------
    contributed = {}  # issue_num → info dict
    cursor = None
    for _ in range(30):  # safety cap: 30 pages × 100 = 3000 comments
        data = api_post({"query": QUERY, "variables": {"cursor": cursor}})
        if "errors" in data:
            raise RuntimeError(f"GraphQL errors: {data['errors']}")
        conn = data["data"]["user"]["issueComments"]
        for node in conn["nodes"]:
            if node.get("repository", {}).get("nameWithOwner") != REPO:
                continue
            it = node.get("issue") or node.get("pullRequest")
            if not it:
                continue
            contributed[it["number"]] = {
                "number": it["number"],
                "title": it["title"],
                "state": it["state"],
                "created": it["createdAt"],
                "is_pr": bool(node.get("pullRequest")),
                "labels": fmt_labels(it),
            }
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]

    # ---- 2. REST: authored items (may have zero comments) -----------------
    q = urllib.parse.quote(f"author:{USER} repo:{REPO}")
    authored_resp = api_get(f"/search/issues?q={q}&per_page=100")
    authored_items = authored_resp.get("items", [])

    # Separate authored Issues from authored PRs
    authored_issues = [it for it in authored_items if "pull_request" not in it]
    authored_prs = [it for it in authored_items if "pull_request" in it]

    # Merge authored items into contributed (enrich with labels)
    authored_nums = set()
    for it in authored_items:
        num = it["number"]
        authored_nums.add(num)
        if num not in contributed:
            contributed[num] = {
                "number": num,
                "title": it["title"],
                "state": it["state"],
                "created": it["created_at"],
                "is_pr": "pull_request" in it,
                "labels": fmt_labels(it),
            }
        else:
            # Already there from comments; backfill labels if missing
            if contributed[num].get("labels") == "-":
                contributed[num]["labels"] = fmt_labels(it)

    # Tag role: "Author" if the user opened it, else "Participant"
    for num, info in contributed.items():
        info["role"] = "Author" if num in authored_nums else "Participant"

    # Sort by creation date, newest first
    rows_sorted = sorted(
        contributed.values(), key=lambda x: x["created"], reverse=True
    )

    # ---- 3. Counts --------------------------------------------------------
    issues_count = len(authored_issues)
    pr_reviews_count = len([r for r in contributed.values() if r["is_pr"]])
    participated_count = len(rows_sorted)

    # ---- 4. Badges --------------------------------------------------------
    badge_issues = (
        f"[![Issues](https://img.shields.io/badge/Issues-{issues_count}-blue"
        f"?logo=github&logoColor=white)]"
        f"(https://github.com/{REPO}/issues?q=author%3A{USER})"
    )
    badge_pr_reviews = (
        f"[![PR Reviews](https://img.shields.io/badge/PR_Reviews-{pr_reviews_count}-brightgreen"
        f"?logo=github&logoColor=white)]"
        f"(https://github.com/{REPO}/pulls?q=involves%3A{USER})"
    )
    badge_participated = (
        f"[![Participated](https://img.shields.io/badge/Participated-{participated_count}-orange"
        f"?logo=github&logoColor=white)]"
        f"(https://github.com/{REPO}/issues?q=involves%3A{USER})"
    )
    badges = "\n".join([badge_issues, badge_pr_reviews, badge_participated])

    # ---- 5. Table ---------------------------------------------------------
    header = "| # | Type | Role | Labels | Title | Status |"
    sep = "|--|------|------|--------|-------|--------|"
    rows = [header, sep]
    for r in rows_sorted:
        typ = "PR" if r["is_pr"] else "Issue"
        state = "🟢 Open" if str(r["state"]).lower() == "open" else "🔴 Closed"
        role = r.get("role", "Participant")
        labels = r.get("labels", "-")
        title = r["title"].replace("|", "/")
        url = f"https://github.com/{REPO}/{'pull' if r['is_pr'] else 'issues'}/{r['number']}"
        rows.append(
            f"| [#{r['number']}]({url}) | {typ} | {role} | {labels} | {title} | {state} |"
        )
    table = "\n".join(rows)

    # ---- 6. Update README.md markers -------------------------------------
    with open(README, encoding="utf-8") as f:
        text = f.read()

    text = re.sub(
        r"<!-- CONTRIB_BADGES -->.*?<!-- /CONTRIB_BADGES -->",
        f"<!-- CONTRIB_BADGES -->\n{badges}\n<!-- /CONTRIB_BADGES -->",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"<!-- CONTRIB_TABLE -->.*?<!-- /CONTRIB_TABLE -->",
        f"<!-- CONTRIB_TABLE -->\n{table}\n<!-- /CONTRIB_TABLE -->",
        text,
        flags=re.S,
    )

    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    print(
        f"OK: issues={issues_count} pr_reviews={pr_reviews_count} "
        f"participated={participated_count} rows={len(rows_sorted)}"
    )
    for r in rows_sorted:
        role = r.get("role", "?")
        typ = "PR" if r["is_pr"] else "Issue"
        print(f"  #{r['number']} [{role}] ({typ})  {r['title'][:70]}")


if __name__ == "__main__":
    main()
