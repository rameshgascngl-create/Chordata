# CHORDATA — pointwise learning enrichment: academic QA intake
**Date:** 11 November 2026

## Scope and actual changes
- Original `app/src/main/assets/chordata_content.json` is byte-for-byte unchanged. The immutable course-pack checksum in `scripts/audit_content.py` is not bypassed.
- Added `app/src/main/assets/chordata_learning_points.json`: 39 topic-specific supplements, each attached to one existing registered section and containing **three new bilingual teaching points** (117 English + 117 Tamil explanations).
- Integrated the supplementary points in the **native Kotlin/Compose reader** immediately after the original explanatory paragraph and before that exact section's image, in both continuous reading and page-by-page modes.
- Preserved 5 units, 39 topics, 127 original sections, 117 quizzes, 64 image slots and the 68 manifest variants.
- Added strict load-time JSON validation, static anchor auditing and Android instrumentation coverage.
- Every student-facing point is about Chordate biology, learning method, safety, comparative anatomy or conservation. No internal build/reviewer statuses are displayed.

## Academic scope and editorial status
These are **new original teaching explanations, not copied source text**. The material is candidate classroom content rather than independently peer-reviewed or independently Tamil-edited. Do not mark `ACCEPTED`, change scientific image review records or publish a store release based solely on this extension.

- Unit I: comparative embryology, chordate diagnostic features, Balanoglossus, ascidian metamorphosis, Amphioxus feeding, vertebrate characters, classification and lamprey larvae.
- Unit II: fish classes, Scoliodon digestion, Dipnoi, scales, accessory respiration, parental care, migration and sustainable fisheries.
- Unit III: amphibian orders, Devonian transition, Rana respiration, caecilian adaptations, neoteny and parental care.
- Unit IV: amniotic egg, Calotes arterial anatomy, extinct reptile lineages, medically important Indian snakes, evidence-based snakebite first aid and temporal skull openings.
- Unit V: bird characters, pigeon urinogenital systems, avian ventilation, bird migration, mammals, rabbit kidney, monotremes, marsupials, bat echolocation, aquatic mammals and dental formulae.

## Reference leads (not image credits)
- OpenStax Biology 2e, Chordates: https://openstax.org/books/biology-2e/pages/29-1-chordates
- OpenStax Biology 2e, Fishes: https://openstax.org/books/biology-2e/pages/29-2-fishes
- OpenStax Biology 2e, Amphibians: https://openstax.org/books/biology-2e/pages/29-3-amphibians
- OpenStax Biology 2e, Reptiles: https://openstax.org/books/biology-2e/pages/29-4-reptiles
- OpenStax Biology 2e, Birds: https://openstax.org/books/biology-2e/pages/29-5-birds
- OpenStax Biology 2e, Mammals: https://openstax.org/books/biology-2e/pages/29-6-mammals
- WHO snakebite envenoming first aid: https://www.who.int/teams/control-of-neglected-tropical-diseases/snakebite-envenoming/treatment

**Reviewer follow-up:** subject specialist and Tamil science editor should check taxon-specific and medically important points; review after any content amendment. The figure and production gates remain unchanged.
