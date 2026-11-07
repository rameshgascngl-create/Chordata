#!/usr/bin/env python3
"""Strict offline figure-to-lesson QA gate for the 39-topic Chordata app.

A provisional specimen outline is never counted as a finished, labelled plate.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"


def require(ok, message):
    if not ok:
        raise SystemExit("FIGURE PLACEMENT FAIL: " + message)


def read_json(name):
    return json.loads((ASSETS / name).read_text(encoding="utf-8"))


def main():
    pack = read_json("chordata_content.json")
    topics = [topic for unit in pack["units"] for topic in unit["topics"]]
    topic_by_id = {topic["id"]: topic for topic in topics}
    required = {diagram_id for topic in topics for diagram_id in topic["diagramIds"]}
    require(len(required) == 64, "course content must contain 64 unique diagram IDs")

    registry = read_json("figure_slots.json")
    require(registry.get("schemaVersion") == 1, "unknown placement schema")
    slots = registry.get("slots", [])
    require(len(slots) == 64, "registry must have 64 slots")
    require(len({slot["id"] for slot in slots}) == 64, "duplicate diagram slots")
    require({slot["id"] for slot in slots} == required, "missing or invented diagram IDs")

    known_statuses = {"PENDING", "ACADEMICALLY_APPROVED"}
    for slot in slots:
        topic = topic_by_id.get(slot.get("topicId"))
        require(topic is not None, "orphan diagram " + slot["id"])
        require(slot["id"] in topic["diagramIds"], "diagram in wrong topic: " + slot["id"])
        page = slot.get("page")
        require(isinstance(page, int) and 1 <= page <= len(topic["sections"]),
                "diagram assigned to intro, quiz, or invalid page: " + slot["id"])
        require(topic["sections"][page - 1]["key"] == slot.get("sectionKey"),
                "wrong lesson section for: " + slot["id"])
        require(slot.get("status") in known_statuses, "invalid review status: " + slot["id"])
        for name in ("captionEn", "captionTa"):
            require(isinstance(slot.get(name), str) and slot[name].strip(),
                    "missing bilingual caption: " + slot["id"])

    provisional = read_json("figures.json")
    require(isinstance(provisional, list), "provisional figure register invalid")
    require(len({f["id"] for f in provisional}) == len(provisional),
            "duplicate provisional figure IDs")
    require(len(provisional) == 7, "QA build must contain exactly 3 original + 4 credited images")
    provisional_by_id = {f["id"]: f for f in provisional}
    draft_slots = [s for s in slots if s.get("provisionalFigureId")]
    require(len(draft_slots) == 7, "expected seven explicitly mapped reference illustrations")
    require({s["provisionalFigureId"] for s in draft_slots} == set(provisional_by_id),
            "provisional illustration not linked to exactly one diagram slot")
    for slot in draft_slots:
        figure = provisional_by_id[slot["provisionalFigureId"]]
        require(figure["topicId"] == slot["topicId"] and figure["page"] == slot["page"],
                "draft illustration placed on wrong page: " + figure["id"])
        require(slot["status"] == "PENDING",
                "unlabelled outline cannot satisfy labelled anatomical plate: " + slot["id"])

    png_dir = ASSETS / "figures"
    digest_records = json.loads((png_dir / "source-hashes.json").read_text(encoding="utf-8"))
    hashes = {v["id"]: v for v in digest_records}
    require(set(hashes) == set(provisional_by_id), "hash inventory mismatch")
    expected_files = {f["file"] for f in provisional}
    actual_files = {p.name for p in png_dir.glob("*.png")}
    require(actual_files == expected_files, "unexpected or absent PNG image assets")
    for figure in provisional:
        name = figure["file"]
        require(name.endswith(".png") and Path(name).name == name, "unsafe figure filename")
        data = (png_dir / name).read_bytes()
        require(len(data) > 10_000 and data.startswith(bytes.fromhex("89504e470d0a1a0a")),
                "invalid PNG file: " + name)
        width, height = struct.unpack(">II", data[16:24])
        require(width >= 1200 and height >= 600, "figure too small: " + name)
        expected_digest = hashes[figure["id"]]["sha256"]
        require(hashlib.sha256(data).hexdigest() == expected_digest, "figure checksum mismatch")
        is_original = figure["id"] in ("scoliodon-external", "columba-external", "rabbit-external")
        if is_original:
            require(figure.get("author") and figure.get("license", "").startswith("Provisional QA artwork"),
                    "original QA figure wrongly credited: " + figure["id"])
        else:
            require(figure["id"].startswith("commons-") and figure.get("origin") == "Wikimedia Commons",
                    "source figure missing Commons provenance: " + figure["id"])
            require(figure.get("sourceUrl", "").startswith("https://commons.wikimedia.org/wiki/File:"),
                    "source image lacks exact owner file page: " + figure["id"])
            require(figure.get("licenseUrl", "").startswith("https://creativecommons.org/"),
                    "source image lacks licence URL: " + figure["id"])
            require(figure.get("reviewStatus") == "REFERENCE_SOURCE_AWAITING_ACADEMIC_REVIEW",
                    "unreviewed figure misrepresented: " + figure["id"])
    pencil_dir = ASSETS / "pencil_plates"
    manifest = read_json("pencil_plates/manifest.json")
    require(manifest["status"] in ("QA_NOT_ACADEMICALLY_APPROVED", "PROVISIONAL_QA_NOT_ACADEMICALLY_APPROVED"), "pencil plate review status")
    pencil_ids = {
        "u1-cephalochordata-branchiostoma-labelled",
        "u5-flight-adaptations-avian-lung",
        "u5-columba-endoskeleton",
        "u5-rabbit-endoskeleton",
    }
    shared_ids = {
        "u5-egg-laying-mammals-monotreme-reproduction",
        "u5-dentition-tooth-types",
        "u5-dentition-human-rabbit-dental-formula",
        "u5-rabbit-excretory-system",
        "u1-origin-deuterostome-relationships",
        "u1-vertebrata-classification-vertebrate-phylogeny",
        "u3-amphibia-classification-life-cycle",
        "u4-origin-extinct-amniote-phylogeny",
        "u2-migration-migration-cycle",
        "u4-skull-temporal-skull-types",
        "u2-scales-fins-fins-labelled",
        "u2-scales-fins-scale-types-labelled",
        "u1-agnatha-petromyzon-adult-larva",
        "u1-hemichordata-balanoglossus-external",
        "u1-urochordata-ascidia-larva-adult",
        "u1-general-characters-five-chordate-characters",
        "u2-scoliodon-gills-labelled",
    }
    pairs = Counter((f["diagramId"], f["lang"]) for f in manifest["figures"])
    require(all(n == 1 for n in pairs.values()), "duplicate diagram/language pairs")
    original_required = (Counter((id, lang) for id in pencil_ids for lang in ("en", "ta"))
                         + Counter((id, "shared") for id in shared_ids))
    require(all(pairs[k] == n for k, n in original_required.items()),
            "original validated source plates missing")
    pending_ids = {slot["id"] for slot in slots if slot["status"] == "PENDING"}
    filled_ids = {f["diagramId"] for f in manifest["figures"]}
    require(filled_ids <= pending_ids, "pencil plates falsely academically approved")
    require(filled_ids == {slot["id"] for slot in slots}, "registered anatomical sketch missing from lesson")
    require(all("en" in {k[1] for k in pairs if k[0] == id} or
                "shared" in {k[1] for k in pairs if k[0] == id}
                for id in filled_ids), "no English/shared figure for a lesson")
    pencil_names = {Path(f["path"]).name for f in manifest["figures"]}
    require(pencil_names == {p.name for p in pencil_dir.glob("*.png")},
            "pencil plate inventory mismatch, including unregistered files")
    for figure in manifest["figures"]:
        rel = Path(figure["path"])
        require(not rel.is_absolute() and len(rel.parts) == 2 and
                rel.parts[0] == "pencil_plates" and rel.name.endswith(".png"),
                "noncanonical manifest path: " + figure["path"])
        name = rel.name
        raw = (ASSETS / rel).read_bytes()
        require(raw.startswith(bytes.fromhex("89504e470d0a1a0a")) and len(raw) == figure["size"]
                and hashlib.sha256(raw).hexdigest() == figure["sha256"],
                "pencil plate file integrity mismatch: " + name)
        require(figure["author"] and figure.get("reviewStatus", "").startswith("PROVISIONAL_"),
                "pencil plate provenance or review status mismatch: " + name)
        if figure["diagramId"] in shared_ids:
            require(figure["lang"] == "shared" and
                    all(figure.get(k) for k in ("keyEn", "keyTa", "referenceUrl")),
                    "original bilingual numbered key/reference missing: " + name)
            if figure["diagramId"] == "u1-agnatha-petromyzon-adult-larva" and figure.get("sourceUrl"):
                require(figure["author"] == "LadyofHats (adult); H. G. Seeley, 1886 (larva); CHORDATA QA (layout)",
                        "source plate creator attribution changed: " + name)
                require(figure.get("license", "").startswith("Public domain") and
                        figure.get("sourceUrls") == [
                            "https://commons.wikimedia.org/wiki/File:Lamprey_anatomy.png",
                            "https://commons.wikimedia.org/wiki/File:FMIB_48179_Larval_Form_of_Petromyzon_branchialis,_Formerly_Known_as_Ammocoetes.jpeg"],
                        "sourced lamprey artwork lacks both original licence/provenance records")
                require(figure.get("modifications") and len(figure.get("sourceSha256", [])) == 2,
                        "lamprey derivative missing transformation and source checksums")
            elif figure["diagramId"] == "u1-general-characters-five-chordate-characters" and figure.get("sourceUrl"):
                require(
                    figure.get("author") == "Microvipera (generalised chordate morphology); CHORDATA QA (layout)"
                    and figure.get("sourceUrl") == "https://commons.wikimedia.org/wiki/File:General_chordate_morphology.svg"
                    and figure.get("license", "").startswith("CC0 1.0")
                    and figure.get("licenseUrl") == "https://creativecommons.org/publicdomain/zero/1.0/"
                    and len(figure.get("sourceSha256", [])) == 1
                    and "embryo" in figure.get("keyEn", "")
                    and "endostyle" in figure.get("keyEn", "").lower()
                    and figure.get("visualReview") == "REPLACED_VISUAL_QA_PENDING",
                    "five hallmark Chordata structures lack original source/rights or life-stage caveat"
                )
            elif figure["diagramId"] == "u1-hemichordata-balanoglossus-external" and figure.get("sourceUrl"):
                require(
                    figure["author"] == "Unknown illustrator, New International Encyclopaedia (1905); CHORDATA QA (layout)"
                    and figure.get("sourceUrl") == "https://commons.wikimedia.org/wiki/File:NIE_1905_Ascidians_and_balanoglossus.png"
                    and figure.get("license", "").startswith("Public domain")
                    and len(figure.get("sourceSha256", [])) == 1
                    and figure.get("modifications"),
                    "Balanoglossus adapted plate lacks origin, public-domain status, or modification evidence"
                )
            elif figure["diagramId"] == "u2-scales-fins-scale-types-labelled" and figure.get("sourceUrl"):
                require(
                    figure["author"] == "Jon Houseman (ganoid/cycloid/ctenoid); CHORDATA QA (original placoid section and layout)"
                    and figure.get("sourceUrl") == "https://commons.wikimedia.org/wiki/File:Fishscales.png"
                    and figure.get("license") == "CC BY-SA 3.0 Unported — composite derivative, source credited"
                    and figure.get("licenseUrl") == "https://creativecommons.org/licenses/by-sa/3.0/"
                    and len(figure.get("sourceSha256", [])) == 1
                    and all(term in figure.get("keyEn", "") for term in ("Placoid", "Ganoid", "Cycloid", "Ctenoid")),
                    "fish-scale plate missing rights, four types, or original Houseman source"
                )
            elif figure["diagramId"] == "u2-scales-fins-fins-labelled" and figure.get("sourceUrl"):
                require(
                    figure["author"].startswith("Unknown original illustrator (1898)")
                    and "FMIB_47883_" in figure.get("sourceUrl", "")
                    and figure.get("license", "").startswith("Public domain")
                    and figure.get("licenseUrl") == "https://creativecommons.org/publicdomain/mark/1.0/"
                    and len(figure.get("sourceSha256", [])) == 1
                    and all(str(i) in figure.get("keyEn", "") for i in range(1, 7))
                    and "not all fishes" in figure.get("keyEn", ""),
                    "historical fish-fins key/source rights do not match original numbers"
                )
            elif figure["diagramId"] == "u5-rabbit-excretory-system" and figure.get("sourceUrl"):
                require(
                    figure["author"].startswith("J. Arthur Thomson, Outlines of Zoology (1916)")
                    and figure.get("sourceUrl") == "https://commons.wikimedia.org/wiki/File:Image_from_page_743_of_%22Outlines_of_zoology%22_(1916)_(14597351000).jpg"
                    and figure.get("license", "").startswith("Public domain")
                    and len(figure.get("sourceSha256", [])) == 1
                    and "Female" in figure.get("keyEn", "")
                    and "vestibule" in figure.get("keyEn", "").lower()
                    and "Male" in figure.get("keyEn", ""),
                    "rabbit urinary plate must preserve male/female distinctions and 1916 rights"
                )
            else:
                if (figure["diagramId"] == "u2-scoliodon-gills-labelled"
                        and figure.get("visualReview") == "REPLACED_VISUAL_QA_PENDING"):
                    require(figure["author"] == "CHORDATA QA project — original vector shark septal-gill teaching schematic",
                            "staged shark-gill original art has wrong creator attribution")
                else:
                    require(figure["author"] == "Chordata QA project — original numbered schematic",
                            "original plate creator attribution changed: " + name)
        if (figure["diagramId"] == "u2-scoliodon-brain-labelled"
                and figure.get("visualReview") == "REPLACED_VISUAL_QA_PENDING"):
            require(
                figure.get("lang") == "en"
                and figure.get("author") == "CHORDATA QA — original reference-guided shark dorsal brain reconstruction"
                and figure.get("sourceUrl", "") == ""
                and figure.get("svgMaster") == "docs/original_plate_svg/shark_brain_dorsal_en.svg"
                and len(figure.get("svgSha256", "")) == 64
                and figure.get("scope", "").startswith("Dorsal shark brain")
                and all(term in figure.get("keyEn", "").lower() for term in
                        ("olfactory sacs", "bilobed", "optic lobes", "cerebellum",
                         "restiformia", "spinal cord"))
                and len(figure.get("referenceUrls", [])) == 4
                and figure.get("reviewStatus") == "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
                "Wave 6 dorsal brain scientific scope/provenance guard failed"
            )
        if (figure["diagramId"] == "u2-scoliodon-digestive-labelled"
                and figure.get("visualReview") == "REPLACED_VISUAL_QA_PENDING"):
            require(
                figure["lang"] == "en"
                and figure["author"] == "CHORDATA QA — original, reference-guided Scoliodon-type digestive anatomy plate"
                and figure.get("sourceUrl", "") == ""
                and figure.get("svgMaster") == "docs/original_plate_svg/scoliodon_digestive_anatomy_en.svg"
                and len(figure.get("svgSha256", "")) == 64
                and figure.get("size", 0) > 100000
                and len(figure.get("referenceUrls", [])) == 4
                and all(term in figure.get("keyEn", "").lower()
                        for term in ("cardiac", "pyloric", "blind sac", "gallbladder",
                                     "pancreas", "scroll", "rectal gland", "salt"))
                and figure.get("reviewStatus") == "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
                "Scoliodon digestive plate missing expected anatomy/rights/SVG/review evidence"
            )
        if (figure["diagramId"] in ("u5-columba-endoskeleton", "u5-rabbit-endoskeleton")
                and figure["lang"] == "en" and figure.get("sourceUrl")):
            original_name = ("pigeon_endoskeleton_line_art.png"
                             if figure["diagramId"] == "u5-columba-endoskeleton"
                             else "rabbit_endoskeleton_line_art.png")
            original_bytes = (ASSETS / "figures" / original_name).read_bytes()
            require(
                hashlib.sha256(original_bytes).hexdigest() == figure.get("sourceAssetSha256")
                and figure.get("sourceAsset") == "figures/" + original_name
                and original_bytes == raw
                and figure.get("license", "").startswith("Public domain")
                and figure.get("sourceUrl", "").startswith("https://commons.wikimedia.org/wiki/File:")
                and figure.get("modifications"),
                "historical skeleton source bytes/rights/credits mismatch: " + name
            )
        if (figure["diagramId"] == "u3-rana-brain" and figure.get("sourceUrl")):
            require(
                figure["lang"] == "en" and figure.get("sourceUrl") ==
                "https://commons.wikimedia.org/wiki/File:The_biology_of_the_frog_(1927)_(20356465586).jpg"
                and "1927" in figure.get("author", "")
                and figure.get("license", "").startswith("Public domain")
                and len(figure.get("sourceSha256", [])) == 1
                and figure.get("modifications")
                ,
                "frog dorsal historical source/rights missing: " + name
            )
        if (figure["diagramId"] == "u3-rana-arterial-system" and figure.get("sourceUrl")):
            require(
                figure["lang"] == "en"
                and figure["author"].startswith("Alexander Ecker")
                and figure.get("sourceUrl") == "https://www.gutenberg.org/cache/epub/77560/pg77560-images.html"
                and figure.get("sourceImageUrl", "").startswith("https://www.gutenberg.org/")
                and figure.get("license", "").startswith("Public domain")
                and len(figure.get("sourceSha256", [])) == 1
                and "Fig. 143" in figure.get("modifications", ""),
                "Ecker fig. 143 arterial plate attribution or source image missing"
            )
        if figure["diagramId"] == "u3-rana-respiration" and figure.get("sourceUrl"):
            require(
                figure["lang"] == "en"
                and figure.get("sourceUrl") == "https://commons.wikimedia.org/wiki/File:Amph001B.png"
                and figure["author"].startswith("Jon Houseman (frog buccal-pump sequence)")
                and figure.get("license", "").startswith("CC BY-SA 3.0")
                and figure.get("licenseUrl") == "https://creativecommons.org/licenses/by-sa/3.0/"
                and len(figure.get("sourceSha256", [])) == 1
                and all(x in figure.get("keyEn", "") for x in
                        ("Cutaneous", "Buccopharyngeal", "Pulmonary")),
                "frog respiratory source or three gas-exchange modes missing"
            )
        if figure["diagramId"] == "u5-columba-urinogenital" and figure.get("sourceUrl"):
            require(
                figure["lang"] == "en"
                and figure.get("author") == "CHORDATA QA original comparative diagram; George Howard Parker (1928) female pigeon anatomy"
                and figure.get("sourceUrl") == "https://commons.wikimedia.org/wiki/File:Creation_by_Evolution_(1928)_p037_reproductive_organs_of_a_female_pigeon.png"
                and figure.get("license", "").startswith("Public domain")
                and len(figure.get("sourceSha256", [])) == 1
                and len(figure.get("originalSvgSha256", "")) == 64
                and figure.get("sourceCaptionUrl") == "https://en.wikisource.org/wiki/Creation_by_Evolution/Vestigial_Organs"
                and all(item in figure.get("keyEn", "") for item in ("Male:", "Female:", "O:", "Od:", "V:")),
                "pigeon male/female source provenance or O/Od/V key missing"
            )
        if (figure["diagramId"] == "u2-scoliodon-gills-labelled"
                and figure.get("visualReview") == "REPLACED_VISUAL_QA_PENDING"):
            require(
                figure["lang"] == "shared"
                and figure["author"] == "CHORDATA QA project — original vector shark septal-gill teaching schematic"
                and figure.get("sourceUrl", "") == ""
                and figure.get("svgMaster") == "docs/original_plate_svg/shark_septal_gills_en.svg"
                and len(figure.get("svgSha256", "")) == 64
                and all(term in figure.get("keyEn", "").lower()
                        for term in ("interbranchial septa", "hemibranchs",
                                     "secondary lamellae", "countercurrent"))
                and len(figure.get("referenceUrls", [])) == 3
                and all(u.startswith("https://") for u in figure.get("referenceUrls", []))
                and figure.get("reviewStatus") == "PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING",
                "original septal-gill plate lacks correct anatomy, SVG, references, or draft status"
            )
        if (figure["diagramId"] == "u2-scoliodon-external-labelled"
                and figure.get("sourceUrl")):
            # Guard against the previous scientific error: the historically
            # mislabeled Scoliodon laticaudus is spadenose, not the milk
            # shark covered by the S. sorrakowah type-study lesson.
            require(
                figure["lang"] == "en"
                and figure["author"] == "Eduard Rüppell (1837) — historical plate; Field Museum Library/BHL scan; CHORDATA QA crop/layout"
                and figure["sourceUrl"] == (
                    "https://commons.wikimedia.org/wiki/File:"
                    "Neue_Wirbelthiere_zu_der_Fauna_von_Abyssinien_geh%C3%B6rig_"
                    "(Taf._18_Fig.1-4)_BHL37140507.jpg"
                )
                and figure.get("sourceSha1") == "884bc3fdcd1dcfe357c51e33f86ecd2a226a78d0"
                and figure.get("licenseUrl") == "https://creativecommons.org/publicdomain/mark/1.0/"
                and figure.get("license", "").startswith("Public domain")
                and len(figure.get("sourceSha256", [])) == 1
                and figure.get("taxon") == "Rhizoprionodon acutus (Rüppell, 1837)"
                and figure.get("historicLessonName") == "Scoliodon sorrakowah"
                and figure.get("historicalPlateFigure") == "Plate XVIII, Figure 4 only"
                and "five pairs of gill slits" in figure.get("keyEn", "")
                and "NOT Scoliodon laticaudus" in figure.get("keyEn", "")
                and "Figure 4" in figure.get("modifications", "")
                and figure.get("visualReview") == "REPLACED_VISUAL_QA_PENDING"
                and not figure.get("svgMaster"),
                "milk-shark figure: wrong species, original scan, fig. 4 crop or rights"
            )
        if figure["diagramId"] == "u1-vertebrata-characters-vertebrate-anatomy":
            require(
                figure["lang"] == "en"
                and figure.get("author") == "Chiswick Chap (vertebrate body plan); Uwe Gille (teleost organs); CHORDATA QA (layout)"
                and figure.get("sourceUrls") == [
                    "https://commons.wikimedia.org/wiki/File:Vertebrate_body_plan.svg",
                    "https://commons.wikimedia.org/wiki/File:Fish-anatomy.svg"
                ]
                and figure.get("license") == "CC BY-SA 4.0 — composite derivative, both original artists credited"
                and figure.get("licenseUrl") == "https://creativecommons.org/licenses/by-sa/4.0/"
                and len(figure.get("sourceSha256", [])) == 2
                and len(figure.get("originalLicences", [])) == 2
                and "NOT universal" in figure.get("keyEn", "")
                and figure.get("visualReview") == "REPLACED_VISUAL_QA_PENDING"
                and not figure.get("svgMaster"),
                "Vertebrata organ panel source, attribution, licence or caveat missing"
            )
        if figure["diagramId"] in pencil_ids:
            if (figure["diagramId"] == "u1-cephalochordata-branchiostoma-labelled"
                    and figure["lang"] == "en" and figure.get("sourceUrl")):
                require(figure["author"] == "Hans Hillewaert — original 32-label Branchiostoma lanceolatum drawing"
                        and figure.get("sourceUrl") == "https://commons.wikimedia.org/wiki/File:Branchiostoma_anatomy.jpg"
                        and figure.get("license") == "CC BY-SA 4.0 (drawing and PNG adaptation)"
                        and figure.get("licenseUrl") == "https://creativecommons.org/licenses/by-sa/4.0/"
                        and len(figure.get("sourceSha256", [])) == 1
                        and figure.get("modifications"),
                        "Branchiostoma original credit / ShareAlike / JPEG-to-PNG modification missing")
                require(all(str(i) in figure.get("keyEn", "") for i in range(1, 33)),
                        "Branchiostoma 32-part external anatomy key missing")
            elif (figure["diagramId"] in ("u5-columba-endoskeleton", "u5-rabbit-endoskeleton")
                    and figure["lang"] == "en" and figure.get("sourceUrl")):
                require(figure["author"] != "AI-generated original (ChatGPT ImageGen)",
                        "historical skeleton still incorrectly labelled ImageGen: " + name)
            elif (figure["diagramId"] == "u5-flight-adaptations-avian-lung"
                  and figure["lang"] == "en" and figure.get("sourceUrl")):
                require(
                    figure["author"].startswith("L. Shyamal (2007")
                    and figure.get("sourceUrl") == "https://commons.wikimedia.org/wiki/File:BirdRespiration.svg"
                    and figure.get("license", "").startswith("Public domain")
                    and len(figure.get("sourceSha256", [])) == 1
                    and "2400" in figure.get("modifications", "")
                    and figure.get("licenseUrl") == "https://creativecommons.org/publicdomain/mark/1.0/",
                    "source-credited avian air-sac illustration lacks correct rights/metadata"
                )
            else:
                require(figure["author"] == "AI-generated original (ChatGPT ImageGen)",
                        "original ImageGen plate creator attribution changed: " + name)
        if figure.get("referenceUrls"):
            require(all(u.startswith("https://") for u in figure["referenceUrls"]),
                    "bad anatomical reference URL: " + name)
    print(f"PASS: {len(pencil_names)} PNG files verified across {len(filled_ids)}/64 lesson slots")
    print("PASS: original bilingual variants retained; new English-labelled variants shared across reading languages")
    print("PASS: 64/64 figure slots have unique exact lesson-page assignments")
    print("PASS: 7/7 legacy PNG assets correctly placed, PNG/hash checked (3 original QA + 4 credited sources)")
    print(f"PENDING: 0/64 academically approved; {64-len(filled_ids)} pencil slots unfilled")
    unit_counts = Counter(s["topicId"].split("-")[0] for s in slots)
    print("PASS: overview contains no figure slot; bilingual captions exist for all slots")
    print("BY UNIT:", dict(sorted(unit_counts.items())))


if __name__ == "__main__":
    main()
