# CHORDATA — 64-plate QA and reviewer-signoff safeguards

**Date:** 6 November 2026  
**Target GitHub branch:** `native/qa-chordata-illustration-coverage`  
**Verified remote HEAD before this checkpoint:** `5371d7ecfc8a03955ba86100578dad6538c5fd26`  
**Remote workflow at that head:** GitHub Actions `42193819051` — success **for the older seven-figure branch only**.  
**Updated source push:** NOT PERFORMED. No claim of Android compilation or updated APK.

## Completed in this source checkpoint

1. Retained all 64 diagram IDs across 39 topics/127 sections/117 quizzes, 68 manifest variants and 67 distinct pencil-plate PNGs.
2. Fixed the extracted-ZIP QA runner to invoke `run_core_tests.sh` with `bash`, without depending on preserved Unix executable permissions.
3. Added `scripts/audit_android_qa_contract.py`: fail-closed checks for registered Compose figure-image selectors, Scoliodon page-4 brain reachability, English labels shared across English/Tamil pages, complete CI figure verification and screenshot evidence hooks.
4. Extended `prepare-figures` to run the test/figure contract and a **read-only** reviewer-sheet validation before uploading the offline assets.
5. Made `scripts/write_figure_review_register.py` preserve previous scientific/Tamil reviewer names, decisions and notes if the underlying figure SHA-256 is unchanged. If an image SHA changes, any previous signoff automatically resets to PENDING. Duplicate rows and unattributed ACCEPTED decisions are rejected. `--check` is non-writing.
6. Added specific scientific review checks for 18 high-priority anatomy/safety figures, leaving the remaining 46 as standard review priority. All 64 decisions remain PENDING.
7. Hardened the one-command local QA (`bash scripts/qa_all.sh`) to check scientific figure credits, reviewed register currency and source XML.

## Local checks actually run

- ZIP CRC and figure mapping: PASS.
- 64/64 registered diagram slots, 68 image variants, 67 distinct pencil PNGs, hashes, dimensions and SVG masters: PASS.
- Seven legacy credited figures, provenance and scientific-approval hold: PASS.
- 24 Kotlin core smoke assertions: PASS.
- XML parse, source-only/no-WebView checks: PASS.
- 64-row reviewer register read-only check: PASS.
- Deliberate test fixture: review decisions preserved on unchanged hash; ACCEPTED invalidated on changed hash: PASS.
- Updated Compose instrumented tests: **not compiled or run**. Local environment has no Android SDK/Gradle connection.

## Unresolved acceptance gates

- Expert review of 64 scientific diagrams, with targeted priority for brain/arterial/respiratory/venom diagrams. None is independently approved.
- Tamil scientific editorial review (English lettering within artwork is intentional; English and Tamil prose pages remain separate).
- GitHub push of the **complete source including PNG/SVG files** to the dedicated QA branch. The GitHub connector can inspect the repository, but the container cannot reach github.com; a text-only push would leave the remote branch inconsistent.
- Android Gradle compilation and emulator screenshots (English/Tamil 100% and 200%, portrait and landscape), then physical-device checks.

## Commands for an Android-enabled QA runner after complete-source synchronisation

```bash
bash scripts/qa_all.sh
gradle --no-daemon :app:compileDebugKotlin
gradle --no-daemon :app:assembleDebug
gradle --no-daemon :app:connectedDebugAndroidTest
```

**Production status:** HOLD. No production merge or release is authorised by these static results.
