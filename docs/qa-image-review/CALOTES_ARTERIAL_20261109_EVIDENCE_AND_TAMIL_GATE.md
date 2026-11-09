# CHORDATA — Calotes versicolor arterial-system evidence and bilingual QA gate
**Date:** 9 November 2026
**Branch:** `qa/chordata-calotes-arterial-evidence-20261109`
**Outcome:** SOURCE AND TAMIL KEY CORRECTION; EXISTING PROVISIONAL PNG RETAINED.

## Exact classroom destination
- Diagram ID: `u4-calotes-arterial-system`.
- Unit IV; `u4-calotes`; page **4**; `arterial-system`.
- Registered PNG: `app/src/main/assets/pencil_plates/calotes_heart_arteries_en.png`.
- Installed PNG size: **137,849 bytes**; SHA-256: `12305ec4249359a17fd4c17f5445fa7ba7e73894d6feea5e701072dc467840ed`.
- Retained (not modified) editable SVG: `docs/original_plate_svg/calotes_heart_arteries_en.svg`; SHA-256 `c70d16457a5329a5c26388f491e20c9eab5fddb1a5b8121a9bb1356b8b658c7b`.
- No change to PNG, SVG, `figure_slots.json`, or `chordata_content.json`. No new artwork, original photograph, AI candidate or simulator has been installed.

## Verified species-specific anatomy and restrictions
The 1956 P.H.D.H. de Silva *Calotes versicolor* arterial-system account explicitly states:

1. The right and left systemic arches unite into the dorsal aorta near the level of the ventricular apex.
2. The vertebral and subclavian arteries originate on the dorsal surface of the **right systemico-carotid pathway**. Therefore a symmetric right-and-left depiction of subclavian origins from opposite systemic arches is not established.
3. The ductus caroticus relates the carotid and systemic pathways: a line straight across the left and right carotid trunks is not the same structure.
4. The described oesophageal, thyroid, mesenteric and dorsal aortic arterial branches are much more detailed than the installed generic cavity-flow sketch. A full species-specific branch map should not be claimed from that sketch.

Comparative reptile heart literature supports a functionally divided ventricle with **cavum arteriosum**, **cavum venosum**, and **cavum pulmonale**, not the mammalian four-chamber arrangement.

**Existing labelled-image caution:** The retained original vector master and its PNG show `Intercaval flow`. The term `intercaval` usually refers to the venae cavae; it is not a correct unqualified name for *intercavitary* flow among the ventricular cava. The label is not silently altered in this QA branch. It is disclosed in the displayed English/Tamil figure key until a species-validated figure replaces it.

## Audit and licensing
- **Primary anatomical source:** de Silva, P.H.D.H. (1956), *The arterial system of Calotes versicolor (Daudin)...*, `Spolia Zeylanica` **28(1):69–86**, https://eurekamag.com/research/023/819/023819374.php .
- **Comparative cardiac anatomy:** Jensen et al. (2013), *Development of the Hearts of Lizards and Snakes and Perspectives to Cardiac Evolution*, https://pmc.ncbi.nlm.nih.gov/articles/PMC3673951/ .
- **Earlier image-rejection and technical rationale:** `docs/qa-image-review/calotes_arterial_image_rejection_20261108.md`.

The 1956 paper and modern comparative publications are **anatomical references**, not redistribution licences. The rejected AI-generated arterial image has uncertain carotid ductus, subclavian laterality, vessel orientation and missing ventricular cavity labels. It remains **NOT INSTALLED**. The existing project-drawn PNG carries its actual project origin and is still provisional.

## Actual changes on this branch
- Revised `keyEn`, `keyTa`, `scope` and non-displayed `editorialCaution` of the one registered figure in `pencil_plates/manifest.json`.
- Added de Silva 1956 URL as an anatomical reference (`referenceUrls`, **not** `sourceUrl`): cited research is not represented as the creator of the existing drawing.
- Added `scripts/test_calotes_arterial_species_evidence.py`, validating the exact old PNG/SVG, source attribution, absent green tick, bilingual science keys and provisionally pending review. It also runs **8 negative manipulations**.
- Added the check to `scripts/qa_all.sh`; the native Android/CI gate continues to test all 64 registered lessons and 68 asset variants.
- All previously accepted, credited and green-ticked images remain untouched.

## Acceptance still blocked
Independent Zoology review must verify a new complete species-specific topology and every label. Separate Tamil scientific editing and 360px/200% text-scale phone checks, pinch zoom, orientation and physical-device QA remain outstanding. After a replacement is explicitly approved for provisional QA, its **real binary** and hash, creator, source licence, original provenance, and review register must be committed atomically. A green CI run for these text-only corrections **does not imply the Calotes arterial artwork is corrected**.

**No production merge; production release HOLD.**
