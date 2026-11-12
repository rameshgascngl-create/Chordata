#!/usr/bin/env python3
"""Source-level Google Play preflight for this offline QA build.

This verifies claims against the codebase; it does not sign a production AAB,
audit a future dependency upgrade, or attest to a hosted privacy URL.
"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ANDROID = "{http://schemas.android.com/apk/res/android}"
manifest = ET.parse(ROOT / "app/src/main/AndroidManifest.xml").getroot()
application = manifest.find("application")
assert application is not None, "Missing Android application"
permissions = manifest.findall("uses-permission") + manifest.findall("uses-permission-sdk-23")
assert not permissions, "Unexpected runtime/network permissions: " + str([
    x.get(ANDROID + "name") for x in permissions
])
assert application.get(ANDROID + "allowBackup") == "false", "Automatic Android backup must remain disabled"
assert application.get(ANDROID + "usesCleartextTraffic") == "false", "Cleartext traffic must remain disabled"
activities = application.findall("activity")
assert len(activities) == 1
assert activities[0].get(ANDROID + "exported") == "true"
assert activities[0].get(ANDROID + "name") == ".MainActivity"

gradle = (ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
target = re.search(r"\btargetSdk\s*=\s*(\d+)", gradle)
assert target and int(target.group(1)) >= 36, "Target SDK must satisfy the 2026 Play policy"
assert 'isMinifyEnabled = true' in gradle and 'isShrinkResources = true' in gradle, "Release shrinking is disabled"
assert re.search(r'versionName\s*=\s*"[^"]+-qa"', gradle), "QA source unexpectedly labelled as production"
assert not re.search(r'\bsigningConfig\s*=', gradle), "Production signing must not be configured in the QA branch"

store = (ROOT / "app/src/main/java/in/gasc/zoology/chordata/data/ProgressStore.kt").read_text(encoding="utf-8")
for token in ('getSharedPreferences(', '"done"', '"saved"', '"lang"', '"scale"', '"quiz:$topicId"'):
    assert token in store, f"Privacy disclosure needs review: missing {token}"

policy = (ROOT / "docs/privacy-policy.html").read_text(encoding="utf-8").lower()
inapp = (ROOT / "app/src/main/java/in/gasc/zoology/chordata/ui/PrivacyPolicyScreen.kt").read_text(encoding="utf-8")
for term in ("privacy policy", "chordata atlas", "offline", "quiz scores",
             "not request internet access", "not transmit", "uninstall"):
    if term == "not transmit":
        assert "not transmitted" in policy, "Missing policy disclosure: not transmitted"
    else:
        assert term in policy, f"Missing policy disclosure: {term}"
assert 'privacy-policy-page' in inapp
assert 'fun PrivacyPolicyPage(language: ReadingLanguage, textScale: Float)' in inapp
assert 'fontSize = (16f * scale).sp' in inapp, "Privacy text does not respect 200% scale"
assert 'The app does not request Internet access.' in inapp

print("PASS: no app-declared permissions, network/backup disabled, private offline progress")
print("PASS: API 36+ target, release shrinker enabled, QA version, no release-signing keys")
print("PASS: policy and in-app offline data disclosure anchored to current source")
print("HOLD: public hosted policy URL, publisher privacy contact, human review, Play declarations")
print("HOLD: upload-key signing, release-bundle distribution and physical-device acceptance")
