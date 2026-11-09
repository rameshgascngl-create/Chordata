# CHORDATA — *Scoliodon* gill lesson QA decision (9 November 2026)

**Decision: retain current original schematic, not green-tick the AI-generated alternative.**
This is editorial, scientific-provenance and CI-gate work; **no new image was integrated**.

## Exact registered slot and retained art
- Unit II, `u2-scoliodon`, page 3, `respiratory-system`; ID `u2-scoliodon-gills-labelled`, `lang: shared`.
- Installed PNG `app/src/main/assets/pencil_plates/shark_gill_flow.png`: 442,559 bytes, SHA-256 `675f497ab223df417274b8641bfc09b5a40729a4c74e419208bb08794353a90c`.
- Editable source `docs/original_plate_svg/shark_septal_gills_en.svg`: SHA-256 `930f7d9eaa57ab381ea3b20f299c1169b9cb9bda646cd3bb50e2479986a9e2e6`.
- Neither image binary changed; all other accepted or previously installed artwork is preserved.
- Existing origin remains `CHORDATA QA project — original vector shark septal-gill teaching schematic`. Neither historical authors nor AI generators are falsely credited for this image.
- Figure remains `PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING`, `REPLACED_VISUAL_QA_PENDING`. Human review-register decisions are unchanged.

## New candidate inspected, **not installed**
- Filename in the ChatGPT conversation: `CHORDATA_Scoliodon_Gills_Anatomical_Candidate_HOLD.png`.
- Original AI-assisted illustration, 9 November 2026.
- Composed candidate: 1536×1410 pixels, 2,771,641 bytes; SHA-256 `8bdc73552afb268cbef0edfd2c50de818bb2e6da6d063112fa14337ab15b4a27`.
- Candidate strengths: five externally visible gill slits, no external spiracle, appealing gill-filament visual texture.
- Scientific limitations: the right-side cutaway appears to show adjacent conceptual septa but does **not demonstrate the distribution of one hyoid posterior hemibranch, four branchial holobranchs, the gill-free fifth branchial arch, or individual pouch boundaries**. Neither the internal lamellar arrangement nor the anatomical relation to the real milk-shark specimen is verified.
- **No green tick** for this candidate as a complete zoological teaching plate. No candidate binary was uploaded to GitHub and it is not in the QA APK.
- The candidate's external-head drawing also lacks provenance as an actual `Rhizoprionodon acutus` specimen. Do not represent it as a field-identification photograph.

## Scientific corrections provided to the student in English and Tamil
The `keyEn`, `keyTa`, `scope` fields of the **existing** plate were revised, without editing the artwork:
1. Five distinct external gill slits on each side of the studied shark.
2. Hyoid arch with **one posterior hemibranch**, first **four branchial arches** carrying full holobranchs and the **fifth** gill-free arch.
3. Cartilaginous gill arches and supporting rays; septa between adjacent pouches, hemibranchs made of primary gill filaments with capillary-rich secondary lamellae.
4. Water path: mouth → pharynx → pouch/gill-lamellar surfaces → separate external gill slit, with countercurrent blood–water exchange.
5. The course's historical name `Scoliodon sorrakowah` is generally treated as `Rhizoprionodon acutus` (milk shark) in Eschmeyer's Catalog and ITIS; it should **not be conflated** with the distinct spadenose shark `Scoliodon laticaudus`.
6. The milk shark has no externally open spiracle, even though generic dogfish diagrams may show spiracles; do not copy such an opening into this figure.

## Scientific references (not reproduction licences)
- Evans et al. (2005), *The Multifunctional Fish Gill*: https://journals.physiology.org/doi/10.1152/physrev.00050.2003
- Eschmeyer's Catalog of Fishes, synonym status for the historical name: https://researcharchive.calacademy.org/research/ichthyology/catalog/fishcatget.asp?spid=26425
- ITIS taxonomic report, `Scoliodon sorrahkowah`: https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=160219
- Milk-shark morphology and absence of spiracles (2025 species review): https://www.tandfonline.com/doi/full/10.1080/24750263.2025.2537751
- Comparative pedagogical morphology, Uttarakhand Open University `BSCZO-201`: https://uou.ac.in/sites/default/files/slm/BSCZO-201.pdf

## QA enforcement
- `scripts/test_scoliodon_gill_qa_guard.py` verifies the exact registered page, shared PNG/SVG hashes, truthful creator and licence, both detailed language keys, evidence links and pending independent review.
- Nine mutation/negative checks reject false green ticks, false reviewer acceptance, source substitution, incorrect lesson placement, missing Tamil content and missing hemibranch facts.
- The script is included in `scripts/qa_all.sh` and **each of the four required jobs** in `.github/workflows/android-qa.yml`.
- A green CI outcome certifies only **the current provisional source and tests**. Scientific/Tamil reviewer signoff, device-level text legibility and any accurate replacement PNG remain outstanding.
- **Production release HOLD; no merge into main.**
