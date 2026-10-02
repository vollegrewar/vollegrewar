#!/usr/bin/env python3
"""Refresh public upstream issues, PRs, comment participation and reviews.

Exclude own/private repositories. Preserve roles and distinguish merged/closed.
Use Actions GITHUB_TOKEN or local authenticated gh; fail before writes on API errors.
"""
import html
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

USER = 'vollegrewar'
ROOT = Path(__file__).resolve().parents[1]
FIELDS = 'number title state createdAt url repository { nameWithOwner isPrivate owner { login } }'


def graphql(query, cursor=None):
    payload = {'query': query, 'variables': {'cursor': cursor}}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        req = urllib.request.Request('https://api.github.com/graphql', data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.load(response)
    else:
        result = json.loads(subprocess.run(['gh', 'api', 'graphql', '--input', '-'],
            input=json.dumps(payload), capture_output=True, text=True, encoding='utf-8', check=True, timeout=60).stdout)
    if result.get('errors'):
        raise RuntimeError(result['errors'])
    return result['data']


def pages(connection, fields):
    query = f'query($cursor: String) {{ user(login: "{USER}") {{ {connection}(first:100, after:$cursor) {{ pageInfo {{ hasNextPage endCursor }} nodes {{ {fields} }} }} }} }}'
    cursor = None
    while True:
        result = graphql(query, cursor)['user'][connection]
        yield from result['nodes']
        if not result['pageInfo']['hasNextPage']:
            break
        cursor = result['pageInfo']['endCursor']


def reviewed_prs():
    query = f'query($cursor:String) {{ search(query:"reviewed-by:{USER} is:pr is:public", type:ISSUE, first:100, after:$cursor) {{ pageInfo {{ hasNextPage endCursor }} nodes {{ ... on PullRequest {{ {FIELDS} }} }} }} }}'
    cursor = None
    while True:
        result = graphql(query, cursor)['search']
        yield from result['nodes']
        if not result['pageInfo']['hasNextPage']:
            break
        cursor = result['pageInfo']['endCursor']


def collect():
    items = {}
    def add(item, kind, role):
        if not item or not item.get('repository'):
            return
        repo = item['repository']
        if repo['isPrivate'] or repo['owner']['login'].lower() == USER.lower():
            return
        entry = items.setdefault(item['url'], {**item, 'kind':kind, 'roles':set()})
        entry['roles'].add(role)
    for connection, kind in (('issues','Issue'), ('pullRequests','PR')):
        for item in pages(connection, FIELDS):
            add(item, kind, 'Author')
    for comment in pages('issueComments', f'issue {{ {FIELDS} }} pullRequest {{ {FIELDS} }}'):
        if comment.get('pullRequest'):
            add(comment['pullRequest'], 'PR', 'Participant')
        else:
            add(comment.get('issue'), 'Issue', 'Participant')
    for item in reviewed_prs():
        add(item, 'PR', 'Reviewer')
    return sorted(items.values(), key=lambda item:item['createdAt'], reverse=True)


def status(item):
    return {'OPEN':'🟢 Open', 'MERGED':'🟣 Merged', 'CLOSED':'⚪ Closed'}[item['state']]


def counts(items):
    authored = [item for item in items if 'Author' in item['roles']]
    return {'issues':sum(item['kind']=='Issue' for item in authored),
        'prs':sum(item['kind']=='PR' for item in authored),
        'merged':sum(item['kind']=='PR' and item['state']=='MERGED' for item in authored), 'involved':len(items)}


def block(text, marker, value):
    pattern = rf'<!-- {marker} -->.*?<!-- /{marker} -->'
    if len(re.findall(pattern, text, flags=re.S)) != 1:
        raise ValueError(f'Expected exactly one {marker} block')
    return re.sub(pattern, lambda _:f'<!-- {marker} -->\n{value}\n<!-- /{marker} -->', text, flags=re.S)


def table(items):
    lines = ['| Contribution | Role | Title | Status |', '|---|---|---|---|']
    for item in items:
        roles = [role for role in ('Author','Reviewer','Participant') if role in item['roles']]
        if 'Author' in roles and 'Participant' in roles:
            roles.remove('Participant')
        title = html.escape(' '.join(item['title'].split())).replace('|','&#124;')
        title = re.sub(r'([\\`*_\[\]])', r'\\\1', title)
        repo = item['repository']['nameWithOwner']
        lines.append(f"| [{repo} #{item['number']}]({item['url']}) · {item['kind']} | {' + '.join(roles)} | {title} | {status(item)} |")
    return '\n'.join(lines)


def svg(items):
    c = counts(items)
    cells = ''
    for i,(key,label) in enumerate((('issues','AUTHORED ISSUES'),('prs','AUTHORED PRS'),('merged','MERGED PRS'),('involved','TRACKED THREADS'))):
        x = 32+i*218
        cells += f'<text x="{x}" y="91" fill="#edf0ea" font-size="44">{c[key]}</text><text x="{x}" y="124" fill="#a7d7cb" font-size="12" letter-spacing="1">{label}</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="168" viewBox="0 0 900 168" role="img" aria-labelledby="title desc">
<title id="title">Public upstream contribution snapshot</title><desc id="desc">{c['issues']} authored issues, {c['prs']} authored PRs, {c['merged']} merged PRs, {c['involved']} unique tracked threads. Own and private repos excluded.</desc>
<rect width="900" height="168" rx="12" fill="#172523"/><g font-family="Consolas, monospace"><text x="32" y="30" fill="#99aba5" font-size="11" letter-spacing="2">PUBLIC UPSTREAM / GITHUB API</text>{cells}<text x="32" y="153" fill="#99aba5" font-size="10">AUTHORED + COMMENTS + REVIEWS · UNIQUE THREADS · OWN / PRIVATE REPOS EXCLUDED</text></g></svg>\n'''


def main():
    items = collect()
    if not items:
        raise RuntimeError('No contributions returned; refusing to erase log')
    readme = ROOT/'README.md'
    text = readme.read_text(encoding='utf-8')
    hermes = [item for item in items if item['repository']['nameWithOwner']=='NousResearch/hermes-agent']
    c = counts(items)
    labels = (('issues','Authored issues','a7d7cb'),('prs','Authored PRs','b6c7ed'),('merged','Merged PRs','e0b777'),('involved','Tracked threads','b8c4cd'))
    badges = '\n'.join(f"![{label}: {c[key]}](https://img.shields.io/badge/{label.replace(' ','_')}-{c[key]}-{color}?style=flat-square)" for key,label,color in labels)
    text = block(text,'CONTRIB_BADGES',badges)
    text = block(text,'CONTRIB_TABLE',table(hermes))
    text = block(text,'CROSS_CONTRIB_TABLE',table([item for item in items if item not in hermes]))
    lookup = {item['url']:item for item in items}
    text = re.sub(r'<!-- STATUS (https://github.com/[^ ]+) -->.*?<!-- /STATUS -->',
        lambda m:f'<!-- STATUS {m[1]} -->{status(lookup[m[1]])}<!-- /STATUS -->',text)
    snapshot = [{**item,'roles':sorted(item['roles'])} for item in items]
    (ROOT/'assets').mkdir(exist_ok=True)
    readme.write_text(text,encoding='utf-8',newline='\n')
    (ROOT/'assets/contributions.svg').write_text(svg(items),encoding='utf-8',newline='\n')
    (ROOT/'assets/contributions.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'[OK] Public upstream: {c}; Hermes threads: {len(hermes)}')


if __name__=='__main__':
    main()
