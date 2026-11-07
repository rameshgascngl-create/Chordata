#!/usr/bin/env python3
"""Read authentic Project Gutenberg fig. 43 image, report dimensions and source."""
from urllib.request import Request,urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import hashlib
from pathlib import Path
URL="https://www.gutenberg.org/cache/epub/72060/pg72060-images.html"
request=Request(URL,headers={"User-Agent":"Mozilla/5.0 (educational Zoology source audit)"})
raw=urlopen(request,timeout=60).read()
soup=BeautifulSoup(raw,"html.parser")
hit=None
for item in soup.find_all(["figure","div"]):
  fig_text=item.get_text(" ",strip=True)
  if "Fig. 43." in fig_text and "Brain of Carcharias" in fig_text and len(fig_text)<2000:
    if item.find("img"):
      hit=item
      break
if hit is None:
  # Gutenberg often uses adjacent <div class=figcenter> and a <p> caption.
  matches=soup.find_all(string=lambda s: s and "Brain of Carcharias" in s)
  for match in matches:
    prev=match.parent.find_previous("img")
    if prev:
      hit=prev
      break
if hit is None:raise ValueError("Authentic Fig. 43 image not located")
imgtag=hit if getattr(hit,'name',None)=="img" else hit.find("img")
file_url=urljoin(URL,imgtag["src"])
buf=urlopen(Request(file_url,headers={"User-Agent":"Mozilla/5.0"}),timeout=60).read()
img=Image.open(BytesIO(buf));img.load()
print("SOURCE",URL,"\nFIGURE_IMAGE",file_url,"\nIMAGE_FORMAT",img.format,
      "\nIMAGE_DIMENSIONS",img.size,"\nBYTES",len(buf),
      "\nSHA256",hashlib.sha256(buf).hexdigest())
Path("candidate_fig43_original."+img.format.lower()).write_bytes(buf)
if img.width<1200:
  print("ACADEMIC QUALITY WARNING: authentic source width < 1200; do not silently enlarge or approve.")
