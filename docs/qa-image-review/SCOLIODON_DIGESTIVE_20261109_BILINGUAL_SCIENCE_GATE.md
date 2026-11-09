# CHORDATA — Scoliodon digestive-system scientific/editorial correction
**Checkpoint:** 9 November 2026 · **Status:** caption/QA-gate improvement only; candidate replacement PNGs are **NOT installed**.

## Exact registered lesson and immutability
- Diagram ID: `u2-scoliodon-digestive-labelled`
- Page: Unit II, `u2-scoliodon`, page **2**, section `digestive-system`
- Installed asset: `app/src/main/assets/pencil_plates/scoliodon_digestive_en.png`
- Installed PNG: **581,960 bytes**, SHA-256 `57f1bd87ee5ea529eff8bec7ca5ac4a60c2dca1be6afb62daf52ba024741cf17`
- Retained editable source: `docs/original_plate_svg/scoliodon_digestive_anatomy_en.svg`, SHA-256 `4730126353f7c18a67cdf45f22ebee5e3669ae0745296d35c98db4735fbcd8bf`.
- Exact image, source, and copyright attribution are **unchanged**. English/Tamil figure explanations are corrected in `pencil_plates/manifest.json`. The immutable `chordata_content.json` is **not edited**. All other 63 registered lesson images and their artwork bytes are **unchanged**.
- Existing figure remains `PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING`, no independent Zoology or Tamil sign-off.

## Anatomy gate grounded in published Zoology teaching sources
1. Follow the **luminal continuity**: mouth → pharynx → oesophagus → long cardiac stomach → short pyloric stomach → pyloric valve → **bursa entiana** → broad intestine with scroll valve → narrow rectum → cloaca.
2. **Blind sac** arises at the junction/bend between the cardiac and pyloric limbs, not at the pyloric valve or from the intestinal wall.
3. **Bursa entiana** is a short thick-walled chamber immediately distal to the pyloric valve. Do not omit it or label the stomach–intestine junction directly as the scroll-valve intestine.
4. The **scroll valve** is an internally rolled longitudinal mucosal sheet; cross-sectional appearance is a watch spring (about two and a half turns in the IGNOU teaching account), not a generic ladder or externally coiled small intestine.
5. The **bilobed liver, gallbladder and bile duct** supply the **anterior intestine**, not the pyloric stomach. The pancreas is adjacent to the stomach–intestine fold and its duct enters the intestine; exact duct openings require species-level verification.
6. The **tubular rectal gland** opens into the rectum; it is involved in **salt elimination**, not digestive enzyme secretion.
7. Traditional course name **Scoliodon sorrakowah** denotes a historical milk-shark combination (now associated with *Rhizoprionodon acutus*); avoid claiming that a generic dogfish drawing is a dissected specimen of *S. laticaudus* or *R. acutus*.
8. On-device: examine the exact figure at 360 px width, Tamil 200% type scaling, pinch zoom, portrait and landscape. No simulated screenshot equals physical-device acceptance.

### Scientific sources — for verification, not figure-reproduction permission
- IGNOU, *Comparative Anatomy of Vertebrates-I*, Unit 3, pp. 88–90: https://www.egyankosh.ac.in/bitstream/123456789/58839/1/Unit%203%20Digestive%20System.pdf
- IGNOU, *Animal Diversity-II*, Unit 6: https://egyankosh.ac.in/bitstream/123456789/16525/1/Unit-6.pdf
- NTR Government Degree College, *Digestive System in Scoliodon*: https://www.ntrgdc.ac.in/userfiles/file/Course%20Materials/Semester-2-Digestive%20system%20in%20Scoliodon.pdf
- Biol. Discussion anatomy explanation (secondary cross-check): https://www.biologydiscussion.com/fisheries/dogfishes/scoliodon-distribution-structure-and-sense-organs-dogfishes/40699
- Wikimedia Commons [Squa152p.png](https://commons.wikimedia.org/wiki/File:Squa152p.png), **Jon Houseman**, CC BY-SA 3.0: a *dogfish* digestive reference, **not verified Scoliodon-specific**. Do not substitute it silently.

## AI-generated candidates and decisions — no misleading green ticks
| Candidate | Image SHA-256 | Resolution | Decision | Material defect |
|---|---|---:|---|---|
| Previous candidate with numbered callouts | `de1ff7e35de060dc0733efa61ec23f0b905a948b7e3b7e6e7944ea4a533eb010` | 1199×1312 | **HOLD** | Duplicate numeral 11; generic helical intestine inset; sub-1200 px width; duct geometry uncertain |
| New unlabelled anatomical reconstruction | `8dcfd0d8fc43fef3816e793b9adf8a405e03877c409efd252d731838f5814bb7` | 1086×1448 | **HOLD** | Source width below QA minimum; longitudinal exposed intestine resembles transverse ridges instead of unequivocally longitudinal scroll; bile/pancreatic duct insertions unverified |
| Generated two-topic poster | `c2cf142749b6d643936a5bf95fbb0537e6bf9104048f3930f33f71ae0444b84c` | 1536×1024 | **REJECT** | Incorrectly claims Scoliodon and Calotes plates are installed and tested; contains unverified anatomical labelling. Not appropriate as evidence or a lesson figure |

Generated imagery is original AI-created art. Published Zoology references provide **scientific comparison**, not artwork credits or permission to claim these are verified dissections. Candidate binaries are kept separate from the GitHub Android asset directory. They have **not** been pushed to this branch and are **not part of the APK**.

## Implemented improvement
- Revised bilingual English/Tamil figure keys and scope using Tamil Nadu Zoology textbook-style terminology.
- Added `scripts/test_scoliodon_digestive_science_gate.py` to fail closed if the installed source SHA, author, original SVG master, provisional review state, lesson placement or critical anatomy keys change unexpectedly.
- Exercised seven negative manipulations (including false approval and AI green-ticking) as automated mutation tests.
- Added this script to `scripts/qa_all.sh`, before the guarded native Kotlin and emulator jobs.
- **No production merge.**

## Remaining, before any true image replacement
A licensed original figure correctly depicting the species and all structures, or a scientifically corrected original PNG, must be independently reviewed for topology; every callout and its leader must be checked. Then update the exact binary, SHA-256, rights and review register together, run the complete 64-figure audit, Kotlin compilation and instrumented tests, and obtain physical-device acceptance. **Production release remains on HOLD.**
