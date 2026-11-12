# CHORDATA ATLAS — verified AI10 packaging and release-readiness checkpoint

**Recorded:** 12 November 2026  
**Working branch:** `qa/chordata-play-finalisation-20261112`  
**Scope:** release preparation only, **not** Play Store publication.

## What has been verified

- GitHub Actions [#43248574501](https://github.com/rameshgascngl-create/Chordata/actions/runs/43248574501) passed native Android compilation, emulator tests, release bundle creation, Android lint and 16 KiB checks **for the pre-AI10 GitHub source**.
- The ten owner-selected AI PNGs are present in the **local** `CHORDATA_AI10_Source_Integration_Patch_20261112.zip` (SHA-256 `5b5e58004975bff151bb0dfd298a67803201732b83fd703dd7794498ecc5f8b7`). The patch contains ten PNGs, the updated manifest, original-image backups, the image provenance ledger and a reader adjustment.
- An earlier local AI10 APK was signed and structurally valid but two 32-bit architectures had *APK ZIP offsets* that were not 16 KiB aligned. This was corrected in the local QA package **without calling it a production release**.
- Corrected **local QA APK**: `CHORDATA_AI10_16K_ALIGNED_QA_20261112.apk`; 152,142,875 bytes; SHA-256 `7f034a842b8ede4cf36860274d23b660db6375ef61b2892e836a4cbad44a0072`.
- Corrected local APK checks: ZIP integrity, APK signature scheme v2 and content digest valid; four native `libandroidx.graphics.path.so` binaries have ELF PT_LOAD alignment `16384` and ZIP data offsets divisible by `16384`.
- The local APK was signed with a **new temporary QA certificate**, not the Play upload certificate. Fingerprint: `35b9c8ef65be7008a2823b7d87ab6d03d01c675e65e6f9bd860595e49d7f6409`. It cannot upgrade older installations signed by a different key.

## Steps that must be completed before a Play AAB can be distributed

1. Import all ten PNGs and the manifest into **this QA branch**; do not upload a repackaged APK as the store binary. Before committing, verify each `diagramId` / filename / SHA-256 using `scripts/audit_ai10_release_assets.py`.
2. Apply the reader adjustment from the source overlay only if not already present on this branch; current `FigureGallery.kt` contains the AI10 creator override, so do **not** duplicate it.
3. Regenerate dependent source metadata with `python3 scripts/write_figure_review_register.py`, and any required coverage/source-hash reports, preserving earlier independent reviewer decisions for unchanged images. Do not claim changed images were already signed off.
4. Re-run `scripts/qa_all.sh`, all 64-slot asset/placement checks, Android unit/instrumentation tests, Android lint, R8 and a **source-built** `bundleRelease`. Require a successful QA workflow at the exact commit containing the AI10 files.
5. Check the actual produced AAB for 16 KiB ELF compatibility, 64-bit support and Play app metadata. Test app installation, figure zoom, page progression, Tamil at 200%, orientation, TalkBack, and low-memory devices on an actual Android device.
6. Complete genuine scientific/editorial sign-offs and confirm figure sources/AI credits. The project currently requires two different qualified reviewers (biology and Tamil); no acceptance should be invented.
7. Publish the `docs/privacy-policy.html` document on a public HTTPS **webpage**, and confirm the authorised developer/privacy contact. Review the final Play Data safety, target audience, IARC content rating, advertising and app access declarations.
8. Produce and verify an **upload-key signed** production `.aab` using the protected, manually gated `.github/workflows/play-upload-candidate.yml`. Do not place private keys in the repository or in chat.
9. Use real final-build phone screenshots, 512×512 store icon, 1024×500 feature graphic and approved English/Tamil descriptions for the listing.

## Source/artifact distinction

GitHub Actions #43248574501 is a green baseline **without** the ten new image binaries. A pre-AI10 green build cannot prove the local AI10 APK's device behaviour, nor can a locally repackaged QA APK satisfy Google's source-built, upload-signed bundle requirement.

**Current decision: QA package structurally valid; production submission is on hold pending source integration and the independent publisher/release inputs above.**
