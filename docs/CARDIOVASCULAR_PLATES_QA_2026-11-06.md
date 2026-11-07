# CHORDATA — cardiovascular figures: topology correction checkpoint

**Scope:** Independent source-level corrections for two of 64 registered lesson diagram slots in the five-unit, native Android course. **Date:** 6 November 2026.

## Original deficiencies and implemented corrections

| Exact registered diagram ID | Deficiency in older provisional plate | New provisional plate (English labels) |
|---|---|---|
| `u3-rana-arterial-system` | Three arterial categories represented by single arrows from a common pipe; no bilateral arteries or systemic arch union | Two arterial trunk branches from the truncus, paired carotid / systemic / pulmocutaneous paths; split cutaneous and pulmonary branches, bilateral systemic arches joining into dorsal aorta; schematic three-chambered heart |
| `u4-calotes-arterial-system` | Outflow arrows drawn from one undifferentiated ventricular region; key squamate cavities unlabelled | One continuous ventricular outline with labelled communicating cavum arteriosum, cavum venosum, cavum pulmonale; incompletely separating septal structures, paired aortae, pulmonary artery, and a route schematic for atrial inflow |

Both are **topological teaching schematics only**, not life-size anatomical views or dissection substitutes. Vessel branch routing, functional cardiac compartments and proportions require independent discipline review before publication.

### Primary references for anatomical topology (not copied artwork)

- The Anatomy of the Frog (historical text, arterial anatomy), https://readingroo.ms/7/7/5/6/77560/77560-h/77560-h.htm
- Tamil Nadu Open University, M.Sc. Zoology course notes, frog arterial branches, https://tnou.ac.in/NAAC/SSR/C1/1.1.5/MZON-P1.pdf
- Jensen et al. (2013), *Development of the Hearts of Lizards and Snakes and Perspectives to Cardiac Evolution*, https://pmc.ncbi.nlm.nih.gov/articles/PMC3673951/
- Australian Government, *Fauna of Australia: Squamata — Morphology*, https://www.dcceew.gov.au/sites/default/files/env/pages/dc11235d-8b3b-43f7-b991-8429f477a1d4/files/24-fauna-2a-squamata-morphology.pdf

### Reproducibility and provenance

The artwork is original SVG authored for this QA project and rasterised into full-resolution PNG. Run `python3 scripts/rebuild_cardiovascular_plates.py` to reproduce only these two diagrams and refresh their SHA-256 manifest entries, then run `python3 scripts/write_figure_review_register.py` and `bash scripts/qa_all.sh`. All previous binary assets are preserved except these two replacement PNGs. The updated SVG masters are retained in `docs/original_plate_svg`.

**Warning:** `scripts/build_remaining_plates.py` is the earlier baseline generator for the entire remaining-plate series. If used for re-generation, rerun the subsequent refinements in order: `python3 scripts/rebuild_comparative_brains.py`; `python3 scripts/rebuild_cardiovascular_plates.py`; `python3 scripts/write_figure_review_register.py`; `bash scripts/qa_all.sh`.

### Validation and release limits

- 64/64 registered figure slots and 68 manifest variants: **source QA PASS**.
- 74 PNGs (67 pencil + seven credited/legacy): **source SHA-256 PASS**.
- Source integrity, native Android metadata and 24 Kotlin smoke assertions: **PASS**.
- Reviewer register re-generated while preserving prior human decisions, and change hashes ensure prior approvals cannot be reused: **PASS**.
- Independent scientific approval: **PENDING for all 64 plates**.
- Android compilation, emulator and physical-device testing: **NOT EXECUTED for this new source**.
- `native/qa-chordata-illustration-coverage` at remote commit `5371d7ec...` remains an earlier branch version; no GitHub synchronisation or new Android APK is claimed.

**Production release remains on HOLD.**
