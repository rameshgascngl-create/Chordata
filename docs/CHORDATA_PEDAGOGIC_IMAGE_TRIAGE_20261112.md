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
