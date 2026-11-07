# CHORDATA — APK asset integrity and dual-review safeguard

**Checkpoint:** 6 November 2026 · dedicated QA branch `native/qa-chordata-illustration-coverage` · scientific release HOLD.

## New checks

1. **Post-assembly audit** — `scripts/audit_built_apk_assets.py` compares uncompressed bytes inside the assembled Android APK to the local reviewed source. Exactly 80 mandatory paths are checked: 67 unique pencil-plate PNGs, seven legacy/reference PNGs, and six data/inventory/attribution JSON files. A duplicate ZIP member, missing/corrupted required asset, or unregistered pencil PNG is a hard failure.
2. **Source/runtime path consistency** — 25 early pencil-plate records retain a historical `figures/` provenance path in the manifest, but the app reads the filename from the `pencil_plates/` directory. The checker uses the real runtime location without rewriting preserved legacy metadata.
3. **Independent review** — dual scientific and Tamil acceptance requires separate named people and substantive notes. Any change in image SHA-256 cancels prior decisions. The `--release-check` option is expected to fail on this provisional checkpoint (64 without sign-off).
4. **Visible content correction** — the home page no longer says only three reference figures exist. It states correctly that there are 64 provisional lesson diagrams in either reading language. The pending banner no longer claims the figures are unlabelled.

## Tested here

- ZIP source integrity and 64/64 placement / 68 variants: **PASS**.
- Complete-source synthetic APK ZIP fixture (using fabricated test manifest/classes.dex, *not* an Android build) with all 80 required asset files: **PASS**.
- Corruption, omission, unregistered image and duplicate member rejection: **PASS**.
- Independent-review rejection tests (missing reviewer, missing notes, duplicate reviewer, unrecognised status and changed figure SHA): **PASS**.
- Local Kotlin-domain smoke assertions: **24 PASS**.
- Actual Gradle APK assembly, emulator screenshots, actual APK asset audit and physical-device acceptance: **NOT RUN**.

## Next build steps, on a networked Android runner

Synchronise the entire source folder, including the binary drawings, to the QA branch with `bash scripts/sync_qa_branch.sh --dry-run`, then after diff inspection `bash scripts/sync_qa_branch.sh --push`. No force-push or main-branch changes. Verify `prepare-figures`, `native-qa` and `android-instrumentation` each finish successfully. Require the assembled-APK asset-hash report and inspect emulator screenshots. Production release remains blocked by 64 independent figure sign-offs and real-device acceptance.
