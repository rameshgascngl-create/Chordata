# CHORDATA Native Kotlin/Compose — QA Status

**Original foundation date:** 5 November 2026; **figure continuation:** 6 November 2026
**Deliverable:** Native Android Studio source project with 64/64 provisional figure slots, **NOT an APK**.

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
| Approved scientific figures | **0 / 64** | All 64 now have provisional figure artwork; independent external review required |

## Design and correctness notes

- Every topic gets an overview, separate scrollable lesson pages, and a quiz page. Progress is marked after quiz submission, irrespective of the score (course completion, not exam pass/fail).
- Kotlin `rememberSaveable` is used for current screen/page, language and quiz response state. Persistent bookmarks, quiz scores and topic completion use local SharedPreferences.
- Quiz choices are locked after submission and explanations are shown; retry resets choices. A previously submitted quiz stays marked as completed even after retry.
- All original English/Tamil scientific text is bundled unedited; further expert review is **still pending**.
- Layout and orientation handling cannot be declared accepted without Android screenshot/emulator evidence.
- API/Gradle versions follow published compatibility guidance; the concrete combinations need CI compilation and may require adjustment on an Android-capable runner.

## Required next engineering decisions

Do not merge/publish until `android-qa.yml` builds and tests green and reviewers sign off. If compilation fails, capture exact `file:line` errors before making further edits. Use isolated feature branches. The target remains pure native Android, not an HTML wrapper.

## 6 November 2026 addendum — 64-plate provisional checkpoint

- The historical foundation report above records the earlier source baseline. All 64 registered lesson diagram slots now have provisional pencil-plate artwork; 68 manifest variants refer to 67 distinct PNG files, plus seven credited/legacy QA figure assets. No image is academically approved.
- This continuation replaces three mislabelled generic brain schematics with species-specific, original dorsal views for Scoliodon, frog and Calotes; each supplies an editable SVG master, updated PNG SHA-256 and scientific reference links.
- Instrumentation tests now check all 64 manifest diagram IDs, image bounds and provisional status. Obsolete external-figure semantics tags have been replaced by exact lesson diagram IDs. The chapter-overview pager scroll target has been corrected from index 4 to 3 (the page has four LazyColumn items).
- Android Actions now verifies pencil_plates/manifest.json and all PNG hashes in its preparation, build and instrumentation jobs, and includes pencil_plates/ in the transferred asset artifact.
- **The local source QA scripts pass; Android/Compose compilation and emulator/physical-device acceptance have not been run on this continuation.** The last known remote QA branch has not received these changes. Production release remains on HOLD.

## 6 November 2026 — assembled-APK and reviewer integrity gates

- The local `scripts/qa_all.sh` now tests the ZIP and source using a **new post-build APK audit self-test**, `scripts/audit_built_apk_assets.py --self-test`. The actual build job invokes the same audit against `app/build/outputs/apk/debug/app-debug.apk` **after assembly** and before publishing an APK artefact; emulator CI checks the APK a second time.
- The APK audit requires all 74 artwork PNGs and six mandatory supporting JSON records to appear unmodified in the package. The 25 historical manifest paths labelled `figures/...` resolve in the running gallery to `pencil_plates/<basename>`; verification uses the actual runtime location and fails on missing, tampered, duplicate or extra unregistered figure entries.
- The scientific/Tamil sign-off script rejects approval with missing reviewer identity or evidence notes, and rejects one person approving both columns. A changed image SHA cancels both approvals. `--release-check` is a separate **failing** release gate until all 64 have independent approvals.
- The home-page count and figure-pending explanation were corrected to match 64 **provisional** illustrations. No academic or clinical correctness certification is implied by source integrity.
- **No Gradle compiler or emulator tests were run locally.** The latest checked remote GitHub QA HEAD remained `5371d7ec...`; no new APK build or GitHub push was performed.

## 7 November 2026 — canonical figure asset path repair

- Reconciled the 25 historical `figures/` staging prefixes in `pencil_plates/manifest.json` with their actual `pencil_plates/` runtime paths. Total stays 68 variants across 64 slots; no drawing, figure ID, approved text, or licence attribution was changed.
- `FigureGallery.kt` now uses the full registered directory and filename instead of silently discarding the manifest prefix. The local and post-build APK auditors now require canonical `pencil_plates/<filename>.png` paths and reject stale aliases. The synthetic APK test includes a failing legacy-prefix case.
- Refreshed `docs/figure-coverage.tsv`: all 64 slots are marked **Present (provisional)**, none academically approved, none device-accepted. A new CI coverage-ledger audit checks that this report cannot drift from the manifest.
- `bash scripts/qa_all.sh` passed locally, including the 24 domain-level Kotlin assertions. This is not Compose compilation, Android emulator evidence, image-content scientific certification, or a device-tested APK.
- The remote isolated QA branch remained at `5371d7ecfc8a03955ba86100578dad6538c5fd26` when last checked. These changes have not been pushed. Production release stays on HOLD.
