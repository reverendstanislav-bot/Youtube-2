#!/usr/bin/env python3
"""QC evidence extractor for EXISTING Lake Peigneur V4 MP4. No video re-encode or PASS fabrication."""
import csv, json, hashlib, pathlib, subprocess, sys
from PIL import Image, ImageDraw
root=pathlib.Path.cwd()
master=root/"qc_inputs/HIA_LAKE_PEIGNEUR_V4_ACCENTS_REVIEW_MASTER_1080P25.mp4"
shorts=sorted((root/"qc_inputs/shorts").rglob("*.mp4"))
map_path=root/"LAKE_PEIGNEUR/PUBLISHING/ACCENT_V4/IMPLEMENTATION/HIA_LAKE_PEIGNEUR_V4_ACCENT_MAP_MACHINE.json"
manifest=json.loads(map_path.read_text())
out=root/"qc_results"
stills=out/"stills"
stills.mkdir(parents=True,exist_ok=True)
def run(cmd, logfile=None):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if logfile: pathlib.Path(logfile).write_text(p.stdout+"\n"+p.stderr)
    if p.returncode: raise RuntimeError("cmd failed "+str(cmd)+"\n"+p.stderr[-3500:])
    return p
def probe(p):
    return json.loads(run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(p)]).stdout)
def hashfile(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(4*1024*1024),b""): h.update(c)
    return h.hexdigest()
def validate(p,w,h,frames=None):
    d=probe(p);v=[x for x in d["streams"] if x["codec_type"]=="video"];a=[x for x in d["streams"] if x["codec_type"]=="audio"]
    assert len(v)==1 and len(a)>=1 and not any(x["codec_type"]=="subtitle" for x in d["streams"]),p
    assert (v[0]["width"],v[0]["height"],v[0]["r_frame_rate"])==(w,h,"25/1"),p
    if frames is not None: assert int(v[0]["nb_frames"])==frames,p
    assert a[0]["codec_name"]=="aac" and a[0]["sample_rate"]=="48000",p
    run(["ffmpeg","-hide_banner","-nostdin","-v","error","-xerror","-i",str(p),"-f","null","-"],out/(p.stem+"_full_decode.log"))
    return d
d=validate(master,1920,1080,24711)
v=next(x for x in d["streams"] if x["codec_type"]=="video")
assert (v.get("color_primaries"),v.get("color_space"),v.get("color_transfer"))==("bt709","bt709","bt709")
assert abs(float(d["format"]["duration"])-988.44)<0.15
expected=["6020400d27d2d3e07f0d65e9169d5634feebf1e2d6cd8c3cb6d60c76649da48d","3fdeb7f64e290b01a05810ce0f9ce3920fd786158b7376f35a1c119e807f4987","3e9ff822decae0f531967386b67279071cb147d82913ad5427c447464cc65aaa","39a060f6a907d594cf3acf623fdf09bd8ff587947219b46e9b44fad83fac1296"]
assert len(shorts)==4,(len(shorts),shorts)
hashes=[hashfile(p) for p in shorts]
assert sorted(hashes)==sorted(expected), "Unexpected Shorts source hashes"
for p in shorts: validate(p,1080,1920)
# Gather black/silence events without asserting that their absence proves creative quality.
run(["ffmpeg","-nostdin","-hide_banner","-i",str(master),"-vf","blackdetect=d=0.4:pix_th=0.10:pic_th=0.98","-an","-f","null","-"],out/"master_blackdetect.log")
run(["ffmpeg","-nostdin","-hide_banner","-i",str(master),"-af","silencedetect=noise=-50dB:d=0.75","-vn","-f","null","-"],out/"master_silencedetect.log")
rows=[]
active=[a for a in manifest["items"] if a["effect"] not in ("HOLD","QC_HOLD")]
assert len(active)==36
def add(kind,asset,beat,mark,frame,effect):
    rows.append(dict(group=kind,asset_id=asset,beat_id=beat,phase=mark,frame=frame,timestamp_seconds=round(frame/25,3),effect=effect,visual_qc="OPEN"))
for a in active:
    first=int(a["accent_in_frame"]);last=int(a["accent_out_frame_exclusive"])-1
    for phase,f in [("start",first+3),("middle",(first+last)//2),("end",max(first+3,last-3))]:
        add("ACCENT",a["asset_id"],a["beat_id"],phase,f,a["effect"])
for a in manifest["items"]:
    first=int(a["slot_in_frame"]);last=int(a["slot_out_frame_exclusive"])-1
    add("SLOT",a["asset_id"],a["beat_id"],"middle",(first+last)//2,a["effect"])
    if a["effect"]=="QC_HOLD":
        add("CONDITIONAL",a["asset_id"],a["beat_id"],"middle",(first+last)//2,a["effect"])
for t in [0,1,3,5,8,15,30,60,90,330,460,540,615,750,885,968,970,975,982,987]:
    add("SAFETY","TIMELINE","",str(t)+"s",int(t*25),"")
with (out/"FRAME_REVIEW_MANIFEST.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
# Save exact decoded samples, lossy preview JPEGs only; master stays untouched.
for i,row in enumerate(rows):
    t=row["timestamp_seconds"]
    fn=stills/f'{i:03d}_{row["group"]}_{row["asset_id"]}_{row["phase"]}.jpg'
    run(["ffmpeg","-v","error","-nostdin","-ss",str(t),"-i",str(master),"-vf","scale=960:-2","-frames:v","1","-q:v","3","-y",str(fn)])
# Contact sheets (each panel 480x270, no original master changes)
for group in ["ACCENT","CONDITIONAL","SLOT","SAFETY"]:
    subset=[(i,r) for i,r in enumerate(rows) if r["group"]==group]
    for j in range(0,len(subset),24):
        batch=subset[j:j+24]; sheet=Image.new("RGB",(4*480,6*303),"#111");draw=ImageDraw.Draw(sheet)
        for k,(idx,r) in enumerate(batch):
            name=f'{idx:03d}_{r["group"]}_{r["asset_id"]}_{r["phase"]}.jpg'
            im=Image.open(stills/name).convert("RGB").resize((480,270))
            x=(k%4)*480;y=(k//4)*303;sheet.paste(im,(x,y))
            draw.text((x+8,y+274),f'{r["asset_id"]} {r["phase"]} {r["timestamp_seconds"]}s',fill="white")
        sheet.save(out/f"{group}_contact_{j//24+1:02d}.jpg",quality=90)
with (out/"QC_TECHNICAL_REPORT.json").open("w") as f:
    json.dump({"original_master":{"filename":master.name,"sha256":hashfile(master),"bytes":master.stat().st_size,"duration":d["format"]["duration"],"frames":v["nb_frames"],"codec":v["codec_name"],"audio":"AAC 48kHz"},"shorts":[{"filename":p.name,"sha256":hashfile(p),"bytes":p.stat().st_size} for p in shorts],"accent_windows":len(active),"visual_qc":"OPEN; no automatic editorial PASS","conditional_assets":"OPEN; human factual/provenance review required","publication":"NO-GO"},f,indent=2)
print("TECHNICAL VALIDATION COMPLETED; VISUAL QC OPEN; no rerender, no claims of editorial PASS")
