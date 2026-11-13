# CHORDATA — science, Tamil and illustration pre-sign-off audit

**Date:** 13 November 2026  
**Project:** `rameshgascngl-create/Chordata`  
**Branch:** `qa/chordata-textbook-unit2-continuation-20261113`  
**Classification:** AI-assisted desk audit and issue triage; **NOT independent Zoology, Tamil or image approval**.

## Verified scope and limitations

- **39/39 syllabus topics** have expanded bilingual chapters: **298 extended sections** in English and Tamil. Schema and topic coverage are auditable; this does not certify the accuracy of every sentence.
- **64 registered figure slots**, **68 manifest variants**. The review register has **64 rows**, **18 high-priority anatomy/safety** flags. All **64 scientific and Tamil reviewer decisions remain PENDING** in the independent review register.
- **7 manifest variants have empty `license` fields.** These require origin/permission declarations; do not invent licences. Files: `pencil_plates/avian_respiration_ta.png`; `pencil_plates/columba_skeleton_ta.png`; `pencil_plates/rabbit_skeleton_ta.png`; `pencil_plates/amniote_phylogeny.png`; `pencil_plates/deuterostome_relationships.png`; `pencil_plates/vertebrate_phylogeny.png`; `pencil_plates/human_rabbit_dental_formula.png`.
- Image identifiers, manifests, historical sources and review registers were examined as **metadata and accompanying descriptive records**. **The actual PNG pixels were not directly inspected in this connector session**; therefore recognisability, leader-line accuracy, text legibility and actual anatomical topology are **NOT visually certified**.
- Full sentence-by-sentence independent Zoology review of all 298 extended sections, all Tamil prose and the original 117 quiz keys remains outstanding. Source links below are reference leads, not an assertion that every URL/licence was fully verified.

## Corrected source defects on this QA branch

1. `u2-parental-care/seahorse-pouch`: Tamil male brood pouch was incorrectly called `கருப்பை` (uterus) and "male pregnancy" used `ஆண் கருவுறுதல்`; replaced with `கரு அடைகாப்புப் பை` and `ஆண் கருத் தாங்குதல்`.
2. `u5-rabbit/classification-and-lagomorph-identity`: corrected the mammal-wide presentation of placental development, which excludes monotremes and misrepresents marsupial diversity.
3. `u5-marsupials/short-gestation`: standardised `மஞ்சள் கருப் பை` for yolk sac.
4. `u2-scoliodon-external-labelled`: the illustration is a milk shark `Rhizoprionodon acutus`, not `Scoliodon`. Both displayed captions and the independent review register explicitly say it is **comparative, not the named type specimen**. The PNG itself is unchanged.

## Scientific checkpoints demanding qualified visual inspection

- **Phylogeny and taxonomy:** modern Chordata, Olfactores, Cyclostomata, actinopterygian/sarcopterygian split, bird-inclusive sauropsids, and distinguish traditional classes from monophyletic clades. Verify current `Phrynoderma hexadactylum` with synonym `Rana hexadactyla`.
- **Anatomical topology:** shark gills and sensory openings, frog carotid/systemic/pulmocutaneous arches, Calotes ventricles and outflow tracts, avian respiratory airflow and reproductive structures, rabbit skull/skeleton and neuroanatomy.
- **Reproductive sequence:** axolotl paedomorphosis is not a mandatory normal metamorphic stage; platypus and echidna photographs are different species; marsupial pouch is not a uterus; seahorse male pouch is not a mammalian placenta.
- **Safety:** snake photos are not safe field identification keys; no tight tourniquet, cutting, suction or delay in transport. Recheck medical content against WHO and Indian Ministry of Health/NCDC.
- **Terminology editorial policy:** retain English species names and anatomical plate labels when they aid accuracy, but provide correct Tamil prose, captions and explanatory keys; do not substitute phonetic transliteration for a precise Tamil explanation where one exists. Use `முதுகுநாண்` (notochord), `தொண்டைச் செவுள் பிளவுகள்` (pharyngeal slits), `கரு அடைகாப்புப் பை` (brood pouch), `நஞ்சுக்கொடி` (placenta), `பற்சூத்திரம்` (dental formula) consistently in context. Preserve recognised English taxonomic terms parenthetically where warranted.

## Sixty-four-figure independent acceptance worksheet

**Interpretation:** "Provisional" means the file is registered, **not anatomically approved**. "High" is the current register's risk priority, not a rejection. A missing licence is a rights blocker, not necessarily a biological error.

| # | Registered figure ID | Priority | Desk flag | Provenance / variants | What the independent reviewers must establish |
|---:|---|---|---|---|---|
| 1 | `u1-origin-deuterostome-relationships` | Standard | **RIGHTS DECLARATION OPEN** | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 2 | `u1-general-characters-five-chordate-characters` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 3 | `u1-hemichordata-balanoglossus-external` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 4 | `u1-urochordata-ascidia-larva-adult` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 5 | `u1-cephalochordata-branchiostoma-labelled` | Standard | Provisional | Published / sourced; 2 variants | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 6 | `u1-vertebrata-characters-vertebrate-anatomy` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 7 | `u1-vertebrata-classification-vertebrate-phylogeny` | High | **RIGHTS DECLARATION OPEN** | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 8 | `u1-agnatha-petromyzon-adult-larva` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 9 | `u2-pisces-classification-fish-groups` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 10 | `u2-scoliodon-external-labelled` | Standard | Provisional | Published / sourced; 1 variant | **Species mismatch**: picture is Rhizoprionodon acutus, not Scoliodon. Comparison caption corrected; require verified Scoliodon specimen before exact-species anatomical acceptance. |
| 11 | `u2-scoliodon-digestive-labelled` | High | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 12 | `u2-scoliodon-gills-labelled` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 13 | `u2-scoliodon-brain-labelled` | High | Provisional | Published / sourced; 1 variant | Historical dogfish comparison, not verified Scoliodon; verify every neuroanatomical label and make comparative limitation visible. |
| 14 | `u2-scoliodon-sense-organs-labelled` | High | Provisional | Published / sourced; 1 variant | Peer-reviewed epaulette shark Hemiscyllium ocellatum, not Scoliodon; restrict to comparative systems. |
| 15 | `u2-dipnoi-lungfish-comparison` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 16 | `u2-scales-fins-scale-types-labelled` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 17 | `u2-scales-fins-fins-labelled` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 18 | `u2-accessory-respiration-accessory-organs-comparison` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 19 | `u2-parental-care-parental-care-comparison` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 20 | `u2-migration-migration-cycle` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 21 | `u2-economic-importance-fishery-value-chain` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 22 | `u3-amphibia-classification-living-orders` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 23 | `u3-amphibia-classification-life-cycle` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 24 | `u3-origin-devonian-transition` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 25 | `u3-rana-external` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 26 | `u3-rana-respiration` | High | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 27 | `u3-rana-arterial-system` | High | Provisional | Published / sourced; 1 variant | Historical Rana esculenta arterial source is not the Phrynoderma type study; verify topology and present as comparative only. |
| 28 | `u3-rana-brain` | High | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 29 | `u3-adaptive-features-comparative-body-plans` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 30 | `u3-neoteny-axolotl-development` | Standard | Provisional | Published / sourced; 1 variant | Published comparison not a mandatory two-stage normal axolotl life cycle; check paedomorphosis caption. |
| 31 | `u3-parental-care-parental-care-comparison` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 32 | `u4-reptilia-classification-living-reptile-orders` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 33 | `u4-calotes-external` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 34 | `u4-calotes-digestive-system` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 35 | `u4-calotes-respiratory-system` | Standard | Provisional | Original or AI (source declaration); 1 variant | AI candidate: glottis, trachea, bronchi, lungs and ventilatory mechanics require specialist inspection. |
| 36 | `u4-calotes-arterial-system` | High | Provisional | Original or AI (source declaration); 1 variant | **High anatomical risk**: AI provisional Calotes heart/arterial plate; check both systemic arches, cavum partitions, pulmonary veins, outflow/neck branches against published Calotes dissection before acceptance. |
| 37 | `u4-calotes-brain` | High | Provisional | Original or AI (source declaration); 1 variant | AI candidate: taxon-specific shape, lobe order and leader lines not certified. |
| 38 | `u4-origin-extinct-amniote-phylogeny` | High | **RIGHTS DECLARATION OPEN** | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 39 | `u4-origin-extinct-extinct-groups` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 40 | `u4-snakes-india-big-four-identification` | High | Provisional | Published / sourced; 1 variant | Source-based photographs only for academic comparison; must not provide a lay identification test or delay emergency care. |
| 41 | `u4-poison-apparatus-venom-apparatus` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 42 | `u4-poison-apparatus-first-aid-flowchart` | High | Provisional | Original or AI (source declaration); 1 variant | **Safety critical**: check against WHO and current Indian guidance; immobilisation and immediate transport, no tourniquet/cut/suction; figure cannot be used as medical decision chart. |
| 43 | `u4-skull-temporal-skull-types` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 44 | `u5-aves-classification-bird-lineages` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 45 | `u5-columba-external` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 46 | `u5-columba-endoskeleton` | Standard | **RIGHTS DECLARATION OPEN** | Published / sourced; 2 variants | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 47 | `u5-columba-urinogenital` | High | Provisional | Original or AI (source declaration); 1 variant | Check paired testes, functional left ovary/oviduct, absent urinary bladder and ureter-to-cloaca route. |
| 48 | `u5-columba-sense-organs` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 49 | `u5-flight-adaptations-wing-aerodynamics` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 50 | `u5-flight-adaptations-flight-muscles` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 51 | `u5-flight-adaptations-avian-lung` | High | **RIGHTS DECLARATION OPEN** | Published / sourced; 2 variants | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 52 | `u5-bird-migration-flyway-stopovers` | High | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 53 | `u5-mammalia-classification-mammal-lineages` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 54 | `u5-rabbit-external` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 55 | `u5-rabbit-endoskeleton` | Standard | **HOLD: material defect** | Published / sourced; 2 variants | Tamil-specific AI variant marked MATERIAL_ANATOMY_ERROR and withheld: verify English historical fallback in both reading languages; do not clear incorrect image. |
| 56 | `u5-rabbit-excretory-system` | High | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 57 | `u5-rabbit-brain` | High | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 58 | `u5-rabbit-sense-organs` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 59 | `u5-egg-laying-mammals-monotreme-reproduction` | Standard | Provisional | Published / sourced; 1 variant | Platypus adult and echidna young are different species, not consecutive photographs of one life cycle. |
| 60 | `u5-marsupials-marsupial-life-history` | Standard | Provisional | Published / sourced; 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 61 | `u5-flying-mammals-bat-wing-glider-comparison` | Standard | Provisional | Original or AI (source declaration); 1 variant | Inspect image anatomy, caption, Tamil key, species/view, 100%/200% zoom and source credit. |
| 62 | `u5-aquatic-mammals-aquatic-mammal-groups` | Standard | Provisional | Published / sourced; 1 variant | Composite real photographs; figures show convergent aquatic adaptations, not one mammalian taxonomic order. |
| 63 | `u5-dentition-human-rabbit-dental-formula` | High | **RIGHTS DECLARATION OPEN** | Original or AI (source declaration); 1 variant | Independent count verification: human 32; Oryctolagus 28; rabbit 2/1 upper/lower incisors per side including peg tooth. No licence declaration recorded. |
| 64 | `u5-dentition-tooth-types` | Standard | Provisional | Published / sourced; 1 variant | Historical HUMAN tooth engraving; do not caption as typical morphology of all mammal taxa. |

## Independent dual-review protocol

1. **Zoology reviewer (named, qualified, not the Tamil reviewer):** open the actual English PNG at original resolution and on a phone; validate taxon/specimen, view and developmental stage, organ connections, leader-line termini, function, and source comparison. Record exact pass/revision reasons with cited anatomical pages or specimen evidence. A cosmetic flaw alone is not a rejection; an impossible organ, incorrect species attribution or unsafe treatment arrow is a hold.
2. **Tamil scientific editor (different named reviewer):** compare each full English/Tamil chapter and each figure key; verify Tamil Nadu biology textbook register, transliterations, grammar, scientific referents, mathematical notation and unambiguous captions at 100%, 150% and 200%. Image labels may remain in English when Tamil explanatory text is accurate.
3. **Provenance and rights reviewer:** verify every original source page, image author, specific licence version, adaptation duties and actual redistributed PNG. Resolve all 7 blank declarations; never infer that an online image is freely reusable.
4. **Approval evidence:** update `docs/FIGURE_REVIEW_REGISTER_64.csv` with the two real reviewer identities, separate decisions, notes, source evidence and exact asset hashes. Do not mark `ACCEPTED` by proxy or use the project owner as both independent reviewers. Replacing any PNG invalidates prior sign-off for that variant.
5. **Device/engineering gate:** run `python3 scripts/write_figure_review_register.py --check`, source, APK and hash audits, emulator UI/image screenshots and release checks. Only run `--release-check` when true dual decisions have been recorded; keep app-store submission on hold until Android and rights gates pass.

## Reference leads used for targeted cross-checks

- American Museum of Natural History, *Amphibian Species of the World*: https://amphibiansoftheworld.amnh.org/Amphibia/Anura/Dicroglossidae/Dicroglossinae/Phrynoderma/Phrynoderma-hexadactylum
- ITIS, accepted Phrynoderma and older Rana combination: https://itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=1270588
- WHO snakebite envenoming treatment and first aid: https://www.who.int/teams/control-of-neglected-tropical-diseases/snakebite-envenoming/treatment
- Indian national snakebite action plan: https://ncdc.mohfw.gov.in/wp-content/uploads/2024/07/NATIONAL-ACTION-PLAN-FOR-PREVENTION-AND-CONTROL-OF-SNAKEBITE-ENVENOMING-NAPSE.pdf
- MSPCA-Angell veterinary rabbit dentition: https://www.mspca.org/clinical/dental-anatomy-and-disease-of-the-domestic-rabbit-oryctolagus-cuniculus/
- Calotes circulatory references cited in existing dedicated QA note `docs/CHORDATA_CALOTES_AMSTERDAM_ORIGINAL_PNG_WAVE10_QA.md` and `docs/CARDIOVASCULAR_PLATES_QA_2026-11-06.md`; these are reference leads, **not permission to reproduce the figures**.

**Bottom line:** technical placement and provisional owner permission must not be represented as independent anatomical/Tamil approval. Keep **64/64** figure decisions pending until genuine dual review evidence is supplied, while permitting existing policy-compliant provisional QA display.
