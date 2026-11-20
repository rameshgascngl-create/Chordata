# CHORDATA — Google Play readiness and Tamil editorial audit

**Date:** 20 November 2026  
**Repository:** `rameshgascngl-create/Chordata`  
**Branch:** `qa/chordata-textbook-unit2-continuation-20261113`  
**Scope:** user-supplied QA APK archive and current GitHub native Android source. This is a release-preparation report, **not certification of a published app or signed Play-upload AAB**.

## Source and uploaded-package identity

- Uploaded archive: `Chordata_Pointwise_Answers_QA_APK.zip`, containing `Chordata_Pointwise_Answers_QA_d09d45e5.apk`.
- Embedded APK: **135,407,716 bytes**, SHA-256 `04280e5fd2fe4423a63d04affacf1e4c30ea26bc7c6d132d0bddf955ecb9c3c1`.
- Archive and embedded APK both passed ZIP CRC integrity checks.
- This APK was built at **commit d09d45e5**, *not* the newer Tamil editorial branch HEAD. It must not be represented as an APK incorporating the 20 November corrections.
- The APK contained four `libandroidx.graphics.path.so` ABI variants; all PT_LOAD ELF alignments were **16,384 bytes**, and all uncompressed shared-library ZIP data offsets were 16 KiB-aligned. This is a targeted binary verification of the uploaded **QA** artifact, not a substitute for final release/AAB/device testing.
- Current source: **39/39 syllabus topics, 127 core bilingual sections, 298 expanded bilingual textbook sections, 117 MCQs and 64 illustration slots**.

## Verified source-level Play requirements

| Requirement | Verified evidence / next check |
|---|---|
| Android SDK | `targetSdk = 36` (required for 2026 new submissions); `compileSdk = 37`, `minSdk = 24` |
| Android App Bundle | `:app:bundleRelease` and `:app:lintRelease` are in the QA workflow; signed production AAB is **not** issued automatically |
| App identifier | `in.gasc.zoology.chordata` |
| Declared permissions | None in `AndroidManifest.xml`; `android:usesCleartextTraffic="false"` |
| User data | Learning progress stored locally; Android automatic backup disabled; optional manual export produces an **unencrypted JSON file** |
| Privacy | In-app English/Tamil privacy screen and `docs/privacy-policy.html` source exist; a **live public HTTPS hosted page** and verified publisher privacy contact are still required |
| App signing | QA signing/debug identity is **not** an upload key; manual workflow requires four protected upload-key secrets and reviewer-gated GitHub environment |
| Testing | Latest *pre-editorial* successful SHA was `d09d45e5` (native/emulator/release preflight); newer Tamil revisions require exact-commit green validation |
| Google Play declarations | Publisher must complete actual Data safety, target-age, content-rating, app-access and other applicable Play Console forms |
| Store graphics | Verify 512 × 512 store icon, 1024 × 500 feature graphic, and **real screenshots of the final build**, including Tamil reading at 200% |
| Reuse rights | Seven manifest variants lacked explicit `license` declarations when audited (four original project schematics and three Tamil AI variants, including one held variant). Owner's permission for educational display does **not automatically establish all redistributed image rights** |
| Academic approval | The 64-row register retains independent Zoology and Tamil decisions as **PENDING**; do not create fictitious reviewer identities |
| Calotes cardiovascular figure | Earlier materially erroneous AI image archived; source-checked functional schematic now active; independent anatomical validation remains pending |
| Tamil rabbit skeleton | Materially erroneous Tamil AI variant withheld; sourced English plate used as fallback |

## Tamil editorial work on 20 November

- Retained all existing 16 November Tamil-polishing commits rather than redoing validated lessons.
- Rewrote **all five** extended sections on classification and general characteristics of fishes (`u2-pisces-classification`).
- Rewrote **all six** extended sections on fish migration (`u2-migration`).
- Rewrote **all six** extended sections on bird migration (`u5-bird-migration`).
- Rewrote **all six** extended sections on reptile classification (`u4-reptilia-classification`).
- Rewrote **all eight** extended sections on amphibian classification (`u3-amphibia-classification`).
- Polished **18 additional topic-opening headings** and corrected the Tamil embryological term `மஞ்சள் கருப் பை`.
- **Total newly rewritten in this session: 31 full textbook sections**, with English explanations, section IDs, quiz keys, figures and source references preserved. This is not a claim that all 298 sections have received final sentence-level human editorial approval.
- Kept the reader's academic text status as a draft pending independent language and subject sign-off.
- Repaired the Tamil 200%-font navigation test to compare against the bundled current heading, avoiding an obsolete hardcoded phrase.
- Re-pinned the exact SHA-256 of the previously corrected **core course pack** in `scripts/audit_content.py`, preserving immutable-content checking rather than disabling the gate.
- Updated `docs/PLAY_LISTING_DRAFT_20261112.md` with natural Tamil copy that reflects expanded lessons and study answers.

## Remaining academic tasks (not completed)

A complete human editorial pass must still check every untouched extended section and all 127 core sections for natural prose, accurate taxonomy and consistent terminology, including a separate verification of all 117 quiz answer keys. Use Tamil Nadu State Council of Educational Research and Training (SCERT) Zoology textbook vocabulary where scientifically accurate, while retaining Latin binomials and specialised English terms parenthetically on first introduction.

Do not replace source-backed species descriptions with an invented translation, conflate different species in comparative figures, or shorten explanatory content to make the page appear cleaner. The **native book reader** must retain continuous and page-by-page reading and accessible 100–200% text.

## Release verdict

**NOT READY TO SUBMIT TO GOOGLE PLAY** until: (1) the exact final source SHA passes native, release-bundle, 16 KiB and emulator QA; (2) academic/figure and image-rights requirements are genuinely cleared; (3) the publisher supplies a live hosted policy page and authorised privacy email, completes Play Console declarations and screenshots; and (4) the manual release workflow creates a correctly versioned **upload-key-signed AAB**.

The project already has an appropriate manual release workflow: `.github/workflows/play-upload-candidate.yml`. Do not send the uploaded compact QA APK to Play or sign an unreviewed bundle with debug/QA keys.

## Primary policy references

- Target API: https://support.google.com/googleplay/android-developer/answer/11926878
- User data and privacy policy: https://support.google.com/googleplay/android-developer/answer/10144311
- Data safety: https://support.google.com/googleplay/android-developer/answer/10787469
- Android App Bundles: https://developer.android.com/guide/app-bundle/
- 16 KiB pages: https://developer.android.com/guide/practices/page-sizes
- Store graphics: https://support.google.com/googleplay/android-developer/answer/9866151
- Store metadata: https://support.google.com/googleplay/android-developer/answer/13393723

**Release engineering principle:** a passing QA APK is not equivalent to a signed, compliant production AAB.
