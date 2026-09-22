#!/usr/bin/env python3
import argparse
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("--base",required=True)
ap.add_argument("--output",required=True)
a=ap.parse_args()

src=Image.open(a.base).convert("RGB")
if src.size!=(1920,1080):
    raise SystemExit(f"unexpected base size {src.size}")

dark=Image.new("RGB",src.size,(0,0,0))
im=Image.blend(src,dark,0.12)
d=ImageDraw.Draw(im)

PAPER=(243,235,221)
IVORY=(246,241,232)
RUST=(165,82,53)
INK=(20,22,23)

reg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
title=ImageFont.truetype(bold,52)
tag=ImageFont.truetype(reg,28)
sub=ImageFont.truetype(bold,30)
sub2=ImageFont.truetype(reg,21)

# Brand header.
x=105; y=92
d.rectangle([x,y,x+68,y+6],fill=RUST)
d.text((x+92,y-24),"HIDDEN INDUSTRIAL AMERICA",font=title,fill=IVORY,
       stroke_width=2,stroke_fill=INK)
d.text((x+92,y+55),"THE INFRASTRUCTURE REMAINS",font=tag,fill=PAPER,
       stroke_width=1,stroke_fill=INK)

# Canonical Subscribe geometry from 06 End Screen.
cx,cy,r=957,704,138

# Local circle readability field only.
overlay=Image.new("RGBA",im.size,(0,0,0,0))
od=ImageDraw.Draw(overlay)
od.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(10,12,13,72))
im=Image.alpha_composite(im.convert("RGBA"),overlay).convert("RGB")
d=ImageDraw.Draw(im)

# HIA double ring.
d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=PAPER,width=4)
d.arc([cx-r-8,cy-r-8,cx+r+8,cy+r+8],start=210,end=325,fill=RUST,width=5)

# Subscribe copy.
bbox=d.textbbox((0,0),"SUBSCRIBE",font=sub)
tw=bbox[2]-bbox[0]
d.text((cx-tw/2,cy+r+42),"SUBSCRIBE",font=sub,fill=RUST,
       stroke_width=1,stroke_fill=INK)

line="HIDDEN INDUSTRIAL AMERICA"
bbox=d.textbbox((0,0),line,font=sub2)
tw=bbox[2]-bbox[0]
d.text((cx-tw/2,cy+r+88),line,font=sub2,fill=PAPER,
       stroke_width=1,stroke_fill=INK)

Path(a.output).parent.mkdir(parents=True,exist_ok=True)
im.save(a.output,compress_level=6)
print(a.output)
