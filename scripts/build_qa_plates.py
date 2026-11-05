#!/usr/bin/env python3
"""Build reproducible offline, provisional zoology line plates.

These are structural QA drawings to demonstrate figure placement and zoom, NOT
reviewed specimen illustrations or labelled internal anatomical diagrams.
They are deliberately made without network requests.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
PLATES = ASSETS / "figures"
WIDTH, HEIGHT = 1600, 900
INK = (38, 45, 49)
HATCH = (120, 127, 132)
BODY = (230, 234, 234)

def canvas():
    img = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    return img, ImageDraw.Draw(img)

def line(draw, pts, width=5, fill=INK):
    draw.line(pts, fill=fill, width=width, joint="curve")

def shark():
    img, d = canvas()
    # Planar outline: leftward head, 5 gill slits, 2 dorsal fins,
    # pectoral, pelvic and anal fins, unequal caudal lobes.
    # No spiracle is depicted (not characteristic of Scoliodon).
    body = [
        (82,449),(146,415),(270,387),(405,366),(528,347),
        (605,349),(655,270),(714,154),(723,350),
        (856,354),(1035,375),(1100,334),(1130,358),(1134,393),
        (1280,402),(1545,155),(1456,448),(1545,678),
        (1295,492),(1220,477),(1134,482),(1111,528),
        (1089,486),(996,493),(970,551),(937,491),
        (744,516),(600,530),(533,687),(486,523),
        (405,522),(300,510),(178,488),(98,458)
    ]
    d.polygon(body, fill=BODY)
    line(d, body + [body[0]], width=8)
    # The large triangular fin is a pectoral fin; a posterior small fin is pelvic.
    d.polygon([(440,488),(551,690),(600,518)], fill=(207,213,215))
    line(d, [(440,488),(551,690),(600,518)], width=7)
    d.polygon([(937,483),(979,556),(1001,482)], fill=(207,213,215))
    line(d, [(937,483),(979,556),(1001,482)], width=6)
    # Eye and nostril on the rostral portion.
    d.ellipse((253,422,285,449), fill=INK)
    d.ellipse((260,427,270,437), fill=(246,249,248))
    d.arc((119,427,167,472), 190, 330, fill=INK, width=4)
    line(d, [(93,459),(160,470),(222,464)], width=4)
    # Five separate branchial slits in front of pectoral girdle.
    for i in range(5):
        x = 349 + 27 * i
        d.arc((x,399,x+24,500), 260, 78, fill=INK, width=5)
    # Posterior gill slits become shorter.
    for i in range(70):
        x=590+i*6
        y=390+int(17*(i/70))
        if i % 4 == 0:
            line(d,[(x,y),(x+17,y-8)],width=2,fill=HATCH)
    # Short hatch pattern along dorsal lobe and under the first dorsal.
    for k in range(24):
        x=656+k*3
        line(d,[(x,334-k*3),(x+12,347-k*3)],width=2,fill=HATCH)
    return img

def pigeon():
    img, d = canvas()
    # Lateral morphology: beak/cere, head, neck, folded wing,
    # tail, paired legs and anisodactyl toes.
    tail=[(1025,476),(1505,577),(1500,628),(1015,573)]
    d.polygon(tail,fill=(211,216,219))
    line(d,tail+[tail[0]],width=8)
    d.ellipse((454,328,1185,640),fill=BODY,outline=INK,width=8)
    neck=[(478,448),(455,289),(500,235),(566,285),(648,374),(705,506)]
    d.polygon(neck,fill=BODY)
    line(d,[(478,448),(455,289),(500,235),(566,285),(648,374)],width=8)
    d.ellipse((377,193,565,351),fill=BODY,outline=INK,width=8)
    beak=[(383,263),(277,293),(382,310)]
    d.polygon(beak,fill=(218,219,214),outline=INK,width=5)
    d.ellipse((385,261,408,283),fill=(238,239,236),outline=INK,width=3)
    d.ellipse((435,241,463,270),fill=INK)
    d.ellipse((443,247,452,256),fill=(249,249,249))
    # One externally visible folded wing, scalloped primary coverts.
    d.ellipse((620,360,1120,569),fill=(223,227,228),outline=INK,width=7)
    for k in range(8):
        x=675+k*48
        d.arc((x,380,x+135,550),0,158,fill=HATCH,width=3)
    for k in range(7):
        x=980+k*40
        line(d,[(x,530),(x+95,591)],width=3,fill=HATCH)
    # Stout legs, scaled tarsi and three forward toes plus backward hallux.
    for x in (643,804):
        line(d,[(x,594),(x-22,746)],width=12)
        for sy in range(621,739,19):
            line(d,[(x-11,sy),(x+9,sy+5)],width=2,fill=HATCH)
        for dx in (-79,-25,41):
            line(d,[(x-22,745),(x+dx,769)],width=8)
            line(d,[(x+dx,769),(x+dx-10,780)],width=4)
        line(d,[(x-22,749),(x+20,708)],width=8)
    # Repeated crosshatch, not extra anatomical labels.
    for k in range(20):
        x=534+k*9
        line(d,[(x,388),(x+16,408)],width=2,fill=HATCH)
    return img

def rabbit():
    img, d=canvas()
    # Large pinnae, lateral eyes, vibrissae, compact scut and
    # prominent hind limbs. No internal anatomy implied.
    d.ellipse((408,360,1276,711),fill=BODY,outline=INK,width=8)
    d.ellipse((320,336,592,565),fill=BODY,outline=INK,width=7)
    ear1=[(401,363),(359,103),(382,57),(428,84),(478,342)]
    ear2=[(465,348),(502,117),(549,78),(573,132),(542,368)]
    for ear in (ear1,ear2):
        d.polygon(ear,fill=(228,230,230))
        line(d,ear+[ear[0]],width=7)
    line(d,[(395,321),(389,145),(415,107),(456,327)],width=3,fill=HATCH)
    line(d,[(487,322),(522,151),(538,126),(537,322)],width=3,fill=HATCH)
    d.ellipse((370,416,409,453),fill=INK)
    d.ellipse((381,424,391,435),fill=(250,250,250))
    d.ellipse((316,500,342,518),fill=(174,176,176),outline=INK,width=3)
    d.ellipse((1251,503,1367,611),fill=(248,249,249),outline=INK,width=7)
    # Massive hind thigh and elongated hind feet.
    d.ellipse((956,532,1212,755),fill=(217,222,222),outline=INK,width=7)
    d.ellipse((1000,730,1270,800),fill=(231,234,234),outline=INK,width=6)
    d.ellipse((566,636,753,776),fill=(219,223,223),outline=INK,width=6)
    d.ellipse((548,756,794,804),fill=(231,234,234),outline=INK,width=5)
    for y in (480,494,508):
        line(d,[(320,y),(180,y-54)],width=2,fill=HATCH)
        line(d,[(326,y),(182,y+38)],width=2,fill=HATCH)
    # Sparse fine hatch for fur texture, reproducible.
    rng=random.Random(20261105)
    for _ in range(1200):
        x=rng.randint(580,1180); y=rng.randint(389,672)
        # Ellipse test keeps hatching within trunk.
        if ((x-842)/420)**2 + ((y-535)/166)**2 < 0.86:
            line(d,[(x,y),(x+9,y+4)],width=1,fill=HATCH)
    return img

def main():
    records=json.loads((ASSETS/"figures.json").read_text(encoding="utf-8"))
    builders={"scoliodon-external":shark,"columba-external":pigeon,"rabbit-external":rabbit}
    if set(r["id"] for r in records)!=set(builders):
        raise SystemExit("Figure registry does not match offline QA generator")
    PLATES.mkdir(parents=True,exist_ok=True)
    hashes=[]
    for rec in records:
        if not rec["license"].startswith("Provisional QA artwork"):
            raise SystemExit("Refusing to misattribute original QA illustration")
        img=builders[rec["id"]]()
        img.save(PLATES/rec["file"],format="PNG",optimize=True)
        raw=(PLATES/rec["file"]).read_bytes()
        if not raw.startswith(bytes.fromhex("89504e470d0a1a0a")) or len(raw)<10000:
            raise SystemExit("Invalid PNG: "+rec["file"])
        hashes.append({"id":rec["id"],"file":rec["file"],"size":len(raw),
            "sha256":hashlib.sha256(raw).hexdigest(),"status":"PROVISIONAL"})
        print("QA_PNG",rec["id"],len(raw))
    (PLATES/"source-hashes.json").write_text(json.dumps(hashes,indent=2)+"\n",encoding="utf-8")
    print("PASS: exactly three original provisional offline PNGs; no network calls")

if __name__=="__main__":
    main()
