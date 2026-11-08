# CHORDATA Calotes digestive-system scientific/text QA — 8 November 2026

Scope: `u4-calotes`, page 2, `digestive-system`, registered ID `u4-calotes-digestive-system`.

## Disposition
- Corrected the lesson's English and Tamil text to distinguish cardiac/pyloric stomach, duodenum, ileum, blind caecum, rectum, cloaca, liver, gall bladder, pancreas and bile duct.
- Existing `pencil_plates/calotes_digestive_en.png` is **unchanged**, original registered SHA-256 `4cf2bbbcbd3a7375b4649f3cebafc95a156d675a881e6765534521dadf5806fc`.
- The image remains **PROVISIONAL**. This commit changes no figure manifest, artwork hash, reviewer approval or credits.
- Candidate A, local original AI PNG (1024×1536): SHA-256 `c2718672545f26ae45dd96d966e3133fb9713cf55797e01fe617642ba9e0ff68`. Anatomical QA **NOT ACCEPTED** for direct integration: oral opening appears anthropomorphic and region proportions have not been verified.
- Candidate B, newly redrawn original AI PNG (1024×1536): SHA-256 `704affefb37e785174dfa23e59af3017b35b0cdfc0ebf77638e552405d8d166a`. Better reptile external head and clearer labels, but **REQUIRES REVISION / REVIEW**: proportions, gastric/duodenal continuity, pancreas placement, ileo-caecal junction and every leader line are not independently verified. Neither candidate was uploaded to this repository or embedded in the APK.
- ImageGen is the creator of the two candidates; **no reference illustration is copied or used as the image credit**.

## Text/reference checks
1. Veerashaiva College, G. Mallanagoud and Vedavyasa Sagar, *Chordate Zoology* (2018), comparative digestive anatomy of *Calotes*: https://veerashaivacollege.org/images/II_sem_Chordate_Zoology_text_Book_CBCS.pdf . **All rights reserved**; teaching reference only; neither book diagrams nor text copied.
2. M.N.D. College, `Study of Calotes versicolor`, digestive-system teaching handout: https://www.mndcollegerajur.org/uploads/download/TYBSC_DIGESTIVE_SYSTEM_CALOTES_1_pptx.pdf . Text reference only; reuse licence not established.
3. S. Y. Paranjape (1974), *The Anatomy of the Garden Lizard (Calotes versicolor)*, University of Poona, digestive anatomy section: https://books.google.com/books?id=t4o_AAAAYAAJ . Bibliographic lead only; exact illustrations were not accessed or cleared for reuse.

## Mandatory next image acceptance
- Check species-specific relative geometry, whether pyloric stomach/duodenum really form the depicted loop, ducts and pancreas position, bilobed liver and blind caecum near ileum-to-large-intestine transition. Confirm that leader lines point to the correct tissues.
- English figure labels are permitted in both language modes. Tamil explanatory text needs separate Tamil academic review.
- Obtain explicit independent Biology and Tamil decisions, phone-scale legibility and pinch-to-zoom. New art must have exact image size/hash and creator rights in the manifest and review register; rerun source checks and Android emulation before any QA APK promotion.
- Production: **HOLD**. No reviewer decision or image approval was inferred from automated QA.

## Build scope
This text-only content change should be validated by the existing `android-qa.yml` workflow. The preceding QA APK built from `938487b7e48a1033d139615736175b0d248e30ec` and does **not** contain this lesson-text revision.
