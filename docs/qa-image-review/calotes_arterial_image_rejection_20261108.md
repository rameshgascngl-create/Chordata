# CHORDATA — Calotes arterial-system QA gate (8 November 2026)

## Registered slot and current asset
- Exact diagram ID: `u4-calotes-arterial-system`
- Topic/page/section: `u4-calotes`, 4, `arterial-system`
- Current manifest path: `pencil_plates/calotes_heart_arteries_en.png`
- Current PNG SHA-256: `12305ec4249359a17fd4c17f5445fa7ba7e73894d6feea5e701072dc467840ed`
- Current master: `docs/original_plate_svg/calotes_heart_arteries_en.svg`
- Retain this figure **provisionally** while sourcing a scientifically accurate replacement. It shows cardiac flow topology but not the full species-specific arterial branching expected from the lesson caption.
- Current SVG master uses the label `Intercaval flow` between ventricular cavity regions. Review this terminology: `intercaval` conventionally concerns the venae cavae, not communications between `cavum arteriosum`, `cavum venosum` and `cavum pulmonale`. Do not silently amend the approved source without review.

## Original AI candidate (NOT embedded)
- Generated with OpenAI ImageGen, 8 November 2026; species/theme: `Calotes versicolor` arterial circulation. This is an original generated candidate, **not** artwork from any primary textbook.
- Original file `a_detailed_anatomical_illustration_poster_an_orna.png`, 1086×1448 px, 3,231,722 bytes.
- Exact SHA-256: `7a2be21f59f9949d63726b80f7cf87ba317bde03004ac91053f135b619f1deaa`.
- Current disposition: `REJECT_AS_TEACHING_PLATE__REVISE_AND_SCIENTIFICALLY_REVIEW`.
- The carotid-duct drawing looks like a transverse connection between carotids. In the `Calotes` teaching anatomy, the ductus caroticus is a lateral connection between the carotid and systemic pathways. This is a significant suspected topological error.
- The candidate depicts left and right subclavians symmetrically from opposite systemic arches, whereas the species-specific De Silva account places the vertebral and subclavian supply in the right systemico-carotid pathway. Resolve branch identity and side orientation against the primary original.
- The generated heart inset does not name the cavum arteriosum, cavum venosum and cavum pulmonale.
- Full circulatory trace, position of the aortic union, pulmonary trunk bifurcation, leader-line placement and correct dorsal/ventral viewing orientation are not independently demonstrated.
- At 360px phone width, finer labels and inset annotations are small. A device screenshot and 200% text-scale test are needed.
- This candidate is **not** in the app assets, review register or APK. Do not treat photorealism as anatomical verification.

## Evidence leads — not redistribution credits
1. P.H.D.H. de Silva (1956), *The arterial system of Calotes versicolor ...*, `Spolia Zeylanica` 28:69–86, species-specific description of arterial arches and branches: https://eurekamag.com/research/023/819/023819374.php .
2. P.H.D.H. de Silva (1956), *The heart and aortic arches in Calotes versicolor ...*, `Spolia Zeylanica` 28:55–67; bibliographic lead in first source.
3. Jensen et al. (2013), *Development of the Hearts of Lizards and Snakes and Perspectives to Cardiac Evolution*, comparative squamate heart anatomy, https://pmc.ncbi.nlm.nih.gov/articles/PMC3673951/ .
4. Tamil Nadu Textbook Society (1978), *Zoology Higher Secondary First Year, Vol. I*, arterial system description; printed `© Government of Tamilnadu`, so do **not** assume diagrams may be redistributed: https://tamildigitallibrary.in/assets/docs/uploads/primary_files/book/TVA_BOK_0001362_Zoology.pdf .
5. IGNOU `Animal Diversity II` comparative circulatory account, https://egyankosh.ac.in/bitstream/123456789/16527/1/Unit-8.pdf . Textual reference only; redistribution rights unverified.

## Next acceptance plan
- Produce an accurate **species-specific topology draft first**, anchored to primary sources; explicitly verify right versus left systemico-carotid arch, ductus caroticus, pulmonary bifurcation, heart chamber morphology and dorsal aorta union.
- Obtain original legally reusable anatomy artwork with verified creator/license if possible; otherwise a new original PNG after a Zoology reviewer validates the draft topology. No scanned textbook art without permission.
- Register full asset SHA, exact rights, correct image and labels, independent Biology/Tamil decisions, and mobile readability. Rebuild and test through native QA and emulator.
- Production release **HOLD**. The immutable `chordata_content.json` remains unchanged after fix `d00e4697aa650d0bd36559eedc7172c29f8c56fb`.
