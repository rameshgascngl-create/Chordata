# CHORDATA — native app anatomical figure coverage QA

**Checkpoint:** 6 November 2026, evening (IST). **Scope:** unmerged local source package prepared from the saved 35/64 checkpoint. GitHub branch `native/qa-chordata-illustration-coverage` was last verified separately at commit `5371d7ecfc8a03955ba86100578dad6538c5fd26` and **has not been updated with the work in this package**.

## Coverage and provenance

- **64 of 64 unique diagram IDs now have a registered, provisionally renderable plate** on an exact lesson-section page; no slot is omitted.
- The recovered checkpoint included **32** distinct pencil-plate slots, plus **three** legacy provisional specimen outlines supplying other slots: 35/64 visible.
- This continuation adds **32 original English-labelled schematics**, including replacements for those three legacy outlines, to reach 64/64 in the pencil-plate registry.
- `pencil_plates/manifest.json` contains **68 diagram/language entries** mapping to **67 distinct PNG files**. The additional entries are retained older language variants and one reused drawing across two related slots.
- The **seven legacy PNG records**, original creators, source pages, modification notes, and license/source-hash metadata remain intact. They are fallback/credited references, not academically approved plates.
- The added 32 plates were drawn as **original editable SVG files** under `docs/original_plate_svg/` and rendered to PNG. No copyright source image was traced or embedded in these new drawings. Each records a factual reference URL; those reference URLs do **not** claim ownership of the generated image.
- The native FigureGallery selects English-labelled plate variants for **both English and Tamil reading modes** while keeping the original Tamil caption and lesson narrative separate. The interface exposes the creator, licence description and factual reference without misidentifying it as a copied source image.

## Local verification — passed

- JSON content pack unchanged: 39 topics, 127 sections, 117 quizzes, 64 unique diagram IDs.
- Every slot has the correct topic, page and section key. New plate entries also contain an exact lesson mapping and learning-objective description.
- PNG signature, dimensions (minimum 1200×600), byte count and SHA-256 verified for all 68 entries; the 32 new SVG masters have independently recorded SHA-256 values.
- No unexpected or unregistered PNG files, duplicate `(diagramId, language)` entries, or missing English/shared assets.
- Existing four cited historical/Commons images and the three original provisional outlines remain credited and intact.
- Native content audit and 24 Kotlin domain smoke assertions passed; Android manifest and strings XML parse.
- Local visual contact-sheet inspection performed. The frog arterial and Calotes cardiovascular schematic were revised during this pass to avoid incorrect direct vessel relationships; all plates retain a **scientific review pending** caption.

## Quality and release constraints — NOT passed

- **Scientific/anatomical approval: 0/64.** These are diagrams for editorial review, not accepted dissection-grade plates. Particularly important review subjects: frog and Calotes circulatory systems, shark and frog brains, accessory breathing organs, pigeon urinogenital ducts, reptile/snake morphology, and pedagogical appropriateness of simple comparative silhouettes. Some figures are deliberately conceptual flow or phylogeny charts rather than anatomical drawings.
- **Tamil editor approval: pending.** In the chosen English-label policy, the Tamil reviewer checks lesson text, page caption, terminology and meaning, not translations inside the artwork.
- **Medical sign-off: pending** for snakebite first aid. The original QA draft uses WHO and Indian NCDC recommendations: immobilise, remove tight items, urgent hospital transfer; avoid tourniquets, cutting, suction and unproven remedies. This plate must not stand alone as a clinical protocol.
- **Android compilation/emulator/physical-device tests: not run on these new bytes.** This environment lacks Gradle, Android SDK and access to Android dependency hosts. The older successful CI run on the remote branch does not validate this updated package.
- **GitHub push: not performed.** `git ls-remote` failed with DNS resolution error in this container. No unrelated branches or production state were modified.
- **Production APK: not generated; release on HOLD.** No signoff is implied by passing static validation.

## Required independent acceptance

Use `docs/FIGURE_REVIEW_REGISTER_64.csv` to record, for each figure, the biological reviewer and Tamil editor, corrections, source and ownership decision, and final sign-off. Re-run local QA and Android CI after review and then perform physical-device tests with English/Tamil at 100% and 200% font scaling, orientation changes, pinch-to-zoom and next-page scroll-to-top.

### Reference anchors

- OpenStax Biology 2e, Chordates: https://openstax.org/books/biology-2e/pages/29-1-chordates
- Frog vascular system, historical public-domain anatomy: https://www.gutenberg.org/cache/epub/77560/pg77560-images.html
- Historical frog anatomy archive: https://upload.wikimedia.org/wikipedia/commons/f/fc/The_frog_-_an_introduction_to_anatomy_and_histology_(IA_frogintroduction00mars).pdf
- Open University comparative anatomy: https://www.egyankosh.ac.in/bitstream/123456789/16528/1/Unit-9.pdf
- Pigeon zoology teaching resource: https://www.kngac.ac.in/elearning-portal/ec/admin/contents/4_18K1B-CHAZ1_2020120708200484.pdf
- WHO snakebite treatment: https://www.who.int/teams/control-of-neglected-tropical-diseases/snakebite-envenoming/treatment
- Indian NCDC snakebite guidance: https://ncdc.mohfw.gov.in/uploads/pdf/COH9.pdf
- NOAA marine mammal lineages: https://www.noaa.gov/education/resource-collections/marine-life/marine-mammals
