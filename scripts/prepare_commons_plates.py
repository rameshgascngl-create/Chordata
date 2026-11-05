#!/usr/bin/env python3
"""Make source-attributed offline PNG reference plates on the CI runner.

Artwork sources are public-domain historical illustrations listed in figures.json.
Do not confuse these references with the pending 64 labelled anatomy plates.
No network is required when the completed APK runs.
"""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import time

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app/src/main/assets"
REGISTRY = ASSETS / "figures.json"
DEST = ASSETS / "figures"
MAX_BYTES = 12 * 1024 * 1024

def main() -> None:
    rows = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert len(rows) == 3 and len({r["id"] for r in rows}) == 3
    DEST.mkdir(parents=True, exist_ok=True)
    verified = []
    for record in rows:
        assert record["license"] == "Public domain", record["id"]
        assert record["sourceUrl"].startswith("https://commons.wikimedia.org/wiki/File:")
        name = record["commonsFile"]
        normalized = name.replace(" ", "_")
        digest = hashlib.md5(normalized.encode("utf-8")).hexdigest()
        direct = "https://upload.wikimedia.org/wikipedia/commons/" + digest[0] + "/" + digest[:2] + "/" + quote(normalized, safe="")
        redirect = "https://commons.wikimedia.org/wiki/Special:Redirect/file/" + quote(name, safe="")
        data = None
        last_error = None
        for attempt in range(6):
            url = direct if attempt % 2 == 0 else redirect
            request = Request(url, headers={
                "User-Agent": "ChordataQA/0.2 (academic teaching; public-domain reference)",
                "Accept": "image/png,image/jpeg,image/*"
            })
            try:
                with urlopen(request, timeout=60) as response:
                    data = response.read(MAX_BYTES + 1)
                break
            except HTTPError as exc:
                last_error = exc
                if exc.code not in (429, 500, 502, 503, 504):
                    raise
                time.sleep(4 * (attempt + 1))
        if data is None:
            raise RuntimeError("Source image fetch failed after six attempts: " + name) from last_error
        if not 1000 < len(data) <= MAX_BYTES:
            raise RuntimeError("Source image size invalid: " + name)
        image = Image.open(io.BytesIO(data))
        image = ImageOps.exif_transpose(image).convert("RGB")
        if image.width < 300 or image.height < 180:
            raise RuntimeError("Source image too small: " + name)
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        output = DEST / record["file"]
        image.save(output, format="PNG", optimize=True)
        raw = output.read_bytes()
        if not raw.startswith(bytes.fromhex("89504e470d0a1a0a")):
            raise RuntimeError("PNG signature missing: " + name)
        verified.append({"id":record["id"],"file":record["file"],
                         "sha256":hashlib.sha256(raw).hexdigest(),
                         "bytes":len(raw),"sourceUrl":record["sourceUrl"],
                         "author":record["author"],"licence":record["license"]})
        print("PLATE_OK", record["id"], image.width, image.height, len(raw))
    (DEST / "source-hashes.json").write_text(json.dumps(verified,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("PASS: three attributed offline PNG plates; remaining labelled anatomy not claimed complete")

if __name__ == "__main__":
    main()
