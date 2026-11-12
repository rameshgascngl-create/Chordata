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
assert 'versionName = releaseVersionNameEnv ?: "0.1.0-qa"' in gradle, "Default QA identity changed"
assert 'versionCode = releaseVersionCodeEnv?.toInt() ?: 1' in gradle, "Default QA version changed"
assert 'CHORDATA_RELEASE_VERSION_CODE' in gradle and 'CHORDATA_RELEASE_VERSION_NAME' in gradle
assert 'Release version code and name must be provided together' in gradle
# Persistent signing applies ONLY to debug builds, using secure environment
# secrets. Release bundles remain unsigned for preflight; no keystore in git.
assert 'create("persistentQa")' in gradle
assert 'CHORDATA_QA_KEYSTORE_PATH' in gradle
assert 'signingConfig = signingConfigs.getByName("persistentQa")' in gradle
release_fragment = gradle.split('release {', 1)[1].split('\n        }', 1)[0]
assert 'signingConfig' not in release_fragment, "QA must never sign production release"
wf = (ROOT / ".github/workflows/android-qa.yml").read_text(encoding="utf-8")
assert wf.count('Restore persistent QA signing from encrypted repository secrets') == 2
assert 'QA_SIGNING_MODE=ephemeral' in wf and 'QA_SIGNING_MODE=persistent' in wf
assert 'Report QA signing certificate without exposing a key' in wf

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
assert 'fun PrivacyPolicyPage(language: ReadingLanguage, textScale: Float,' in inapp
assert 'privacy-erase-entry' in inapp and 'privacy-erase-confirm' in inapp
assert 'privacy-erase-cancel' in inapp and 'privacy-erase-dialog' in inapp
assert 'fun eraseAllLearningData(): Boolean = prefs.edit().clear().commit()' in store
assert 'erase all learning data' in policy
assert 'fontSize = (16f * scale).sp' in inapp, "Privacy text does not respect 200% scale"
assert 'The app does not request Internet access.' in inapp

release_workflow = (ROOT / ".github/workflows/play-upload-candidate.yml").read_text(encoding="utf-8")
for token in ("workflow_dispatch:", "play-upload-review", "scripts/write_figure_review_register.py --release-check",
              "Verify public privacy webpage", "Confirm matching successful QA workflow",
              "jarsigner", "CHORDATA_PLAY_UPLOAD_KEYSTORE_B64", "upload-artifact@v4"):
    assert token in release_workflow, f"Unsafe or incomplete manual release gate: {token}"
assert "push:" not in release_workflow and "pull_request:" not in release_workflow, "Release workflow must be manual only"
print("PASS: manual Play AAB workflow is gated by academic, privacy, tested SHA and secure signing checks")
print("PASS: no app-declared permissions, network/backup disabled, private offline progress")
print("PASS: API 36+ target, release shrinker enabled, QA version, no release-signing keys")
print("PASS: policy and in-app offline data disclosure anchored to current source")
print("HOLD: public hosted policy URL, publisher privacy contact, human review, Play declarations")
print("HOLD: upload-key signing, release-bundle distribution and physical-device acceptance")
