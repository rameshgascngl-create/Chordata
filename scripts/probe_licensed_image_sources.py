#!/usr/bin/env python3
"""Download a small fixed allowlist of credited Wikimedia photographs for offline QA.
Probe only: never overwrite anatomical drawings and never call a photo an approved plate.
"""
from pathlib import Path
import hashlib
import json
import urllib.request
from PIL import Image
from io import BytesIO

root = Path(__file__).resolve().parents[1]
out = root/"build"/"licensed-figure-probe"
out.mkdir(parents=True,exist_ok=True)
examples = [
    {
        "name": "pigeon_skeleton",
        "file": "Pigeon_Skeleton.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Pigeon_Skeleton.jpg",
        "author": "Joshbressers",
        "licence": "CC0 1.0"
    },
    {
        "name": "rabbit_skeleton",
        "file": "Rabbit_skeleton_at_MAV-USP.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Rabbit_skeleton_at_MAV-USP.jpg",
        "author": "Museum of Veterinary Anatomy FMVZ USP / Wagner Souza e Silva",
        "licence": "CC BY-SA 4.0"
    }
]
evidence=[]
for x in examples:
    req=urllib.request.Request(x["url"],headers={"User-Agent":"ChordataEducationalQA/0.1 (educational offline assets; contact via repository issues)", "Accept":"image/jpeg"})
    with urllib.request.urlopen(req,timeout=45) as response:
        if response.status!=200: raise RuntimeError("HTTP error")
        data=response.read(7*1024*1024+1)
    if len(data)>7*1024*1024 or not data.startswith(b"\xff\xd8\xff"):
        raise RuntimeError("Invalid JPEG or oversized source: "+x["file"])
    im=Image.open(BytesIO(data))
    im.verify()
    im=Image.open(BytesIO(data))
    if im.width<900 or im.height<600: raise RuntimeError("Source too small")
    row={"name":x["name"],"author":x["author"],"licence":x["licence"],"original_url":x["url"],
         "width":im.width,"height":im.height,"size":len(data),"sha256":hashlib.sha256(data).hexdigest(),
         "status":"SOURCE_FETCH_VERIFIED_NOT_IN_APK"}
    evidence.append(row)
    print("FETCH_OK",row["name"],row["width"],row["height"],row["sha256"])
(out/"source-probe.json").write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("PASS: Wikimedia file retrieval with actual JPEG checksums; no APK image integration yet")
