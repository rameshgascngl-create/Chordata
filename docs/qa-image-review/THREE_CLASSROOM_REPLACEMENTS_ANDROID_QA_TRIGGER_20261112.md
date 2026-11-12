# CHORDATA — three image replacement QA trigger (12 November 2026)

User screenshot defects addressed on this dedicated QA branch:

1. **Scoliodon digestive anatomy** (\`u2-scoliodon-digestive-labelled\`): original diagram was cramped. Its species-specific component is retained and enlarged in a new page layout, while the comparative Squalus plate is explicitly labelled as a **different genus**, not presented as Scoliodon.
2. **Fish scales** (\`u2-scales-fins-scale-types-labelled\`): the Jon Houseman reference is reorganised so ganoid, cycloid and ctenoid illustrations occupy a larger region. The placoid region uses the separately credited Houseman placoid section. Licence CC BY-SA 3.0.
3. **Devonian transition** (\`u3-origin-devonian-transition\`): stylised, uninformative silhouette panels replaced by Maija Karala's CC BY-SA 3.0 cladogram depicting fossil-based tetrapodomorph taxa. Do not claim all pictured fossils form a direct ancestor–descendant line.

All three original PNGs remain in \`docs/retired_noninstructional_png/\`.
Exact source download SHA-256 values, final asset SHA-256 values and the 3 registered figure IDs are recorded in
\`docs/qa-image-review/THREE_CLASSROOM_FIGURES_REPLACED_20261112.json\`.

The reader's full-resolution pinch-zoom view has also received a bounded pan and reset correction. Figures and text remain academically **provisional**, not signed off for final retail release.

**Purpose of this commit:** invoke normal Android native QA on the *already staged image-bearing commit*. GitHub Actions pushes using \`GITHUB_TOKEN\` do not generally trigger a second push workflow. Consequently this explicit connector-originated commit is required to run the compiled APK and instrumentation checks for the updated source.
