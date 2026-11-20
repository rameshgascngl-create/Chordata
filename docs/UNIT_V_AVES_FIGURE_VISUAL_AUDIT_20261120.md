# CHORDATA — Unit V Aves illustration visual and rights audit

**Date:** 20 November 2026  
**Comparison baseline:** `951e5a09fbeafa619ef1a53947c7a93431c1f18d`, QA workflow `44700016436`  
**Review material:** original nine PNGs extracted from `Chordata_QA_Source_Figures`, GitHub Actions artifact `14611588850`; cross-checked against register `docs/FIGURE_REVIEW_REGISTER_64.csv`.  
**Scope:** visual preliminary scientific assessment and cryptographic file identity, not a final independent Zoology/Tamil approval, a licence opinion or real-device accessibility certification.

## Verified file identity

All nine original Aves PNG files were opened and viewed. Their independently calculated SHA-256 values match the nine registered hashes. They remain at their existing core-lesson slots (IDs **44–52**); none were modified, cropped, relabelled or moved in this review. The baseline instrumented QA remains **42/42 PASS only for commit `951e5a09`**; newer source commits require fresh testing.

## Figure-by-figure findings

| Register ID | PNG | Observed visual/scientific findings | Next evidence or correction | Independent sign-off |
|---|---|---|---|---|
| 44 | `living_bird_phylogeny_en.png` | Clean, legible **two-way schematic** of Palaeognathae versus Neognathae; explicitly notes flying tinamous. It is **not** a complete modern classification tree and does not display Galloanserae, Neoaves or 2024 Neoaves subclades. | Keep as the first-division overview; clearly identify it as simplified. The new genomic-relationships textbook prose needs a separate sourced phylogenetic tree if illustrating detailed nodes. Original project-illustration redistribution rights must be confirmed. | **PENDING** |
| 45 | `pigeon_external_anatomy_en.png` | Historical, recognisable rock-pigeon painting with head, beak, wings and tail; **no anatomical pointer labels** are present. | Acceptable as a supplementary specimen portrait, **not** a standalone labelled morphology plate. Verify attribution to the named historical original and avoid claiming labelled anatomy. | **PENDING** |
| 46 | `columba_skeleton_en.png` | Historical whole-skeleton drawing; overall pigeon-type skeletal organisation visible, but individual bone labels are **not legible/present in the displayed source plate**. | Companion teaching key needed for keel, furcula, synsacrum, pygostyle and forelimb bone identification. Preserve the historical original; verify the represented taxon against the cited Meyer plate. | **PENDING** |
| 47 | `pigeon_urinogenital_en.png` | Two readable AI-assisted male/female plates depict paired testes and kidneys, ureters, cloaca, and a single ovary/oviduct on the female. The female oviduct is highly stylised and its form/position cannot be accepted as verified *Columba* dissection solely from this image. | **HIGH**: review the location, proportions and routes of the ovary, oviduct subdivisions, kidneys, ureters and vas deferens against verified pigeon anatomical figures; confirm no false bladder or mammalian uterine implication. AI provenance is recorded, but does not establish scientific acceptance. | **PENDING** |
| 48 | `pigeon_eye_ear_en.png` | Two historical eye and ear engravings with an explanatory abbreviation key. The source plate explicitly identifies itself as **comparative bird anatomy, not a verified pigeon specimen**. | Preserve this necessary qualification in the reader, check fine-print legibility at 200% and verify columella/middle-ear interpretation against the original 1905 engravings. | **PENDING** |
| 49 | `avian_aerofoil_en.png` | **Confirmed inaccurate label:** `Lift (net aerodynamic force)`. Lift is the aerodynamic-force component perpendicular to the relative airflow; net aerodynamic force combines lift and drag. Source note correctly rejects the equal-transit-time myth. | **CORRECTION REQUIRED** before academic acceptance: replace the label with `Lift (perpendicular to relative airflow)`; if a total force is illustrated, give it a separate resultant vector. Show drag separately or state explicitly that it is omitted. Re-export PNG and reconcile source SVG, hash, figure-register provenance and all variants in a dedicated figure-change batch. | **NOT APPROVED — corrective action identified** |
| 50 | `avian_flight_muscles_en.png` | Legible vector schematic distinguishes pectoralis and supracoracoideus with coracoid, scapula, furcula and sternum. The **triosseal-canal tendon route is not explicitly named** and the pectoral girdle is very schematically simplified. | Compare the supracoracoideus tendon-pulley route and wing skeleton labels with source `Wing_Muscles,_color.svg`; add an explanatory key if preserving the source original. Verify CC BY-SA 2.5 derivative obligations. | **PENDING** |
| 51 | `avian_respiration_en.png` | Two-stage inhalation/exhalation source-based diagram shows trachea, bronchus, parabronchi, anterior and posterior air sacs, and directional arrows. Some small arrows are ambiguous without the original figure legend and a detailed air-parcel explanation. | **HIGH**: independently check airflow arrows during both phases against the credited source, the distinction between lung gas exchange and sac ventilation, and which arrows denote sac expansion rather than air movement. A source-derived image is not automatically anatomical sign-off. | **PENDING** |
| 52 | `bird_migration_stopovers_en.png` | Clear conceptual breeding–stopover–non-breeding **network**, explicitly disclaims a species-specific route. | Suitable as a conceptual map if labelled illustrative, not as evidence for particular countries or an actual tracked species. Project-original illustration rights/licence need verification. | **PENDING** |

## Rights and academic acceptance

- Source creator, provenance URL, registered PNG path and hash are recorded for all nine. Historical public-domain claims (IDs 45, 46 and 48), source attribution/share-alike rights (IDs 50 and 51), project-created artwork permissions (IDs 44, 49 and 52) and AI distribution status (ID 47) each still require review against the actual distributed derivative and its intended app-store licence.
- The review file **does not** change `docs/FIGURE_REVIEW_REGISTER_64.csv` approval fields. No external Zoology or Tamil reviewers have signed these nine illustrations in this batch; do not set `ACCEPTED`.
- Existing images, registered lesson references, file names and 64-slot manifest have been preserved deliberately. Figure 49 is a verified scientific correction requirement, not a reason to discard all other illustrations.
- The expanded classification chapter cites Stiller et al. (2024), *Nature* 629:851–860, DOI `10.1038/s41586-024-07323-1`. The existing two-way tree remains valid as a **simplification only**, not the complete 2024 topology.
- Next dedicated correction work should update figure 49 and all linked binary hashes atomically and then rerun image, source-integrity, Android instrumentation and release preflight checks. Do not approve the corrected plate without visually examining the replacement.


## 20 November 2026 — figure 49 technical correction

The active source SVG and rendered PNG were changed together to label
`Lift (perpendicular to airflow)`, with the subtitle explicitly indicating
that drag is omitted. The previous inaccurate phrase
`Lift (net aerodynamic force)` has been removed from the new artwork.
The resulting SVG and PNG SHA-256 checksums are recorded in the figure
manifest and in the newly regenerated 64-figure register.

The old owner's SHA-bound provisional display decision was **not carried
to the revised PNG**. The figure remains provisional and still requires
independent Zoology/Tamil sign-off, owner authorisation for changed artwork,
rights clarification, and device-level legibility checking.
