# CHORDATA — Unit V targeted anatomical editorial QA · 20 November 2026

**Parent checkpoint:** `d971c80d41063f411278029ea88570a5c3ff470e`  
**Scope:** Evidence-backed bilingual refinements only; no deletions, chapter order changes, altered PNGs, figure licences, MCQs or owner approvals.

## Textbook corrections

1. **Pigeon (Columba) urinogenital system; registered Figure 47.** The existing chapter omitted an explicit ordered account of infundibulum → magnum → isthmus → shell gland (avian uterus) → vagina, and did not distinguish ureters entering the cloaca from the female oviduct in the figure-associated lesson. The English and Tamil explanations now state these anatomical relationships and the absence of a pigeon urinary bladder.
2. **Avian flight respiration; registered Figure 51.** The prior summary described chiefly one-way parabronchial airflow without distinguishing the palaeopulmo from the neopulmo. The bilingual explanation now states that palaeopulmonic airflow is predominantly caudal-to-cranial in both breathing phases, whereas neopulmonic flow can be bidirectional where that region occurs. Do not interpret a one-way schematic arrow as a claim about every parabronchus.

## Published references consulted

- Ohio State University, *Avian female reproductive tract*: https://ohiostate.pressbooks.pub/vethisto/chapter/13-avian-female-reproductive-tract/
- University of Wisconsin–Milwaukee, *Birds — Animal Care Training*: https://uwm.edu/safety-assurances/programs/research-compliance/animal-care-program/training-education/training-manual/birds/
- *Structure and function of the avian respiratory system* (2025): https://pmc.ncbi.nlm.nih.gov/articles/PMC11864839/
- *Avian air sacs and neopulmo: their evolution, form and function* (2025): https://pmc.ncbi.nlm.nih.gov/articles/PMC11864834/

## Figure status

- **#47, pigeon urinogenital:** Register remains PROVISIONAL, scientific reviewer PENDING, Tamil reviewer PENDING.
- **#51, avian respiration:** Register remains PROVISIONAL, scientific reviewer PENDING, Tamil reviewer PENDING.
- **#57–64, Mammalia figures:** Existing source/licence/hash entries remain unchanged. No additional independent acceptance is implied.
- This batch inspected textual teaching keys and register metadata; it **does not claim new pixel-by-pixel artwork inspection or device-level visual acceptance**. No artwork or licence metadata was modified, so source-image hashes remain unchanged.

## Native reader figure-key legibility

The figure-card code previously collapsed the detailed label keys for Figures **47** and **51** by default. Both are provisional anatomy/physiology images where caveats must be visible without a separate tap. The native reader now displays those full keys at its standard expanded text size in both languages; the image PNGs, zoom functionality, original identifiers, figure placement and independent sign-off status are unchanged. The Android QA-contract script explicitly guards this behaviour. Device-level legibility at 100% and 200% font scale remains subject to the new-commit instrumentation results.

## Figure 47/51 student-visible source keys — follow-up

The Figure 51 key previously implied that all avian lung airflow was unidirectional. The English key now limits predominantly one-way flow to the **palaeopulmonic** parabronchi and explicitly notes bidirectional **neopulmonic** flow where present. Both Tamil variants distinguish these pathways; the selected Tamil AI diagram is described as a *schematic localisation only*, not an exact nine-sac or bronchial airflow map. Figure 47's Tamil key now consistently spells **மேக்னம்** (magnum).

No image, licence, authorship, figure SHA-256, approval field or chapter order was changed. The new QA assertions preserve these scientific cautions and provisional statuses.

References: https://pmc.ncbi.nlm.nih.gov/articles/PMC11864839/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11864834/

## Validation gate

The existing `scripts/audit_textbook_chapters.py` now checks the paired English–Tamil anatomical terms, on every mandated QA workflow execution. Existing 39-topic coverage, bilingual sections, figure source/hash checks, Kotlin compilation and Android instrumentation must pass on **this new commit** before a QA APK can be considered current. Independent scientific and Tamil sign-off remain external release blockers.
