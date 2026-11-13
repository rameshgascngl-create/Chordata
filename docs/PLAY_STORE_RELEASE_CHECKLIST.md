# CHORDATA — Store submission readiness checkpoint

**Source branch:** `qa/chordata-play-finalisation-20261112`  
**Status (13 November 2026):** All ten owner-selected AI PNGs are committed in `4c7e61caa4690ed20dc9a77a0e4efcf41a717acf`. Exact-commit QA runs [#506](https://github.com/rameshgascngl-create/Chordata/actions/runs/43349289905) and [#507](https://github.com/rameshgascngl-create/Chordata/actions/runs/43349295301) passed source/figure integrity, native compilation, release-bundle/R8/lint preflight, 33 Android instrumentation tests and gated QA APK publication. This is QA validation, **not independent scientific/Tamil approval and not a signed Play upload AAB**. The 12 November `docs/AI10_PLAY_READINESS_20261112.md` is retained as a historical pre-integration report.

## Verified technical evidence

- Android app ID `in.gasc.zoology.chordata`, minSdk 24, targetSdk 36.
- Current native Kotlin/Jetpack Compose app declares no Android permissions; there are no
  account, analytics, advertising or online API integrations in the reviewed source.
- Lesson completion, bookmarks, quiz scores, language and reading-scale settings remain
  on-device; Android automatic backup is explicitly disabled.
- An in-app English/Tamil privacy screen and an HTML privacy document are present.
- The QA workflow runs the unsigned release-bundle/R8/lint preflight in addition to
  native debug compilation and Android emulator testing. Its output is never uploaded.
- All ten owner-selected AI illustrations and the updated manifest are now committed. Earlier accepted source art and corresponding provenance remain preserved. GitHub CI confirms 64/64 assigned figure slots and 68 manifest variants; **scientific and Tamil reviewer decisions remain pending**.

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

- Post-integration source-built QA APK at exact commit `4c7e61caa4690ed20dc9a77a0e4efcf41a717acf`: SHA-256 `a6683eeb4402dafe59c676171719a05cccf63741501dda618f0c04a189f34792`. The four bundled native libraries passed both 16 KiB ELF and APK ZIP-placement checks. This is **debug-signed with an ephemeral QA certificate**, not Play-upload signed, and may not upgrade previous APKs signed with another certificate.
- The ten original PNGs and manifest are already committed; **do not re-import, regenerate or overwrite accepted illustrations**. Figure slot hashes, source credits and 64-row reviewer register were checked by CI. The register has no independent dual sign-offs.
- The emulator job published test screenshots as `Chordata_Emulator_QA_Evidence`; final Play listing imagery and physical-device testing still require verification. Provisional launcher-artwork icon (512×512) and feature graphic (1024×500) had been prepared outside GitHub as `CHORDATA_Play_Listing_Assets_20261112.zip`; verify those assets before listing.
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
