#!/usr/bin/env python3
"""Create contact evidence from original recovered Lake Peigneur PNGs. Does not alter sources."""
import json, pathlib, csv, collections, hashlib
from PIL import Image,ImageDraw,ImageOps,ImageFont
R=pathlib.Path(".").resolve(); P=R/"temp/recovered/HIA_LAKE_PEIGNEUR_FULL_SOURCE_RECOVERY/01_EDIT_PROJECT/project_files/Youtube-2/LAKE_PEIGNEUR/REMOTION_V1"
out=R/"inventory_output";out.mkdir(exist_ok=True)
timeline=json.loads((P/"public/timeline.json").read_text())
source=P/"public/assets"
mapdata=json.loads((R/"LAKE_PEIGNEUR/PUBLISHING/ACCENT_V4/IMPLEMENTATION/HIA_LAKE_PEIGNEUR_V4_ACCENT_MAP_MACHINE.json").read_text())
rows=[]
for b in timeline["beats"]:
 for s in b["slots"]:
  p=P/"public"/s["file"]
  rows.append({"beat":b.get("id",""),"file":s["file"],"present":p.is_file(),"name":p.stem,"size":p.stat().st_size if p.is_file() else 0})
counts=collections.Counter(pathlib.Path(x["file"]).stem for x in rows)
mapitems=mapdata["items"]
txt=["# Actual recovered V3 inventory","total timeline: "+str(len(rows)), "assets: "+str(len(list(source.glob('*.png'))))]
txt.append("Timeline fields example: "+json.dumps(timeline["beats"][0],ensure_ascii=False)[:2500])
txt.append("All timeline slots:")
for i,r in enumerate(rows):txt.append(str(i+1)+" "+json.dumps(r,ensure_ascii=False))
txt.append("ALL public assets:")
allp=sorted(source.glob("*.png"))
for p in allp:
 txt.append(p.name+" used="+str(counts.get(p.stem,0))+" bytes="+str(p.stat().st_size))
(out/"SOURCE_INVENTORY.txt").write_text("\n".join(txt))
with (out/"ASSET_USES.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=["beat","file","present","name","size"]);w.writeheader();w.writerows(rows)
bad={"LP-GFX-002","LP-GFX-022","LP-GFX-026","LP-REC-005","LP-REC-008","LP-REC-010","LP-REC-012","LP-REC-038","LP-REC-041"}
used={x['asset_id']:x for x in mapitems if x['asset_id'] in bad}
summary=[]
for i,p in enumerate(allp):
 try:
  im=Image.open(p).convert("RGB")
  w,h=im.size
  summary.append({"file":p.name,"width":w,"height":h,"uses":counts.get(p.stem,0),"flagged":any(s in p.stem for s in bad)})
 except Exception as e:
  summary.append({"file":p.name,"error":str(e)})
(out/"IMAGE_INDEX.json").write_text(json.dumps(summary,indent=2))
def contact(arr, label):
 for k in range(0,len(arr),20):
  page=Image.new("RGB",(5*352,4*232),"#111315")
  d=ImageDraw.Draw(page)
  for j,p in enumerate(arr[k:k+20]):
   im=ImageOps.contain(Image.open(p).convert("RGB"),(342,192))
   x=(j%5)*352;y=(j//5)*232
   page.paste(im,(x+(342-im.width)//2,y+(192-im.height)//2))
   d.rectangle([x,y+193,x+350,y+231],fill="#151719")
   d.text((x+6,y+196),p.stem[:45],fill="white")
   d.text((x+6,y+214),f"timeline uses {counts.get(p.stem,0)}; {p.stat().st_size//1024} KB",fill="#BBBFC3")
  page.save(out/f"{label}_{k//20+1:02d}.jpg",quality=89)
contact(allp,"ALL_ASSETS")
# Make separate large approved-candidate frame contact for all matched files and contextual neighboring files.
focus=[p for p in allp if any(s in p.stem for s in bad)]
contact(focus,"FLAGGED_ASSETS")
print("TIMELINE",len(rows),"ASSETS",len(allp),"FLAGGED",(len(focus)),"CONTACTS",len(list(out.glob("*.jpg"))))
