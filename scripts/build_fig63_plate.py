#!/usr/bin/env python3
"""Deterministic one-time Figure 63 PNG correction.

Retains original tooth-count grid; adds correctly ordered upper rabbit incisor
inset and human/rabbit permanent formulae. New source hash voids old QA approval.
"""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'app/src/main/assets/pencil_plates'
PNG=BASE/'human_rabbit_dental_formula.png'
MANIFEST=BASE/'manifest.json'
OLD='9f513dc0c910dfe81febd3bb5e02ebfece5f5e5afcb9109ebfbc20cc8748508f'

def font(size,bold=False):
    return ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',size)

def main():
    raw=PNG.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    fig=next(f for f in manifest['figures'] if f['diagramId']=='u5-dentition-human-rabbit-dental-formula')
    assert fig['lang']=='shared'
    if sha != OLD:
        if sha==fig['sha256'] and fig.get('retiredQaAcceptedSha256')==OLD:
            print('PASS: corrected Fig 63 already installed');return
        raise SystemExit('Refusing unknown source image; sha256='+sha)
    img=Image.open(PNG).convert('RGB')
    assert img.size==(1448,780)
    plate=Image.new('RGB',(2200,1060),'#fcfbf7');d=ImageDraw.Draw(plate)
    ink='#213746';accent='#0a6e8a';muted='#3e5866';line='#a4b3ba'
    d.rounded_rectangle([28,22,2170,125],24,fill='#e4f0f1',outline=ink,width=4)
    d.text((62,52),'PERMANENT DENTAL FORMULAE — HUMAN AND RABBIT',font=font(43,True),fill=ink)
    plate.paste(img,(26,170)) # Original symbolic tooth counts are not redrawn.
    d.text((210,172),'1  Adult human | 32 teeth',font=font(32,True),fill=ink)
    d.text((210,585),'2  European rabbit | 28 teeth',font=font(32,True),fill=ink)
    d.rounded_rectangle([1510,152,2165,1020],20,fill='white',outline='#708e9b',width=3)
    d.text((1540,176),'FORMULAE (one side per jaw)',font=font(26,True),fill=accent)
    d.text((1540,220),'Human  I 2/2  C 1/1  PM 2/2  M 3/3',font=font(22,True),fill=ink)
    d.text((1540,253),'(8 upper + 8 lower) × 2 = 32',font=font(23,True),fill=ink)
    d.line([(1535,297),(2140,297)],fill=line,width=3)
    d.text((1540,318),'Rabbit   I 2/1  C 0/0  PM 3/2  M 3/3',font=font(22,True),fill=ink)
    d.text((1540,351),'(8 upper + 6 lower) × 2 = 28',font=font(23,True),fill=ink)
    d.text((1540,399),'COUNT GRID: not actual tooth positions',font=font(21,True),fill='#8f3b2f')
    d.line([(1535,444),(2140,444)],fill=line,width=3)
    d.text((1540,460),'RABBIT UPPER INCISORS',font=font(28,True),fill=accent)
    d.text((1542,500),'Simplified lateral arrangement (not to scale)',font=font(21),fill=muted)
    d.text((1540,547),'ANTERIOR',font=font(18,True),fill=muted)
    d.text((1975,547),'POSTERIOR',font=font(18,True),fill=muted)
    d.line([(1535,588),(2134,588)],fill='#d4bf89',width=30)
    d.line([(1542,588),(2130,588)],fill='#826c46',width=3)
    # Two upper incisors IN ONE QUADRANT: I1 anterior, smaller I2 posterior.
    d.rounded_rectangle([1560,588,1624,750],radius=23,fill='#f7e6b2',outline=ink,width=5)
    d.rounded_rectangle([1639,591,1666,655],radius=12,fill='#f4d6a3',outline=ink,width=4)
    for x in range(1703,1868,28):
        d.line([(x,653),(x+15,653)],fill='#b3c0c5',width=2)
    for i in range(6):
        x=1870+i*43
        d.rounded_rectangle([x,590,x+36,659],radius=8,
            fill='#b7d3c9' if i<3 else '#b5c9db',outline=ink,width=3)
    d.text((1535,777),'I1: large front upper incisor',font=font(22,True),fill=ink)
    d.text((1535,812),'I2: small peg tooth BEHIND I1',font=font(22,True),fill='#8f3b2f')
    d.text((1535,849),'Gap: diastema (canines absent)',font=font(22),fill=ink)
    d.text((1535,890),'Cheek teeth: 3 PM + 3 M (upper half)',font=font(20),fill=ink)
    d.text((1535,942),'Lagomorpha: 2 upper incisor pairs in total',font=font(20),fill=muted)
    d.line([(50,1018),(1460,1018)],fill='#b5c1c7',width=3)
    d.text((55,1025),'Counts are symbolic. The anatomical inset distinguishes the peg tooth position.',
           font=font(19),fill=muted)
    # Preserve previous review-approved (old hash only) image as an archived original.
    archive=ROOT/'docs/figures/retired_fig63_20261120.png'
    archive.parent.mkdir(parents=True,exist_ok=True)
    assert not archive.exists() or hashlib.sha256(archive.read_bytes()).hexdigest()==OLD
    if not archive.exists():shutil.copyfile(PNG,archive)
    tmp=PNG.with_suffix('.candidate.png')
    plate.save(tmp,format='PNG',optimize=True)
    assert Image.open(tmp).size==(2200,1060)
    assert Image.open(tmp).getpixel((2000,1000)) is not None
    tmp.replace(PNG)
    fig['size']=PNG.stat().st_size
    fig['sha256']=hashlib.sha256(PNG.read_bytes()).hexdigest()
    fig['retiredQaAcceptedSha256']=OLD
    fig['modifications']='Count symbols preserved. Added separately labelled schematic upper rabbit I1/I2 lateral inset, correct peg-tooth posterior relation, diastema and bilateral adult tooth-count formulae; original owner-approved hash archived.'
    fig['visualReview']='RECTIFIED_PEG_TOOTH_INSET_CANDIDATE_PENDING_INDEPENDENT_BIOLOGY_TAMIL_AND_DEVICE_REVIEW'
    fig['ownerQaAcceptedSha256']=''
    fig.pop('ownerQaDisplayDecision',None)
    fig['ownerQaDisplayScope']='Old acceptance applied only to retired exact hash; corrected figure requires new owner QA review and independent academic sign-off.'
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('CORRECTED Fig63',fig['sha256'],'bytes',fig['size'])
if __name__=='__main__':main()
