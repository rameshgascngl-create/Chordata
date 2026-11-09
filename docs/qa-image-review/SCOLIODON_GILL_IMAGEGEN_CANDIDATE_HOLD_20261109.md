# Scoliodon gills — high-detail anatomical image candidate (HOLD)
Date: 2026-11-09. Scope: isolated image review only, **no Android asset replacement**.

## Exact destination and untouched installed artwork
- Registered ID: `u2-scoliodon-gills-labelled`
- Unit II, `u2-scoliodon`, page 3, section `respiratory-system`.
- Installed asset (unchanged): `pencil_plates/shark_gill_flow.png`.
- Installed PNG SHA-256: `675f497ab223df417274b8641bfc09b5a40729a4c74e419208bb08794353a90c`.
- Current author remains: CHORDATA QA project — original vector shark septal-gill teaching schematic.
- **No accepted artwork modified, no replacement PNG installed, no content/manifest/review-register changes, no academic sign-off**.

## New image, honestly described
An original AI-assisted high-detail comparative elasmobranch anatomy illustration was generated with OpenAI ChatGPT ImageGen on 9 November 2026. Its head view shows five gill slits without a visible external spiracle; separate magnifications depict a conceptual vascular filament and a cutaway of septal-gill surfaces.

- Raw unlabeled ImageGen PNG: 1536×1024 RGB, SHA-256 `065dbae22e44104322d96e11b668753b0bb8f0aac10050cb2942082834f24ea8`.
- Banded and openly labelled candidate PNG: 1536×1410 RGB, SHA-256 `8bdc73552afb268cbef0edfd2c50de818bb2e6da6d063112fa14337ab15b4a27`, 2,771,641 bytes.
- Image modification: an external header/footer text canvas only. The three source illustration panels remain pixel-identical, with no overlays covering anatomy.
- **Local conversation deliverable:** `CHORDATA_Scoliodon_Gills_Candidate_HOLD.zip`, containing the full-resolution labelled candidate, raw original and review notes. The ZIP/PNGs are **not present in this repository**; filenames here are not evidence of installation.
- Rights: new AI-generated composition; references listed below were consulted for anatomy, not copied or claimed as creators of the illustration. This is not a published or photographed specimen.

## Anatomy acceptance issues
1. **Check actual branchial organization:** five external slits in a requiem/milk-shark type; the posterior hyoid hemibranch plus four branchial holobranchs should be unambiguously distinguishable in any teaching reconstruction. This AI panel does NOT independently establish those counts, so the figure remains a conceptual candidate.
2. The cutaway does not clearly establish the pharynx-to-gill-slit pathway, or branchial arch/gill ray identities with reliable leader lines.
3. The filament view is not a real histological micrograph. Exact arrangement of primary filaments, secondary lamellae, afferent/efferent vasculature and opposite blood/water flow requires expert comparison.
4. No external spiracle is shown. A *Squalus* specimen with an obvious spiracle is not a species-specific replacement for historical `Scoliodon sorrakowah` (milk shark, treated as *Rhizoprionodon acutus*).
5. If approved for provisional QA use, add *precisely verified* English callouts, separate Tamil textbook-style explanatory key, full PNG SHA/provenance, and update `docs/FIGURE_REVIEW_REGISTER_64.csv`; then pass 64-slot static checks, Kotlin compilation, emulator 100/200%, zoom/landscape, and physical-device inspection.

## Anatomical references — not reproduction rights
- Evans et al. 2005, *The Multifunctional Fish Gill*, *Physiol. Rev.*: https://journals.physiology.org/doi/10.1152/physrev.00050.2003
- Hawaiʻi DLNR, shark gills and respiration: https://dlnr.hawaii.gov/sharks/anatomy/gills-respiration/
- Uttarakhand Open University, Zoology `BSCZO-201`, Scoliodon septal gill anatomy: https://uou.ac.in/sites/default/files/slm/BSCZO-201.pdf
- Fisheries and Oceans Canada shark anatomy: https://www.dfo-mpo.gc.ca/species-especes/sharks/anatomy-eng.html?wbdisable=true

## Disposition
**HOLD**: improved visual fidelity but insufficient independently verified branchial topology for automatic integration. An earlier green CI run at `8d6c2512be33efae0aa62bf664a934f0b9c390c8` remains the latest verified executable baseline; do not imply a new APK was produced for this candidate-only note. No production merge.
