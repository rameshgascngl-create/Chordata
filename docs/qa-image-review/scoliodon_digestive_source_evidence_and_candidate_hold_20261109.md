# CHORDATA — *Scoliodon* digestive-system artwork: exact-source review and candidate HOLD

**Date:** 9 November 2026  
**Branch:** `qa/chordata-scoliodon-digestive-review-20261109`  
**Verified source baseline:** `81034f4969d7e8915dc16a5ac29f8f8f499aa0fb` (four-snake-photograph QA build, all four CI jobs green).  
**Disposition:** **RESEARCH / REVIEW ONLY. No new image integrated or app-visible image changed.**

## Registered lesson and existing protected artwork

- Figure ID: `u2-scoliodon-digestive-labelled`
- Topic: `u2-scoliodon` · Unit II · page **2** · section `digestive-system`
- Installed canonical PNG: `app/src/main/assets/pencil_plates/scoliodon_digestive_en.png`
- Last verified PNG SHA-256: `57f1bd87ee5ea529eff8bec7ca5ac4a60c2dca1be6afb62daf52ba024741cf17`
- Installed size: 581,960 bytes; retained original schematic master: `docs/original_plate_svg/scoliodon_digestive_anatomy_en.svg`
- Existing status: `PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING`
- Existing drawing must **not** be called academically approved; it remains a provisional source-backed teaching schematic. Retain its exact bytes and attribution pending a better asset.

## Original AI image generation candidate — rejected pending correction

The conversation review package `CHORDATA_Scoliodon_Anatomy_Candidate_HOLD.zip` contains an original *OpenAI ChatGPT ImageGen* **PNG candidate**, a phone-sized preview, a JSON integrity record and a reviewer readme. **The ZIP and its PNG are not committed to this GitHub branch and not inside an APK.**

| Property | Verified value |
|---|---|
| Candidate PNG | `Scoliodon_AI_Reconstruction_HOLD.png` |
| SHA-256 | `de1ff7e35de060dc0733efa61ec23f0b905a948b7e3b7e6e7944ea4a533eb010` |
| Actual dimensions | 1199 × 1312 px |
| Actual file size | 2,265,660 bytes |
| Source credit | Original AI illustration generated in ChatGPT on 9 November 2026 |
| Decision | **HOLD — NOT STAGED, NOT GREEN-TICKED, NOT INSTALLED** |

### Scientific and technical blockers

1. **Scroll-valve geometry:** The inset is rendered like a helical staircase. A *Scoliodon* teaching reconstruction must instead accurately show the rolled longitudinal mucosal fold (scroll valve), with a watch-spring-like cross-section. The cited teaching account describes approximately 2½ turns. An open dissection and a transverse inset must be clearly distinguished, and the overall architecture should not be inferred from a generic helical shark intestine.
2. **Repeated callout number:** The image uses **11** both on the main intestine and the inset without a distinct subfigure convention. Renumber uniquely or introduce formally paired A/B references with explicit keys. No leader line may terminate between organs.
3. **Minimum PNG width:** The candidate width is **1199 pixels**, one pixel below the current Android source-integrity requirement of at least 1200 px. Pure resampling would solve this *technical* gate, but would not validate anatomy or restore visual detail.
4. **Biliary and pancreatic outlets:** The bile duct belongs to the *proximal intestinal region*, near the beginning of the scroll valve, not the lumen of the pyloric stomach or pyloric sphincter. The pancreas drains through a distinct duct into the intestine. Require expert confirmation of both positions and the leader-line contacts.
5. **Taxon and scope:** A plausible generic shark is not automatically a scientifically verified dissection of `Scoliodon`. Include an explicit comparative/schematic scope note and do not turn a model reconstruction into a named specimen claim.

### Non-negotiable anatomy acceptance topology

`buccal cavity/pharynx → oesophagus → long cardiac stomach → short pyloric stomach → pyloric valve → bursa entiana → broad, straight scroll-valve intestine → narrow rectum → cloaca`.

- The **blind sac** lies at the junction of the cardiac and pyloric stomach limbs.
- The **liver** is large and bilobed; its gallbladder is associated with the right lobe; bile and pancreatic ducts empty into the anterior intestine (not the pyloric valve).
- The **rectal gland** is a tubular appendage opening into the rectum; it has a known salt-excretion function in elasmobranchs and must not be misrepresented as a digestive-enzyme gland.
- The **scroll valve** is a rolled intestinal mucosal fold; it is not a stack of disconnected saucer-shaped diaphragms.
- Separate **ventral whole-animal dissection**, **opened gut**, and **transverse scroll-valve** views; never combine different views without labelling.

**Tamil editorial key (conceptual, subject to independent Tamil proofing):** `இரைப்பையின் கார்டியாக் பகுதி`; `பைலோரிக் பகுதி`; `கண்முட்டு நீட்சி (blind sac)`; `பைலோரிக் வால்வு`; `பர்ஸா என்டியானா`; `குடலின் சுருள் மடிப்பு`; `பித்தநாளம்`; `கணைய நாளம்`; `மலக்குடல் சுரப்பி`; `பொது வெளியேற்ற அறை (குளோயாக்கா)`. English anatomical terms may be retained in image callouts; Tamil lesson narration remains separate.

## Scientific references — verification only, not redistribution licences

1. NTR Government Degree College, `Digestive System of Scoliodon`: <https://www.ntrgdc.ac.in/userfiles/file/Course%20Materials/Semester-2-Digestive%20system%20in%20Scoliodon.pdf> — J-shaped stomach; blind sac; bursa entiana; bile/pancreatic duct entries and scroll valve.
2. IGNOU, `Digestive System`: <https://egyankosh.ac.in/bitstream/123456789/16525/1/Unit-6.pdf> — longitudinally rolled scroll valve, lumen and rectal duct topology.
3. Comparative shark spiral-intestine research: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8292776/> — shark spiral valves vary by lineage; an illustration of another species does not prove the *Scoliodon* condition.
4. Jon Houseman, `Squa152p.png`, <https://commons.wikimedia.org/wiki/File:Squa152p.png>, CC BY-SA 3.0 — researched as legally reusable but **rejected as a direct replacement**: the artwork concerns `Squalus acanthias`, has only **450 × 337 source pixels**, and cannot faithfully establish the named *Scoliodon* anatomy.
5. Historical 1907 frilled-shark digestive plate <https://commons.wikimedia.org/wiki/File:PZSL1907Page472.png> — similarly **not an exact species match**; research reference only.

Source images from institutional PDFs have **not** been copied, traced, downloaded into an app asset, credited as newly generated work or treated as permission to redistribute.

## Acceptance gate for a replacement

A revised candidate requires (a) documented scientific visual review of every numbered leader line and the entire digestive continuity; (b) explicit author, originality, exact byte length, image SHA-256, image dimensions and reuse rights; (c) a provisional `GREEN_TICK_ALLOW_PROVISIONAL_QA_USE` decision on that **specific PNG**, without fabricating independent Zoology or Tamil approval; (d) replacement of only the registered Unit II figure and paired review/inventory records; and (e) passing `scripts/qa_all.sh`, native Kotlin build, emulator instrumentation, phone-scale zoom and real-device checks. Production remains **HOLD** until independent subject/Tamil reviewers and physical-device acceptance are recorded.

**No source image, figure registry, Kotlin source, course pack, approved illustration, main branch or production APK is modified by this evidence-only checkpoint.**
