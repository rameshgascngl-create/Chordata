#!/usr/bin/env python3
"""Original, editable comparative-vertebrate dorsal brain QA schematics.

Educational region diagrams, not dissections. Source landmark references are
provided in manifest.json; no third-party artwork is embedded or traced.
Run only when revising the three identified provisional plates.
"""
from pathlib import Path
import hashlib, html, json
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'app/src/main/assets/pencil_plates/manifest.json'
PNG_DIR = MANIFEST.parent
SVG_DIR = ROOT / 'docs/original_plate_svg'
SVG_DIR.mkdir(exist_ok=True, parents=True)
INK='#273944'; LIGHT='#f0f4f1'; MID='#e0eae6'; PALE='#d2e0db'; ACCENT='#346b79'; GREY='#627780'

class Drawing:
    def __init__(self,title,subtitle,foot):
        self.body=[]
        self.title=title;self.subtitle=subtitle;self.foot=foot
    def path(self,d,fill=LIGHT,sw=4):
        self.body.append(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    def line(self,x1,y1,x2,y2,stroke=INK,sw=3,dash=None):
        self.body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+' stroke-linecap="round"/>')
    def ellipse(self,x,y,rx,ry,fill=LIGHT,sw=4):
        self.body.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>')
    def dot(self,x,y):
        self.body.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{ACCENT}"/>')
    def text(self,x,y,t,size=26,bold=False,color=INK,anchor='start'):
        t=html.escape(t)
        self.body.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans, Arial, sans-serif" font-size="{size}"'+(' font-weight="bold"' if bold else '')+f' text-anchor="{anchor}">{t}</text>')
    def label(self,text,x,y,tx,ty,side='left'):
        self.text(x,y,text,25,True)
        start_x=x+485 if side=='left' else x-25
        bend_x=670 if side=='left' else 1220
        self.line(start_x,y-8,bend_x,y-8,ACCENT,2)
        self.line(bend_x,y-8,tx,ty,ACCENT,2)
        self.dot(tx,ty)
    def render(self):
        head=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1120" viewBox="0 0 1800 1120"><rect width="1800" height="1120" fill="white"/>
        <text x="70" y="85" font-family="DejaVu Sans" font-weight="bold" font-size="54" fill="{INK}">{html.escape(self.title)}</text>
        <text x="72" y="130" font-family="DejaVu Sans" font-size="27" fill="{GREY}">{html.escape(self.subtitle)}</text>
        <line x1="70" y1="154" x2="1728" y2="154" stroke="{ACCENT}" stroke-width="4"/>
        <path d="M900 192 L900 940" stroke="{PALE}" stroke-width="2" stroke-dasharray="10 8" fill="none"/>
        <text x="886" y="198" text-anchor="end" font-family="DejaVu Sans" font-size="20" fill="{GREY}">ANTERIOR</text>
        <path d="M900 966 L900 989" stroke="{ACCENT}" stroke-width="4"/><path d="M900 997 l-9 -14 h18 z" fill="{ACCENT}"/>
        <text x="925" y="991" font-family="DejaVu Sans" font-size="20" fill="{GREY}">POSTERIOR</text>'''
        end=f'''<text x="70" y="1050" font-family="DejaVu Sans" font-size="23" fill="{GREY}">{html.escape(self.foot)}</text><text x="70" y="1082" font-family="DejaVu Sans" font-size="19" fill="{GREY}">ORIGINAL EDUCATIONAL SCHEMATIC · NOT TO SCALE · SCIENTIFIC REVIEW PENDING</text></svg>'''
        return head+'\n'+'\n'.join(self.body)+'\n'+end

def shark():
    d=Drawing('Scoliodon brain — dorsal view','Elasmobranch forebrain, optic regions and prominent cerebellum','Large olfactory organs and cerebellum distinguish this shark diagram from amphibian and reptile brains.')
    # Slightly widened cerebrum, optic areas mostly flanking the conspicuous cerebellum.
    d.path('M852 358 Q855 330 880 320 L920 320 Q944 330 948 358 L940 485 Q901 514 860 485 Z',MID)
    # olfactory peduncles arise from anterior of cerebral body
    for x in [858,942]:
        d.path(f'M{x-10} 360 Q{x-22} 313 {x-58 if x<900 else x+58} 280 L{x-61 if x<900 else x+61} 250', 'none', 11)
    d.path('M748 209 Q727 194 708 217 Q694 246 726 266 Q758 273 775 250 Q788 225 748 209 Z',MID)
    d.path('M1052 209 Q1073 194 1092 217 Q1106 246 1074 266 Q1042 273 1025 250 Q1012 225 1052 209 Z',MID)
    d.line(726,235,780,249, GREY,2);d.line(1074,235,1020,249,GREY,2)
    # optic lobes are paired dorsolateral and partially concealed by huge cerebellum
    d.ellipse(821,545,70,60,PALE);d.ellipse(979,545,70,60,PALE)
    d.path('M856 474 Q900 443 943 474 L965 527 Q965 568 949 595 Q970 636 959 686 Q954 738 900 773 Q846 738 841 686 Q830 636 851 595 Q835 565 835 527 Z',MID)
    d.line(900,497,900,755,GREY,2)
    for y in [582,657]: d.path(f'M848 {y} Q900 {y+17} 952 {y}', 'none',2)
    # medulla broad anteriorly, tapering into cord
    d.path('M853 760 Q900 782 947 760 Q958 814 932 883 L920 927 L880 927 L868 883 Q842 814 853 760 Z',LIGHT)
    d.path('M892 783 L900 848 L908 783', 'none',2)
    d.path('M882 920 L881 973 Q900 984 919 973 L918 920',LIGHT,3)
    d.label('Olfactory lobes',98,240,738,236,'left')
    d.label('Olfactory peduncles',98,360,826,298,'left')
    d.label('Cerebrum',98,475,900,419,'left')
    d.label('Optic lobes (partly exposed)',98,600,797,539,'left')
    d.label('Cerebellum (enlarged)',1275,606,932,665,'right')
    d.label('Medulla oblongata',1275,790,922,844,'right')
    d.label('Spinal cord',1275,923,912,954,'right')
    return d

def frog():
    d=Drawing('Adult frog brain — dorsal view','Distinct paired cerebral hemispheres, large optic lobes and thin cerebellar band','The optic lobes form a conspicuous midbrain pair; the cerebellum is a thin transverse ridge.')
    d.path('M865 287 Q900 260 935 287 L935 311 Q900 330 865 311 Z',MID)
    # thin olfactory nerve ends
    d.line(879,286,861,245,INK,5);d.line(921,286,939,245,INK,5)
    # paired ovoid cerebral hemispheres elongated along head-tail axis
    d.path('M892 332 Q814 320 806 405 Q800 486 877 504 L895 492 Z',LIGHT)
    d.path('M908 332 Q986 320 994 405 Q1000 486 923 504 L905 492 Z',LIGHT)
    d.line(900,335,900,493,GREY,2)
    # median thalamencephalon/pineal between hemispheres and optic lobes
    d.path('M879 498 Q900 493 921 498 L930 537 L900 562 L870 537 Z',MID)
    d.ellipse(900,520,10,10,PALE,3)
    # large paired midbrain optic lobes touching centrally
    d.path('M898 558 Q846 530 794 573 Q757 644 819 695 Q856 721 898 694 Z',PALE)
    d.path('M902 558 Q954 530 1006 573 Q1043 644 981 695 Q944 721 902 694 Z',PALE)
    d.path('M825 715 Q900 703 975 715 L971 738 Q900 758 829 738 Z',MID)
    # medulla triangular tapering to cord
    d.path('M831 744 Q900 758 969 744 Q987 797 960 854 Q935 909 916 925 L884 925 Q865 909 840 854 Q813 797 831 744 Z',LIGHT)
    d.path('M857 771 Q900 798 943 771 L934 857 Q900 882 866 857 Z','none',2)
    d.path('M883 920 L884 967 Q900 974 916 967 L917 920',LIGHT,3)
    d.label('Olfactory lobes',98,287,895,298,'left')
    d.label('Cerebral hemispheres',98,425,849,420,'left')
    d.label('Diencephalon / pineal region',98,536,900,523,'left')
    d.label('Optic lobes',1260,610,968,628,'right')
    d.label('Cerebellum (narrow band)',1260,738,945,728,'right')
    d.label('Medulla oblongata',1260,846,943,830,'right')
    d.label('Spinal cord',1260,932,908,949,'right')
    return d

def calotes():
    d=Drawing('Calotes brain — dorsal view','Reptilian forebrain expansion, optic lobes, cerebellar flap and medulla','Expanded paired hemispheres and a curved cerebellar flap contrast with the frog.')
    d.ellipse(862,278,23,38,MID)
    d.ellipse(938,278,23,38,MID)
    d.path('M856 312 Q840 350 837 379', 'none',7)
    d.path('M944 312 Q960 350 963 379', 'none',7)
    # Large elongated broad hemispheres, medial fissure
    d.path('M884 374 Q814 335 780 399 Q758 457 790 539 Q826 578 887 553 Z',LIGHT)
    d.path('M916 374 Q986 335 1020 399 Q1042 457 1010 539 Q974 578 913 553 Z',LIGHT)
    d.line(900,371,900,551,GREY,2)
    d.path('M878 553 Q900 541 922 553 L925 594 Q900 617 875 594 Z',MID)
    d.ellipse(900,573,9,10,PALE,2)
    # paired optic lobes posterior to enlarged forebrain
    d.path('M896 607 Q841 575 805 616 Q784 667 824 712 Q855 733 896 712 Z',PALE)
    d.path('M904 607 Q959 575 995 616 Q1016 667 976 712 Q945 733 904 712 Z',PALE)
    # short raised cerebellar arch/flap, posterior to optic lobes
    d.path('M821 728 Q900 694 979 728 L965 751 Q900 735 835 751 Z',MID)
    d.path('M848 754 Q900 770 952 754 L968 816 Q947 883 917 921 L883 921 Q853 883 832 816 Z',LIGHT)
    d.path('M866 789 Q900 800 934 789', 'none',2)
    d.path('M880 915 L882 963 Q900 972 918 963 L920 915',LIGHT,3)
    d.label('Olfactory bulbs',98,283,862,272,'left')
    d.label('Olfactory peduncles',98,372,844,353,'left')
    d.label('Cerebral hemispheres',98,479,817,458,'left')
    d.label('Diencephalon / pineal region',98,578,900,575,'left')
    d.label('Optic lobes',1260,656,967,669,'right')
    d.label('Cerebellum (curved flap)',1260,755,936,729,'right')
    d.label('Medulla oblongata',1260,840,935,834,'right')
    d.label('Spinal cord',1260,925,905,952,'right')
    return d

def main():
    m=json.loads(MANIFEST.read_text('utf-8'))
    refs={
        'shark_brain_dorsal_en': ['https://gcwgandhinagar.com/econtent/document/15878893641ZOOTC0201-%20Brain%20%20of%20scoliodon%20%281%29-1.pdf', 'https://www.hansrajcollege.ac.in/hCPanel/uploads/elearning/elearning_document/comparative_Nervous_Syst_Vertebrate_Life_Sciences_1yr_PDF.pdf'],
        'frog_brain_dorsal_en': ['https://mirrors.xmission.com/gutenberg/7/7/5/6/77560/77560-h/77560-h.htm','https://embryology.med.unsw.edu.au/embryology/index.php?title=Vertebrate_Embryology_-_A_Text-book_for_Students_and_Practitioners_%281893%29_3'],
        'calotes_brain_dorsal_en': ['https://gdcpenukonda.ac.in/userfiles/Biology%20of%20chordates%2020242025.pdf','https://www.hansrajcollege.ac.in/hCPanel/uploads/elearning/elearning_document/comparative_Nervous_Syst_Vertebrate_Life_Sciences_1yr_PDF.pdf'],
    }
    variants={'shark_brain_dorsal_en':shark(), 'frog_brain_dorsal_en':frog(), 'calotes_brain_dorsal_en':calotes()}
    for name, drawing in variants.items():
        svg=SVG_DIR/(name+'.svg'); png=PNG_DIR/(name+'.png')
        svg.write_text(drawing.render(), encoding='utf-8')
        cairosvg.svg2png(url=str(svg),write_to=str(png),output_width=1800,output_height=1120)
        entry=next(x for x in m['figures'] if Path(x['path']).name==name+'.png')
        entry['size']=png.stat().st_size
        entry['sha256']=hashlib.sha256(png.read_bytes()).hexdigest()
        entry['svgMaster']=str(svg.relative_to(ROOT))
        entry['svgSha256']=hashlib.sha256(svg.read_bytes()).hexdigest()
        entry['referenceUrls']=refs[name]
        entry['modifications']='Reconstructed original, species-specific dorsal region schematic; all leader anchors and labels redrawn; 2026-11-06'
        entry['reviewStatus']='PROVISIONAL_QA_ANATOMICAL_AND_TAMIL_REVIEW_PENDING'
        print('REBUILT',name,entry['size'],entry['sha256'][:14])
    MANIFEST.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
