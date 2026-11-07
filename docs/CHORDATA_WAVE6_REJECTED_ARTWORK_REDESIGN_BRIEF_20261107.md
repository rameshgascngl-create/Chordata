# CHORDATA anatomical image quality reset — 7 November 2026

## User feedback — rejected illustrations

The user explicitly rejected the generated anatomical illustrations as unsuitable for this Zoology app. The current Wave 6 brain candidate is **USER_REJECTED_REPLACEMENT_REQUIRED**. This is a visual-pedagogical rejection, not a signed professional assessment of every internal organ. Do **not** advertise this image as a scientifically approved atlas plate or release the application to production based on its technical tests.

### Defects found in the existing Wave 6 figure
- Smooth abstract lobes and simplified line geometry do not resemble a serious textbook anatomical dissection.
- Fine regional anatomy and cranial-nerve relationships are underspecified.
- The exact visual appearance of the olfactory apparatus, partly concealed optic lobes, folded shark cerebellum, and corpora restiformia needs comparison with actual specimen drawings.
- Caption, art creator, illustration taxon, and lesson's old *Scoliodon sorrakowah* designation must remain distinct.

### Defects in the NEW AI-generated naturalistic *candidate* (not added to app)
- Although visually more detailed, its apparently separated cerebrum is inconsistent with the **undivided, smooth dorsal cerebrum** described for Scoliodon; cannot claim a verified anatomical view.
- Cerebellar surface looks strongly mammalian/cerebral in its convolution and requires shark-specific comparison; render realism ≠ scientific fidelity.
- Olfactory bulb vs sac, cranial nerve placement and labels have **not** received independent scientific review.
- **DISPOSITION: REJECTED AS A VERIFIED TEACHING PLATE, never embedded or approved.**

## Replacement sourcing standard
1. Prioritise a clear, authentic, detailed dorsal/ventral/section textbook-anatomy plate (not a museum photograph, decorative shark image, abstract SVG or generic algorithmic silhouette).
2. Verify taxon. **Scoliodon terrae-novae** in the 1902 primary source is **Rhizoprionodon terraenovae**, the Atlantic sharpnose shark, **not** the Indian milk shark *Rhizoprionodon acutus* referenced by the course's historic *Scoliodon sorrakowah*. Historical comparative drawings of other sharks may support scientific checking, but must NEVER be captioned as species-specific milk-shark dissection.
3. Source references and rights for each exact plate before reuse; modern textbook scans supplied on public URLs are not automatically licensed for redistribution.
4. Retain author, primary source/page, date, actual licence and modifications; do not credit a generated drawing to an original textbook author.
5. Independent Zoology reviewer checks topological anatomy and every leader line, separate Tamil reviewer checks terms, and phone-scale inspect. Do not mark APPROVED without these gates.
6. Keep rejected PNG out of the **approved** artwork collection and maintain separate QA provenance. QA compilation and image-file checksum success alone do not establish academic suitability.

### Sources verified for anatomy and candidate historic reference
- Gandhinagar Government College *Brain of Elasmobranchs (Scoliodon)* (teaching reference, **not licensed for in-app reproduction**): https://gcwgandhinagar.com/econtent/document/15878893641ZOOTC0201-%20Brain%20%20of%20scoliodon%20%281%29-1.pdf
- UPRTOU UGZY-104, pp. 54 ff. (undivided cerebrum and Scoliodon structure, **not assumed licensed for reuse**): https://www.uprtou.ac.in/other_pdf/28062025_UGZY_104.pdf
- Historic original research by W. A. Locy, *A New Cranial Nerve in Selachians* (published 1903), Plate V, Figure 9; taxon `Scoliodon terrae-novae` (Atlantic sharpnose; **not milk shark**): https://upload.wikimedia.org/wikipedia/commons/8/82/MBLWHOI_Library_%28IA_markanniversaryv00park%29.pdf
- Scoliodon taxon mismatch verified via Harvard MCZ revised identification: https://mczbase.mcz.harvard.edu/guid/MCZ:Ich:35209
- Comparative neuroanatomy source only: https://anatomypubs.onlinelibrary.wiley.com/doi/full/10.1002/ar.25028

## QA isolation
Wave 5 commit `60f5270de6ea9ee22087b2e0a1b7f2677118c303` remains the latest historical successful APK checkpoint preceding Wave 6; **neither Wave 5 nor Wave 6 is production-accepted**.
Wave 6 tested branch `qa/chordata-scoliodon-brain-wave6-20261107` remains unchanged to preserve audit and CI evidence.
This **review** branch records user's rejection without making a new distributable APK. It must not be merged to main or interpreted as scientific validation.
