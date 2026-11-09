# CHORDATA — Scoliodon digestive-system illustration QA (9 November 2026)

**Status: ORIGINAL AI PNG CANDIDATE ONLY — NOT INSTALLED / NOT GREEN-TICKED.**

Baseline: `qa/chordata-illustrations-continuous` at `534706347d48b70872ed1b1977fd07c13bf6e67b`.
Registered slot: `u2-scoliodon-digestive-labelled`, Unit II / `u2-scoliodon` / page 2 / `digestive-system`.

Current installed PNG **unchanged**: `app/src/main/assets/pencil_plates/scoliodon_digestive_en.png`, SHA-256 `57f1bd87ee5ea529eff8bec7ca5ac4a60c2dca1be6afb62daf52ba024741cf17`.

## Search outcome

Wikimedia Commons [Squa152p.png](https://commons.wikimedia.org/wiki/File:Squa152p.png), by Jon Houseman, CC BY-SA 3.0, is authentic but **Squalus acanthias**, only 450×337 px; it is not an acceptable species-specific full-system substitute for Scoliodon. Other Scoliodon diagrams were found in teaching notes without verified redistribution rights; they were consulted as anatomical references, not copied.

## Newly generated candidate history

- v1 SHA-256 `0b1dede75c48df0bf513d32e37c46a767181e05a793a018ef522f82f3ed4d56f` — REJECTED: visibly coiled external intestine.
- v2 SHA-256 `81f5be1a0fb26b1898d2c0ffa8c85ac043d532253ee542ea445cdb0af47f4a33` — REJECTED: misleading long mammalian-like intestinal looping.
- v3 SHA-256 `be594e9b16f6f149fad9d62f44c2419ce62d02d1cc383a1a60fd9d318503b69a`, 1536×1024 RGB PNG; OpenAI ChatGPT ImageGen — **HOLD**: realistic presentation with visible internal intestinal valve, but **blind sac, bursa entiana and rectal gland remain absent**, and internal fold geometry/species fidelity need expert review. Not adequate to replace the complete registered teaching plate.

v3 candidate is in the separate ChatGPT conversation artifact `CHORDATA_Scoliodon_Digestive_QA_20261109.zip`, not this repository, not any Android APK. Do **not** claim its image binary is installed or reuse the existing asset's credit.

## Required to unblock

Create a scientifically checked complete Scoliodon plate showing J-shaped cardiac/pyloric stomach and blind sac, bursa entiana, a short broad intestine with internal scroll valve, separate osmoregulatory rectal gland joining rectum, liver, gall bladder/bile duct, pancreas and cloaca. Check all label leaders and source rights; allow English anatomical labels, and keep Tamil prose separate. Only after exact PNG binary and manifest SHA are updated on an isolated QA branch, run static gate, Kotlin compilation, Android emulator and physical-device review. Biology and Tamil reviewer decisions remain pending; production HOLD.

References (not reproduction permission):
- https://www.ntrgdc.ac.in/userfiles/file/Course%20Materials/Semester-2-Digestive%20system%20in%20Scoliodon.pdf
- https://www.egyankosh.ac.in/bitstream/123456789/58839/1/Unit%203%20Digestive%20System.pdf

**All previously integrated acceptable authentic or near-realistic images remain unchanged.**
