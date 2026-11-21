# CHORDATA — Project-owner illustration authorisation

Date: 21 November 2026
Repository: rameshgascngl-create/Chordata
Branch: qa/chordata-textbook-unit2-continuation-20261113

## Owner decision
The project owner explicitly authorised use of the CHORDATA illustrations in the educational application by stating: "approve illustrations". On 21 November 2026 the owner additionally clarified: **"I reviewed and approved the illustrations myself as project owner."** This supersedes the earlier conversational claim of two separate scientific and Tamil reviewers, which is **not substantiated by the review register**. This records the owner’s own review and approval, not an independent dual-review sign-off.

Scope: the 64 registered undergraduate lesson illustration slots in `app/src/main/assets/figure_slots.json`, with associated offline images as actually selected by the Compose gallery. This is approval for use in the project and the owner’s statement that they personally reviewed the images. It is **not** evidence of two independent human reviewers, a documented per-figure scientific/Tamil decision, or verified third-party image rights.

## Conditions retained
- Any image/variant explicitly marked `USER_REJECTED_REPLACEMENT_REQUIRED` or `scientificRiskHold` remains withheld as gallery logic requires. The previously held Tamil rabbit-skeleton plate has since been replaced with the exact credited public-domain historical rabbit engraving in commit `5fdc498f6ccf0681e3d31ceb342c2d2669b04c20`, and its source/audit repairs passed QA at commit `01e25c2c0d2073e3e0bb4af2722ccd73f3e8c5bd`. The rejected AI artwork must not be reactivated.
- Preserve exact existing illustrations, captions, source attribution, licence notices and source hashes. Do not replace or redraw illustrations through this approval.
- The existing 64-row figure review register remains unchanged: do not fill scientific/tamil reviewer names, decisions or evidence on another person's behalf.
- The independent two-reviewer release gate and declared image-rights requirements remain distinct from project-owner authorisation. Record a failed release gate transparently rather than bypassing or falsifying it.
- Changes to a figure's bytes require renewed checks against the updated asset and provenance.

**Current release condition (21 November 2026):** The canonical `docs/FIGURE_REVIEW_REGISTER_64.csv` still shows 64 slots and 128 `PENDING` reviewer decisions. The gated `--release-check` currently requires separately named scientific and Tamil reviewers with evidence. An owner-only review does not satisfy that rule. The release gate has not been bypassed, and production signing must not be represented as complete.

This note records the owner’s review/authorisation, not a build, a production signature, an app-store approval or an independent two-person review.
