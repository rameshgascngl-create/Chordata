# Corrected Branchiostoma AI figure: controlled QA intake

Verified local candidate: branchiostoma_corrected_en_QA.png, 1536 x 1024 RGB PNG, 1,199,846 bytes, SHA-256 2fbd48be62b83309c87214492ea20dfea1995a3e624fca66c17ed995c95d9b1e.

Registered lesson ID: u1-cephalochordata-branchiostoma-labelled. The only replacement path is app/src/main/assets/pencil_plates/branchiostoma_ta.png, original SHA-256 e1d8b5a749628f3c49cae235c5dd52649f44fa597eb86ca6ce43a8b7404a1e75.

The original AI image's two oversized gonads were rejected. The corrected candidate has repeated serial ventrolateral gonads, dorsal nerve cord, notochord, pharyngeal slits, myomeres, intestine, atriopore and oral cirri. It is an original OpenAI ChatGPT ImageGen illustration with added English leader labels, not a photograph or a copy of the references. Green tick allows provisional QA integration with minor stylisation, never automatic scientific acceptance.

The exact PNG lives in the separate CHORDATA_Branchiostoma_Corrected_AI_QA.zip conversation artifact. It is NOT in this GitHub commit and is NOT inside any APK yet.

To stage after placing the PNG locally, on the isolated QA branch run:

    python3 scripts/stage_approved_branchiostoma_qa.py --repo . --candidate /path/to/branchiostoma_corrected_en_QA.png
    python3 scripts/stage_approved_branchiostoma_qa.py --repo . --candidate /path/to/branchiostoma_corrected_en_QA.png --apply
    bash scripts/qa_all.sh
    git diff --check

Review the changed Tamil PNG and manifest before committing. Existing English Hans Hillewaert PNG and its CC BY-SA credit must not change. Human biology and Tamil decisions remain PENDING; the reviewer CSV records the credited English source and does not constitute a sign-off for the new Tamil image. Full Android/emulator and physical-device QA remain mandatory. Production HOLD.

Anatomical verification: https://doi.org/10.1080/00212210.1996.10688880 and https://www.gutenberg.org/cache/epub/73702/pg73702-images.html. These are scientific references only, not image copying permission.

The local exact-hash staging procedure was tested with check-only and apply on a mocked Git checkout.