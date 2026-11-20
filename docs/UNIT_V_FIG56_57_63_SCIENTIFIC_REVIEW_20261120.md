# CHORDATA — Figures 56, 57, 63: Source-level Scientific Visual Review

Date: 20 November 2026
Source baseline: `6b727eec3ff8c90c2bb453c0c33fb4c361ef6faa`
Correction commits: `558bbc7045433f81e4a4f07c7101659e654eec16`, `319947d382d49d03652ebd4542280afdc691c3cc`
Authority: source-image visual comparison and named historical/veterinary reference; **NOT independent third-party academic approval**.

## Figure 56 — Rabbit excretory system

- Registered image: `rabbit_urinary_tract.png` (3300×1780); original SHA-256 `7abf4f2b443086b9e323e0f32080da9be71e0eb1449416279ab5bde475430d6b`. Bitmap preserved.
- Visual check: two historical 1916 panels depict kidney, ureter, bladder and sex-specific lower urinary/reproductive arrangements. Male `Ur` marks urethra; female `Ve` marks the vestibule, **not** urethra. These are combined urogenital views, not isolated nephron sections.
- Corrected bilingual key and rabbit kidney lesson separate **ureter — சிறுநீர்க்குழல்**, **urethra — சிறுநீர்த்தாரை**, and **renal tubule — சிறுநீரக நுண்குழாய்**; **renal pelvis — சிறுநீரக இடுப்புக்குழி**. Additional renin, erythropoietin and vitamin D endocrine functions are explained in both languages.
- Historical proportions are not specimen-scaled. Independent biology and Tamil review still PENDING.
- Reference: Thomson, *Outlines of Zoology* (1916), figures 393–394; *BSAVA Manual of Rabbit Surgery, Dentistry and Imaging*, rabbit urinary anatomy; Central Scientific and Technical Terminology medical English–Tamil glossary (CSTT).

## Figure 57 — Rabbit brain

- Registered image: `rabbit_brain_en.png` (1644×1109), SHA-256 `d22d4ac27faddb7d40f67123d346f907970c8517539cfcb71313988f0d883a35`. Bitmap preserved.
- Source: Wiedersheim & Parker, *Comparative Anatomy of Vertebrates* (1907), fig. 170. A is dorsal, B ventral, C lateral. Original b.o. refers to olfactory bulb, f.b. to cerebral hemisphere, h.b. to cerebellum, md. to medulla oblongata.
- Scientific and Tamil keys now explain all four corresponding labels; historical micro-labels may require figure zoom on phones. No unsupported rescaling of anatomical parts was introduced. Independent biology, Tamil and 200% device sign-off PENDING.
- Reference: https://www.flickr.com/photos/internetarchivebookimages/20481807000/

## Figure 63 — Human–rabbit permanent dental formula

- **Pre-correction issue**: original 1448×780 count grid is numerically correct, but could mislead students about positional adjacency of the rabbit's small upper peg incisor. Original SHA-256 `9f513dc0c910dfe81febd3bb5e02ebfece5f5e5afcb9109ebfbc20cc8748508f`.
- **Corrected bitmap**: `human_rabbit_dental_formula.png`, 2200×1060, SHA-256 `29d0ac32251a09aedd446233d675dd8fd6a75122223ccdd206ca3132b9df1afc`; source script `scripts/build_fig63_plate.py`. Retains original quadrant count symbols and adds an explicit *schematic lateral inset*, with **peg tooth I2 posterior to large upper incisor I1**, diastema, absence of canines and six upper cheek teeth.
- Adult human: I 2/2, C 1/1, PM 2/2, M 3/3 = **32**.
- Adult rabbit (*Oryctolagus cuniculus*): I 2/1, C 0/0, PM 3/2, M 3/3 = **28**. One upper half-jaw has 8 teeth; one lower half-jaw has 6; total `2 × (8 + 6) = 28`.
- Exact original PNG archived at `docs/figures/retired_fig63_20261120.png`; original approval applied to that SHA only. Corrected art remains provisional; no inherited owner consent or independent biology/Tamil sign-off. Registration and source checksum updated only after actual bitmap replacement.
- Clinical references: https://www.mspca.org/clinical/dental-anatomy-and-disease-of-the-domestic-rabbit-oryctolagus-cuniculus/ ; https://www.vin.com/apputil/content/defaultadv1.aspx?id=3860700&pid=11242

## Final acceptance gates

The registered source PNG, hash, provenance, review state and figure slot must match in native APK. Figure 63 remains **QA CANDIDATE**, not an academically signed-off production figure; do not reuse its retired approval. Every figure still requires two distinct named independent reviewers for final release. Android 100%/200% text scaling, figure zoom and device readability remain engineering acceptance responsibilities.
