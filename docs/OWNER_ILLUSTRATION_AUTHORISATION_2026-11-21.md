# CHORDATA — Project-owner illustration authorisation

Date: 21 November 2026
Repository: rameshgascngl-create/Chordata
Branch: qa/chordata-textbook-unit2-continuation-20261113

## Owner decision
The project owner explicitly authorised use of the CHORDATA illustrations in the educational application by stating: "approve illustrations".

Scope: the 64 registered undergraduate lesson illustration slots in `app/src/main/assets/figure_slots.json`, with associated offline images as actually selected by the Compose gallery. This is approval for use in the project; it is **not** an assertion that a human reviewer has independently inspected each image or certified anatomical, Tamil-label, attribution or licensing accuracy.

## Conditions retained
- Any image/variant explicitly marked `USER_REJECTED_REPLACEMENT_REQUIRED` or `scientificRiskHold` remains withheld as the current gallery logic requires, including the held Tamil rabbit-skeleton variant. Owner authorisation does not silently reverse an image-specific rejection.
- Preserve exact existing illustrations, captions, source attribution, licence notices and source hashes. Do not replace or redraw illustrations through this approval.
- The existing 64-row figure review register remains unchanged: do not fill scientific/tamil reviewer names, decisions or evidence on another person's behalf.
- The independent two-reviewer release gate and declared image-rights requirements remain distinct from project-owner authorisation. Record a failed release gate transparently rather than bypassing or falsifying it.
- Changes to a figure's bytes require renewed checks against the updated asset and provenance.

This note records the owner's decision only; it is not a build, a production signature, an app-store approval or independent scientific sign-off.
