#!/usr/bin/env python3
"""Replace museum photographs with historically published anatomy drawings.

The two drawings are public-domain source references, NOT independently reviewed
modern textbook plates. Source page, artist/author, processing and SHA-256 are
preserved for each. Only stage into an isolated QA branch.
"""
from __future__ import annotations
import hashlib, io, json, pathlib, time, urllib.parse, urllib.request
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

ROOT=pathlib.Path(__file__).resolve().parents[1]
ASSETS=ROOT/"app/src/main/assets"
FIGS=ASSETS/"figures"
SOURCES=[
    {
      "id":"commons-pigeon-skeleton",
      "referenceId":"pigeon-skeleton",
      "originalFilename":"Abbildungen von Vogel-Skeletten (Tafel XC) (6981817141).jpg",
      "originalArtist":"Adolf Bernhard Meyer",
      "originalWork":"Abbildungen von Vogel-Skeletten, plate XC (1879–1888), Columba livia",
      "license":"Public domain — historical 19th-century illustration",
      "sourcePageUrl":"https://commons.wikimedia.org/wiki/File:Abbildungen_von_Vogel-Skeletten_(Tafel_XC)_(6981817141).jpg",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "filename":"pigeon_endoskeleton_line_art.png",
      "oldFile":"pigeon_skeleton.png",
      "captionEn":"Columba livia endoskeleton: historical anatomical line drawing (scientific labelling review pending)",
      "captionTa":"கொலும்பா லிவியாவின் உள் எலும்புக்கூடு: வரலாற்று உடற்கூறியல் கோட்டோவியம் (பெயரிடல் சரிபார்ப்பு நிலுவை)"
    },
    {
      "id":"commons-rabbit-skeleton",
      "referenceId":"rabbit-skeleton",
      "originalFilename":"SqueletteLapinChauveau1990.JPG",
      "originalArtist":"Auguste Chauveau and Saturnin Arloing (1890); Commons digitisation credited to Meyer C.",
      "originalWork":"Traité d'anatomie comparée des animaux domestiques, 1890 — Oryctolagus cuniculus",
      "license":"Public domain — historical 1890 illustration",
      "sourcePageUrl":"https://commons.wikimedia.org/wiki/File:SqueletteLapinChauveau1990.JPG",
      "licenseUrl":"https://creativecommons.org/publicdomain/mark/1.0/",
      "filename":"rabbit_endoskeleton_line_art.png",
      "oldFile":"rabbit_skeleton.png",
      "captionEn":"Oryctolagus cuniculus endoskeleton: historical anatomical line drawing (scientific labelling review pending)",
      "captionTa":"ஓரிக்டோலாகஸ் குனிகுலஸ் முயலின் உள் எலும்புக்கூடு: வரலாற்று உடற்கூறியல் கோட்டோவியம் (பெயரிடல் சரிபார்ப்பு நிலுவை)"
    }
]

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def write_json(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def url_for(name):
    from urllib.parse import quote
    safe=name.replace(" ","_")
    digest=hashlib.md5(safe.encode("utf-8")).hexdigest()
    return ("https://upload.wikimedia.org/wikipedia/commons/"
            +digest[0]+"/"+digest[:2]+"/"+quote(safe,safe="()_-.,"))
def fetch(source):
    name=source["originalFilename"]
    urls=[url_for(name),"https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(name.replace(" ","_"))]
    errors=[]
    for url in urls:
        for attempt in range(3):
            try:
                req=urllib.request.Request(url,headers={
                    "User-Agent":"ChordataZoologyEducationalResearch/0.2 (https://github.com/rameshgascngl-create/Chordata)",
                    "Accept":"image/jpeg,image/png"})
                with urllib.request.urlopen(req,timeout=35) as response:
                    if urllib.parse.urlsplit(response.geturl()).hostname not in ("upload.wikimedia.org","commons.wikimedia.org"):
                        raise RuntimeError("Unexpected redirect host")
                    data=response.read(8_000_001)
                if len(data)<30000 or len(data)>8_000_000 or data[:3]!=b"\xff\xd8\xff":
                    raise ValueError("Unexpected file type/size")
                with Image.open(io.BytesIO(data)) as im:
                    im.verify()
                with Image.open(io.BytesIO(data)) as im:
                    width,height=im.size
                if width<1000 or height<500: raise ValueError("Insufficient source resolution")
                return url,data,(width,height)
            except Exception as err:
                errors.append(f"{type(err).__name__}: {err}")
                time.sleep(2+3*attempt)
    raise RuntimeError("Could not access public-domain illustration "+name+"; "+str(errors[-4:]))

def make_plate(original):
    with Image.open(io.BytesIO(original)) as im:
        im=ImageOps.exif_transpose(im).convert("L")
        orig=im.size
        # Keep the intact skeletal drawing, including any diagnostic bones.
        # Improve faded paper contrast; retain printed Latin names for provenance.
        im=ImageOps.autocontrast(im,cutoff=0.8)
        im=ImageEnhance.Contrast(im).enhance(1.28)
        im=im.filter(ImageFilter.UnsharpMask(radius=1.1,percent=120,threshold=4))
        if im.width<1500:
            im=im.resize((1600,round(im.height*1600/im.width)),Image.Resampling.LANCZOS)
        if im.width>2200:
            im.thumbnail((2200,2400),Image.Resampling.LANCZOS)
        buff=io.BytesIO()
        im.convert("RGB").save(buff,"PNG",optimize=True)
        return buff.getvalue(),orig,im.size

def main():
    manifest=read_json(ASSETS/"figures.json")
    credits=read_json(ASSETS/"source_reference_credits.json")
    hashes=read_json(FIGS/"source-hashes.json")
    assert len(manifest)==7 and len(hashes)==7
    assert set(x["id"] for x in manifest)==set(x["id"] for x in hashes)
    figmap={x["id"]:x for x in manifest}
    hashmap={x["id"]:x for x in hashes}
    creditmap={x["id"]:x for x in credits["sources"]}
    for source in SOURCES:
        fig=figmap[source["id"]]
        credit=creditmap[source["referenceId"]]
        assert fig["file"]==source["oldFile"]
        assert fig["topicId"] in ("u5-columba","u5-rabbit") and fig["page"]==2
        assert FIGS.joinpath(source["oldFile"]).exists()
        realurl,original,original_size=fetch(source)
        plate,orig,newsize=make_plate(original)
        path=FIGS/source["filename"]
        path.write_bytes(plate)
        assert plate.startswith(bytes.fromhex("89504e470d0a1a0a")) and len(plate)>20000
        print("STAGED",source["id"],"download",realurl,"original",orig,"png",newsize,"bytes",len(plate))
        # Exactly one replacement for each previous museum photograph.
        (FIGS/source["oldFile"]).unlink()
        fig.update(file=source["filename"],author=source["originalArtist"],
             license=source["license"],licenseUrl=source["licenseUrl"],sourceUrl=source["sourcePageUrl"],
             captionEn=source["captionEn"],captionTa=source["captionTa"],
             modifications="Historical public-domain line engraving converted to greyscale PNG; faded-paper contrast adjusted; scaled for mobile readability",
             originalFilename=source["originalFilename"],origin="Wikimedia Commons",
             reviewStatus="REFERENCE_SOURCE_AWAITING_ACADEMIC_REVIEW")
        digest=hashlib.sha256(plate).hexdigest()
        hashmap[source["id"]].update(file=source["filename"],size=len(plate),sha256=digest,
                                     status="HISTORICAL_LINE_DRAWING_AWAITING_ANATOMICAL_REVIEW")
        credit.update(sourcePageUrl=source["sourcePageUrl"],
            originalFilename=source["originalFilename"],
            creator=source["originalArtist"],license=source["license"],
            licenseUrl=source["licenseUrl"],originalUrl=realurl,
            originalWidth=orig[0],originalHeight=orig[1],
            width=newsize[0],height=newsize[1],sha256=digest,
            modifications=fig["modifications"],bytes=len(plate),
            suitability="HISTORICAL_ANATOMICAL_LINE_DRAWING",
            academicNotes=source["originalWork"]+"; labels and modern anatomical interpretation still awaiting independent Zoology/Tamil review.",
            reviewStatus="SOURCE_ONLY_AWAITING_INDEPENDENT_ANATOMICAL_REVIEW")
    # Reconcile every imported reference image with its actual embedded filename.
    # The previous manifest incorrectly retained old museum photo paths.
    for entry in credits["sources"]:
        matching=next(x for x in manifest if x["id"]=="commons-"+entry["id"])
        entry.update(localFile=matching["file"],sourcePageUrl=matching["sourceUrl"],
                     creator=matching["author"],license=matching["license"],
                     licenseUrl=matching["licenseUrl"],modifications=matching["modifications"],
                     sourceStatus="STAGED_OFFLINE_QA",embeddedInApk=True,
                     academicStatus="PENDING",
                     reviewStatus="SOURCE_ONLY_AWAITING_INDEPENDENT_ANATOMICAL_REVIEW")
        write_json(ASSETS/"figures.json",manifest)
    write_json(FIGS/"source-hashes.json",[hashmap[x["id"]] for x in manifest])
    write_json(ASSETS/"source_reference_credits.json",credits)
    images={p.name for p in FIGS.glob("*.png")}
    expected={x["file"] for x in manifest}
    assert images==expected,("wrong images",images.symmetric_difference(expected))
    assert "pigeon_skeleton.png" not in images and "rabbit_skeleton.png" not in images
    print("PASS: removed both museum photographs, added two original historical line drawings; retained all seven QA image slots")
if __name__=="__main__":main()
