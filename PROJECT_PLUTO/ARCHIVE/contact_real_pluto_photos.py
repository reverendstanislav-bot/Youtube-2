#!/usr/bin/env python3
"""Create review contact sheets from actual verified Project Pluto source archive."""
import pathlib,csv,math,zipfile
from PIL import Image,ImageDraw,ImageFont,ImageOps
zip_path=pathlib.Path("PROJECT_PLUTO_REAL_HISTORICAL_PHOTOS_39_FILES.zip")
out=pathlib.Path("PROJECT_PLUTO/ARCHIVE/REAL_PLUTO_PHOTO_SCREENING")
out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(zip_path) as z:
 source=list(csv.DictReader(z.open("PROJECT_PLUTO_HIA_PHOTO_ARCHIVE/PHOTO_MASTER_INDEX.csv").read().decode("utf-8").splitlines()))
 font=ImageFont.load_default()
 for page_no in range(math.ceil(len(source)/12)):
  panel=Image.new("RGB",(4*368,3*290+37),"#1c2022")
  d=ImageDraw.Draw(panel)
  d.text((9,8),f"ACTUAL PROJECT PLUTO HISTORICAL SOURCE IMAGES — PAGE {page_no+1}",font=font,fill="white")
  for tile,row in enumerate(source[page_no*12:(page_no+1)*12]):
   key="PROJECT_PLUTO_HIA_PHOTO_ARCHIVE/"+row["file"]
   with z.open(key) as raw:
    with Image.open(raw) as pic:
     pic.draft("RGB",(345,227))
     pic.thumbnail((345,227))
     im=pic.convert("RGB")
   x=(tile%4)*368+8;y=(tile//4)*290+37
   panel.paste(im,(x+(345-im.width)//2,y+20))
   name=pathlib.Path(row["file"]).name
   d.text((x,y),name+"  "+row["class"][:11],font=font,fill="white")
   d.text((x,y+252),row["date"][:36],font=font,fill="white")
  dest=out/(f"PLUTO_ORIGINALS_SCREEN_{page_no+1:02}.jpg")
  panel.save(dest,quality=80,optimize=True)
 print("Original source images screened",len(source),"contact sheets",math.ceil(len(source)/12))
