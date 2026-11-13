#!/usr/bin/env python3
"""Compare the *actual assembled APK* against the 64-figure reviewed source.

This runs after :app:assembleDebug. It checks uncompressed APK members byte for
byte; a successful local source audit alone never proves that Android packaged
an image correctly. No Android SDK or network is required for this audit.

Usage: python3 scripts/audit_built_apk_assets.py app/build/outputs/apk/debug/app-debug.apk
       python3 scripts/audit_built_apk_assets.py --self-test
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'app/src/main/assets'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expected_assets(root: Path = ASSETS) -> dict[str, str]:
    """Paths and source digests for the assets essential to native diagram rendering."""
    manifest = json.loads((root / 'pencil_plates/manifest.json').read_text(encoding='utf-8'))
    slots = json.loads((root / 'figure_slots.json').read_text(encoding='utf-8'))['slots']
    figures = json.loads((root / 'figures.json').read_text(encoding='utf-8'))
    if len(slots) != 64 or len({s['id'] for s in slots}) != 64:
        raise ValueError('Expected exactly 64 registered and distinct lesson slots')
    variants = manifest['figures']
    if len(variants) != 68 or {v['diagramId'] for v in variants} != {s['id'] for s in slots}:
        raise ValueError('64 slots and 68 manifest variants disagree')
    if len(figures) != 7:
        raise ValueError('Expected seven independent legacy source/reference figures')

    paths = {
        'chordata_content.json', 'chordata_learning_points.json',
        'chordata_textbook_chapters.json', 'figure_slots.json', 'figures.json',
        'pencil_plates/manifest.json', 'source_reference_credits.json',
        'figures/source-hashes.json',
    }
    for entry in variants:
        rel = Path(entry['path'])
        # Permit only canonical, relative asset references. Reject traversal and
        # path aliases that could mask a missing or misplaced image.
        if (rel.is_absolute() or '..' in rel.parts or len(rel.parts) != 2
                or rel.parts[0] != 'pencil_plates' or rel.suffix != '.png'):
            raise ValueError(f'Noncanonical pencil plate asset path: {entry["path"]}')
        # The registered location is the *actual* path opened by FigureGallery.
        paths.add(rel.as_posix())
    for entry in figures:
        name = entry['file']
        if Path(name).name != name or not name.endswith('.png'):
            raise ValueError(f'Unsafe legacy figure file name: {name}')
        paths.add('figures/' + name)
    expected = {}
    for name in sorted(paths):
        file = root / name
        if not file.is_file():
            raise FileNotFoundError(f'Source asset missing: {name}')
        expected['assets/' + name] = sha256(file.read_bytes())
    return expected


def audit_members(zf: zipfile.ZipFile, expected: dict[str, str]) -> None:
    names = zf.namelist()
    if len(names) != len(set(names)):
        raise ValueError('APK contains ambiguous duplicate ZIP member names')
    name_set = set(names)
    missing = set(expected) - name_set
    if missing:
        raise ValueError(f'APK missing {len(missing)} mandatory assets: ' + ', '.join(sorted(missing)[:8]))
    if 'AndroidManifest.xml' not in name_set or 'classes.dex' not in name_set:
        raise ValueError('Archive has no AndroidManifest.xml or primary classes.dex; not an Android app package')
    unexpected_figures = {
        n for n in name_set if n.startswith('assets/pencil_plates/') and n.endswith('.png')
    } - {
        n for n in expected if n.startswith('assets/pencil_plates/') and n.endswith('.png')
    }
    if unexpected_figures:
        raise ValueError('Unregistered pencil figure(s) inside APK: ' + ', '.join(sorted(unexpected_figures)[:6]))
    for name, expected_hash in expected.items():
        with zf.open(name) as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if digest != expected_hash:
            raise ValueError(f'APK asset changed or corrupted: {name} ({digest} != {expected_hash})')


def audit_apk(apk: Path, root: Path = ASSETS):
    if not apk.is_file():
        raise FileNotFoundError(f'Built APK does not exist: {apk}')
    with zipfile.ZipFile(apk) as zf:
        audit_members(zf, expected_assets(root))
    return sha256(apk.read_bytes())


def self_test():
    good = {
        'assets/pencil_plates/test.png': sha256(b'alpha'),
        'assets/figure_slots.json': sha256(b'{}'),
    }
    with tempfile.TemporaryDirectory() as tmp:
        test_apk = Path(tmp) / 'test.apk'
        def write(missing=None, corrupt=None, duplicate=False):
            with zipfile.ZipFile(test_apk, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr('AndroidManifest.xml', b'compiled-binary-manifest')
                z.writestr('classes.dex', b'dex')
                for name, data in [('assets/pencil_plates/test.png', b'alpha'),
                                   ('assets/figure_slots.json', b'{}')]:
                    if name != missing:
                        z.writestr(name, b'changed' if name == corrupt else data)
                if duplicate:
                    with warnings.catch_warnings():
                        warnings.filterwarnings('ignore', category=UserWarning, message='Duplicate name:')
                        z.writestr('assets/pencil_plates/test.png', b'alpha')
        write()
        with zipfile.ZipFile(test_apk) as z:
            audit_members(z, good)
        for label, kwargs in [('missing', {'missing': 'assets/pencil_plates/test.png'}),
                              ('modified', {'corrupt': 'assets/figure_slots.json'}),
                              ('duplicate', {'duplicate': True})]:
            write(**kwargs)
            try:
                with zipfile.ZipFile(test_apk) as z:
                    audit_members(z, good)
            except ValueError:
                pass
            else:
                raise AssertionError(f'APK self-test incorrectly passed {label} asset')
    print('PASS: APK archive audit self-test (valid, missing, corrupted and duplicate assets)')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('apk', nargs='?', type=Path)
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if args.apk is None:
        p.error('a built APK path is mandatory unless --self-test is used')
    apk_hash = audit_apk(args.apk)
    print('PASS: assembled APK contains 64 lesson figure slots / 68 variants / 7 legacy figures')
    print('PASS: all required APK image/content/credit bytes match source SHA-256 digests')
    print('APK SHA-256:', apk_hash)
    print('NOTE: scientific review, emulator screenshots and physical-device acceptance remain separate gates')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, AssertionError, zipfile.BadZipFile) as exc:
        sys.exit('APK ASSET GATE FAIL: ' + str(exc))
