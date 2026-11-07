#!/usr/bin/env python3
"""Build a 64-figure review sheet without erasing human review decisions.

--check validates the saved sheet but never writes it. Generated metadata
is updated from the exact figure registry; reviewer decisions are carried
forward only when the associated figure SHA-256 remains unchanged. A changed
image resets acceptance to PENDING, retaining the previous notes as context.
"""
from pathlib import Path
import argparse
import csv
import io
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'app/src/main/assets'
OUTPUT = ROOT / 'docs/FIGURE_REVIEW_REGISTER_64.csv'

REVIEW_CHECKS = {
    'u2-scoliodon-brain-labelled': 'Compare telencephalon, optic lobes and enlarged cerebellum with a shark dorsal-brain atlas; verify every leader line.',
    'u3-rana-brain': 'Check adult frog paired optic lobes, olfactory tracts, narrow cerebellum and medulla in dorsal view.',
    'u4-calotes-brain': 'Verify reptilian cerebral hemispheres, optic lobes, diencephalon and cerebellar contour against Calotes anatomy.',
    'u3-rana-arterial-system': 'Verify carotid, systemic and pulmocutaneous arches; ensure systemic-arch continuity and heart-chamber labels.',
    'u4-calotes-arterial-system': 'Check lizard aortic arches and ventricular partitioning; do not present the lizard heart as a mammalian four-chambered heart.',
    'u5-columba-urinogenital': 'Verify paired male testes, female functional left ovary/oviduct, ureter-to-cloaca relationship and absent urinary bladder.',
    'u4-poison-apparatus-first-aid-flowchart': 'Review wording against current WHO and Indian snakebite guidance; reject tourniquets, cutting, suction and treatment delay.',
    'u4-snakes-india-big-four-identification': 'Check identification characteristics against Indian taxa; caution that appearance is not reliable for treating suspected bites.',
    'u5-flight-adaptations-avian-lung': 'Check posterior/anterior air-sac relationships, parabronchial airflow direction and breathing-cycle terminology.',
    'u2-scoliodon-sense-organs-labelled': 'Verify ampullae of Lorenzini, lateral line and paired olfactory structures without inventing external openings.',
    'u2-scoliodon-digestive-labelled': 'Confirm stomach/duodenum/spiral-valve intestine, rectal gland and liver relationships against shark dissection references.',
    'u5-rabbit-brain': 'Check mammalian cerebral hemispheres, cerebellum, olfactory bulbs and brainstem in the stated view.',
    'u5-rabbit-excretory-system': 'Verify kidney, ureter, urinary bladder and urethra; distinguish urinary from reproductive structures.',
    'u3-rana-respiration': 'Distinguish cutaneous, buccopharyngeal and pulmonary respiration; check airflow depiction.',
    'u5-dentition-human-rabbit-dental-formula': 'Check deciduous/permanent status and dental formula notation; distinguish human and rabbit counts.',
    'u1-vertebrata-classification-vertebrate-phylogeny': 'Check that clade branching represents modern relationships, not a ladder of evolutionary progress.',
    'u4-origin-extinct-amniote-phylogeny': 'Check amniote branching and avoid presenting paraphyletic traditional reptile groups as modern clades.',
    'u5-bird-migration-flyway-stopovers': 'Confirm illustrative routes are not depicted as verified species-specific migrations.',
}
CRITICAL = set(REVIEW_CHECKS)

VALID_DECISIONS = {'PENDING', 'ACCEPTED', 'REVISION_REQUIRED', 'REJECTED'}

HUMAN_FIELDS = (
    'scientific_reviewer', 'scientific_decision', 'scientific_notes',
    'tamil_reviewer', 'tamil_decision', 'tamil_notes', 'visual_legibility'
)

def validate_review_decisions(row):
    """Reject unauthenticated or single-reviewer sign-off (never fabricate approval)."""
    diagram_id = row.get('diagram_id', '<unknown>')
    for domain in ('scientific', 'tamil'):
        decision = row.get(domain + '_decision', 'PENDING').strip().upper()
        if decision not in VALID_DECISIONS:
            raise ValueError(f'Unknown {domain} decision for {diagram_id}: {decision}')
        if decision == 'ACCEPTED':
            if not row.get(domain + '_reviewer', '').strip():
                raise ValueError(f'Unattributed {domain} ACCEPTED decision for {diagram_id}')
            if not row.get(domain + '_notes', '').strip():
                raise ValueError(f'Missing {domain} review evidence/notes for {diagram_id}')
    if (row.get('scientific_decision', '').strip().upper() == 'ACCEPTED'
            and row.get('tamil_decision', '').strip().upper() == 'ACCEPTED'
            and row.get('scientific_reviewer', '').strip().casefold()
                == row.get('tamil_reviewer', '').strip().casefold()):
        raise ValueError(f'Scientific and Tamil reviewers must be independent: {diagram_id}')


def load_old():
    if not OUTPUT.exists():
        return {}
    with OUTPUT.open(newline='', encoding='utf-8-sig') as f:
        records = list(csv.DictReader(f))
    ids = [r.get('diagram_id', '') for r in records]
    if len(ids) != len(set(ids)) or any(not x for x in ids):
        raise ValueError('Duplicate/blank diagram ID in existing reviewer sheet')
    for r in records:
        validate_review_decisions(r)
    return {r['diagram_id']: r for r in records}


def build_rows(old):
    slots = json.loads((ASSETS / 'figure_slots.json').read_text(encoding='utf-8'))['slots']
    manifest = json.loads((ASSETS / 'pencil_plates/manifest.json').read_text(encoding='utf-8'))['figures']
    by_id = {e['diagramId']: e for e in manifest if e['lang'] in ('en', 'shared')}
    if len(slots) != 64 or len(by_id) != 64 or len({s['id'] for s in slots}) != 64:
        raise ValueError('Not exactly 64 unique reviewed lesson slots')
    rows=[]
    for index, s in enumerate(slots, 1):
        x = by_id[s['id']]
        reference_urls = x.get('referenceUrls') or [x.get('referenceUrl', '')]
        row = {
            'number': index, 'unit': s['topicId'].split('-')[0].upper(),
            'topic_id': s['topicId'], 'page': s['page'], 'section_key': s['sectionKey'],
            'diagram_id': s['id'], 'caption_english': s['captionEn'], 'caption_tamil': s['captionTa'],
            'app_visible_png': x['path'].split('/')[-1], 'image_creator': x['author'],
            'image_license': x.get('license', ''),
            'image_provenance': x.get('sourceUrl') or 'Original project illustration',
            'reference_urls': ' | '.join(filter(None, reference_urls)),
            'image_sha256': x['sha256'], 'image_status': 'PROVISIONAL — not independently approved',
            'review_priority': 'HIGH — anatomy/safety' if s['id'] in CRITICAL else 'STANDARD',
            'specific_review_check': REVIEW_CHECKS.get(s['id'], 'Check diagram morphology, arrows, labels, caption and age/taxon appropriateness.'),
            'scientific_reviewer': '', 'scientific_decision': 'PENDING', 'scientific_notes': '',
            'tamil_reviewer': '', 'tamil_decision': 'PENDING', 'tamil_notes': '',
            'visual_legibility': 'SELF-INSPECTED; DEVICE QA PENDING',
            'svg_master': x.get('svgMaster', ''),
        }
        previous = old.get(s['id'])
        if previous:
            for field in HUMAN_FIELDS:
                if previous.get(field):
                    row[field] = previous[field]
            if previous.get('image_sha256') != x['sha256']:
                # An earlier signature cannot approve a modified figure.
                for field in ('scientific_decision', 'tamil_decision'):
                    row[field] = 'PENDING'
                row['scientific_notes'] = (row['scientific_notes'] + ' [Image content changed; re-review required.]').strip()
                row['tamil_notes'] = (row['tamil_notes'] + ' [Image content changed; re-review required.]').strip()
        rows.append(row)
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='validate without writing the review sheet')
    parser.add_argument('--release-check', action='store_true', help='fail unless all 64 plates have two independent acceptances')
    args = parser.parse_args()
    old = load_old()
    rows = build_rows(old)
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    rendered = buffer.getvalue().encode('utf-8-sig')
    if args.release_check:
        not_signed = [r['diagram_id'] for r in rows if
                      r['scientific_decision'].strip().upper() != 'ACCEPTED' or
                      r['tamil_decision'].strip().upper() != 'ACCEPTED']
        if not_signed:
            raise SystemExit(f'RELEASE HOLD: {len(not_signed)}/64 figures lack dual independent ACCEPTED decisions; first: {", ".join(not_signed[:5])}')
        print('PASS: all 64 figures signed by distinct scientific and Tamil reviewers')
        return
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != rendered:
            raise SystemExit('REVIEW REGISTER STALE: regenerate with python3 scripts/write_figure_review_register.py')
        print('PASS: reviewer register --check (64 rows, zero writes, prior reviewer decisions preserved)')
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temp = OUTPUT.with_suffix('.csv.tmp')
    temp.write_bytes(rendered)
    temp.replace(OUTPUT)
    print('PASS: reviewer register regenerated (64 rows; original human decisions preserved)')

if __name__ == '__main__':
    main()
