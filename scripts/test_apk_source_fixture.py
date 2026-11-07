#!/usr/bin/env python3
"""Non-Android source-fixture test of APK asset integrity (no SDK required).

WARNING: the fabricated ZIP below is NOT an Android APK. It contains dummy
AndroidManifest.xml/classes.dex purely to drive the post-build archive verifier.
"""
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_built_apk_assets import audit_apk, expected_assets


def main():
    expected = expected_assets()
    # A noncanonical prefix must fail, never be silently rewritten to the
    # runtime basename, even if the PNG exists under pencil_plates/.
    import json
    source = ROOT / 'app/src/main/assets'
    with tempfile.TemporaryDirectory() as temp:
        from shutil import copytree, copy2
        fixture_root = Path(temp) / 'assets'
        copytree(source, fixture_root)
        manifest_path = fixture_root / 'pencil_plates/manifest.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        manifest['figures'][0]['path'] = 'figures/' + Path(manifest['figures'][0]['path']).name
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
        try:
            expected_assets(fixture_root)
        except ValueError as error:
            assert 'Noncanonical pencil plate' in str(error)
        else:
            raise AssertionError('APK source fixture accepted a legacy staging prefix')
    print('PASS: APK source audit rejects historical figures/ path alias')
    plate_pngs = {p for p in expected if p.endswith('.png')}
    assert len(expected) == 80 and len(plate_pngs) == 74
    with tempfile.TemporaryDirectory() as directory:
        fixture = Path(directory) / 'not-an-android-apk.zip'
        with zipfile.ZipFile(fixture, 'w', compression=zipfile.ZIP_STORED) as z:
            z.writestr('AndroidManifest.xml', b'SYNTHETIC-TEST-NOT-ANDROID')
            z.writestr('classes.dex', b'SYNTHETIC-TEST-NOT-DEX')
            for member in sorted(expected):
                z.write(ROOT / 'app/src/main' / member, member)
        audit_apk(fixture)
        with zipfile.ZipFile(fixture, 'a') as z:
            z.writestr('assets/pencil_plates/unregistered_test.png', b'test-only')
        try:
            audit_apk(fixture)
        except ValueError as e:
            assert 'Unregistered pencil' in str(e)
        else:
            raise AssertionError('APK gate accepted an unregistered figure')
    print('PASS: synthetic ZIP fixture verified all 80 required asset members (74 PNGs)')
    print('PASS: source-fixture gate rejected unregistered PNG; this is NOT Android compilation')


if __name__ == '__main__':
    main()
