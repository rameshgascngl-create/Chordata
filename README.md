# CHORDATA — Native Android QA foundation

**Status:** QA source project only. **No APK has been compiled or installed in this environment.**

This is a **genuinely native Kotlin/Jetpack Compose application**. It does not use HTML, JavaScript, a WebView, network requests or an online API. The five-unit `chordata_content.json` from the 5 November 2026 validated source project is bundled *byte-for-byte* in `app/src/main/assets/`.

## Academic scope

- Unit I Chordata: 8 topics
- Unit II Pisces: 8 topics
- Unit III Amphibia: 6 topics
- Unit IV Reptilia: 6 topics
- Unit V Aves and Mammalia: 11 topics
- **Total: 39 topics, 127 bilingual sections, 117 explanatory MCQs, 64 figure IDs**.

**The 64 referenced figures are NOT included** because the prior review identified missing asset, attribution, licence and scientific-accuracy decisions. The app explicitly displays a pending-illustration notice instead of presenting a fabricated plate.

## Engineering features implemented

- Native Compose Material 3 reader; no HTML/WebView shell.
- English, Tamil and combined reading modes; custom 100%, 125%, 150%, 200% reading scale.
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

**Important:** The Android SDK, Gradle and Android dependency repositories are not available in this particular container. Consequently, the configuration **has not yet been confirmed by an Android compilation**. Android Studio/CI must resolve/verify the exact AGP/Kotlin/Compose combination and report compiler errors if any; do not treat a successful Kotlin-domain smoke test as a build pass.

## Test locally with available tooling

```bash
python3 scripts/audit_content.py
bash scripts/run_core_tests.sh
```

The original content pack's Node suite is also in the uploaded HTML source project and has been rerun independently (73/73 pass). Native logic smoke tests pass 24 assertions. These do not exercise Android rendering.

## Produce a debug QA APK in an Android-capable environment

1. Copy this entire project into a **new, isolated GitHub repository** or branch. Avoid using an INVERTEBRATA/Chordata production branch.
2. Trigger `.github/workflows/android-qa.yml` using **Actions → Chordata Native QA Debug APK → Run workflow**.
3. CI installs Android SDK 37, invokes `gradle :app:assembleDebug`, and uploads the `Chordata_Native_QA_Debug` artifact only if compilation succeeds.
4. The second job runs Android instrumentation tests on an API 35 emulator. Review both jobs and capture screenshot/device evidence before installation or distribution.
5. If building in Android Studio, use **Gradle 9.3.1** and **JDK 17** with Android SDK 37, then `gradle :app:assembleDebug`. The project omits a local Gradle wrapper because its files could not be generated/verified here. Generate the wrapper in a working Android development environment (`gradle wrapper --gradle-version 9.3.1`) if desired.

There is **no signed APK** and no production-release certification in this deliverable.

## Review gates (not waived by passing tests)

1. Independent Zoology specialist review of every lesson and all quiz keys.
2. Tamil Nadu school/college textbook-register editorial review and 200% Tamil on a physical device.
3. Sign-off for all 64 figure assets: source provenance, licence, taxonomic accuracy, text labels, reviewer approval.
4. Android native build, automated UI/emulator testing, process-death, screen orientation, TalkBack and low-RAM phone acceptance.
5. Store metadata, privacy policy, release signing and full app publication review.

Department credit follows the supplied pack: `Department of Zoology, GASC, Nagercoil / Created by R. Ramesh`.
