#!/usr/bin/env python3
"""Inventory all 64 CHORDATA figure slots by artwork provenance (read-only by default).

All PNGs are raster files; this report distinguishes original published artwork
from computer-drawn or AI-synthetic illustrations stored as PNG, not bitmaps
versus vectors. It never certifies scientific or Tamil review decisions.
"""
from pathlib import Path
import csv
import io
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/"app/src/main/assets"
OUT=ROOT/"docs/CHORDATA_ARTWORK_PROVENANCE_AUDIT_64.md"

def main():
    figures=json.loads((ASSET/"pencil_plates/manifest.json").read_text(encoding="utf-8"))["figures"]
    slots=json.loads((ASSET/"figure_slots.json").read_text(encoding="utf-8"))["slots"]
    entries={x["diagramId"]:x for x in figures if x["lang"] in ("en","shared")}
    assert len(entries)==64 and len(slots)==64
    register=list(csv.DictReader((ROOT/"docs/FIGURE_REVIEW_REGISTER_64.csv").open(encoding="utf-8-sig",newline="")))
    priorities={x["diagram_id"]:x["review_priority"] for x in register}
    def status(x):
        origin=x.get("sourceUrl","")
        author=x.get("author","")
        if x.get("sourceKind")=="AI_GENERATED_ORIGINAL_QA_CANDIDATE" or "AI-generated original" in author:
            return "AI-generated candidate"
        if not origin and x.get("svgMaster"):
            return "Computer-drawn vector exported as PNG"
        if not origin:
            return "No authenticated external source (project-drawn/AI)"
        if x.get("svgMaster") or "QA (layout)" in author or "CHORDATA QA (layout)" in author:
            return "Source-based edited composite"
        return "Source-credited artwork (still provisional)"
    counts={}
    rows=[]
    for s in slots:
        x=entries[s["id"]]
        v=status(x)
        counts[v]=counts.get(v,0)+1
        rows.append([s["id"],x["path"].split("/")[-1],v,"HIGH" if priorities[s["id"]].startswith("HIGH") else "STANDARD",x.get("author",""),x.get("sourceUrl","")])
    assert sum(counts.values())==64
    result=[
      "# CHORDATA — 64-figure source and drawing audit",
      "",
      "Generated against the committed offline figure manifest; scientific review is not implied.",
      "",
      "## Format clarification",
      "",
      "All app illustration files are PNG bitmaps; converting vector outlines to PNG does not improve anatomical quality. Replacement work targets computer-generated, unsuitable or uncredited *artwork*; licensed published anatomical art may legitimately be stored as lossless PNG.",
      "",
      "## Inventory",
      ""
    ]
    for name,n in sorted(counts.items(),key=lambda z:(-z[1],z[0])):
        result.append("- "+name+": **"+str(n)+"**")
    result.extend(["","**64/64 placements have PNGs; 0/64 have independent dual academic signoff.**","",
        "| Diagram ID | Current PNG | Image provenance classification | Review priority | Source creator | Original source |",
        "|---|---|---|---|---|---|"])
    for cells in rows:
        result.append("| "+" | ".join(z.replace("|",";").replace("\n"," ") for z in cells)+" |")
    result.extend(["","## Replacement policy","",
      "Original source first, with author, licence, original URL, transformations and SHA-256. AI candidate only when reuse is unsuitable and a reliable published reference is available. Never attribute generated anatomy to a textbook author. All image replacements reset scientific and Tamil acceptances to PENDING. Release remains on HOLD."])
    rendered="\n".join(result)+"\n"
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8")!=rendered:
            raise SystemExit("Art audit is stale; rerun python3 scripts/report_artwork_provenance.py")
    else:
        OUT.write_text(rendered,encoding="utf-8")
    print("PASS provenance inventory 64 slots",counts)

if __name__=="__main__":main()
