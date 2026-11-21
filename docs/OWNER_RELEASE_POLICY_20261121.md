# CHORDATA — Auditable owner-approval release route

**Authorisation:** On 21 November 2026 the project owner explicitly chose personal academic image approval in place of two distinct human figure reviewers. This is a release policy decision; it does not assert independent science/Tamil certification or transfer copyright.

**Mechanism:** `docs/OWNER_FIGURE_APPROVED_ASSETS_20261121.json` locks all 64 slots and 68 exact PNGs by SHA-256, language, lesson placement, source, creator and declared licence. `scripts/verify_owner_release.py` must pass in both Android QA and the protected manual Play release workflow. Any changed or held image, credit, rights claim, path, or unregistered variant invalidates approval; rerun actual human review and explicitly replace the lock only with renewed owner authority. `scripts/test_owner_release_policy.py` exercises negative cases.

**Preserved separate checks:** `scripts/write_figure_review_register.py --check` maintains the 64-row independent register without manufacturing signatures. `--release-check` for genuine independent reviewer certification remains available and unmodified. Source/figure placement, AI10 bundle assets, scientific content, Tamil editorials, privacy preflight, exact-SHA emulator QA, release compilation/lint, 16 KiB audits, upload signing and signed artifact verification are still mandatory.

**Licensing:** Owner approval is not a licence from a third-party author. Public-domain, CC BY, CC BY-SA, AI-generated and project-original claims remain distinct; attribution, modifications and rights declarations are preserved and checked against the original metadata. Copyright validity is not conclusively established merely because an entry contains a licence string. Externally sourced image authors' own licence notices and any share-alike terms must be respected.

**Production AAB:** The signing workflow is manual and gated by protected `play-upload-review` environment, GitHub QA success on the same SHA, public privacy URL, publisher-contact confirmation, and four secret upload-key values. It does not automatically submit anything to Play Console.
