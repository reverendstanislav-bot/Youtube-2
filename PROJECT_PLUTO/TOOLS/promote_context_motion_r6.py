#!/usr/bin/env python3
"""Re-QC and promote the 20 previously reserved context scenes for R6."""

from __future__ import annotations

import csv, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageOps

REPO = Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
SRC = REPO / "PROJECT_PLUTO" / "SOURCE_BANK_V2"
INVENTORY = SRC / "CONTEXT_ALL_40_INVENTORY_V2.csv"
SELECTED = SRC / "CONTEXT_MOTION_MANIFEST_V2.csv"
OUT = SRC / "CONTEXT_MOTION_PROMOTED_R6_MANIFEST.csv"
SHEETS = Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_V2\13_PROMOTED_CONTEXT_CONTACT_SHEETS")
CLEAN = Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_V2\14_PROMOTED_CONTEXT_CLEAN")

BEATS = {
    "SC001":"PLUTO-CH05-B05", "SC002":"PLUTO-CH03-B01", "SC003":"PLUTO-CH04-B02",
    "SC004":"PLUTO-CH02-B03", "SC005":"PLUTO-CH05-B01", "SC006":"PLUTO-CH05-B01",
    "SC007":"PLUTO-CH05-B04", "SC008":"PLUTO-CH05-B04", "SC009":"PLUTO-CH05-B04",
    "SC010":"PLUTO-CH05-B05", "SC011":"PLUTO-CH05-B05", "SC012":"PLUTO-CH05-B04",
    "SC013":"PLUTO-CH05-B05", "SC014":"PLUTO-CH05-B05", "SC015":"PLUTO-CH05-B05",
    "SC016":"PLUTO-CH07-B04", "SC017":"PLUTO-CH05-B05", "SC018":"PLUTO-CH03-B01",
    "SC039":"PLUTO-CH02-B01", "SC040":"PLUTO-CH02-B01",
}

def run(args):
    return subprocess.run(args, text=True, capture_output=True, encoding="utf-8", errors="replace")

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def main():
    with INVENTORY.open("r",newline="",encoding="utf-8-sig") as f: inv=list(csv.DictReader(f))
    with SELECTED.open("r",newline="",encoding="utf-8-sig") as f: already={r["scene_id"] for r in csv.DictReader(f)}
    rows=[]; images=[]; SHEETS.mkdir(parents=True,exist_ok=True)
    CLEAN.mkdir(parents=True,exist_ok=True)
    for r in inv:
        if r["scene_id"] in already: continue
        p=Path(r["file"])
        source_actual=sha(p)
        if source_actual.lower()!=r["sha256"].lower(): raise SystemExit(f"hash mismatch {r['scene_id']}")
        source_out=float(r["source_out_sec"])
        # SC004 ends in a 0.60-second black transition. Keep the useful wind-tunnel shot only.
        if r["scene_id"]=="SC004":
            clean=CLEAN/"SC004_F020_TRIMMED.mp4"
            cut=run(["ffmpeg","-y","-v","error","-i",str(p),"-t","11.300","-an","-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart",str(clean)])
            if cut.returncode: raise SystemExit(cut.stderr)
            p=clean; source_out=float(r["source_in_sec"])+11.3
        actual=sha(p)
        dec=run(["ffmpeg","-v","error","-xerror","-i",str(p),"-f","null","-"])
        black=run(["ffmpeg","-hide_banner","-i",str(p),"-vf","blackdetect=d=0.40:pix_th=0.10","-an","-f","null","-"])
        black_lines=" | ".join(x.strip() for x in black.stderr.splitlines() if "black_start:" in x)
        probe=json.loads(run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=codec_name,width,height,avg_frame_rate:format=duration","-of","json",str(p)]).stdout)
        s=probe["streams"][0]; dur=float(probe["format"]["duration"])
        jpg=SHEETS/f"{r['scene_id']}.jpg"
        interval=max(dur/5,0.2)
        q=run(["ffmpeg","-y","-v","error","-i",str(p),"-vf",f"fps=1/{interval:.6f},scale=320:-2,tile=5x1:padding=4:margin=4","-frames:v","1",str(jpg)])
        if q.returncode==0 and jpg.exists(): images.append(jpg)
        is_x15=r["source_film_id"]=="F020"
        rows.append({
            "scene_id":r["scene_id"],"file":str(p),"source_film_id":r["source_film_id"],
            "source_in_sec":r["source_in_sec"],"source_out_sec":f"{source_out:.3f}",
            "duration_sec":f"{dur:.3f}","historical_context":r["historical_context"],
            "editorial_purpose":r["editorial_purpose"],"suggested_beat_id":BEATS[r["scene_id"]],
            "rights_status":"HOLD_PER_SHOT_RIGHTS_REVIEW",
            "screen_label":"CONTEXT — NASA X-15 / NOT PROJECT PLUTO" if is_x15 else "CONTEXT — FORT BELVOIR, 1957 / NOT PROJECT PLUTO",
            "provenance_guard":r["provenance_guard"],"source_file_sha256":source_actual,"sha256":actual,"bytes":p.stat().st_size,
            "codec":s["codec_name"],"width":s["width"],"height":s["height"],"fps":s["avg_frame_rate"],
            "decode_qc":"PASS" if dec.returncode==0 else "FAIL","black_intervals":black_lines,
        })
    with OUT.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    if images:
        ims=[Image.open(x).convert("RGB") for x in images]; w=max(i.width for i in ims); h=max(i.height for i in ims)
        canvas=Image.new("RGB",(w*2,h*((len(ims)+1)//2)),(16,24,32))
        for i,im in enumerate(ims): canvas.paste(ImageOps.pad(im,(w,h),color=(16,24,32)),((i%2)*w,(i//2)*h))
        canvas.save(SHEETS/"PROMOTED_CONTEXT_R6_ALL.jpg",quality=90)
    print(json.dumps({"clips":len(rows),"duration_sec":round(sum(float(r["duration_sec"]) for r in rows),3),"decode_pass":sum(r["decode_qc"]=="PASS" for r in rows),"black_free":sum(not r["black_intervals"] for r in rows)},indent=2))

if __name__=="__main__": main()
