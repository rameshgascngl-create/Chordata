# CHORDATA — Indian snakebite first-aid flowchart, safety evidence check

Date: 9 November 2026. **Status: medically source-checked provisional classroom text; original PNG retained; independent medical and Tamil approval outstanding.**

## Exact lesson, image provenance and disposition

- Figure ID: `u4-poison-apparatus-first-aid-flowchart`, Unit IV, `u4-poison-apparatus`, page 3, `evidence-based-first-aid`.
- Asset: `app/src/main/assets/pencil_plates/snakebite_first_aid_en.png`; 1800 × 1120, 115,692 bytes; SHA-256 `1ace57d4694bace1b0da1e5f41b2693a99bb50429f7699f18e4a3377debf52a7`.
- Retained master: `docs/original_plate_svg/snakebite_first_aid_en.svg`; SHA-256 `ef08bed905d6616dd512011a212bbd3c1ef27c87605d53b482f20105fb4bbfa2`.
- Actual diagram is a simple readable text-based emergency decision sequence, not a scientific dissection or species-ID plate. The existing PNG is appropriate to retain for the provisional QA reader; vector origins alone do not make a flowchart unfit for teaching. **Both original image and master remain unchanged**.
- Original author/licence stays `CHORDATA QA — original vector anatomical schematic`; `Original project illustration; no source images copied`. WHO/NCDC are clinical **references, not image authors**.
- Figure status unchanged: `PROVISIONAL_QA_ANATOMICAL_REVIEW_PENDING`. No fabricated scientific/Tamil sign-off.

## Verified safety priorities

1. Any suspected snakebite warrants immediate medical evaluation **even with little pain, no swelling or uncertain fang marks**. Observe the airway and breathing during transfer.
2. Move away from the animal; do not catch, handle or kill it. Call emergency services promptly and get transport to a hospital equipped for snakebite.
3. Keep the patient calm and still. Support and immobilise the bitten limb with a **loose, non-constricting splint**; remove rings, anklets, watches and tight garments before swelling.
4. Avoid tight arterial tourniquets, cutting, sucking, electric shock, ice, herbal treatments and **any delay** in medical evaluation. If vomiting occurs in a breathing person with reduced consciousness, airway-protective lateral positioning is appropriate.
5. **Pressure-immobilisation bandaging is not a universal Indian first-aid step.** Applicability depends on species and local cytotoxic injury; expert protocols and training are needed. Do not teach generic tight compression for all Indian bites.
6. Antivenom and airway/haemodynamic support are **clinical decisions**, not community self-treatment. The teaching flowchart does not replace emergency medical protocols.

## Sources verified 9 November 2026

- WHO snakebite treatment, explicit first-aid guidance and transport: https://www.who.int/teams/control-of-neglected-tropical-diseases/snakebite-envenoming/treatment
- WHO evidence discussion and country-specific pressure-bandage limits: https://www.who.int/news-room/questions-and-answers/item/snakebite-envenoming
- India's National Action Plan 2024 (NAPSE), including pressure-immobilisation uncertainty and splint priority where resources are limited: https://www.ncdc.mohfw.gov.in/wp-content/uploads/2024/07/NATIONAL-ACTION-PLAN-FOR-PREVENTION-AND-CONTROL-OF-SNAKEBITE-ENVENOMING-NAPSE.pdf
- IFRC 2025 first aid guidelines (published online 2026), snakebite immobilisation and avoidance of harmful practices: https://www.ifrc.org/sites/default/files/2026-03/IFRC%20International%20First%20Aid%2C%20Resuscitation%20and%20Education%20Guidelines%202025.pdf

## Source/QA changes, excluding artwork

- Expanded the bilingual `keyEn`, `keyTa` and `scope` in `pencil_plates/manifest.json`, without touching the immutable lessons in `chordata_content.json` or the existing registered PNG.
- Kept the original two `referenceUrls` unchanged to preserve reviewer register identity; added `scientificEvidenceUrls` for the WHO/NCDC/IFRC cross-check.
- Added `scripts/test_snakebite_first_aid_safety.py`, enforcing original image/master binary checks, accurate author attribution, page/section, both language safety messages, medical review status and nine negative mutations.
- Added safety test to `scripts/qa_all.sh` and each of the four required jobs of `.github/workflows/android-qa.yml`.
- **Unresolved:** an independent clinical reviewer must validate wording for Indian practice, and a Tamil reviewer must check terminology. Phone/tablet 100%/200% text scale and physical-device review remain outstanding. Production release HOLD.

The project never claims image-generation/replacement, medical approval, or production deployment on the strength of this text-only patch.
