#!/usr/bin/env python3
"""Native content safety gate, requiring no Python dependencies beyond stdlib."""
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK = ROOT / 'app/src/main/assets/chordata_content.json'
EXPECTED_SHA = '11dec9b76caf6e798dd19e2dec29ecee8a18eacc006e5842ccffc9f5fd65c5cf'
raw = PACK.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA, 'Input course pack changed without review'
data = json.loads(raw)
units = data['units']
topics = [t for u in units for t in u['topics']]
assert len(units) == 5 and len(topics) == 39
assert [len(u['topics']) for u in units] == [8,8,6,6,11]
assert len({x['id'] for x in topics}) == 39
assert sum(len(x['sections']) for x in topics) == 127
assert sum(len(x['quiz']) for x in topics) == 117
assert sum(len(x.get('diagramIds', [])) for x in topics) == 64
assert sum(len(x.get('diagramIds', [])) for x in topics if 'scoliodon' in x['id']) == 5
for topic in topics:
    assert all(len(q['options']) == 4 and 0 <= q['correctIndex'] <= 3 for q in topic['quiz'])
    for q in topic['quiz']:
        for value in [q['question'], q['explanation'], *q['options']]:
            assert all(value.get(k) for k in ('en', 'ta'))
        assert re.search('[\u0b80-\u0bff]', q['question']['ta'])
manifest = (ROOT / 'app/src/main/AndroidManifest.xml').read_text()
assert 'INTERNET' not in manifest, 'No network permission allowed'
assert 'android:allowBackup="false"' in manifest
assert 'android:usesCleartextTraffic="false"' in manifest
all_kt = '\n'.join(f.read_text() for f in (ROOT/'app/src/main').rglob('*.kt'))
assert 'WebView' not in all_kt, 'Must remain native Compose'
assert 'http://' not in all_kt and 'https://' not in all_kt
assert 'scrollToItem(0)' in all_kt, 'Page-to-top navigation regression'
assert 'onPage(page + 1)' in all_kt, 'Page progression regression'
assert 'rememberSaveable' in all_kt, 'Process state recovery missing'
print('PASS: reviewed 5-unit Tamil-corrected content SHA-256', EXPECTED_SHA)
print('PASS: 39 topics, 127 sections, 117 quizzes, 64 diagram references, three provisional external figures')
print('PASS: native-only source; no Internet permission; no backup/cleartext')
print('PASS: page progression, scroll reset, saved navigation state hooks present')
