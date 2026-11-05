# Chordata diagram placement evidence

- Every one of the 64 syllabus figure IDs has an explicit page and section mapping in `app/src/main/assets/figure_placements.json`.
- `figures.json` maps exactly three generated provisional PNGs to their respective external-morphology lesson pages; absence of a PNG does not count as approval.
- `scripts/audit_figure_placements.py` audits 64/64 mappings, all present PNGs, hashes and bilingual captions and offers `--require-complete` as a separate strict production gate.
- No labelled organ-system drawing has been supplied. The QA APK is not academically approved.
