# CHORDATA continuous illustration QA — source-first, AI fallback

**Scope:** native Kotlin/Android CHORDATA project, 64 registered lesson figures. This is a continuous QA stream, not a numbered stage. **Production remains on HOLD.**

## Owner direction — 11 November 2026: AI artwork may be used in QA

The project owner has authorised **provisional use of original AI-generated figure artwork** and acceptance of **minor cosmetic imperfections** in the QA app. This direction is tracked per currently registered AI figure by the `ownerQaAcceptance` manifest field, and documented in [CHORDATA_AI_QA_OWNER_APPROVAL_20261111.md](CHORDATA_AI_QA_OWNER_APPROVAL_20261111.md). It is **not** independent scientific or Tamil approval. A materially wrong organ relationship, species label, leader line or learning-objective mismatch still requires correction before academic or store release. Do not block QA merely for the artwork's AI origin.

## Selection standard

1. Use an authentic published anatomical drawing or scientifically documented source when it correctly depicts the species, exact organ system, orientation and lesson learning objective. Verify the exact creator, original file/page, reuse licence, transformations and source checksum. Convert to an offline PNG without inventing or silently altering anatomy. Do not use museum specimen photographs in place of anatomical teaching diagrams.
2. Where no fit-for-purpose legally reusable plate can be confirmed, generate an original **AI-assisted anatomical PNG candidate** grounded in appropriate Zoology references. AI-generated images are *not* credited to the historical references; record the actual generator, production date, prompt summary and review warnings. Do not describe it as historically published, public-domain source artwork or scientifically verified.
3. Match precisely the existing diagram ID, topic ID, section key and page in `figure_slots.json`. Preserve separate English and Tamil lesson pages. English labels in the image are acceptable; explanatory captions and keys remain bilingual.
4. Before changing a figure, preserve previous image metadata and checksum. After replacing a figure, regenerate `docs/FIGURE_REVIEW_REGISTER_64.csv` using `scripts/write_figure_review_register.py` so any previous acceptance for a modified image resets to PENDING.
5. Check PNG signature and dimensions, filename/path integrity, SHA-256, Android placement, legibility at 100%/200% font scaling, pinch-to-zoom, orientation, academic accuracy and independent biological/Tamil sign-off. Only then generate a *QA* APK through the guarded Android workflow. Do not imply physical-device acceptance from CI alone.

## Current verified inventory — 7 November 2026

- **64/64** figure slots have a renderable provisional PNG. This represents *placement coverage*, not textbook quality.
- **44/64** existing review-register entries have original project/computer-assisted/AI-described creators and are candidates for source-first replacement or further scientific review. This count is based on the descriptions in the registered review sheet; it is not a claim that the other 20 are academically approved.
- **64/64** register entries remain `PROVISIONAL — not independently approved`, with scientific and Tamil decisions PENDING.
- Last fully successful gated QA build was commit `e4ff837887e93833183a19e3ce6ed693a90ea9d4`, workflow run `42381279942`. The build and emulator suite passed. **No physical-device sign-off or production release.**

## First AI-fallback candidate (not yet installed)

- Exact registered diagram ID: `u4-calotes-brain`
- Installed figure awaiting replacement: `pencil_plates/calotes_brain_dorsal_en.png`
- Unit IV / `u4-calotes` / brain section (verify the actual manifest page before integration).
- Generated content: `Calotes versicolor` dorsal brain schematic with six numbered regions: olfactory bulbs/tracts, cerebral hemispheres, optic lobes, cerebellum, medulla oblongata, spinal cord.
- Provenance: OpenAI ChatGPT image generation, 2026-11-07. This is **AI-assisted original candidate artwork**, not a historical source image. No reference plate was copied or traced; anatomical topology requires critical review.
- Reference leads for anatomical checks (not source-image credits): S. Y. Paranjape, *The Anatomy of the Garden Lizard* (1974), and published reptilian-brain comparative anatomy resources.
- Current status: **CANDIDATE GENERATED, NOT IN THE REPOSITORY, NOT SCIENTIFICALLY ACCEPTED**. Import the exact PNG with metadata and SHA only after comparing it against an appropriate anatomical reference. Do not trigger a release solely from this record.

## Specific scientific warning

AI renderings can exaggerate the size of the paired optic lobes and misrepresent the relationships of the olfactory bulbs, diencephalon and cerebellum. The *Calotes* brain illustration must be checked against species-specific, correctly oriented anatomy before it becomes a teaching plate. The six labels are intended as a review checklist, not an approval.

**Release gate:** scientific review + independent Tamil editorial review + on-device visual testing are all required.