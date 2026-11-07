#!/usr/bin/env python3
"""Inspect historic high-resolution source scan: Günther, Fishes (1880), Fig.43."""
from urllib.request import Request,urlopen
from pathlib import Path
import fitz,hashlib
URL="https://darwin-online.org.uk/converted/pdf/1880_G%C3%BCntherFishes_DlibD_A3025.pdf"
r=Request(URL,headers={"User-Agent":"Mozilla/5.0 (academic image preservation)"})
with urlopen(r,timeout=100) as response: raw=response.read(35_000_001)
if not raw.startswith(b"%PDF-"): raise ValueError("Original publication is not PDF")
doc=fitz.open(stream=raw,filetype="pdf")
print("PDF_SHA256",hashlib.sha256(raw).hexdigest(),"PAGES",len(doc))
hits=[]
for n in range(len(doc)):
 text=doc[n].get_text().lower()
 if "brain of carcharias" in text or ("fig. 43" in text and "carcharias" in text):
  hits.append(n)
print("CANDIDATE_PAGES",hits[:24])
if len(hits)!=1:raise ValueError("Cannot uniquely locate Fig. 43 by printed caption, do not guess")
page=doc[hits[0]]
print("SELECTED_INDEX_ZERO_BASED",hits[0],"PAGE_RECT",page.rect)
imgs=page.get_images(full=True)
print("EMBEDDED_IMAGES",[(a[0],a[2],a[3]) for a in imgs])
for a in imgs[:10]:
 obj=doc.extract_image(a[0])
 print("SOURCE_IMAGE",a[0],obj["width"],obj["height"],obj["ext"])
p=page.get_pixmap(matrix=fitz.Matrix(3,3),alpha=False)
p.save("original_gunther_fig43_fullpage.png")
print("RENDERED_SCAN",p.width,p.height)
