#!/usr/bin/env python3
"""Offline regression checks for the GitHub runner SDK 37.0 path guard.

This uses a synthetic SDK directory and does not validate an actual Android SDK.
"""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/verify_sdk37_platform.sh'

with tempfile.TemporaryDirectory(prefix='chordata-sdk37-') as base:
    sdk = Path(base) / 'sdk'
    env = os.environ.copy()
    env['ANDROID_SDK_ROOT'] = str(sdk)
    env.pop('ANDROID_HOME', None)
    def run():
        return subprocess.run(['bash', str(SCRIPT)], env=env,
                              capture_output=True, text=True)
    r = run()
    assert r.returncode == 3 and 'not installed' in r.stderr, (r.returncode, r.stderr)
    platform = sdk / 'platforms/android-37.0'
    platform.mkdir(parents=True)
    (platform / 'android.jar').write_bytes(b'qa-test-sentinel-not-a-real-android-jar')
    r = run()
    assert r.returncode == 0, (r.stdout, r.stderr)
    alias = sdk / 'platforms/android-37'
    assert alias.is_symlink() and alias.resolve() == platform
    r = run()
    assert r.returncode == 0, (r.stdout, r.stderr)
    assert alias.is_symlink() and alias.resolve() == platform, 'Idempotence failed'
    alias.unlink()
    alias.mkdir()
    r = run()
    assert r.returncode == 4 and 'compatibility path unavailable' in r.stderr, (r.returncode, r.stderr)

print('PASS: SDK37.0 offline CI compatibility guard — missing SDK fails; alias works; idempotence; unsafe path rejected')
