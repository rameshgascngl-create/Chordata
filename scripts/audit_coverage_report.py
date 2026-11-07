#!/usr/bin/env python3
"""Check that the student-facing figure coverage ledger matches the canonical register."""
from pathlib import Path
import csv,json,sys
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'app/src/main/assets'
manifest=json.loads((ASSETS/'pencil_plates/manifest.json').read_text(encoding='utf-8'))['figures']
slots=json.loads((ASSETS/'figure_slots.json').read_text(encoding='utf-8'))['slots']
by_id={}
for fig in manifest:
    by_id.setdefault(fig['diagramId'],[]).append(fig['path'])
with (ROOT/'docs/figure-coverage.tsv').open(newline='',encoding='utf-8') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
if len(rows)!=64 or {r['diagramId'] for r in rows}!={s['id'] for s in slots}:
    sys.exit('COVERAGE LEDGER FAIL: missing or duplicate registered slot')
for row in rows:
    expected=' | '.join(by_id[row['diagramId']])
    if row['assets']!=expected or row['assetStatus']!='Present (provisional)' or row['scientificSignoff']!='Not approved':
        sys.exit('COVERAGE LEDGER FAIL: misleading or outdated record for '+row['diagramId'])
print('PASS: coverage ledger records all 64 provisional slots with canonical asset paths')
