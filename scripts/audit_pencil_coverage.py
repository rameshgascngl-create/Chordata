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
# The project owner's permission for minor AI defects is not anatomical approval.
# A flagged material error must never be promoted by a blanket green tick.
held=[f for f in fs if f.get('scientificRiskHold')=='MATERIAL_ANATOMY_ERROR']
assert len(held)==1 and held[0]['diagramId']=='u5-rabbit-endoskeleton' and held[0]['lang']=='ta'
assert held[0].get('aiQaIntegrationDecision')=='HOLD_MATERIAL_ANATOMY_ERROR'
assert held[0].get('ownerQaAcceptance')=='OWNER_APPROVAL_EXCLUDED_MATERIAL_ANATOMY_ERROR_2026-11-11'
assert not any(f.get('scientificRiskHold') and f.get('aiQaIntegrationDecision')=='GREEN_TICK_ALLOW_PROVISIONAL_QA_USE' for f in fs)

# Pedagogical utility is a separate gate from PNG integrity. These user-
# rejected shapes remain in source control for provenance but cannot be used
# as anatomy/species teaching images in either language.
noninstructional_ids = {
    'u4-snakes-india-big-four-identification',
    'u5-flight-adaptations-flight-muscles',
    'u5-rabbit-sense-organs',
    'u5-egg-laying-mammals-monotreme-reproduction',
    'u5-marsupials-marsupial-life-history',
    'u5-aquatic-mammals-aquatic-mammal-groups',
}
rejected = [x for x in fs if x.get('pedagogicStatus') ==
            'WITHHELD_BIOLOGICALLY_NON_INSTRUCTIVE_2026-11-12']
assert {x['diagramId'] for x in rejected} == noninstructional_ids, (
    'Six user-rejected figures must remain suppressed until verified replacement')
assert len(rejected) == 6 and len({x['diagramId'] for x in rejected}) == 6
assert all(x.get('visualReview') == 'USER_REJECTED_REPLACEMENT_REQUIRED'
           and x.get('pedagogicReason') and x.get('reviewStatus', '').startswith('PROVISIONAL_')
           for x in rejected), 'Symbolic non-instructional diagrams must not reappear as valid plates'
print('PASS: six pedagogically rejected figures are withheld; original PNGs and credits retained')

# Rendering shows English-labelled plates in English and Tamil, with shared fallback.
for id,languages in byid.items():
    assert 'en' in languages or 'shared' in languages,('no English/shared asset',id)
assert not any(s['status']=='ACADEMICALLY_APPROVED' for s in registry)
source=(ROOT/'app/src/main/java/in/gasc/zoology/chordata/ui/FigureGallery.kt').read_text()
assert 'selectedPlateNeedsReplacement(pencilPlates, slot.id, lang)' in source, 'Image rejection must follow the displayed language variant'
assert 'tamil-label-review-' not in source
assert 'pencilPlates[slot.id to language]' not in source

# Original 1904 accessory respiratory anatomy: three sourced plates, not
# drawings generated for the app. Verify bit-for-bit Git object identity.
historic=json.loads((a/'historical_figures/sources.json').read_text(encoding='utf-8'))
assert historic['registeredDiagramId']=='u2-accessory-respiration-accessory-organs-comparison'
assert historic['topicId']=='u2-accessory-respiration' and historic['page']==2
assert [x['figure'] for x in historic['figures']]==[169,171,172]
assert [x['originalCaptionTaxon'] for x in historic['figures']]==[
    'Anabas scandens','Clarias','Saccobranchus singio']
for image in historic['figures']:
    f=a/image['path']
    data=f.read_bytes()
    assert data.startswith(bytes.fromhex('ffd8ff')), ('invalid sourced JPEG',f)
    assert len(data)==image['byteLength'],('size differs from published source',f)
    git_sha=hashlib.sha1(('blob '+str(len(data))).encode()+bytes([0])+data).hexdigest()
    assert git_sha==image['gitBlobSha1'],('original source image modified',f)
    assert image['sourceImageUrl'].startswith(
        'https://github.com/GITenberg/The-Cambridge-natural-history-Vol-07-of-10_73702/')
assert 'HistoricalAirBreathingGallery(lang)' in source
assert 'historical-accessory-figure-' in source
print('PASS: original Cambridge 1904 Figs 169/171/172 preserved and rendered in registered lesson')

print(f'PASS: {len(byid)}/64 distinct lesson slots populated with registered provisional pencil drawings ({64-len(byid)} remain)')
print(f'PASS: {len(fs)} manifest variants; all source files, 1200px sizes, SHA-256, and page/section links validated')
print('PASS: English diagram labels are used in both English and Tamil reading modes')
print('HOLD: no scientific approval and no device/emulator acceptance evidenced')
