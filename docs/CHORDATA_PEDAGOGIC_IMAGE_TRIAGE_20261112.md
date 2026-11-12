# CHORDATA — pedagogical image triage (12 November 2026)

**Trigger:** Direct classroom/handset review of the Android app with six screenshots.
**Decision:** Six diagram variants are unsuitable for teaching. Their artwork remains
in source control with original metadata, but the native reader must not present
them in either language as if they were scientifically acceptable.

## Revised educational acceptance criterion

Image files passing PNG integrity, dimensions, correct lesson assignment,
hash and attribution are **only technically valid**. They are not necessarily
**biologically useful**.

Review each candidate in this order:

1. **Observable/recognisable biology:** real organism, body region or clearly
   defined process must be recognisable from the image itself.
2. **Anatomical relationships:** organ topology, physiological direction,
   life-cycle transitions and homology must be reliable.
3. **Exact lesson relevance:** no generic shape substituted for a species
   or a developmental state simply because the artwork fits the layout.
4. **Readable teaching information:** labels, arrows, scale disclaimer, view
   and caption must help a student independently interpret the figure.
5. **Sourcing and reuse rights:** retain actual creator, source page, exact
   reuse licence and modifications. Source-referenced original and AI figures
   must never be falsely credited as source image reproductions.

**A tolerable cosmetic flaw is NOT an automatic rejection.** Minor line
irregularity, small text-spacing problems, modest stylisation or low-risk
aesthetic imperfections may be accepted provisionally when the depicted
biology is correct, clearly recognisable and labelled. Conversely, a clean,
decorative image can be rejected if it fails educational utility. An
AI-generated image is evaluated by the same scientific standard as
a photo, raster rendering or hand-drawn plate.

A minor fault is never permission to show reversed organ connections,
wrong species, impossible structure, fictitious organs, or unsafe
snake-identification claims.

## Six confirmed unsatisfactory illustrations

| Registered diagram ID | Screenshot finding | Correct replacement requirement |
|---|---|---|
| `u4-snakes-india-big-four-identification` | Curves and loops are not identifiable snakes | Four genuine species photographs: *Naja naja*, *Bungarus caeruleus*, *Daboia russelii*, *Echis carinatus*, identified by scientific names and credited individually; not a self-identification field key |
| `u5-flight-adaptations-flight-muscles` | No useful avian muscle/skeletal anatomy | Actual labelled pectoralis, supracoracoideus, coracoid, sternum/keel, humerus and tendon-pulley pathway |
| `u5-rabbit-sense-organs` | Icons rather than rabbit morphology | Genuine annotated rabbit head/external eye, pinna and tactile facial vibrissae; explain hearing/balance and tactile receptors separately |
| `u5-egg-laying-mammals-monotreme-reproduction` | Meaningless stages | Distinct source-verifiable oviposition, hatching and milk provisioning through mammary patches; do not invent a nipple |
| `u5-marsupials-marsupial-life-history` | Outline ovals instead of neonatal development | Representative marsupial neonate, mammary teat attachment and developing joey; caveat that not all marsupials have complete pouches |
| `u5-aquatic-mammals-aquatic-mammal-groups` | Generic ovals conceal morphology | Real comparison of cetaceans, sirenians, pinnipeds and sea otters, with taxonomic note: they are not one order |

The six `visualReview` fields are set to `USER_REJECTED_REPLACEMENT_REQUIRED`.
The viewer uses this to withhold those plates in English and Tamil; the
registered 64 slots, original PNGs, original sources and other accepted
variants remain untouched. Technical QA continues to assert each original
PNG is intact. This is NOT a claim that 6/64 figures have been replaced.

## Legally reusable replacement candidates and scientific references

- **Avian flight musculature:** L. Shyamal (2012), *Wing Muscles, color.svg*,
  Wikimedia Commons, CC BY-SA 2.5, https://commons.wikimedia.org/wiki/File:Wing_Muscles,_color.svg .
  Preferred anatomical plate, but the original SVG must first be obtained,
  rendered legibly as a PNG and inspected; do not invent source bytes.
- **Marsupial care:** Johnscotaus (2016), *Baby kangaroo in pouch.jpg*,
  Wikimedia Commons, CC BY-SA 4.0,
  https://commons.wikimedia.org/wiki/File:Baby_kangaroo_in_pouch.jpg .
  Useful for actual pouch morphology/young; not a complete lifecycle diagram.
- **Indian snakes:** ICMR-NIRRCH official illustrated chart
  https://nirrch.res.in/wp-content/uploads/2023/10/Snake-Identification-Chart-English.pdf .
  Reference for species comparison only; publication/reuse permission for
  the photos must be independently established before bundling.
  Independently licensed photographs can be sourced per taxon on Wikimedia
  Commons; retain four separate source pages and CC licence conditions.
- **Echis example:** Jnprasad2001, *Saw-scaled Viper.jpg*, Commons,
  CC BY-SA 4.0, https://commons.wikimedia.org/wiki/File:Saw-scaled_Viper.jpg .
- **Other mammal topics:** use anatomically demonstrative museum or specimen
  images with explicit reuse terms, not unsourced stock artwork or symbolic
  substitutes. The exact photograph and rights remain pending verification.

## Release and reader constraints

- The primary course content and paragraph pagination remain unaffected.
- Figure placeholders should not consume an image-sized blank frame.
- Pinch-zoom for **retained** figures positions wide images near the top
  instead of suspending them in the centre of a mostly empty handset screen.
- Never conflate `PROVISIONAL_QA` with independent scientific acceptance.
- Do not raise a figure's review status to ACCEPTED merely because the image
  file exists or is photorealistic.
- A new candidate requires exact figure ID, matching lesson objective,
  actual asset, checksum, source/rights, readable labels, and a visual QA
  screenshot before enabling it in the reader.

## Implemented source-based replacements — provisional QA

On 12 November 2026, three original low-utility images were replaced at
their **same registered lesson IDs** using genuinely photographed or
published anatomical source material. The assets are fully attributed in
`docs/CHORDATA_LICENSED_SOURCE_PROVENANCE_20261112.json`. The retired
original PNGs have been retained under `docs/retired_noninstructional_png/`
with the corresponding editable SVGs unchanged.

- India's Big Four snakes: four real Commons photographs, individual source
  pages, explicit warning against using photographs for live snake identification.
- Flight muscles: L. Shyamal's original coloured avian flight-muscle anatomy,
  cleanly rasterised, not redrawn from symbolic curves.
- Marsupial reproduction: authentic kangaroo with joey in pouch, with a caveat
  that pouch structure varies across marsupials.

**Still withheld:** only the inadequate Calotes heart-flow schematic. No new abstract diagrams are substituted.

These are quality-improved *QA teaching figures*, not scientific release approval.

## Calotes photographic replacement and heart correction (12 November 2026)

- `u4-calotes-external`: the historic curled-tail engraving was replaced at its
  original registered lesson position by a sourced living-specimen photograph,
  credited to Azim Khan Ronnie, Wikimedia Commons, CC BY-SA 4.0. The existing
  historic image and full source record remain archived outside the APK.
  Provenance and installed SHA are in
  `docs/qa-image-review/CALOTES_PHOTOGRAPHIC_REPLACEMENT_20261112.json`.
- `u4-calotes-arterial-system`: the existing diagram is a generic functional
  cavity/flow schematic, not a reliable species-specific anatomical plate.
  This figure is **withheld** in English and Tamil after owner rejection; the
  physical PNG, corrected SVG master, original credit and file SHA remain
  unchanged. References: Prakash (1960), DOI 10.1002/ar.1091360406;
  de Silva (1956) original Calotes arterial account; Jensen et al. (2013)
  comparative reptile-heart morphology. These references do **not** grant
  reproduction rights for their figures.
- A replacement heart illustration must show actual gross morphology and
  documented vessel relationships. A generic vertebrate circulation diagram,
  stock heart icon or invented symmetric arterial branches is not acceptable.

**Image QA status:** One genuine Calotes photograph integrated (provisional);
Calotes heart replacement still absent; no release sign-off asserted.

## Rabbit sensory-organs source replacement (12 November 2026)

- Target: `u5-rabbit-sense-organs` on Unit V rabbit lesson, page 5.
- Supersedes the unusable eye/ear/whisker icons with an actual domestic
  rabbit side-profile photograph. Source: Trougnouf (Benoit Brummer),
  [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Side_view_of_the_head_of_a_pet_rabbit_in_Brussels_(DSCF0830).jpg),
  CC BY 4.0. The specimen photo remains intact apart from proportional
  sizing; only a separate numbered label layer is added.
- The plate identifies the *pinna*, *lateral eye* and *mystacial vibrissae*,
  with the crucial caveat that balance receptors are in the internal ear,
  **not** in the pinna. No pretend internal organ diagram is displayed.
- The old vector PNG is archived under `docs/retired_noninstructional_png/`,
  with original editable SVG untouched and its hash retained. Attribution,
  source JPEG checksum, new PNG checksum, exact transformations and
  source licence appear in
  `docs/qa-image-review/RABBIT_SENSE_ORGANS_PHOTOGRAPHIC_REPLACEMENT_20261112.json`.
- Human biological review, Tamil editorial review and device screenshots
  remain pending; asset presence is **not** independent acceptance.

## Monotreme reproduction—sourced teaching plate (12 November 2026)

- Replaced `u5-egg-laying-mammals-monotreme-reproduction` shared plate with
  a non-symbolic comparison: real adult platypus photograph (Eric Chan,
  CC BY 2.0), actual echidna puggle photo (Ian R McCann/Museums Victoria,
  CC BY-SA 4.0), and F. E. Beddard's genuine 1902 anatomical figure showing
  echidna pouch and mammary-gland regions (public domain).
- Crucially, *platypus* nests and incubates eggs in a **burrow**; the
  *echidna* incubates an egg in a **temporary ventral pouch**. The actual
  puggle is an **echidna**, not a platypus hatchling, and the adult platypus's
  sex is not inferred from the photograph.
- Milk is secreted without nipples; the actual published echidna mammary
  anatomy is included instead of symbolic nipples or false diagrams.
- The old user-rejected schematic PNG is preserved outside APK under
  `docs/retired_noninstructional_png/platypus_reproduction.png`; source
  hashes, modifications, each source creator, and licence appear in
  `docs/qa-image-review/MONOTREME_REPRODUCTION_SOURCE_PLATE_20261112.json`.
- This is **not** direct photographic evidence of egg laying or a continuous
  life cycle. Academic, Tamil editorial, device and release approvals remain
  pending.

## Aquatic mammal groups: independent, source-licensed photographic comparison

- Unit V `u5-aquatic-mammals-aquatic-mammal-groups`, page 1, exact original
  registered figure ID. Four authentic photographic sources replace symbolic
  ovals: bottlenose dolphin (Caroline Legg, CC BY 2.0); dugong (Jerome Paillet,
  IFREMER, CC BY 4.0); harbour seal (Arnstein Rønning, CC BY-SA 4.0); and
  sea otter (U.S. Fish and Wildlife Service, public domain). All four creator
  records and full source SHA-256 digests are retained in
  `docs/qa-image-review/AQUATIC_MAMMAL_FOUR_PHOTOGRAPHS_20261112.json`.
- Whole original photograph frames are proportionally fitted, not stretched,
  distorted, upscaled, traced, or redrawn into symbols.  The new plate
  compares Cetacea, Sirenia, Pinnipedia and sea otters (Mustelidae).
  Dolphin and dugong are obligately aquatic; seals can haul out, and sea
  otters belong to Carnivora but **not** Pinnipedia. Sirenians belong to
  Afrotheria; cetaceans are nested within Artiodactyla. Convergent aquatic
  adaptation is not evidence of one taxonomic order.
- The exact old symbolic PNG and its original SVG remain archived with
  historic SHA-256. Independent zoological/Tamil review and phone UI
  screenshots are still needed; source presence does not imply app-store
  readiness or academic certification.
