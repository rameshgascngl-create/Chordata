# Calotes arterial-system AI PNG — new provisional candidate (11 November 2026)

## Grounded integration slot
- Figure ID: `u4-calotes-arterial-system`.
- Unit IV / `u4-calotes` / page 4 / `arterial-system`.
- Current APK asset remains `app/src/main/assets/pencil_plates/calotes_heart_arteries_en.png`, manifest SHA-256 `12305ec4249359a17fd4c17f5445fa7ba7e73894d6feea5e701072dc467840ed`.
- This note is **NOT** an integration or approval of new image bytes. The current file, JSON manifest, figure-review register, all image binaries and production branch are unchanged.

## Candidate file (generated outside repository)
- Candidate basename: `CHORDATA_Calotes_Arterial_AI_Provisional_20261111.png`.
- Original generated file: `a_highly_detailed_educational_anatomical_infograph.png`.
- Original AI-generated PNG, 1086 × 1448 RGB, 2,856,303 bytes.
- SHA-256 `57470d8b5c251d39a3a6e80765ef0aa6bcfe802ed9307d9abdb71c06b7100efb`.
- Origin: OpenAI ChatGPT ImageGen, 11 November 2026. No copyrighted source plate was copied. English labels; not-to-scale schematic.
- The candidate and an independently downscaled 360-pixel-width readability preview are available separately in the conversation attachment `CHORDATA_Calotes_Arterial_QA_Candidate_20261111.zip`; **the bytes have not been staged in the repository or APK**.
- **Status:** `PROVISIONAL_CANDIDATE__REQUIRES_SPECIES_TOPOLOGY_AND_PHONE_REVIEW`.
- Relative to the earlier rejected candidate, this version labels a single dorsal aorta formed by joining two systemic arches, paired pulmonary branches, a right-pathway subclavian/vertebral branch, carotid arteries and an inset with the three ventricular cavities.

## Critical anatomical checks before image installation
1. Verify the connection from carotid pathway to each systemic arch (`ductus caroticus`); do not mistake a transverse carotid connection for this anatomical duct.
2. Confirm exact right systemico-carotid branch placement, subclavian and vertebral branch origins, and left/right ventral orientation against de Silva's 1956 species-specific descriptions.
3. Validate pulmonary trunk bifurcation, aortic arch convergence, and the cavities `cavum arteriosum`, `cavum venosum`, `cavum pulmonale` in the heart inset.
4. On 360 px-wide screens labels become small: check zoom and orientation, not just visual attractiveness.
5. The user's 11 November 2026 blanket consent for AI-generated QA illustrations accepts **minor cosmetic imperfections**, but does not override misleading vascular connections, independent Zoology/Tamil review or device checks.

## Anatomical sources (not image credits)
- P. H. D. H. de Silva (1956), `The arterial system of Calotes versicolor`, *Spolia Zeylanica* 28(1):69–86, https://eurekamag.com/research/023/819/023819374.php
- Jensen et al. (2013), `Development of the Hearts of Lizards and Snakes and Perspectives to Cardiac Evolution`, https://pmc.ncbi.nlm.nih.gov/articles/PMC3673951/

## Install procedure
If validated and source bytes are actually available to the build system: replace only the exact registered PNG, update manifest source/rights/size/SHA fields, regenerate the figure-review register with changed image reviewer decisions reset, run source/placement/hash checks, Kotlin native compilation, emulator image/zoom tests and APK hash audit. Do not mark as installed without a real Git commit containing the PNG and a successful rebuilt APK. Production is on HOLD.
