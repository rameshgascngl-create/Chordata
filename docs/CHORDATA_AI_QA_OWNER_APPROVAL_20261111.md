# CHORDATA — Owner approval for AI-generated illustration use in QA
**Decision date:** 11 November 2026

The project owner explicitly approves the use of original AI-generated illustrations in the CHORDATA *QA Android application*, accepting **minor cosmetic/visual imperfections** when the teaching structure, taxonomy and leader-line anatomy are not materially misleading.

This grants **owner/editorial acceptance for provisional QA display**, not independent scientific certification, Tamil language sign-off, image ownership beyond recorded provenance, or approval to publish to an app store. It does not waive native compilation, file integrity, licence/creator metadata, physical-device checks, or the existing separate release gate.

## Current registered AI images
The current manifest at parent commit `58768e9ee4a745afd3051a31d097272366cb4afa` has **9 manifest variants representing 8 distinct PNG paths**. The general owner direction was considered for nine entries; eight are approved for provisional QA display and the existing materially erroneous Tamil rabbit-skeleton variant is explicitly excluded. Each entry records the applicable decision as `ownerQaAcceptance=OWNER_APPROVED_FOR_PROVISIONAL_QA_USE_2026-11-11` (without changing `reviewStatus`, `visualReview`, image SHA-256, image source, captions or binary bytes).

| Diagram ID | Image path | Owner QA use |
|---|---|---|
| `u1-cephalochordata-branchiostoma-labelled` | `pencil_plates/branchiostoma_ta.png` | Approved for provisional display |
| `u5-flight-adaptations-avian-lung` | `pencil_plates/avian_respiration_ta.png` | Approved for provisional display |
| `u5-columba-endoskeleton` | `pencil_plates/columba_skeleton_ta.png` | Approved for provisional display |
| `u5-rabbit-endoskeleton` | `pencil_plates/rabbit_skeleton_ta.png` | **WITHHELD — material anatomical error; existing English source remains the QA fallback** |
| `u3-amphibia-classification-living-orders` | `pencil_plates/amphibian_orders.png` | Approved for provisional display |
| `u3-adaptive-features-comparative-body-plans` | `pencil_plates/amphibian_orders.png` | Approved for provisional display |
| `u4-calotes-digestive-system` | `pencil_plates/calotes_digestive_en.png` | Approved for provisional display |
| `u4-calotes-respiratory-system` | `pencil_plates/calotes_respiratory_en.png` | Approved for provisional display |
| `u4-calotes-brain` | `pencil_plates/calotes_brain_dorsal_en.png` | Approved for provisional display |

## Remaining exceptions and checks
- An AI figure already present in the app **may remain** during QA with minor visual defects. Do not remove a correct image just because it was AI-generated.
- Incorrect organ connections, fabricated organs, misidentified taxa, incorrect labels, incorrect lesion/venom/first-aid content, materially wrong vascular routes and mismatched learning objectives **do not qualify as minor cosmetic errors**. Record such concerns as pending correction without representing them as academically approved.
- `u3-adaptive-features-comparative-body-plans` currently shares `pencil_plates/amphibian_orders.png` with the separate living-orders page. It is owner-approved only for **provisional QA**, and its fit to the adaptive-features objective must be reviewed.
- `u4-calotes-brain`, `u4-calotes-respiratory-system` and `u4-calotes-digestive-system` remain pending independent anatomical and Tamil checks. The separate arterial-system ImageGen candidate flagged for a possible carotid-duct topology error was not integrated and is **not** approved as an accurate species-specific teaching plate by this statement.
- Register scientific/tamil reviewer identities and evidence **only after real reviews**. Do not fabricate signatures or mark all 64 `ACCEPTED`.
- For **future** AI-generated images, this is permission to use AI as an original-artwork source and tolerate minor cosmetic errors; it is not an automatic visual/anatomical sign-off for unseen images.

**Scope:** QA branch only, no production merge or release approval. All existing original/credited source images are preserved.

## 11 November 2026 — material-anatomy exception audit
A subsequent source audit found the `u5-rabbit-endoskeleton` Tamil candidate already carried `aiQaIntegrationDecision=HOLD_MATERIAL_ANATOMY_ERROR`. It is **not** a minor cosmetic issue and is excluded from the otherwise general owner permission. The manifest records `scientificRiskHold=MATERIAL_ANATOMY_ERROR`, the app's Tamil selector is guarded, and the integration test asserts the credited English plate remains the fallback. **No image was replaced, scientifically approved, or removed.**
