# CHORDATA AI10 source intake — all 10 original PNGs committed

**Date:** 13 November 2026
**Working branch:** `qa/chordata-play-finalisation-20261112`

All ten exact, owner-selected AI10 original PNGs have been committed to their registered Chordata lesson paths. The first eight were already accepted into this QA branch; the remaining two have now been transferred as unmodified bytes through GitHub Git Data blobs, without Colab, and attached through an atomic Git tree commit.

| Diagram ID | Installed PNG | SHA-256 |
|---|---|---|
| `u4-origin-extinct-extinct-groups` | `extinct_reptile_lineages_en.png` | `c36f69163bd291ee663f54c1575e6de3dd52caa80d6990cdb5bd81b02a367f18` |
| `u5-columba-urinogenital` | `pigeon_urinogenital_en.png` | `f0678127364b73f72dff3a857aa61a0fae56715003c1805d86606ad679630404` |

The Git object identities for those exact PNG bytes are `072af78849d9e6500f009e2e3f8d5baf65d64a30` and `16bfe7fd35de459d21a772481b63264022406148`. The previous provisional PNGs remain recoverable from Git history. Manifest attributions now correctly identify OpenAI ImageGen originals rather than falsely crediting unrelated historical figures. All other previously accepted figures and source credits remain unchanged.

**RELEASE HOLD:** Owner-directed integration approval is not independent anatomical or Tamil editorial sign-off. Both reviews remain `PENDING`, as do final on-device checks and Play upload-key signing. Run `python3 scripts/audit_ai10_release_assets.py`, `python3 scripts/qa_all.sh` and the exact-commit Android QA workflow before distributing an APK. Do not publish an AAB based on a pre-AI10 green build.
