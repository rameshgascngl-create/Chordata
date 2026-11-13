# CHORDATA — Owner decision on 64 illustrations

**Date:** 13 November 2026  
**Authority:** Explicit project-owner instruction in the current ChatGPT conversation: approve all images except the Calotes cardiovascular illustration, which may be corrected if needed.  
**Scope:** This is **owner permission for provisional use in the undergraduate QA textbook**, not independent scientific/Tamil sign-off, not copyright verification, and not an app-store release clearance.

## Decision

- **63/64 canonical figures: OWNER APPROVED for provisional reader display.** Accepted minor cosmetic imperfections do not invalidate their use at this stage. The exact SHA-256 is preserved in `app/src/main/assets/pencil_plates/manifest.json` as `ownerQaAcceptedSha256`.
- **One canonical figure withheld:** `u4-calotes-arterial-system`. The original 1536 × 1024 PNG has a material arterial topology problem; the pulmonary trunk appears continuous with the systemic/dorsal-aortic channel. Do not present that image to students as correct anatomy. Scientific replacement/correction required. Original asset and credits remain intact for traceability.
- **Rabbit skeleton variant:** The `u5-rabbit-endoskeleton` slot **is owner approved via the historical English/shared fallback** (1890 sourced engraving). The separate Tamil AI image remains withheld because of its documented exaggerated caudal/skeletal proportions. This does not reduce the approved canonical count below 63.
- Existing three user-green-ticked Tamil QA figures continue to be displayed only when they meet the code's selected-variant checks; their hashes are covered separately in the manifest.
- The 64-row independent figure review register retains the scientific and Tamil decisions as `PENDING`, because owner consent cannot be represented as two independent subject-editor signatures.

## Non-negotiable image constraints

Preserve exact lesson-page placement, PNG bytes, source authorship, image licences, bilingual captions and the pure Kotlin/Jetpack Compose reader. A user-rejected or materially erroneous variant must not be shown merely because all *other* figures have permission. The Calotes replacement must have separate pulmonary outflow from cavum pulmonale and paired systemic aortic arches from cavum venosum; the systemic arches join posteriorly into the dorsal aorta. Do not depict a pulmonary-artery connection to the aorta. Distinguish schematic vessel crossings from anatomical junctions.

## Exact 64 canonical decisions

| # | Registered figure ID | Owner QA decision | PNG SHA-256 prefix |
|---:|---|---|---|
| 1 | `u1-origin-deuterostome-relationships` | OWNER APPROVED — QA | `ee710fdc11c2851c…` |
| 2 | `u1-general-characters-five-chordate-characters` | OWNER APPROVED — QA | `8f0daae6d7180613…` |
| 3 | `u1-hemichordata-balanoglossus-external` | OWNER APPROVED — QA | `fd237c4155fd2a1e…` |
| 4 | `u1-urochordata-ascidia-larva-adult` | OWNER APPROVED — QA | `af4f986941cd3b9f…` |
| 5 | `u1-cephalochordata-branchiostoma-labelled` | OWNER APPROVED — QA | `68acc2123fa7f57c…` |
| 6 | `u1-vertebrata-characters-vertebrate-anatomy` | OWNER APPROVED — QA | `f828c226f6d99ab9…` |
| 7 | `u1-vertebrata-classification-vertebrate-phylogeny` | OWNER APPROVED — QA | `376a255f8c67d250…` |
| 8 | `u1-agnatha-petromyzon-adult-larva` | OWNER APPROVED — QA | `d833b1aec9541f1c…` |
| 9 | `u2-pisces-classification-fish-groups` | OWNER APPROVED — QA | `54617d2619e40baa…` |
| 10 | `u2-scoliodon-external-labelled` | OWNER APPROVED — QA | `f422a6fedf39b78c…` |
| 11 | `u2-scoliodon-digestive-labelled` | OWNER APPROVED — QA | `195e816c3f80b1f6…` |
| 12 | `u2-scoliodon-gills-labelled` | OWNER APPROVED — QA | `675f497ab223df41…` |
| 13 | `u2-scoliodon-brain-labelled` | OWNER APPROVED — QA | `8d61c1196f020158…` |
| 14 | `u2-scoliodon-sense-organs-labelled` | OWNER APPROVED — QA | `f4772942d441d025…` |
| 15 | `u2-dipnoi-lungfish-comparison` | OWNER APPROVED — QA | `1437c11f73c9ee05…` |
| 16 | `u2-scales-fins-scale-types-labelled` | OWNER APPROVED — QA | `e38720273c567a67…` |
| 17 | `u2-scales-fins-fins-labelled` | OWNER APPROVED — QA | `aeba9a4f555fd14b…` |
| 18 | `u2-accessory-respiration-accessory-organs-comparison` | OWNER APPROVED — QA | `30c841301b6042ee…` |
| 19 | `u2-parental-care-parental-care-comparison` | OWNER APPROVED — QA | `8bbd87a865d337f6…` |
| 20 | `u2-migration-migration-cycle` | OWNER APPROVED — QA | `f9133cf0914059e1…` |
| 21 | `u2-economic-importance-fishery-value-chain` | OWNER APPROVED — QA | `b8e92f0384e194bd…` |
| 22 | `u3-amphibia-classification-living-orders` | OWNER APPROVED — QA | `c870937f5036cbfc…` |
| 23 | `u3-amphibia-classification-life-cycle` | OWNER APPROVED — QA | `ef964ec0e3b79971…` |
| 24 | `u3-origin-devonian-transition` | OWNER APPROVED — QA | `5ccf005dc7c9729f…` |
| 25 | `u3-rana-external` | OWNER APPROVED — QA | `14aff74ada05aa62…` |
| 26 | `u3-rana-respiration` | OWNER APPROVED — QA | `99c7af022ef4ba7b…` |
| 27 | `u3-rana-arterial-system` | OWNER APPROVED — QA | `899fdfb9b260a209…` |
| 28 | `u3-rana-brain` | OWNER APPROVED — QA | `444c7eefc643da3f…` |
| 29 | `u3-adaptive-features-comparative-body-plans` | OWNER APPROVED — QA | `c870937f5036cbfc…` |
| 30 | `u3-neoteny-axolotl-development` | OWNER APPROVED — QA | `fcf3c3e327d535e8…` |
| 31 | `u3-parental-care-parental-care-comparison` | OWNER APPROVED — QA | `dac94c5386b213c8…` |
| 32 | `u4-reptilia-classification-living-reptile-orders` | OWNER APPROVED — QA | `8f47ff3fb6091fa5…` |
| 33 | `u4-calotes-external` | OWNER APPROVED — QA | `8439ff408895aaa1…` |
| 34 | `u4-calotes-digestive-system` | OWNER APPROVED — QA | `5da6f592cd726621…` |
| 35 | `u4-calotes-respiratory-system` | OWNER APPROVED — QA | `5f63ba851ba07488…` |
| 36 | `u4-calotes-arterial-system` | WITHHELD — anatomy error | `2c3406c9def947bc…` |
| 37 | `u4-calotes-brain` | OWNER APPROVED — QA | `a9d3136b213c96e6…` |
| 38 | `u4-origin-extinct-amniote-phylogeny` | OWNER APPROVED — QA | `30e155bfc27e6e84…` |
| 39 | `u4-origin-extinct-extinct-groups` | OWNER APPROVED — QA | `c36f69163bd291ee…` |
| 40 | `u4-snakes-india-big-four-identification` | OWNER APPROVED — QA | `60e62f263f46f4a4…` |
| 41 | `u4-poison-apparatus-venom-apparatus` | OWNER APPROVED — QA | `e148ff90ecfe3206…` |
| 42 | `u4-poison-apparatus-first-aid-flowchart` | OWNER APPROVED — QA | `1ace57d4694bace1…` |
| 43 | `u4-skull-temporal-skull-types` | OWNER APPROVED — QA | `e8f29b8b0f579da0…` |
| 44 | `u5-aves-classification-bird-lineages` | OWNER APPROVED — QA | `ce2378fa9c280260…` |
| 45 | `u5-columba-external` | OWNER APPROVED — QA | `38d10a35534d7b1a…` |
| 46 | `u5-columba-endoskeleton` | OWNER APPROVED — QA | `15213b2c1423a5d1…` |
| 47 | `u5-columba-urinogenital` | OWNER APPROVED — QA | `f0678127364b73f7…` |
| 48 | `u5-columba-sense-organs` | OWNER APPROVED — QA | `3873ea66a86d8540…` |
| 49 | `u5-flight-adaptations-wing-aerodynamics` | OWNER APPROVED — QA | `7021e9247f61ba90…` |
| 50 | `u5-flight-adaptations-flight-muscles` | OWNER APPROVED — QA | `3b424eb0227d3b77…` |
| 51 | `u5-flight-adaptations-avian-lung` | OWNER APPROVED — QA | `c3d43b9dbdf71d41…` |
| 52 | `u5-bird-migration-flyway-stopovers` | OWNER APPROVED — QA | `bc124ea5859a9284…` |
| 53 | `u5-mammalia-classification-mammal-lineages` | OWNER APPROVED — QA | `86f40d17432f9376…` |
| 54 | `u5-rabbit-external` | OWNER APPROVED — QA | `9a5c6e1a7870bbeb…` |
| 55 | `u5-rabbit-endoskeleton` | OWNER APPROVED — QA | `25a9d4a68486c540…` |
| 56 | `u5-rabbit-excretory-system` | OWNER APPROVED — QA | `7abf4f2b443086b9…` |
| 57 | `u5-rabbit-brain` | OWNER APPROVED — QA | `d22d4ac27faddb7d…` |
| 58 | `u5-rabbit-sense-organs` | OWNER APPROVED — QA | `868ca1fa8803f902…` |
| 59 | `u5-egg-laying-mammals-monotreme-reproduction` | OWNER APPROVED — QA | `018d3e2e8c0c4dc4…` |
| 60 | `u5-marsupials-marsupial-life-history` | OWNER APPROVED — QA | `36a23af112b64db6…` |
| 61 | `u5-flying-mammals-bat-wing-glider-comparison` | OWNER APPROVED — QA | `a28bc2f6ea085406…` |
| 62 | `u5-aquatic-mammals-aquatic-mammal-groups` | OWNER APPROVED — QA | `491c242f293c2ed2…` |
| 63 | `u5-dentition-human-rabbit-dental-formula` | OWNER APPROVED — QA | `9f513dc0c910dfe8…` |
| 64 | `u5-dentition-tooth-types` | OWNER APPROVED — QA | `f4769037610ed1ea…` |

## Independent acceptance gates unaffected

Formal Zoology editorial review, Tamil scientific-language review, source-licence resolution, and final store-release signing remain separate. Never populate the independent reviewers' names or `ACCEPTED` fields without actual reviewer evidence.

**Key comparative anatomy reference:** Jensen et al., 2013, *PLOS ONE*, https://pmc.ncbi.nlm.nih.gov/articles/PMC3673951/ .
