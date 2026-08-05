#!/usr/bin/env python3
"""Update Hermes Agent contribution badges + table in README.md.

Uses GraphQL (repository.issueComments) to capture BOTH issue and PR comments,
plus REST search for issues authored by the user. GitHub's `involves:` search
does NOT index PR comments, so GraphQL is required for the full record.
"""
import json
import os
import re
import urllib.parse
import urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN", "")
USER = "vollegrewar"
OWNER = "NousResearch"
REPO_NAME = "hermes-agent"
REPO = f"{OWNER}/{REPO_NAME}"
README = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")

GRAPHQL = "https://api.github.com/graphql"
REST = "https://api.github.com"

ISSUES_QUERY = """
query($cursor: String) {
  user(login: "%s") {
    issueComments(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        repository { nameWithOwner }
        issue { number title state createdAt }
        pullRequest { number title state createdAt }
      }
    }
  }
}
""" % (USER,)


def api_post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def api_get(path):
    req = urllib.request.Request(f"{REST}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    # 1) All comments by the user (cross-repo), filter to the Hermes repo
    commented = {}
    cursor = None
    for _ in range(30):  # safety cap: 30 pages x 100 = 3000 comments
        data = api_post(GRAPHQL, {"query": ISSUES_QUERY, "variables": {"cursor": cursor}})
        if "errors" in data:
            raise RuntimeError(f"GraphQL errors: {data['errors']}")
        conn = data["data"]["user"]["issueComments"]
        for node in conn["nodes"]:
            if node.get("repository", {}).get("nameWithOwner") != REPO:
                continue
            it = node.get("issue") or node.get("pullRequest")
            if not it:
                continue
            commented[it["number"]] = {
                "number": it["number"],
                "title": it["title"],
                "state": it["state"],
                "created": it["createdAt"],
                "is_pr": bool(node.get("pullRequest")),
            }
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]

    # 2) Issues authored by the user (may have zero comments)
    q = urllib.parse.quote(f"author:{USER} repo:{REPO}")
    authored = api_get(f"/search/issues?q={q}&per_page=100")
    for it in authored.get("items", []):
        commented[it["number"]] = {
            "number": it["number"],
            "title": it["title"],
            "state": it["state"],
            "created": it["created_at"],
            "is_pr": bool(it.get("pull_request")),
        }

    rows_sorted = sorted(commented.values(), key=lambda x: x["created"], reverse=True)
    created_count = authored.get("total_count", 0)
    involved_count = len(rows_sorted)

    badges = "\n".join([
        f"[![Hermes Issues Created](https://img.shields.io/badge/Hermes_Issues_Created-{created_count}-blue)](https://github.com/{REPO}/issues?q=author%3A{USER})",
        f"[![Hermes Discussions](https://img.shields.io/badge/Hermes_Discussions-{involved_count}-green)](https://github.com/{REPO}/issues?q=involves%3A{USER})",
    ])

    rows = []
    for r in rows_sorted:
        typ = "PR" if r["is_pr"] else "Issue"
        state = "🟢 Open" if str(r["state"]).lower() == "open" else "🔴 Closed"
        title = r["title"].replace("|", "/")
        rows.append(f"| [#{r['number']}](https://github.com/{REPO}/{'pull' if r['is_pr'] else 'issues'}/{r['number']}) | {typ} | {title} | {state} |")
    table = "\n".join(rows)

    with open(README, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"<!-- CONTRIB_BADGES -->.*?<!-- /CONTRIB_BADGES -->",
                  f"<!-- CONTRIB_BADGES -->\n{badges}\n<!-- /CONTRIB_BADGES -->",
                  text, flags=re.S)
    text = re.sub(r"<!-- CONTRIB_TABLE -->.*?<!-- /CONTRIB_TABLE -->",
                  f"<!-- CONTRIB_TABLE -->\n{table}\n<!-- /CONTRIB_TABLE -->",
                  text, flags=re.S)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"OK: created={created_count} involved={involved_count} rows={len(rows_sorted)}")
    for r in rows_sorted:
        print(f"  #{r['number']} ({'PR' if r['is_pr'] else 'Issue'}) {r['title'][:50]}")


if __name__ == "__main__":
    main()
