#!/usr/bin/env python3
"""Update Hermes Agent contribution badges + full log in README.md.

v3 — Badge semantics fixed: authored Issues / authored PRs / total involved.
Table slimmed to [# / Type / Role / Title / Status]; the labels column was
noise on the profile and is gone. The curated highlights table lives OUTSIDE
the markers and is never touched by this script.
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
        issue   { number title state createdAt }
        pullRequest { number title state createdAt }
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

    # Merge authored items into contributed
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
            }

    # Tag role: "Author" if the user opened it, else "Participant"
    for num, info in contributed.items():
        info["role"] = "Author" if num in authored_nums else "Participant"

    # Sort by creation date, newest first
    rows_sorted = sorted(
        contributed.values(), key=lambda x: x["created"], reverse=True
    )

    # ---- 3. Counts --------------------------------------------------------
    issues_count = len(authored_issues)
    pr_count = len(authored_prs)
    involved_count = len(rows_sorted)

    # ---- 4. Badges --------------------------------------------------------
    badge_issues = (
        f"[![Issues](https://img.shields.io/badge/Issues-{issues_count}-blue"
        f"?logo=github&logoColor=white)]"
        f"(https://github.com/{REPO}/issues?q=author%3A{USER})"
    )
    badge_prs = (
        f"[![PRs](https://img.shields.io/badge/PRs-{pr_count}-brightgreen"
        f"?logo=github&logoColor=white)]"
        f"(https://github.com/{REPO}/pulls?q=author%3A{USER})"
    )
    badge_involved = (
        f"[![Involved](https://img.shields.io/badge/Involved-{involved_count}-orange"
        f"?logo=github&logoColor=white)]"
        f"(https://github.com/{REPO}/issues?q=involves%3A{USER})"
    )
    badges = "\n".join([badge_issues, badge_prs, badge_involved])

    # ---- 5. Table ---------------------------------------------------------
    header = "| # | Type | Role | Title | Status |"
    sep = "|--|------|------|-------|--------|"
    rows = [header, sep]
    for r in rows_sorted:
        typ = "PR" if r["is_pr"] else "Issue"
        state = "🟢 Open" if str(r["state"]).lower() == "open" else "🔴 Closed"
        role = r.get("role", "Participant")
        title = r["title"].replace("|", "/")
        url = f"https://github.com/{REPO}/{'pull' if r['is_pr'] else 'issues'}/{r['number']}"
        rows.append(
            f"| [#{r['number']}]({url}) | {typ} | {role} | {title} | {state} |"
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
        f"OK: authored_issues={issues_count} authored_prs={pr_count} "
        f"involved={involved_count} rows={len(rows_sorted)}"
    )
    for r in rows_sorted:
        role = r.get("role", "?")
        typ = "PR" if r["is_pr"] else "Issue"
        print(f"  #{r['number']} [{role}] ({typ})  {r['title'][:70]}")


if __name__ == "__main__":
    main()
