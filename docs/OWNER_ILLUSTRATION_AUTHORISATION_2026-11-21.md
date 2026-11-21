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
- On 21 November 2026 the owner explicitly authorised an *alternative release policy*: accept their documented project-owner figure review instead of demanding two independent science/Tamil reviewer identities. The release workflow must enforce exact versioned assets via `docs/OWNER_FIGURE_APPROVED_ASSETS_20261121.json` and `scripts/verify_owner_release.py`. The original independent-review register and strict two-reviewer validator remain intact as an optional separate track. All source-licence, scientific-safety, hash, privacy, Android-QA and signing requirements remain independent gates.
- Changes to a figure's bytes require renewed checks against the updated asset and provenance.

**Updated owner-authorised release policy (21 November 2026):** The canonical `docs/FIGURE_REVIEW_REGISTER_64.csv` still shows 64 slots and 128 `PENDING` *independent* reviewer decisions. These have not been falsified or marked accepted. The owner authorises the protected Play workflow to use the separate **locked owner-approval evidence** and SHA-256/image-rights validator instead of the independent two-reviewer `--release-check`. Any illustration, slot, source, attribution, rights or SHA change invalidates this approval until the owner explicitly approves a new lock. Owner approval does not independently verify third-party licences, publisher declarations or the upload signing key; separate tests remain in place. Production signing has not yet occurred.

This note records the owner’s review/authorisation, not a build, a production signature, an app-store approval or an independent two-person review.
