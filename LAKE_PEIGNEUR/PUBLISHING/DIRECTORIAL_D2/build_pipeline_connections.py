#!/usr/bin/env python3
"""ONEOK-reported eight connections shown as 8 schematic spokes, never geographic routes."""
from PIL import Image,ImageDraw,ImageFont
import math,pathlib,argparse
p=argparse.ArgumentParser();p.add_argument('--project',required=True);a=p.parse_args()
W,H=1920,1080
im=Image.new('RGB',(W,H),'#171A1C')
d=ImageDraw.Draw(im)
IV='#F3EBDD';PAPER='#E6DDC8';RUST='#A55235'
def ft(size,bold=True):
 s='DejaVuSansCondensed-Bold.ttf' if bold else 'DejaVuSans.ttf'
 return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+s,size)
def txt(x,y,t,n,c=IV,bold=True):d.text((x,y),t,font=ft(n,bold),fill=c)
d.rectangle((111,111,127,186),fill=RUST)
txt(158,104,'EIGHT MAJOR PIPELINES',67)
txt(159,195,'Jefferson Island Storage Hub  |  ONEOK-reported connections',27,PAPER,False)
d.line((110,271,1810,271),fill='#30363A',width=4)
cx,cy=960,616
for i in range(8):
 angle=math.radians(-90+i*45)
 x=int(cx+602*math.cos(angle));y=int(cy+314*math.sin(angle))
 d.line((cx,cy,x,y),fill='#577c8d' if i%2==0 else '#8e705d',width=17)
 d.line((cx,cy,x,y),fill='#7893a0' if i%2==0 else '#b28769',width=4)
 d.ellipse((x-51,y-51,x+51,y+51),fill='#30363A',outline=PAPER,width=5)
 d.text((x,y),str(i+1),font=ft(43),fill=IV,anchor='mm')
d.ellipse((cx-186,cy-146,cx+186,cy+146),fill='#232d32',outline=RUST,width=12)
d.text((cx,cy-34),'STORAGE',font=ft(63),fill=IV,anchor='mm')
d.text((cx,cy+46),'HUB',font=ft(59),fill=PAPER,anchor='mm')
d.line((110,985,1810,985),fill='#30363A',width=4)
txt(120,1004,'ILLUSTRATIVE NETWORK   |   NOT A GEOGRAPHIC PIPELINE MAP',23,'#b2b4ae')
out=pathlib.Path(a.project)/'public/assets/LP-EDITOR-PIPELINE-EIGHT-01.png'
out.parent.mkdir(parents=True,exist_ok=True);im.save(out,optimize=True)
assert out.stat().st_size>20000
print('8 distinct pipeline spokes generated as editor-native concept',out)
