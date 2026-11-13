#!/usr/bin/env python3
"""Native content safety gate, requiring no Python dependencies beyond stdlib."""
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK = ROOT / 'app/src/main/assets/chordata_content.json'
EXPECTED_SHA = 'c1e31440c211f9c6ce90ccde99ba62f418b8e857f798df489ed9761c2bd39c1a'
raw = PACK.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA, 'Revised syllabus pack changed without academic review and updated digest'
data = json.loads(raw)
units = data['units']
topics = [t for u in units for t in u['topics']]
assert len(units) == 5 and len(topics) == 39
assert [len(u['topics']) for u in units] == [5,11,6,6,11], 'Chapter-unit allocation must follow the photographed syllabus'
assert len({x['id'] for x in topics}) == 39
assert sum(len(x['sections']) for x in topics) == 200, 'Expanded bilingual lesson sections missing'
assert sum(len(x['quiz']) for x in topics) == 117
assert sum(len(x.get('diagramIds', [])) for x in topics) == 64
assert sum(len(x.get('diagramIds', [])) for x in topics if 'scoliodon' in x['id']) == 5
# The accepted original topic/figure anchors are stable; only bilingual content
# and grouping have changed. Mandate substantive coverage in both languages.
required_coverage = {
    'u1-general-characters': ('chordate-nonchordate-comparison', 'prochordate-subphyla'),
    'u1-hemichordata': ('balanoglossus-organ-systems',),
    'u1-urochordata': ('ascidia-complete-type-study',),
    'u1-cephalochordata': ('amphioxus-complete-type-study',),
    'u2-pisces-classification': ('early-jawed-fish-lineages', 'cartilaginous-bony-subgroups', 'fossil-origin-of-fishes'),
    'u2-scoliodon': ('scoliodon-internal-systems',),
    'u2-accessory-respiration': ('swim-bladder-function-types',),
    'u3-amphibia-classification': ('historical-fossil-amphibian-groups', 'lepospondyl-lissamphibian-orders'),
    'u3-rana': ('rana-circulation-heart', 'rana-excretory-and-reproduction'),
    'u4-calotes': ('calotes-heart-circulation', 'calotes-respiratory-urinary-reproduction'),
    'u4-origin-extinct': ('reptile-fossils-synapsids', 'terrestrialisation-amniote-egg'),
    'u5-aves-classification': ('archaeornithes-neornithes', 'origin-of-birds-theropods'),
    'u5-columba': ('pigeon-digestive-respiratory', 'pigeon-circulation-excretion'),
    'u5-mammalia-classification': ('mammalian-orders-and-radiation',),
    'u5-rabbit': ('rabbit-digestion-cecotrophy', 'rabbit-cardiovascular-reproduction'),
    'u5-dentition': ('dental-formula-comparison',),
    'u3-adaptive-features': ('anura-special-adaptations', 'urodela-special-adaptations', 'apoda-special-adaptations'),
    'u4-reptilia-classification': ('reptilian-historical-subclasses', 'living-orders-and-archosauria', 'chelonia-turtle-anatomy', 'sphenodon-rhynchocephalia', 'crocodylia-archosaur-special'),
    'u5-marsupials': ('marsupial-orders-comparison',),
}
all_topics = {t['id']:t for t in topics}
for topic_id, keys in required_coverage.items():
    assert topic_id in all_topics
    present = {section['key'] for section in all_topics[topic_id]['sections']}
    assert set(keys) <= present, ('Missing syllabus depth sections', topic_id)
assert {t['id'] for t in units[1]['topics']} >= {
    'u1-vertebrata-characters', 'u1-vertebrata-classification', 'u1-agnatha'
}, 'Vertebrata and Agnatha must be taught in Unit II'
for topic in topics:
    keys = [section['key'] for section in topic['sections']]
    assert len(set(keys)) == len(keys), ('Duplicate section keys', topic['id'])
    en_words = sum(len(s['body']['en'].split()) for s in topic['sections'])
    ta_words = sum(len(s['body']['ta'].split()) for s in topic['sections'])
    assert en_words >= 200 and ta_words >= 150, ('Insufficient bilingual lesson depth', topic['id'], en_words, ta_words)
    for section in topic['sections']:
        assert all(section.get('heading', {}).get(lang) and section.get('body', {}).get(lang)
                   for lang in ('en','ta')), ('Incomplete section', topic['id'], section.get('key'))
        assert re.search('[\\u0b80-\\u0bff]', section['body']['ta']), ('Non-Tamil section', topic['id'])
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
print('PASS: academically expanded five-unit bilingual content SHA-256', EXPECTED_SHA)
print('PASS: 39 syllabus chapters, 200 bilingual sections, 117 quizzes and 64 preserved figure anchors')
print('PASS: native-only source; no Internet permission; no backup/cleartext')
print('PASS: page progression, scroll reset, saved navigation state hooks present')
