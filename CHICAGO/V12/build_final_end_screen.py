#!/usr/bin/env python3
import argparse
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("--base",required=True)
ap.add_argument("--output",required=True)
a=ap.parse_args()

src=Image.open(a.base).convert("RGB")
assert src.size==(1920,1080), src.size
im=Image.blend(src,Image.new("RGB",src.size,(0,0,0)),0.15)
d=ImageDraw.Draw(im)

PAPER=(230,221,200); IVORY=(243,235,221); RUST=(165,82,53); INK=(18,20,21)
reg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_title=ImageFont.truetype(bold,54)
f_tag=ImageFont.truetype(reg,29)
f_label=ImageFont.truetype(bold,27)
f_small=ImageFont.truetype(reg,21)

x=105;y=88
d.rectangle([x,y,x+70,y+6],fill=RUST)
d.text((x+92,y-28),"HIDDEN INDUSTRIAL AMERICA",font=f_title,fill=IVORY,stroke_width=2,stroke_fill=INK)
d.text((x+92,y+58),"THE INFRASTRUCTURE REMAINS",font=f_tag,fill=PAPER,stroke_width=1,stroke_fill=INK)

# Exactly one Previous Story slot.
rx1,ry1,rx2,ry2=185,350,1015,817
d.rounded_rectangle([rx1,ry1,rx2,ry2],radius=6,fill=(22,25,27),outline=PAPER,width=5)
d.line([rx1,ry1,rx1+155,ry1],fill=RUST,width=7)
d.text((rx1,ry1-58),"PREVIOUS STORY",font=f_label,fill=RUST,stroke_width=1,stroke_fill=INK)
d.text((rx1,ry2+24),"CONTINUE EXPLORING HIDDEN INDUSTRIAL AMERICA",font=f_small,fill=PAPER,stroke_width=1,stroke_fill=INK)

# Exactly one Subscribe/avatar circle.
cx,cy,r=1425,590,145
d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(18,21,23),outline=PAPER,width=5)
d.arc([cx-r-9,cy-r-9,cx+r+9,cy+r+9],start=208,end=325,fill=RUST,width=6)
label="SUBSCRIBE"
bb=d.textbbox((0,0),label,font=f_label); tw=bb[2]-bb[0]
d.text((cx-tw/2,cy+r+38),label,font=f_label,fill=RUST,stroke_width=1,stroke_fill=INK)
label2="HIDDEN INDUSTRIAL AMERICA"
bb=d.textbbox((0,0),label2,font=f_small); tw=bb[2]-bb[0]
d.text((cx-tw/2,cy+r+82),label2,font=f_small,fill=PAPER,stroke_width=1,stroke_fill=INK)

# IMPORTANT: no "YOUTUBE END SCREEN" marker and no technical/instructional copy.
Path(a.output).parent.mkdir(parents=True,exist_ok=True)
im.save(a.output,compress_level=6)
