# CHORDATA — Illustration integration QA checkpoint (6 November 2026)

## Source and scope
- Recovered source baseline: `Chordata_Monotreme_QA_Source.zip` (valid archive).
- A subsequent English-labelled archive was found truncated after 48 recoverable local ZIP entries; verified complete entries were recovered by checking raw deflate length and ZIP CRC32. The incomplete shark-sensory PNG was **not** copied.
- Work is based on `native/qa-chordata-illustration-coverage`; **the contents of this ZIP are local and are NOT claimed to have been pushed to GitHub**. Last remotely verified branch head prior to this checkpoint: `5371d7ecfc8a03955ba86100578dad6538c5fd26`.
- The 64 registered diagram IDs, their lesson pages and Tamil/English course content are unchanged.

## Coverage definitions (no inflated completion claims)
| Evidence category | Count | Meaning |
| --- | ---: | --- |
| Registered lesson figure slots | 64 | Every slot mapped to exactly one real lesson section |
| Slots with **provisional pencil-plate registration** | 32 | Includes 36 language variants and 35 unique pencil PNG files |
| Other slots with visible legacy PNGs | 3 | The remaining three of seven legacy PNG mappings (the other four overlap pencil plates) |
| **Distinct slots with displayable QA artwork** | **35/64** | Previous recovered English-label checkpoint: 28/64; **seven new slot placements** |
| **Remaining without displayed artwork** | **29/64** | Still need appropriate anatomical images |
| Academically accepted scientific plates | **0/64** | Independent Zoology sign-off pending |
| Independently verified Tamil scientific prose | Pending | English-only artwork labels are permitted; Tamil lesson narrative remains separate |
| Android compile / emulator tests of this source | Not run | No accessible SDK / Gradle host in this local environment |
| Physical-device acceptance / production release | HOLD | No production merge or release |

## Figures newly placed on exact lesson pages
All following figures are **original computer-assisted, English-labelled schematic PNGs**; references are for anatomical verification only, not copied source artwork.

| Diagram ID | Illustration | Primary anatomical check |
| --- | --- | --- |
| `u3-rana-external` | `rana_external_en.png` | nares, eye, tympanum, skin, hind foot webbing |
| `u3-rana-respiration` | `rana_respiration_en.png` | skin, buccopharyngeal lining and paired lungs distinguished |
| `u4-calotes-external` | `calotes_external_en.png` | dorsal crest, keratinised scales, limbs, claws and tail |
| `u5-rabbit-brain` | `rabbit_brain_en.png` | cerebral hemispheres, cerebellum, olfactory region, medulla |
| `u5-flying-mammals-bat-wing-glider-comparison` | `bat_glider_comparison_en.png` | prolonged bat fingers versus gliding membrane |
| `u2-dipnoi-lungfish-comparison` | `dipnoi_lungfin_comparison_en.png` | lobed fin, paired versus single-lung condition |
| `u2-scoliodon-digestive-labelled` | `scoliodon_digestive_en.png` | connected oesophagus, stomach, spiral intestine and cloaca |

Additionally, `u2-scoliodon-sense-organs-labelled` now has a **replacement** `shark_sensory_systems_en.png` with intact CRC/SHA-256 verification. The attempted previous image in the damaged ZIP was incomplete. It is not counted as a newly added slot. The amphibian orders and axolotl neoteny plates from the recoverable archive are also retained.

## English diagram labels in Tamil lessons
The native `FigureGallery.kt` now resolves `en` then `shared` for **both** English and Tamil modes, as requested. Separate Tamil lesson body, section headings, descriptions and captions remain untouched. The obsolete rule hiding English-labelled credited diagrams in Tamil mode was removed. All new source records remain provisional and include creator, technical rendering method, SHA-256, source-independent scientific reference URLs and pending expert review.

## References used to check relationships, not for reusing their graphics
- Shark sensory structures: https://dlnr.hawaii.gov/sharks/about-sharks/senses/ ; https://australian.museum/publications/sharks/bodies-senses/
- Frog respiration: https://jnanabhumi.ap.gov.in/Uploads/Materials/Zoology-I.pdf ; https://www.egyankosh.ac.in/bitstream/123456789/104742/1/Block-1.pdf
- Lungfish anatomy: https://www.lkouniv.ac.in/site/writereaddata/siteContent/202004021912558038manoj_kumar_zool_Dipnoi_General_organization.pdf
- Other direct references are registered against exact `diagramId` values in `pencil_plates/manifest.json`.

## Local verification
- `scripts/audit_content.py` — PASS: 39 topics, 127 lesson sections, 117 quizzes, 64 figure slots.
- `scripts/audit_figure_placement.py` — PASS: registered slot, PNG hash and attribution checks.
- `scripts/audit_pencil_coverage.py` — PASS: 32/64 pencil placements, manifest/PNG verification, English mode policy.
- `scripts/run_core_tests.sh` — PASS: 24 Kotlin core assertions.
- `scripts/qa_all.sh` — PASS: all the preceding checks and Android manifest/XML parsing.
- No instrumentation/emulator or APK assembly was performed on this checkpoint. Previous green GitHub CI at commit `5371d7e` is **not** a test of these new source changes.

## Critical editorial cautions
These images are educational schematics, not high-fidelity dissections. In particular, review the shark digestive organ geometry and bile drainage, frog respiratory surfaces, Calotes digit/crest proportions, and comparative bat wing skeletal rays before promoting any illustration to academic approval. Historical/source-credited plates require attribution and licence review separately. The remaining 29 placements, scientific acceptance, Android CI and physical-device screenshots are independent release gates.
