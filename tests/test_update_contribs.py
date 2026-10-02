import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('updater', ROOT / 'scripts/update_contribs.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def item(url, owner='upstream', private=False, state='OPEN'):
    return {'url':url, 'number':1, 'title':'Title | [link](url) <script> **bold**',
        'state':state, 'createdAt':'2026-10-02T00:00:00Z',
        'repository':{'nameWithOwner':f'{owner}/repo', 'isPrivate':private, 'owner':{'login':owner}}}


class RefreshTests(unittest.TestCase):
    def test_public_scope_dedup_and_roles(self):
        pr = item('https://github.com/upstream/repo/pull/1', state='MERGED')
        issue = item('https://github.com/upstream/repo/issues/1')
        def pages(connection, fields):
            return {'issues':[issue, item('private', private=True), item('own',owner='vollegrewar')],
                'pullRequests':[pr], 'issueComments':[{'pullRequest':pr}, {'pullRequest':pr}, {'issue':issue}]}[connection]
        with patch.object(m,'pages',side_effect=pages), patch.object(m,'reviewed_prs',return_value=[pr]):
            result = m.collect()
        self.assertEqual(m.counts(result), {'issues':1,'prs':1,'merged':1,'involved':2})
        self.assertEqual(next(x for x in result if x['kind']=='PR')['roles'], {'Author','Participant','Reviewer'})
        self.assertIn('Merged', m.table(result))
        self.assertNotIn('<script>', m.table(result))
        self.assertNotIn('[link](url)', m.table(result))
        ET.fromstring(m.svg(result))

    def test_missing_duplicate_markers_fail(self):
        for text in ('missing', '<!-- X --><!-- /X -->'*2):
            with self.assertRaises(ValueError): m.block(text,'X','new')
        self.assertEqual(m.block('<!-- X -->old<!-- /X -->','X',r'new\1'), '<!-- X -->\nnew\\1\n<!-- /X -->')

    def test_failed_api_never_erases_readme(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'README.md').write_text('preserve',encoding='utf-8')
            with patch.object(m,'ROOT',root), patch.object(m,'collect',side_effect=RuntimeError('API failed')):
                with self.assertRaises(RuntimeError): m.main()
            self.assertEqual((root/'README.md').read_text(), 'preserve')

    def test_same_snapshot_is_idempotent(self):
        actual = json.loads((ROOT/'assets/contributions.json').read_text(encoding='utf-8'))
        for entry in actual: entry['roles']=set(entry['roles'])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'README.md').write_text((ROOT/'README.md').read_text(encoding='utf-8'),encoding='utf-8')
            with patch.object(m,'ROOT',root), patch.object(m,'collect',return_value=actual):
                m.main()
                before = {p.name:p.read_bytes() for p in root.rglob('*') if p.is_file()}
                m.main()
                after = {p.name:p.read_bytes() for p in root.rglob('*') if p.is_file()}
                self.assertEqual(before,after)


if __name__=='__main__': unittest.main()
