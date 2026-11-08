# AI-generated anatomical images — green-tick QA integration policy
**Effective:** 8 November 2026. **Scope:** CHORDATA native Android QA branch only.  
**Decision authority:** User explicitly permitted incorporation of AI-generated PNG artwork with minimal errors. A green tick means **allowed in a provisional QA build**, not scientifically certified or production-approved.

## Decision rule
- **GREEN TICK — `GREEN_TICK_ALLOW_PROVISIONAL_QA_USE`:** An original AI PNG may be installed and shown on its registered lesson page when the main external/anatomical structures, organ relationships, orientation and label directions are materially correct. Minor stylisation, small proportional simplification, missing secondary labels and minor visual defects do not block provisional integration. Explicitly disclose illustration status.
- **HOLD:** Materially incorrect anatomy, missing/incorrect critical organ connections, invented structures, wrong taxon, misleading labels, misleading medical/safety content, licence/provenance uncertainty or serious mobile-legibility defects.
- **Independent formal review:** Biology and Tamil approval, academic accuracy sign-off, real-device verification and production release approval remain distinct, pending requirements. Do not alter `reviewStatus` to approved or mark a human reviewer ACCEPTED because a green tick was granted.
- **Asset identity:** Permission applies only to the exact SHA-256 for the reviewed PNG. Replacement bytes require fresh screening and new provenance/hash checks.
- **CI gates remain mandatory:** 64 slot mapping, 68 manifest variants, source-file hashes, Kotlin compilation, Android instrumentation, and gated QA APK publishing. Never relax checks for easier acceptance.

## Green-tick decisions — 8 November 2026
| Registered slot | Existing file | SHA-256 | Result | Minor limitations |
|---|---|---|---|---|
| `u3-amphibia-classification-living-orders` | `amphibian_orders.png` | `c870937f5036cbfc69f7a6ed38d427a1a3d6aa1d2756a80805a25e17ee442e33` | GREEN TICK | Generalised not-to-scale morphology, not species identification |
| `u3-adaptive-features-comparative-body-plans` | `amphibian_orders.png` | same | GREEN TICK | Shares the same original PNG |
| `u4-calotes-respiratory-system` | `calotes_respiratory_en.png` | `0e0a997568a03986575bc08ed77126ccf10e32e43d2b317cee4a65629be7dc46` | GREEN TICK | Internal faveolar/septal structures are schematic |
| `u4-calotes-brain` | `calotes_brain_dorsal_en.png` | `a9d3136b213c96e62bc5cb45742474b325d9dbb8185502ed7e24bb1a4f3c3030` | GREEN TICK | Pineal/diencephalic details omitted, simplified proportions |

These are **three distinct PNGs across four registered figure slots**, already present in the QA source; no figure content was modified. The green-tick metadata records affirmative permission to retain and use them in the QA app without waiting for perfect artwork. The remaining AI images have **not** been given blanket approval; review individually, including Tamil labels and body-plan geometry.

## Reference checks (verification, not copied artwork)
- Amphibian orders: Zoological Survey of India checklist — https://www.zsi.gov.in/uploads/documents/checklist/english/118_AMPHIBIA_New.pdf
- Caecilian anatomy: NSOU Zoology notes — https://www.wbnsou.ac.in/online_services/SLM_UGC_DEB/UG_4YR/ZOOLOGY/5CC-ZO-02_E.pdf
- `Calotes` lung: https://www.kalikadevicollegeshirurkasar.org/sites/default/files/1595342386113.pdf
- Reptile faveoli/septa: https://pmc.ncbi.nlm.nih.gov/articles/PMC13163023/
- `Calotes` dorsal brain: Tamil Nadu government Higher Secondary Zoology Vol. I — https://www.tamildigitallibrary.in/admin/assets/book/TVA_BOK_0001362_Zoology.pdf

**No image binaries, source credits, academic reviewer decisions, immutable lesson content or production branch were changed by this metadata-only acceptance checkpoint.**

## Next batch of exact-PNG reviews (8 November 2026)

These decisions apply to **Tamil image variants** only; their separately credited English PNG versions are unchanged. Source PNG checksums were confirmed inside the downloaded `CHORDATA_QA_Source_Figures` archive, not inferred from scaled screenshots.

| Registered figure / image | SHA-256 | Decision | Scope and limitations |
|---|---|---|---|
| `u5-flight-adaptations-avian-lung` / `avian_respiration_ta.png` | `e29ead970da9fd42aa067bb810ec414fd0e63a78f84ab6e0ea19b4f4673bee40` | ✅ GREEN TICK | Recognisable trachea, paired lungs and major air-sac groups. Schematic sac sizes and not the exact nine-sac arrangement; use for basic location only, not precise bronchial airflow or individual-sac counts. |
| `u5-columba-endoskeleton` / `columba_skeleton_ta.png` | `358c4d80563995f9b48e744df6d5cd0d924b40ece64bba2d31eb0e59530a8760` | ✅ GREEN TICK | Essential wing, leg, trunk, skull, and keeled-sternum elements are identifiable. Slight proportion and joint simplifications and Tamil orthography await editorial checking; not measurement-grade. |
| `u1-cephalochordata-branchiostoma-labelled` / `branchiostoma_ta.png` | `e1d8b5a749628f3c49cae235c5dd52649f44fa597eb86ca6ce43a8b7404a1e75` | HOLD | Two exaggerated gonads misrepresent the multiple serially arranged segmental gonads of Branchiostoma. Revise anatomy before a green tick; retain existing independent review gates. |
| `u5-rabbit-endoskeleton` / `rabbit_skeleton_ta.png` | `e004bee33be5e6f5f47fdeb4e306bd1b0834d8a6cfc3c6ee5eee070e237a2cad` | HOLD | Rabbit tail/caudal skeletal proportions are exaggerated and not reliably rabbit-specific. Needs comparative skeleton correction before green tick. |

**Cumulative result:** five distinct AI PNGs with green ticks covering six manifest entries (two amphibian reuse slots, Calotes respiratory system, Calotes brain, and the two Tamil avian plates). Two Tamil AI plates are on hold for material anatomy issues. No AI-origin PNG bytes were edited. Green ticks expressly permit **provisional integration and display in QA builds**, without changing `reviewStatus` or independent scientific/Tamil approval, which remain pending. A held variant is not newly authorized by this policy; any preexisting provisional presence in the QA app is unchanged pending correction.

**Review references (not reuse licences):**
- Avian sac anatomy: https://pmc.ncbi.nlm.nih.gov/articles/PMC11864839/
- Bird air-sac labelled reference: https://omeka.uottawa.ca/biodidac/items/show/5570
- Branchiostoma gonads in serial arrangements: https://www.gutenberg.org/cache/epub/73702/pg73702-images.html
- Rabbit vertebral regions: https://lifelib.info/en/biology/science_1/196.html

**Provenance:** No external figure was copied; reviewed PNGs remain credited as generated with ChatGPT ImageGen.
