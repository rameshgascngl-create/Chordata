# CHORDATA — Store submission readiness checkpoint

**Source branch:** `qa/chordata-play-finalisation-20261112`  
**Status (12 November 2026):** CI #43248574501 validated the pre-AI10 native source, including release bundle, lint, emulator and 16 KiB checks. The ten AI source images remain a local overlay and must be committed and retested. No production upload, signed Play AAB or publication is authorised. See `docs/AI10_PLAY_READINESS_20261112.md`.

## Verified technical evidence

- Android app ID `in.gasc.zoology.chordata`, minSdk 24, targetSdk 36.
- Current native Kotlin/Jetpack Compose app declares no Android permissions; there are no
  account, analytics, advertising or online API integrations in the reviewed source.
- Lesson completion, bookmarks, quiz scores, language and reading-scale settings remain
  on-device; Android automatic backup is explicitly disabled.
- An in-app English/Tamil privacy screen and an HTML privacy document are present.
- The QA workflow runs the unsigned release-bundle/R8/lint preflight in addition to
  native debug compilation and Android emulator testing. Its output is never uploaded.
- The previous 54 figures and original image credits are preserved in the local ten-image patch; the ten new PNGs and manifest **are not yet committed to this GitHub branch**.

## Google Play Console declarations — draft, not submitted

| Declaration | Candidate response / remaining action |
|---|---|
| App category | Education |
| Contains ads | No (confirm release dependencies and final manifest) |
| Data collection | No data transmitted off-device by the reviewed version; complete the Data safety form |
| Data sharing | None in the reviewed app; verify any future dependencies |
| Account creation | Not supported |
| Children | Declare intended target age accurately before completing the Families questionnaire |
| Permissions | No runtime/network permission requested in the reviewed manifest |
| Privacy URL | **BLOCKED** — publish `docs/privacy-policy.html` to a live, public HTTPS webpage, not a GitHub code view/PDF/download |
| Privacy contact | **BLOCKED** — confirm an authorised publisher contact; current policy points to store contact details |
| Image licences | Retain source provenance; verify each reused figure's actual licence and conditions |
| Medical/safety-related content | Human-review snakebite first aid, snake identification and related medical/safety text |
| Scientific figure certification | Separate actual Zoology/editorial review needed; material-anatomy holds must remain active |
| App version | Replace QA version with coherent release semver and incrementing versionCode at production build |
| Production signing | **BLOCKED** — provision upload key in secure CI secrets and enrol in Play App Signing; never commit keystore |
| Deliverable | **BLOCKED** — build, sign and validate Android App Bundle for Play, not the debug APK |

## AI10 source intake and verified packaging

- The local corrected AI10 QA APK passed a custom APK-v2 digest/signature verification plus 16 KiB ELF **and APK ZIP-data-offset** alignment checks for all four bundled native libraries. This is still not a Play upload artifact or postintegration emulator evidence.
- Commit the complete `CHORDATA_AI10_Source_Integration_Patch_20261112.zip` overlay, preserve older artwork, regenerate dependent review/coverage registers, and run `scripts/audit_ai10_release_assets.py` on the committed source.
- Capture fresh final screenshots; the provisional launcher-artwork icon (512×512), feature graphic (1024×500) and baseline emulator screenshots were prepared outside GitHub as `CHORDATA_Play_Listing_Assets_20261112.zip`.
- Google Play's phone-app API target requirement is API 36 from 31 August 2026; this project already sets `targetSdk = 36`. Official guidance: https://support.google.com/googleplay/android-developer/answer/11926878
- The current Play base-module limit is calculated from compressed device download size, up to 500 MB; do not infer the Play download size from the 145 MiB QA APK alone. Official guidance: https://support.google.com/googleplay/android-developer/answer/9859372

## Final release gate

A debug QA APK is not a valid Play production release. After evidence is complete:
run Kotlin/unit/instrumented tests, Android lint and release-bundle compilation;
verify merged release manifest, dependency list, screenshots/large-text/low-RAM devices,
application ID, versionCode, app signing certificate and bundle integrity. Only upload
after privacy, reviewer sign-offs and Play Console declarations are complete.

**Official policy references:**
- https://support.google.com/googleplay/android-developer/answer/9859455
- https://support.google.com/googleplay/android-developer/answer/10787469
- https://support.google.com/googleplay/android-developer/answer/11926878
- https://developer.android.com/guide/app-bundle/faq
