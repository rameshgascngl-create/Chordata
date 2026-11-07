#!/usr/bin/env python3
"""Fail closed on wrong lesson mapping, missing/damaged PNG, and false QA approval."""
from pathlib import Path
import hashlib,json,collections,struct
ROOT=Path(__file__).resolve().parents[1];a=ROOT/'app/src/main/assets'; p=a/'pencil_plates'
registry=json.loads((a/'figure_slots.json').read_text())['slots']
assert len(registry)==64 and len({x['id'] for x in registry})==64
slots={x['id']:x for x in registry}
pack=json.loads((a/'chordata_content.json').read_text());topics={t['id']:t for unit in pack['units'] for t in unit['topics']}
m=json.loads((p/'manifest.json').read_text());fs=m['figures'];keys=[]
for x in fs:
    id=x['diagramId']; assert id in slots,('orphan',id)
    s=slots[id];t=topics[s['topicId']]
    assert 1<=s['page']<=len(t['sections']) and t['sections'][s['page']-1]['key']==s['sectionKey']
    assert x['lang'] in ('en','ta','shared')
    k=(id,x['lang']);assert k not in keys,('duplicate',k);keys.append(k)
    rel=Path(x['path'])
    assert (not rel.is_absolute() and rel.parts[0]=='pencil_plates'
            and len(rel.parts)==2 and rel.name.endswith('.png')
            and rel.name not in ('.','..')),('noncanonical pencil asset path',x['path'])
    f=a/rel;assert f.is_file(),('missing',f)
    b=f.read_bytes();assert len(b)>9000 and b[:8]==bytes.fromhex('89504e470d0a1a0a')
    w,h=struct.unpack('>II',b[16:24]);assert w>=1200 and h>=600,(f,w,h)
    assert hashlib.sha256(b).hexdigest()==x['sha256'],('sha256 mismatch',f)
    assert len(b)==x['size']
    assert x.get('author') and x.get('reviewStatus','').startswith('PROVISIONAL_')
    if x.get('sourceUrl'):
        assert x.get('license') and x['sourceUrl'].startswith('https://')
    if x.get('referenceUrls'):
        assert all(url.startswith('https://') for url in x['referenceUrls'])
    if x.get('svgMaster'):
        source=ROOT/x['svgMaster']
        assert source.is_file(), ('missing svg master',source)
        assert hashlib.sha256(source.read_bytes()).hexdigest()==x['svgSha256'], ('svg master modified',source)
        assert all(x.get(k) for k in ('topicId','page','sectionKey','learningObjective','referenceUrls')), ('missing academic traceability',id)
        assert x['topicId']==s['topicId'] and x['page']==s['page'] and x['sectionKey']==s['sectionKey'], ('wrong lesson section',id)
byid=collections.defaultdict(set)
for id,lang in keys:byid[id].add(lang)
assert len(byid)<=64
# Rendering shows English-labelled plates in English and Tamil, with shared fallback.
for id,languages in byid.items():
    assert 'en' in languages or 'shared' in languages,('no English/shared asset',id)
assert not any(s['status']=='ACADEMICALLY_APPROVED' for s in registry)
source=(ROOT/'app/src/main/java/in/gasc/zoology/chordata/ui/FigureGallery.kt').read_text()
assert 'pencilPlates[slot.id to "en"] ?: pencilPlates[slot.id to "shared"]' in source
assert 'tamil-label-review-' not in source
assert 'pencilPlates[slot.id to language]' not in source
print(f'PASS: {len(byid)}/64 distinct lesson slots populated with registered provisional pencil drawings ({64-len(byid)} remain)')
print(f'PASS: {len(fs)} manifest variants; all source files, 1200px sizes, SHA-256, and page/section links validated')
print('PASS: English diagram labels are used in both English and Tamil reading modes')
print('HOLD: no scientific approval and no device/emulator acceptance evidenced')
