# CHORDATA Atlas — Google Play Submission Handoff
**Prepared:** 21 November 2026  
**Repository:** `rameshgascngl-create/Chordata`  
**Branch:** `qa/chordata-textbook-unit2-continuation-20261113`  
**Latest committed review dossier:** `e0e1acb94cd7ffaed1ecfe205563746aea1c21de`  
**Last fully successful 4-job Android QA at preparation:** `01e25c2c0d2073e3e0bb4af2722ccd73f3e8c5bd`, [run #44878704580](https://github.com/rameshgascngl-create/Chordata/actions/runs/44878704580). A newer exact-commit QA run [#44880653113](https://github.com/rameshgascngl-create/Chordata/actions/runs/44880653113) was still executing at preparation and must complete before release signing.

## Release disposition: HOLD — do not upload the QA APK
The app's offline native implementation, 64 illustration slots and replacement historical-source rabbit skeleton have been source checked. A QA APK is **not** a Play upload AAB. The exact current revision must pass full compilation, release lint, emulator instrumentation, source asset audit and gated publish. This handoff does not certify an unpublished release or attest to the publisher's private keystore.

## Google Play identity and listing
- App name: **Chordata Atlas**.
- Application ID: `in.gasc.zoology.chordata` — do not change or substitute another app ID.
- Category: **Education**.
- Default QA metadata: `versionCode 1` / `versionName 0.1.0-qa`. These are **not** acceptable final release metadata.
- Release inputs: choose a never-before-used `versionCode` greater than any previously published code; set `versionName` in numeric `major.minor.patch` format. The earlier candidate `2` / `1.0.0` is conditional on Play Console history; **do not assume 2 is available**.
- Target SDK: **36**; minimum SDK: **24**. Android API requirement and actual merged release manifest still need checking against the signed artifact.
- Store copy in **English and Tamil**: [PLAY_LISTING_DRAFT_20261112.md](PLAY_LISTING_DRAFT_20261112.md). Preserve the scientific simplification caveat, no independent certification claims, and offline functionality. Confirm screenshots, icon and feature graphic before publishing.
- Public privacy-policy URL (reported working by owner): https://rameshgascngl-create.github.io/Chordata/privacy-policy.html. A public HTTP 200 and correct HTML content must still pass the workflow's automated fetch; the assistant environment could not independently open the site.
- Native in-app privacy screen: `app/src/main/java/in/gasc/zoology/chordata/ui/PrivacyPolicyScreen.kt`, reachable from Home, English and Tamil. Offline data deletion and user-selected unencrypted JSON export/import documented.

## Play Console declarations requiring human publisher confirmation
- Developer/support contact: the current policy references the developer contact on the Play listing; an **authorised, public and working contact** must be confirmed and included in Play Console. Do not invent or silently publish an email.
- Data safety: confirm no off-device data collection or sharing in the final signed implementation, including merged manifest and dependencies; note data retained locally and unencrypted backups deliberately exported through the Android system picker.
- Target age and content rating: publisher chooses real audience and completes Play questionnaires. B.Sc. undergraduate teaching should not automatically be represented as a children's app.
- App access: offline, no login (confirm signed release).
- Ads: none observed in source (confirm final release dependencies).
- Educational safety: manually review snakebite identification and first-aid teaching content against authoritative current guidance.
- Store listing images, language localisation, release notes, contact details and Play App Signing enrolment must be completed by the publisher.

## Scientific artwork release gate
- All **64** figure slots are populated; **68** manifest variants.
- Owner approved their use in the project. This is not equivalent to independent acceptance.
- Missing active licence declarations were addressed; corrected Tamil rabbit skeleton uses the exact source image already credited as public-domain historical engraving.
- `docs/FIGURE_REVIEW_REGISTER_64.csv` contains **64** rows and **128 PENDING** scientific/Tamil decisions as of preparation. The existing `scripts/write_figure_review_register.py --release-check` intentionally refuses signing until all distinct named reviewers, evidence, valid image rights and current SHA-specific approvals are present.
- Reviewer packet: [FIGURE_REVIEW_DOSSIER_64.md](FIGURE_REVIEW_DOSSIER_64.md). Enter actual named reviewer findings/evidence into the existing CSV; do not fabricate decisions or loosen a gate silently.

## Signing and packaging
Manual release action: [CHORDATA gated Play upload candidate](https://github.com/rameshgascngl-create/Chordata/actions/workflows/play-upload-candidate.yml).

1. Confirm newest `qa/chordata-textbook-unit2-continuation-20261113` SHA passed all four QA jobs.
2. Complete the independent figure review register and any scientific editorial corrections, then rerun exact-SHA QA after any source changes.
3. Confirm public HTML privacy page, publisher contact, real Data safety and store declarations. Leave `publisher_contact_confirmed=false` until actually done.
4. In protected GitHub environment `play-upload-review`, configure four publisher upload-key secrets: `CHORDATA_PLAY_UPLOAD_KEYSTORE_B64`, `CHORDATA_PLAY_UPLOAD_STORE_PASSWORD`, `CHORDATA_PLAY_UPLOAD_KEY_ALIAS`, `CHORDATA_PLAY_UPLOAD_KEY_PASSWORD`. Their values/status cannot be read through the assistant connector. **Never paste passwords or keys into chat or the repository.**
5. Check Play Console for the existing upload signing certificate if this package has been published before. The upload key must match the registered one (or be reset via Play's process). Version code must be unused.
6. Manually dispatch `.github/workflows/play-upload-candidate.yml` on the **reviewed QA branch**, with version code/name, privacy URL and confirmation checkbox. It verifies exact-SHA green QA, reviewer register, public URL, release lint, AAB/APK integrity and the publisher upload-key signature.
7. Obtain signed `CHORDATA_Manual_Signed_Play_Upload_Candidate` **AAB** artifact. Upload this AAB to Play Console, not the QA debug APK or the separately produced APK for other stores.
8. Review Play Console warnings, complete required testing/closed-track requirements if applicable to the account, and submit only after Play Console accepts the uploaded AAB and declarations.

## Release certificate and evidence
The verified debug QA run [#44878704580](https://github.com/rameshgascngl-create/Chordata/actions/runs/44878704580) used `QA_SIGNING_MODE=ephemeral`. Its debug signer is NOT the production upload certificate. No Play-signed release AAB is asserted by this handoff.

**Release condition:** Do not describe CHORDATA as production-submission-ready until all recorded academic signoffs, publisher declarations, exact-commit QA and secure production signing have passed.
