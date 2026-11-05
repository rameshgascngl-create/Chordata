# CHORDATA Native Kotlin/Compose — QA Status

**Date:** 5 November 2026
**Deliverable:** Native Android Studio source project, **NOT an APK**.

## Verification actually performed

| Test gate | Result | Scope |
|---|---|---|
| Unmodified source pack checksum | PASS | SHA-256 `d667b88a049f6e2bde3ac37da52216d408ca9efb91f4486feb4ac7d19027092f` |
| Original content-pack Node tests | 73 PASS | Source content validation and completeness, in independent unpacked project |
| Kotlin domain smoke tests | 24 PASS | Pages, next/prev boundaries, chapter sequence, searching, quiz scoring, progress percentage |
| Native source-content audit | PASS | Same 39/127/117/64 data, no HTML/WebView, no internet permission, no automatic backup, expected navigation hooks |
| XML manifest parsing | PASS | Basic XML well-formedness |
| Android Gradle assembly | **NOT RUN** | SDK/Gradle missing and download hosts unresolvable |
| Compose compiler verification | **NOT RUN** | Requires Android Gradle sync/build |
| Android emulator instrumentation | **NOT RUN** | CI job authored, but not executed |
| On-device Tamil 200%/TalkBack | **NOT RUN** | Must be accepted on a real device |
| Approved scientific figures | **0 / 64** | Placeholders only; external review required |

## Design and correctness notes

- Every topic gets an overview, separate scrollable lesson pages, and a quiz page. Progress is marked after quiz submission, irrespective of the score (course completion, not exam pass/fail).
- Kotlin `rememberSaveable` is used for current screen/page, language and quiz response state. Persistent bookmarks, quiz scores and topic completion use local SharedPreferences.
- Quiz choices are locked after submission and explanations are shown; retry resets choices. A previously submitted quiz stays marked as completed even after retry.
- All original English/Tamil scientific text is bundled unedited; further expert review is **still pending**.
- Layout and orientation handling cannot be declared accepted without Android screenshot/emulator evidence.
- API/Gradle versions follow published compatibility guidance; the concrete combinations need CI compilation and may require adjustment on an Android-capable runner.

## Required next engineering decisions

Do not merge/publish until `android-qa.yml` builds and tests green and reviewers sign off. If compilation fails, capture exact `file:line` errors before making further edits. Use isolated feature branches. The target remains pure native Android, not an HTML wrapper.
