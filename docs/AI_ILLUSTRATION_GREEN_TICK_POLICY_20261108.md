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
