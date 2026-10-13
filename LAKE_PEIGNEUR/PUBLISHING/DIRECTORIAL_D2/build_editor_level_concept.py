#!/usr/bin/env python3
"""One HIA editor-native CONCEPT illustration, not historical footage or engineering drawing.
The two water levels are qualitative, not surveyed elevations. No false canals/locks/ship models.
"""
from PIL import Image,ImageDraw,ImageFont
import pathlib,argparse
q=argparse.ArgumentParser();q.add_argument('--project',required=True);a=q.parse_args()
out=pathlib.Path(a.project)/'public/assets/LP-EDITOR-LEVEL-DIFFERENCE-01.png'
out.parent.mkdir(parents=True,exist_ok=True)
W,H=1920,1080
im=Image.new('RGB',(W,H),'#171A1C')
d=ImageDraw.Draw(im)
IV='#F3EBDD';PAPER='#E6DDC8';IRON='#30363A';BLUE='#5F747D';RUST='#A55235'
def font(size,bold=False):
    p='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    return ImageFont.truetype(p,size)
def txt(x,y,t,size,color=IV,bold=False):d.text((x,y),t,font=font(size,bold),fill=color)
d.rectangle((104,107,120,172),fill=RUST)
txt(146,99,'THE LEVEL DIFFERENCE',64,IV,True)
txt(146,186,'Lake Peigneur  |  November 1980',27,PAPER)
d.line((113,266,1807,266),fill=IRON,width=4)
# Qualitative section only: no surveyed route, vessel, lock, fabricated arrow path.
land=[(140,525),(352,514),(555,530),(792,548),(950,581),(1140,618),(1344,628),(1510,653),(1780,651),(1780,863),(140,863)]
d.polygon(land,fill='#645b4e')
for delta,color in [(42,'#5a554b'),(100,'#514c44'),(157,'#474742')]:
    d.line([(x,y+delta) for x,y in land[:9]],fill=color,width=7)
d.polygon([(170,470),(790,470),(790,535),(555,530),(352,514),(170,525)],fill='#486d7d')
d.polygon([(1160,708),(1780,708),(1780,651),(1510,653),(1344,628),(1160,618)],fill='#426879')
d.line((171,470,787,470),fill='#a5c8cc',width=7)
d.line((1165,708,1775,708),fill='#a5c8cc',width=7)
for x in range(803,1750,32):d.line((x,470,x+12,470),fill='#9a9f9d',width=3)
d.rounded_rectangle((186,342,770,432),radius=8,fill='#21272a',outline='#5F747D',width=2)
d.rounded_rectangle((1195,542,1767,637),radius=8,fill='#21272a',outline='#5F747D',width=2)
txt(212,355,'DELCAMBRE CANAL',47,IV,True)
txt(1220,557,'LAKE PEIGNEUR',47,IV,True)
txt(1281,754,'FALLING LAKE LEVEL',34,PAPER,True)
# Relative level difference is conceptual, never an absolute elevation or historical survey.
d.line((1024,474,1024,706),fill=RUST,width=8)
d.polygon([(1008,494),(1024,467),(1040,494)],fill=RUST)
d.polygon([(1008,684),(1024,710),(1040,684)],fill=RUST)
txt(1051,549,'RELATIVE',27,PAPER,True)
txt(1051,587,'DROP',27,PAPER,True)
d.line((114,939,1807,939),fill=IRON,width=6)
txt(116,961,'EDITORIAL CONCEPT   |   NOT TO SCALE',25,'#b4b3ab',True)
im.save(out,optimize=True)
print('EDITOR-NATIVE CONCEPT ASSET',out,out.stat().st_size)
