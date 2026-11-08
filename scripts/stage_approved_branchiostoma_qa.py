#!/usr/bin/env python3
"""Safely stage an exact-hash corrected Branchiostoma PNG in isolated CHORDATA QA.

No downloads, no automatic approvals, no production changes. Default read-only.
Specify --candidate pointing to the PNG from the separate QA package.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
import struct
import subprocess
import tempfile
from pathlib import Path

BRANCH = 'qa/chordata-illustrations-continuous'
ID = 'u1-cephalochordata-branchiostoma-labelled'
REL = Path('app/src/main/assets/pencil_plates/branchiostoma_ta.png')
MANIFEST = Path('app/src/main/assets/pencil_plates/manifest.json')
REVIEW = Path('docs/FIGURE_REVIEW_REGISTER_64.csv')
OLD_SHA = 'e1d8b5a749628f3c49cae235c5dd52649f44fa597eb86ca6ce43a8b7404a1e75'
NEW_SHA = '2fbd48be62b83309c87214492ea20dfea1995a3e624fca66c17ed995c95d9b1e'
NEW_SIZE = 1199846


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def branch(repo: Path) -> str:
    return subprocess.check_output(['git', 'branch', '--show-current'], cwd=repo, text=True).strip()


def stable_png(p: Path) -> None:
    with p.open('rb') as f:
        data = f.read(26)
    if data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
        raise ValueError('Not an IHDR PNG image')
    if struct.unpack('>II', data[16:24]) != (1536, 1024):
        raise ValueError('Unexpected image dimensions')
    if p.stat().st_size != NEW_SIZE or digest(p) != NEW_SHA:
        raise ValueError('Candidate PNG does not match reviewed SHA-256 and length')


def stage(repo: Path, candidate: Path, apply: bool) -> None:
    repo = repo.resolve(); candidate = candidate.resolve()
    dest = repo / REL; manifest = repo / MANIFEST; review = repo / REVIEW
    if not all(p.is_file() for p in [candidate, dest, manifest, review]):
        raise FileNotFoundError('Missing candidate/registered PNG/manifest/reviewer sheet')
    stable_png(candidate)
    if digest(dest) != OLD_SHA:
        raise ValueError('Existing Tamil figure differs from audited checkpoint')
    data = json.loads(manifest.read_text(encoding='utf-8'))
    entries = [e for e in data['figures'] if e['diagramId'] == ID and e['lang'] == 'ta'
               and e['path'] == 'pencil_plates/branchiostoma_ta.png']
    if len(entries) != 1 or entries[0]['sha256'] != OLD_SHA:
        raise ValueError('Tamil variant/manifest SHA mismatch')
    with review.open(encoding='utf-8-sig', newline='') as f:
        rows = [r for r in csv.DictReader(f) if r.get('diagram_id') == ID]
    if len(rows) != 1 or any(rows[0].get(x, 'PENDING') != 'PENDING'
                                 for x in ('scientific_decision', 'tamil_decision')):
        raise ValueError('Human review state differs from PENDING; reconcile manually')
    entry = entries[0]
    if entry.get('aiQaIntegrationDecision') != 'HOLD_MATERIAL_ANATOMY_ERROR':
        raise ValueError('Original lacks recorded HOLD decision')
    print('PASS: exact old/new SHA, PNG dimensions and registered Tamil slot')
    if not apply:
        print('CHECK ONLY: no files written; --apply requires dedicated QA branch')
        return
    if branch(repo) != BRANCH:
        raise ValueError('Not on dedicated QA branch')
    tracked = subprocess.check_output(
        ['git', 'status', '--porcelain', '--', str(REL), str(MANIFEST)],
        cwd=repo, text=True).strip()
    if tracked:
        raise ValueError('PNG/manifest have uncommitted modifications; refusing overwrite')
    entry.update({
        'sha256': NEW_SHA, 'size': NEW_SIZE,
        'author': 'OpenAI ChatGPT ImageGen — original anatomical reconstruction, digitally labelled (2026-11-08)',
        'license': 'Original AI-generated illustration; no third-party illustration copied',
        'sourceUrl': '', 'referenceUrls': [
            'https://www.gutenberg.org/cache/epub/73702/pg73702-images.html',
            'https://doi.org/10.1080/00212210.1996.10688880'],
        'modifications': 'AI regeneration of serial gonads and essential chordate structures; English labels.',
        'visualReview': 'AI_GREEN_TICK_PROVISIONAL_NO_INDEPENDENT_SIGNOFF',
        'aiQaIntegrationDecision': 'GREEN_TICK_ALLOW_PROVISIONAL_QA_USE',
        'aiQaIntegrationNotes': 'Serial segmental gonads and basic lancelet anatomy shown; stylised, not a dissection.',
        'aiQaDecisionBasis': 'Exact PNG screened against anatomical references; user permits minor-error AI art in QA.',
        'reviewStatus': 'PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING',
        'keyTa': 'முதுகுநாண்; முதுகு நரம்புக் குழாய்; தசைத்துண்டுகள்; தொண்டைச் செவுள் பிளவுகள்; '
                 'தொடராக அமைந்த இனப்பெருக்கச் சுரப்பிகள்; ஏட்ரியத் துளை; குடல்; மலத்துளை. '
                 'படத்தின் உறுப்புக் குறியீடுகள் ஆங்கிலத்தில் உள்ளன.'
    })
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp_image = tmp_manifest = None
    try:
        with tempfile.NamedTemporaryFile(dir=dest.parent, prefix='.branchiostoma-', delete=False) as f:
            tmp_image = Path(f.name); f.write(candidate.read_bytes())
        with tempfile.NamedTemporaryFile(dir=manifest.parent, prefix='.manifest-', delete=False) as f:
            tmp_manifest = Path(f.name); f.write(raw)
        if digest(tmp_image) != NEW_SHA:
            raise ValueError('Temporary PNG checksum failed')
        check = json.loads(tmp_manifest.read_text(encoding='utf-8'))
        if not any(e['diagramId'] == ID and e['lang'] == 'ta' and e['sha256'] == NEW_SHA
                   for e in check['figures']):
            raise ValueError('Temporary manifest check failed')
        os.replace(tmp_image, dest); tmp_image = None
        os.replace(tmp_manifest, manifest); tmp_manifest = None
    finally:
        if tmp_image is not None: tmp_image.unlink(missing_ok=True)
        if tmp_manifest is not None: tmp_manifest.unlink(missing_ok=True)
    print('STAGED: Tamil PNG and manifest only; independent review PENDING')
    print('Run bash scripts/qa_all.sh; commit; verify Android emulator and gated APK')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True, help='CHORDATA Git checkout')
    parser.add_argument('--candidate', type=Path, required=True, help='Reviewed corrected PNG')
    parser.add_argument('--apply', action='store_true', help='Stage after preflight checks')
    args = parser.parse_args()
    stage(args.repo, args.candidate, args.apply)
