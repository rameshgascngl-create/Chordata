# CHORDATA — SDK 37 hosted CI and instrumented asset-path checks

**Date:** 7 November 2026  
**Branch target:** `native/qa-chordata-illustration-coverage`  
**Source baseline:** `CHORDATA_64of64_Canonical_Asset_Paths_QA_Source_20261107.zip`  
**Release:** HOLD. These are candidate changes not yet compiled with Android Gradle.

## Root cause being guarded

`compileSdk = 37` targets a platform that `sdkmanager` distributes as `platforms;android-37.0` (actual folder `platforms/android-37.0`). Some tool versions have looked for `platforms/android-37` and reported `Failed to find target with hash string 'android-37'`, even when SDK 37.0 is present. This can make otherwise valid source fail before Kotlin compilation. See:

- https://developer.android.com/build/releases/agp-9-1-0-release-notes
- https://github.com/actions/runner-images/issues/13859
- https://github.com/flutter/flutter/issues/192478

## Changes made

1. Both Android CI jobs explicitly run `scripts/verify_sdk37_platform.sh` after SDK installation and before compilation. The script fails closed if the Android 37.0 `android.jar` is absent. It creates the `android-37` symlink only when the alternate path is absent, and never replaces an existing real directory or broken link.
2. New `scripts/test_sdk37_platform.py` performs four offline tests with a synthetic SDK directory: missing SDK rejection; alias creation; idempotence; rejection of a pre-existing non-SDK path. The test runs in both local QA and the preparatory GitHub job.
3. The Android instrumentation test reads and opens the *canonical `path` field* directly from each manifest entry. It enforces `pencil_plates/<filename>.png` instead of reconstructing a path from `substringAfterLast('/')`, which could accidentally mask staging aliases.
4. `scripts/audit_android_qa_contract.py` rejects loss of either CI compatibility call or the exact-path instrumented decoder.
5. PNGs, editable SVGs, lesson JSON, figure credits and the 64 review decisions are unchanged.

## What passed locally

- Full `bash scripts/qa_all.sh`, including **24 Kotlin core assertions**.
- Exact 64 registered figure slots and 68 variants; original 74 PNG assets preserve their SHA-256 digests.
- 80 required assets in the synthetic APK fixture and source-level image budget checks.
- SDK 37 synthetic compatibility guard including its failure paths.
- YAML structure parsing (not Gradle execution), plus fresh ZIP extraction retest.

## Not validated

- Real `sdkmanager`, actual Gradle sync or Android compilation.
- APK binary assembly and 80-asset check against an actual APK.
- API 35 emulator, Android screen captures, physical devices or Tamil 200% runtime.
- Independent scientific/translation approvals (still 0/64).

The complete source ZIP, not a text-only patch, must be pushed to GitHub before triggering a meaningful QA APK workflow. No production branch must be changed.
