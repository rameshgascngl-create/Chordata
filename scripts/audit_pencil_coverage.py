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
remaining_noninstructional_ids = {
    'u4-calotes-arterial-system',
}
verified_source_replacement_ids = {
    'u4-snakes-india-big-four-identification',
    'u5-flight-adaptations-flight-muscles',
    'u5-marsupials-marsupial-life-history',
}
rejected = [x for x in fs if x.get('pedagogicStatus') ==
            'WITHHELD_BIOLOGICALLY_NON_INSTRUCTIVE_2026-11-12']
assert {x['diagramId'] for x in rejected} == remaining_noninstructional_ids, (
    'Only the rejected Calotes heart diagram may remain withheld')
assert len(rejected) == 1
assert all(x.get('visualReview') == 'USER_REJECTED_REPLACEMENT_REQUIRED'
           and x.get('pedagogicReason') and x.get('reviewStatus', '').startswith('PROVISIONAL_')
           for x in rejected), 'Uncorrected symbolic diagrams must remain withheld'
replacements = [x for x in fs if x.get('pedagogicStatus') ==
                'REPLACED_WITH_CC_LICENSED_SOURCE_QA_PENDING_2026-11-12']
assert {x['diagramId'] for x in replacements} == verified_source_replacement_ids, (
    'Missing or invented sourced replacement for three reviewed lessons')
for x in replacements:
    assert x.get('visualReview') == 'SOURCED_TEACHING_FIGURE_QA_PROVISIONAL'
    assert x.get('sourceUrl', '').startswith('https://commons.wikimedia.org/wiki/File:')
    assert x.get('licenseUrl', '').startswith('https://creativecommons.org/licenses/by-sa/')
    assert x.get('sourceSha256') and all(len(h) == 64 for h in x['sourceSha256'])
    assert not x.get('svgMaster'), ('Retired symbolic SVG incorrectly presented as active source', x['diagramId'])
    assert x.get('retiredSchematicSha256') and x.get('retiredSchematicSvg')
    assert x.get('reviewStatus', '').startswith('PROVISIONAL_'), 'No false independent approval'
snake = next(x for x in replacements if x['diagramId'] == 'u4-snakes-india-big-four-identification')
assert len(snake['sourceUrls']) == 4 and len(snake['sourceSha256']) == 4
assert all('creativecommons.org/licenses/by-sa/4.0' in x for x in snake['originalLicences'])
# The newly installed Calotes photographic specimen is not an arterial plate.
calotes = next(v for v in fs if v['diagramId'] == 'u4-calotes-external')
assert calotes['lang'] == 'en'
assert calotes.get('visualReview') == 'SOURCED_REAL_SPECIMEN_PHOTO_QA_PROVISIONAL'
assert calotes.get('sourceUrl') == 'https://commons.wikimedia.org/wiki/File:Oriental_Lizard.jpg'
assert calotes.get('licenseUrl') == 'https://creativecommons.org/licenses/by-sa/4.0/'
old = calotes['retiredHistoricalPlate']
retired = ROOT / old['path']
assert retired.is_file() and hashlib.sha256(retired.read_bytes()).hexdigest() == old['sha256']
assert old['sha256'] == '5fcd2cc2ae68d0adda0b406934a9c07aa857bd53dbda19d99abdb5ef0cc14a2f'
rabbit = next(v for v in fs if v['diagramId'] == 'u5-rabbit-sense-organs')
assert rabbit['lang'] == 'en' and rabbit['path'] == 'pencil_plates/rabbit_senses_en.png'
assert rabbit.get('visualReview') == 'SOURCED_REAL_RABBIT_SENSORY_PHOTO_QA_PROVISIONAL'
assert rabbit.get('pedagogicStatus') == 'REPLACED_WITH_CC_LICENSED_RABBIT_SENSES_QA_PENDING_2026-11-12'
assert rabbit.get('sourceUrl') == 'https://commons.wikimedia.org/wiki/File:Side_view_of_the_head_of_a_pet_rabbit_in_Brussels_(DSCF0830).jpg'
assert rabbit.get('licenseUrl') == 'https://creativecommons.org/licenses/by/4.0/'
assert rabbit.get('author', '').startswith('Trougnouf (Benoit Brummer)')
assert len(rabbit.get('sourceSha256', [])) == 1 and len(rabbit['sourceSha256'][0]) == 64
assert not rabbit.get('svgMaster'), 'Retired symbolic rabbit artwork wrongly declared active'
for field,hashfield in (('retiredSchematicPng','retiredSchematicSha256'),
                        ('retiredSchematicSvg','retiredSchematicSvgSha256')):
    r = ROOT / rabbit[field]
    assert r.is_file() and hashlib.sha256(r.read_bytes()).hexdigest() == rabbit[hashfield]
assert rabbit['retiredSchematicSha256'] == '6f4a798edd974efc549163e09bb37727b49b26f77d507e50f9b6a4b628e2788f'
monotreme = next(v for v in fs if v['diagramId'] == 'u5-egg-laying-mammals-monotreme-reproduction')
assert monotreme['lang'] == 'shared'
assert monotreme['path'] == 'pencil_plates/platypus_reproduction.png'
assert monotreme.get('visualReview') == 'SOURCED_REAL_MONOTREME_SPECIMENS_AND_ANATOMY_QA_PROVISIONAL'
assert monotreme.get('pedagogicStatus') == 'REPLACED_WITH_CC_LICENSED_MONOTREME_SOURCE_QA_PENDING_2026-11-12'
assert len(monotreme.get('sourceUrls', [])) == len(monotreme.get('sourceSha256', [])) == 3
assert len(monotreme.get('originalLicences', [])) == 3
assert any('Cambridge_Natural_History_Mammalia_Fig_003.png' in u for u in monotreme['sourceUrls'])
assert any('Tachyglossus_aculeatus_baby_Museums_Victoria.jpg' in u for u in monotreme['sourceUrls'])
assert monotreme.get('licenseUrl') == 'https://creativecommons.org/licenses/by-sa/4.0/'
assert monotreme.get('retiredSchematicPng') and monotreme.get('retiredSchematicSha256')
archived = ROOT / monotreme['retiredSchematicPng']
assert archived.is_file() and hashlib.sha256(archived.read_bytes()).hexdigest() == monotreme['retiredSchematicSha256']
assert monotreme['retiredSchematicSha256'] == '5936652b851a5c474cf64db332a49736266039c6f6e8b9e6e507122de6ef0284'
assert 'not a chronological photographic life-cycle' in monotreme['keyEn']
marine = next(x for x in fs if x['diagramId'] == 'u5-aquatic-mammals-aquatic-mammal-groups')
assert marine['lang'] == 'en' and marine['path'] == 'pencil_plates/aquatic_mammal_lineages_en.png'
assert marine['visualReview'] == 'SOURCED_FOUR_AQUATIC_MAMMAL_PHOTOGRAPHS_QA_PROVISIONAL'
assert marine['pedagogicStatus'] == 'REPLACED_WITH_CC_LICENSED_AQUATIC_MAMMAL_PHOTOS_QA_PENDING_2026-11-12'
assert len(marine['sourceUrls']) == len(marine['sourceSha256']) == len(marine['originalLicences']) == 4
assert all(url.startswith('https://commons.wikimedia.org/wiki/File:') for url in marine['sourceUrls'])
assert all(len(h) == 64 for h in marine['sourceSha256'])
assert marine['originalLicences'] == [
    'https://creativecommons.org/licenses/by/2.0/',
    'https://creativecommons.org/licenses/by/4.0/',
    'https://creativecommons.org/licenses/by-sa/4.0/',
    'https://creativecommons.org/publicdomain/mark/1.0/',
]
assert marine.get('retiredSchematicSvg') and marine.get('retiredSchematicSvgSha256')
assert not marine.get('svgMaster') and not marine.get('svgSha256')
for oldpath, oldhash in (
    ('retiredSchematicPng', 'retiredSchematicSha256'),
    ('retiredSchematicSvg', 'retiredSchematicSvgSha256'),
):
    original = ROOT / marine[oldpath]
    assert original.is_file()
    assert hashlib.sha256(original.read_bytes()).hexdigest() == marine[oldhash]
assert marine['retiredSchematicSha256'] == 'a330620a0fb6d62fab65caf6c79fd50ee24a686c83bc3a49b034623bfbc987c3'
assert all(word in marine['keyEn'] for word in ('Cetacea', 'Sirenia', 'Pinnipedia', 'Mustelidae', 'NOT one taxonomic order'))
print('PASS: Calotes heart alone withheld; sourced aquatic-mammal photography, taxonomy and archived original verified')

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
