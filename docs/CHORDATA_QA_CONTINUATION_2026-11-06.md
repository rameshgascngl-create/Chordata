# CHORDATA continuation: figure-integrity and emulator-test repair

**Branch target:** `native/qa-chordata-illustration-coverage` (unmerged local QA source).
**Approval state:** 64/64 provisionally mapped; 0/64 scientifically approved.

## Figure corrections

The three generic linear-region brain cartoons contained anatomically misplaced labels. Original SVG drawings and corresponding PNGs were replaced for the dorsal brains of **Scoliodon**, **frog**, and **Calotes**. Differences now shown: the shark's distal olfactory region and expanded cerebellum; the frog's enlarged paired optic lobes and narrow transverse cerebellum; the Calotes enlarged cerebral hemispheres and curved cerebellar flap. These are distinct educational schematics, not dissection-grade preparations. The PNG and SVG SHA-256 fields in the manifest were refreshed. Scientific and Tamil caption reviews remain unapproved.

### Reference text and landmarks (no source images copied)

- Scoliodon forebrain/cerebellum: https://gcwgandhinagar.com/econtent/document/15878893641ZOOTC0201-%20Brain%20%20of%20scoliodon%20%281%29-1.pdf
- Frog dorsal brain: https://mirrors.xmission.com/gutenberg/7/7/5/6/77560/77560-h/77560-h.htm
- Calotes brain: https://gdcpenukonda.ac.in/userfiles/Biology%20of%20chordates%2020242025.pdf

## Engineering fixes

1. Updated Android instrumentation semantics tags to the actual `figure_slots.json` IDs (e.g. `u2-scoliodon-external-labelled`, `u5-columba-external`, `u5-rabbit-external`) used by `FigureGallery`.
2. Changed chapter-overview pager scroll targets to LazyColumn item index 3; section-page footer remains index 4.
3. Added a native instrumentation test that enumerates all bundled pencil plate entries and checks unique (diagramId, language) keys, positive PNG decoder bounds, all 64 IDs, the shared-English-labelling policy and `PROVISIONAL_` review status.
4. Expanded CI workflow's prepare/build/emulator asset audit and artifact transfer to include `pencil_plates/`, with `audit_pencil_coverage.py` run in all three jobs.
5. Corrected stale README and QA status language.

## Verification

- `bash scripts/qa_all.sh`: local static/content/Kotlin core checks passed.
- `python3 scripts/write_figure_review_register.py`: refreshed 64-row reviewer inventory.
- `gradle :app:assembleDebug`, `gradle :app:connectedDebugAndroidTest`, device screenshots: **NOT RUN** in this environment.
- Remote branch push: **NOT PERFORMED**.

## Review instruction

No automatically generated brain image is academically accepted without review of comparative lobe proportions, pineal/diencephalon identity, apparent dorsal exposure and label anchor points by an independent zoologist. A Tamil editor must separately check the two-language captions and science terminology; English anatomical labels within the images are deliberate.
