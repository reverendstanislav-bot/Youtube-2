#!/usr/bin/env python3
"""Cut useful missile-engineering context from verified F018, excluding talking heads."""
from __future__ import annotations
import csv, hashlib, json, subprocess
from pathlib import Path

REPO=Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
BANK=Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_V2")
SOURCE=BANK/"00_ACQUISITION"/"F018_source"/"F018_FULL_SOURCE.mp4"
OUT=BANK/"15_CONTEXT_F018_ARMY_ORDNANCE"
SHEETS=BANK/"16_F018_SELECTED_CONTACT_SHEETS"
MANIFEST=REPO/"PROJECT_PLUTO"/"SOURCE_BANK_V2"/"F018_CONTEXT_MOTION_R6_MANIFEST.csv"
CLIPS=[
 ("F018-R6-01",32,38,"Missile configuration model beside Army briefing desk","PLUTO-CH03-B03"),
 ("F018-R6-02",77,82,"Outdoor guided-missile flight test","PLUTO-CH03-B03"),
 ("F018-R6-03",88,98,"Guided missile and ground support equipment","PLUTO-CH03-B03"),
 ("F018-R6-04",102,112,"Range crew observing missile operations","PLUTO-CH03-B03"),
 ("F018-R6-05",138,143,"Multiple missile test articles on range","PLUTO-CH03-B03"),
 ("F018-R6-06",146,156,"Missile launch and ascent","PLUTO-CH03-B03"),
 ("F018-R6-08",251,261,"Laboratory electronics and instrumentation","PLUTO-CH05-B05"),
 ("F018-R6-09",447,457,"Army missile test facility exterior","PLUTO-CH07-B04"),
 ("F018-R6-10",477,487,"Technician measuring cylindrical missile hardware","PLUTO-CH07-B04"),
 ("F018-R6-11",492,498,"Missile model used for engineering explanation","PLUTO-CH03-B03"),
 ("F018-R6-12",511,517,"Aerial view of missile development installation","PLUTO-CH07-B04"),
 ("F018-R6-13",522,532,"Restricted-area industrial building","PLUTO-CH07-B04"),
 ("F018-R6-14",654,660,"Outdoor static missile firing and plume","PLUTO-CH03-B03"),
 ("F018-R6-15",660,670,"Large missile test stand and launch structure","PLUTO-CH07-B04"),
 ("F018-R6-16",672,682,"Close mechanical view of missile system hardware","PLUTO-CH07-B04"),
]
def run(a): return subprocess.run(a,text=True,capture_output=True,encoding="utf-8",errors="replace")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def main():
 expected="3f5413b83385974bc04c813a35bd446e1a527820d82b7963cecbb6f86981f848"
 if sha(SOURCE)!=expected: raise SystemExit("F018 source SHA mismatch")
 OUT.mkdir(parents=True,exist_ok=True); SHEETS.mkdir(parents=True,exist_ok=True)
 for stale in OUT.glob("F018-R6-*.mp4"): stale.unlink()
 for stale in SHEETS.glob("F018-R6-*.jpg"): stale.unlink()
 rows=[]
 for cid,start,end,context,beat in CLIPS:
  p=OUT/f"{cid}.mp4"; dur=end-start
  q=run(["ffmpeg","-y","-v","error","-ss",str(start),"-i",str(SOURCE),"-t",str(dur),"-map","0:v:0","-an","-c:v","libx264","-preset","slow","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart",str(p)])
  if q.returncode: raise SystemExit(q.stderr)
  dec=run(["ffmpeg","-v","error","-xerror","-i",str(p),"-f","null","-"])
  black=run(["ffmpeg","-hide_banner","-i",str(p),"-vf","blackdetect=d=0.40:pix_th=0.10","-an","-f","null","-"])
  bl=" | ".join(x.strip() for x in black.stderr.splitlines() if "black_start:" in x)
  probe=json.loads(run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=codec_name,width,height,avg_frame_rate:format=duration","-of","json",str(p)]).stdout); s=probe["streams"][0]
  run(["ffmpeg","-y","-v","error","-i",str(p),"-vf","fps=1/2,scale=320:-2,tile=5x1:padding=4:margin=4","-frames:v","1",str(SHEETS/f"{cid}.jpg")])
  rows.append({"clip_id":cid,"file":str(p),"source_master":"F018_Army_Ordnance_Missile_Command_1958","source_sha256":expected,"source_in_sec":f"{start:.3f}","source_out_sec":f"{end:.3f}","duration_sec":f"{float(probe['format']['duration']):.3f}","historical_context":context,"editorial_purpose":"Period missile engineering context; never Project Pluto, SLAM, or Tory evidence","suggested_beat_id":beat,"rights_status":"HOLD_ITEM_SPECIFIC_COMMONS_DERIVATIVE_AI_UPSCALE_WARNING","screen_label":"CONTEXT — ARMY ORDNANCE, 1958 / NOT PROJECT PLUTO","sha256":sha(p),"bytes":p.stat().st_size,"codec":s["codec_name"],"width":s["width"],"height":s["height"],"fps":s["avg_frame_rate"],"decode_qc":"PASS" if dec.returncode==0 else "FAIL","black_intervals":bl})
 with MANIFEST.open("w",newline="",encoding="utf-8-sig") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
 print(json.dumps({"clips":len(rows),"duration_sec":sum(float(r["duration_sec"]) for r in rows),"decode_pass":sum(r["decode_qc"]=="PASS" for r in rows),"black_free":sum(not r["black_intervals"] for r in rows)},indent=2))
if __name__=="__main__": main()
