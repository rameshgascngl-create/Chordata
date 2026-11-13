# CHORDATA — Native Android QA foundation

**Status (12 November 2026):** GitHub Actions workflow [#43248574501](https://github.com/rameshgascngl-create/Chordata/actions/runs/43248574501) passed native QA, emulator tests, and unsigned release-bundle/lint preflight for the committed *pre-AI10* source. Ten owner-selected AI plates are present in a separately validated local QA APK and source overlay, **not yet in this GitHub branch**. This is not a production release.

This is a **genuinely native Kotlin/Jetpack Compose application**. It does not use HTML, JavaScript, a WebView, network requests or an online API. The five-unit `chordata_content.json` from the 5 November 2026 validated source project is bundled *byte-for-byte* in `app/src/main/assets/`.

## Academic scope

- Unit I Chordata: 8 topics
- Unit II Pisces: 8 topics
- Unit III Amphibia: 6 topics
- Unit IV Reptilia: 6 topics
- Unit V Aves and Mammalia: 11 topics
- **Total: 39 topics, 127 bilingual sections, 117 explanatory MCQs, 64 figure IDs**.

**All 64 registered lesson slots now contain PROVISIONAL offline artwork** (68 language-variant manifest entries referencing 67 distinct pencil-plate PNGs; seven legacy/reference PNGs remain bundled separately). The drawings are not academically certified, and the UI marks them as drafts. Presence/placement is not scientific approval.

**Asset path integrity (7 November 2026):** All 68 pencil-plate variants use canonical `pencil_plates/<filename>.png` paths. The native gallery reads that registered directory directly; it does not silently replace a staging prefix. `scripts/audit_coverage_report.py`, the source audit and the assembled-APK audit reject mismatched paths. The 74 PNGs (67 pencil + seven legacy/reference) and all SVG masters retain their original bytes.

## Engineering features implemented

- Native Compose Material 3 reader; no HTML/WebView shell.
- Separate English and Tamil lesson-reading modes; diagram labels intentionally remain in English on both pages, with language-specific captions; custom 100%, 125%, 150%, 200% reading scale.
- Unit/chapter list, full-text bilingual lesson search, fixed bottom navigation.
- Chapter **overview → individual sections → quiz**, with Previous/Next and next-chapter progression.
- Every page change scrolls the lesson back to the top; Android Back returns to the chapter list.
- Four-option MCQs, answer feedback, bilingual explanations, topic completion after quiz submission.
- Local bookmarks, completed topics, score, reading language, scale using private `SharedPreferences`.
- Reader location and unfinished quiz selections saved through `rememberSaveable` for ordinary Activity recreation; persisted long-term progress kept separately.
- Security: no INTERNET permission, no cleartext, Android backup disabled; only launcher Activity exported.

## Build configuration

Based on the published Android/Kotlin documentation as of 5 November 2026:

- Android Gradle plugin `9.1.1`; Gradle `9.3.1`
- Compose BOM `2026.09.00`
- Kotlin Compose Compiler Gradle plugin `2.4.21`
- Android `compileSdk=37`, `targetSdk=36`, `minSdk=24`
- JDK 17 minimum
- Hosted CI explicitly installs `platforms;android-37.0`; an idempotent compatibility guard checks `android.jar` and supplies the `android-37` alias only when missing. This addresses known runner path-resolution problems, not an Android compilation result.

**Verified CI (12 November 2026):** Native Kotlin compilation, Android emulator instrumentation, unsigned release-bundle creation, release lint and native 16 KiB checks passed in [workflow #43248574501](https://github.com/rameshgascngl-create/Chordata/actions/runs/43248574501). These results cover the committed pre-AI10 source only. The local ten-image QA package requires a fresh source-build CI/emulator run after its binary assets and manifest are committed.

## Test locally with available tooling

```bash
bash scripts/qa_all.sh  # all 64 mapped figures, provenance, independent-review safeguards, Kotlin core checks
python3 scripts/write_figure_review_register.py --check  # review-sheet integrity, no write
python3 scripts/write_figure_review_register.py --release-check  # intentionally FAILS until 64 dual sign-offs
```

The original content pack's Node suite is also in the uploaded HTML source project and has been rerun independently (73/73 pass). Native logic smoke tests pass 24 assertions. These do not exercise Android rendering.

## Produce a debug QA APK in an Android-capable environment

1. Copy this entire project into a **new, isolated GitHub repository** or branch. Avoid using an INVERTEBRATA/Chordata production branch.
2. Trigger `.github/workflows/android-qa.yml` using **Actions → Chordata Native QA Debug APK → Run workflow**.
3. CI checks the 64 provisional plates and hashes before compilation and then runs `gradle :app:assembleDebug`.
4. **New APK gate:** `python3 scripts/audit_built_apk_assets.py app/build/outputs/apk/debug/app-debug.apk` opens the assembled APK itself and verifies 80 essential asset members by SHA-256 (74 PNGs and six content/registry/credit files). Its self-test is also run before compilation.
5. A separate instrumentation job runs on an API 35 emulator, repeats APK asset verification and extracts screenshots. Review compiler logs, instrumented tests and screenshots before considering an APK installable or scientifically approved.
6. If building in Android Studio, use **Gradle 9.3.1** and **JDK 17** with Android SDK 37, then `gradle :app:assembleDebug`. The project uses Gradle 9.3.1 in GitHub Actions; the Gradle wrapper is not committed. Use the pinned CI toolchain for reproducible builds or generate and validate a wrapper in a full Android development environment.

A pre-AI10 QA APK is available from the successful workflow; a separate AI10 local QA APK has been repackaged and validated but is **not equivalent to a reproducible source-built release**. The complete ten-image source overlay must be committed alongside its manifest and regenerated reviewer/coverage registers before rerunning native CI and the release workflow. No signed production AAB or Play publication has been completed.

**Sign-off integrity:** The 64-row review register now rejects invented/anonymous `ACCEPTED` statuses, missing review notes and the same person accepting both scientific and Tamil columns. Replacing a PNG revokes previous acceptance for that plate. Reviewer acceptance does **not** waive emulator, TalkBack, low-RAM and physical-device checks.

## Review gates (not waived by passing tests)

1. Independent Zoology specialist review of every lesson and all quiz keys.
2. Tamil Nadu school/college textbook-register editorial review and 200% Tamil on a physical device.
3. Sign-off for all 64 figure assets: source provenance, licence, taxonomic accuracy, text labels, reviewer approval.
4. Android native build, automated UI/emulator testing, process-death, screen orientation, TalkBack and low-RAM phone acceptance.
5. Store metadata, privacy policy, release signing and full app publication review.

Department credit follows the supplied pack: `Department of Zoology, GASC, Nagercoil / Created by R. Ramesh`.
