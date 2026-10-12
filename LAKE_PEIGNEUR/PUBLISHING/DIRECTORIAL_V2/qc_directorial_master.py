#!/usr/bin/env python3
"""Check the one completed full Lake Peigneur script-locked edit, not an extra preview."""
import collections,csv,hashlib,json,pathlib,re,subprocess,sys
from PIL import Image,ImageDraw,ImageOps
root=pathlib.Path(".").resolve()
P=pathlib.Path(sys.argv[1]).resolve()
f=root/"output/HIA_LAKE_PEIGNEUR_DIRECTORIAL_V2_MASTER_1080P25.mp4"
old=root/"output/HIA_LAKE_PEIGNEUR_V6_NO_RINGS_MASTER_1920x1080_25FPS.mp4"
out=root/"output/final_qc"
out.mkdir(parents=True,exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as z:
  for b in iter(lambda:z.read(4*1024*1024),b""): h.update(b)
 return h.hexdigest()
def sh(cmd,outfile=None):
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if outfile: pathlib.Path(outfile).write_text(r.stdout+r.stderr)
 if r.returncode: raise RuntimeError(str(cmd)+"\n"+r.stderr[-3000:])
 return r.stdout+r.stderr
assert f.is_file() and old.is_file(),"Audio video source or new master missing"
tl=json.loads((P/"public/timeline.json").read_text())
assert len(tl["beats"])==87
slots=[s for b in tl["beats"] for s in b["slots"]]
assert len(slots)==141,len(slots)
n=collections.Counter(s["assetId"] for s in slots)
assert max(n.values())<=2,n.most_common(12)
for s in slots:assert (P/"public"/s["file"]).is_file(),s
assert sha(P/"public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3")=="1ae5c97d85b9cf2c10c438a2834d024776ea851a932a02aab2490860fa4afd13"
assert sha(P/"public/approved_first_end_1080.png")=="b794e5582699e90812b25208ca1c5dd053df465825d1ce6e33a7a0c6ea53b575"
source=(P/"src/index.jsx").read_text()
assert not any(e in source for e in ("V4Overlay","V4Picture","V7Retention","v7Motion","V7Focus","V8Cutaways","<Caption"))
assert 'DISSOLVE_HALF=3' in source and 'pictureGroups=makeGroups(pictureShots)' in source and 'const frames=18' not in source,"Disallowed cosmetic motion or captions"
assert "approved_first_end_1080.png" in source and "LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3" in source
d=json.loads(sh(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(f)]))
v=next(x for x in d["streams"] if x["codec_type"]=="video")
a=next(x for x in d["streams"] if x["codec_type"]=="audio")
assert v["codec_name"]=="h264" and v["profile"]=="High"
assert (v["width"],v["height"],v["r_frame_rate"],int(v["nb_frames"]))==(1920,1080,"25/1",24711),v
assert (v.get("color_space"),v.get("color_primaries"),v.get("color_transfer"),v.get("color_range"))==("bt709","bt709","bt709","tv"),v
assert a["codec_name"]=="aac" and a["sample_rate"]=="48000",a
assert abs(float(d["format"]["duration"])-988.44)<0.14
assert not [x for x in d["streams"] if x["codec_type"]=="subtitle"]
def packet(f):
 p=subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(f),"-map","0:a:0","-c:a","copy","-f","adts","-"],capture_output=True)
 assert p.returncode==0,p.stderr[-1000:]
 return hashlib.sha256(p.stdout).hexdigest()
audio=packet(f)
assert audio==packet(old),"Arthur AAC stream was altered"
sh(["ffmpeg","-nostdin","-v","error","-xerror","-i",str(f),"-f","null","-"],out/"FULL_DECODE.log")
black=sh(["ffmpeg","-nostdin","-hide_banner","-i",str(f),"-vf","blackdetect=d=0.4:pix_th=0.10:pic_th=0.98","-an","-f","null","-"],out/"BLACK_EVENTS.log")
assert "black_start:" not in black,"Unexpected >=400ms black scene"
silent=sh(["ffmpeg","-nostdin","-hide_banner","-i",str(f),"-af","silencedetect=noise=-50dB:d=0.75","-vn","-f","null","-"],out/"ARTHUR_SILENCE_EVENTS.log")
# Natural VO pauses are expected. Audio hash identity is stronger evidence.
starts=[float(s) for s in re.findall(r"silence_start: ([0-9.]+)",silent)]
assert any(abs(x-968.47)<.2 for x in starts),"Approved end-screen silence moved"
# Source cut frames are inspected from the ACTUAL finished MP4.
early=json.loads((root/"LAKE_PEIGNEUR/PUBLISHING/EDITORIAL_CUT/FIRST_180S_SCRIPT_LOCK.json").read_text())
later=json.loads((root/"LAKE_PEIGNEUR/PUBLISHING/EDITORIAL_CUT/FULL_STORY_SOURCE_CUT_PLAN.json").read_text())
samples=[]
for c in early["changes"]:
 for s in c["segments"]:
  if s["asset"]==c["replace_original"]:continue
  samples.append({"beat":c["beat"],"asset":s["asset"],"frame":s["from"]+25})
for c in later["cuts"]:samples.append({"beat":c["beat"],"asset":c["asset"],"frame":c["frame"]+25})
assert len(samples)==30
stills=out/"frames"
stills.mkdir(exist_ok=True)
for i,r in enumerate(samples):
    ff=str(stills/f"{i+1:02d}_{r['beat']}_{r['asset']}.jpg")
    sh(["ffmpeg","-nostdin","-v","error","-ss",str(r["frame"]/25),"-i",str(f),"-frames:v","1","-vf","scale=640:360","-q:v","3","-y",ff])
    r["image"]=pathlib.Path(ff).name
for start in range(0,len(samples),10):
 sheet=Image.new("RGB",(2*660,5*408),"#171a1c")
 drawer=ImageDraw.Draw(sheet)
 for i,r in enumerate(samples[start:start+10]):
  x=(i%2)*660;y=(i//2)*408
  image=Image.open(stills/r["image"]).convert("RGB")
  sheet.paste(image,(x+9,y+25))
  drawer.text((x+10,y+5),str(r["frame"]/25)+"s "+r["beat"]+" "+r["asset"],fill="#F3EBDD")
 sheet.save(out/f"ACTUAL_MASTER_30_CUTS_{start//10+1}.jpg",quality=87)
(out/"CUT_FRAME_MANIFEST.json").write_text(json.dumps(samples,indent=2))
result={"status":"HIA CANON R15 FULL MASTER TECHNICAL PASS; OWNER EDITORIAL REVIEW STILL OPEN",
 "filename":f.name,"bytes":f.stat().st_size,"sha256":sha(f),
 "duration":float(d["format"]["duration"]),"frames":int(v["nb_frames"]),
 "video":"H264 High, 1920x1080 25fps BT709 limited","audio":"Arthur 48kHz AAC original bitstream (no re-encode)",
 "audio_packet_sha256":audio,"full_decode":"PASS","black_frames_over_0p4s":0,
 "unchanged_arthur_source_sha256":sha(P/"public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3"),
 "unchanged_endscreen_sha256":sha(P/"public/approved_first_end_1080.png"),
 "narration_word_edit":False,"effect_layers_legacy_v4_v7_v8":False,
 "story_beats":87,"physical_slots":141,"source_reuse_max":max(n.values()),
 "actual_final_master_inserted_cuts_sampled":len(samples),
 "human_editorial_approval":"OPEN","youtube_publication":"NOT DONE"}
(out/"TECHNICAL_REPORT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
