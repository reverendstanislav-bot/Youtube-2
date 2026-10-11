#!/usr/bin/env python3
"""Lake Peigneur V5 local scene replacements from LOCKED source images. No generation."""
import argparse, collections, hashlib, json, pathlib, shutil, subprocess
from PIL import Image,ImageOps,ImageEnhance,ImageDraw
D=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument("--project",required=True)
parser.add_argument("--archive",required=True)
parser.add_argument("--output",required=True)
args=parser.parse_args()
P=pathlib.Path(args.project).resolve()
A=pathlib.Path(args.archive).resolve()
OUT=pathlib.Path(args.output).resolve();OUT.mkdir(parents=True,exist_ok=True)
facts=P/"public/facts.json"
timeline=P/"public/timeline.json"
v4=P/"public/v4_accents.json"
orig_img=P/"public/approved_first_end_1080.png"
master=P/"public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3"
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for q in iter(lambda:f.read(4*1024*1024),b''):h.update(q)
    return h.hexdigest()
assert sha(orig_img)=="b794e5582699e90812b25208ca1c5dd053df465825d1ce6e33a7a0c6ea53b575","WRONG first-video Chicago R15 end screen"
assert sha(master)=="1ae5c97d85b9cf2c10c438a2834d024776ea851a932a02aab2490860fa4afd13","Arthur master changed!"
j=json.loads(timeline.read_text());m=json.loads(v4.read_text())
assert j['fps']==25 and len(j['beats'])==87 and len(m['items'])==100
assert sum(len(b['slots']) for b in j['beats'])==99
archive=A/"LAKE_PEIGNEUR_ARCHIVE_SOURCE_PACK_V1"
topo=archive/"04_USGS_HISTORICAL_MAPS_PD/USGS_Delcambre_1963_24000_GeoPDF.pdf"
landsat=archive/"05_PUBLIC_DOMAIN_CONTEXT/USGS_Landsat8_Salt_Dome_Islands_LA_PD.png"
assert topo.is_file() and landsat.is_file()
federal_assets={}
# Federal government topographic map with *no fabricated flow arrows*.
raw=OUT/"USGS_1963_delcambre_source.png"
subprocess.run(["pdftoppm","-f","1","-l","1","-scale-to-x","3200","-scale-to-y","-1","-singlefile","-png",str(topo),str(raw.with_suffix(""))],check=True)
im=Image.open(raw).convert("RGB");w,h=im.size
# Existing content only, crop/resize and restrained color balance, no added routes, photos or labels.
rect1=(0,int(h*.035),w,int(h*.035)+round(w*9/16))
cropw=round(w*.68);croph=round(cropw*9/16)
rect2=(0,int(h*.06),cropw,int(h*.06)+croph)
assert rect1[3]<=h and rect2[3]<=h
for aid,rect in [("LP-PD-USGS-DELCAMBRE-A",rect1),("LP-PD-USGS-DELCAMBRE-B",rect2)]:
    crop=im.crop(rect).resize((1920,1080),Image.Resampling.LANCZOS)
    path=P/"public/assets"/(aid+".png");assert not path.exists()
    crop.save(path,optimize=True)
    federal_assets[aid]={"original":str(topo.relative_to(A)),"raw_sha256":sha(topo),"image_sha256":sha(path),"crop":rect,"rights":"U.S. Geological Survey historical 1963 map; U.S. government public domain","public_asset":path.name}
aid="LP-PD-USGS-LANDSAT-CONTEXT"
photo=Image.open(landsat).convert('RGB')
photo=ImageOps.fit(photo,(1920,1080),method=Image.Resampling.LANCZOS,centering=(.50,.52))
path=P/"public/assets"/(aid+".png");assert not path.exists()
photo.save(path,optimize=True)
federal_assets[aid]={"original":str(landsat.relative_to(A)),"raw_sha256":sha(landsat),"image_sha256":sha(path),"rights":"USGS Landsat8 Louisiana salt-dome islands, public domain; CONTEMPORARY REGIONAL CONTEXT, not 1980 documentary photo","public_asset":path.name}
# Every replacement is locked to one original source slot/beat, with no time edits.
rep=[
 ("LP-B004","LP-GFX-002","LP-PD-USGS-DELCAMBRE-A","USGS 1963 actual Delcambre/Lake Peigneur geography, no fictional flow arrow"),
 ("LP-B005","LP-REC-005","LP-GFX-041","Existing MSHA investigation editorial card rather than offshore platform"),
 ("LP-B014","LP-REC-008","LP-REC-001","Existing inland lake drilling platform; nonarchival reconstruction, no offshore rig"),
 ("LP-B016","LP-REC-012","LP-GFX-008","Existing schematic mine level/depth diagram, not unattributed workers"),
 ("LP-B038","LP-GFX-022","LP-GFX-029","Existing focused water/salt cavern concept instead of four-panel collage"),
 ("LP-B039","LP-REC-010","LP-REC-033","Existing close view of salt-water contact; illustrative not archival"),
 ("LP-B040","LP-GFX-026","LP-GFX-030","Existing continuous flood channel picture, no feedback-loop arrows"),
 ("LP-B051","LP-REC-038","LP-GFX-038","Existing schematic lower lake basin concept, not unidentified industrial canal"),
 ("LP-B053","LP-REC-038","LP-PD-USGS-DELCAMBRE-B","USGS 1963 real lake/canal map zoom, not unknown refinery canal"),
 ("LP-B080","LP-REC-041","LP-PD-USGS-LANDSAT-CONTEXT","Public domain PRESENT-DAY regional salt dome Landsat context, not imagined refinery"),
]
assert len(rep)==10 and len(set(a for _,a,_,_ in rep))==9
lookup={(b,old):new for b,old,new,_ in rep}
before={};after={}
for b in j["beats"]:
    for s in b["slots"]:
        key=(b["beat"],s["assetId"])
        if key not in lookup: continue
        n=lookup[key]
        before[key]=s["file"]
        s["assetId"]=n
        s["file"]="assets/"+n+".png"
        s["kind"]="real_context" if n.startswith("LP-PD-") else ("gfx" if n.startswith("LP-GFX-") else "reconstruction")
        after[key]=s["file"]
assert len(before)==10,(len(before),list(before))
for x in m["items"]:
    key=(x["beat_id"],x["asset_id"])
    if key in lookup:
        x["asset_id"]=lookup[key]
assert all(x["asset_id"] not in {"LP-GFX-002","LP-GFX-022","LP-GFX-026","LP-REC-005","LP-REC-008","LP-REC-010","LP-REC-012","LP-REC-038","LP-REC-041"} for x in m["items"]),"Old reject still used!"
counts=collections.Counter(x["asset_id"] for x in m["items"])
assert max(counts.values())<=2,counts.most_common(6)
assert len([x for x in m['items'] if x['effect'] not in ('HOLD','QC_HOLD')])==36
assert j['fps']==25 and len(j['beats'])==87 and sum(len(b['slots']) for b in j['beats'])==99
for b in j["beats"]:
 for s in b["slots"]:
  assert (P/"public"/s["file"]).is_file(),s["file"]
# Preserve times and V4 editorial accent windows; do not modify narration or Chicago end screen.
shutil.copy2(timeline,OUT/"V4_TIMELINE_BEFORE.json")
shutil.copy2(v4,OUT/"V4_ACCENTS_BEFORE.json")
timeline.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n")
v4.write_text(json.dumps(m,indent=2,ensure_ascii=False)+"\n")
for key in lookup:
 assert (P/"public"/after[key]).is_file()
report={"verdict":"V5 PICTURE REPAIR SOURCE PREFLIGHT PASS — not editorial/final video QC","replacements":[{"beat":b,"rejected":old,"replacement":new,"reason":reason,"image_sha256":sha(P/"public/assets"/(new+".png"))} for b,old,new,reason in rep],
 "unique_old_ids":9,"replaced_exposures":len(before),"beats":87,"timeline_slots":99,"mapped_exposures":100,"active_accents":36,
 "source_reuse_max":max(counts.values()),"new_federal_sources":federal_assets,
 "unchanged_audio_sha256":sha(master),"unchanged_endscreen_sha256":sha(orig_img),
 "rights_and_editorial_gate":"All newly added sources are U.S. Government PD; other reused provider-generated original PNG images are illustrations not claimed authentic archival photos. All rights and owner/editorial approval gates remain OPEN."}
# Above 'new' shadowed in comprehensions? Python comprehension is scoped; last top-level new is 3 new sources dictionary.

(OUT/"V5_REPLACEMENTS_AND_PROVENANCE.json").write_text(json.dumps(report,indent=2,ensure_ascii=False))
# side by side examples of all 10 real original replacements (5/page)
for offset in (0,5):
    sheet=Image.new("RGB",(1600,5*515),"#171a1c")
    d=ImageDraw.Draw(sheet)
    for row,(beat,old,replacement,reason) in enumerate(rep[offset:offset+5]):
        oldp=P/"public/assets"/(old+".png");newp=P/"public/assets"/(replacement+".png")
        for k,src in enumerate((oldp,newp)):
            pic=ImageOps.fit(Image.open(src).convert("RGB"),(784,437),method=Image.Resampling.LANCZOS)
            sheet.paste(pic,(k*800+8,row*515+30))
            d.text((k*800+12,row*515+8),("BEFORE REJECT: " if not k else "REPAIR CANDIDATE: ")+src.stem,fill="white")
        d.text((10,row*515+476),beat+" | "+reason[:155],fill="#e6ddc8")
    sheet.save(OUT/f"V5_BEFORE_AFTER_{offset//5+1}.jpg",quality=91)
print(json.dumps({"repaired":len(before),"max_source_reuse":max(counts.values()),"active_accents":36,"pd_sources":list(federal_assets)}))
