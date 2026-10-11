#!/usr/bin/env python3
"""Technical final master QC and frame evidence. Automated tests are NOT human editorial approval."""
import json, pathlib, subprocess, hashlib, csv, re, collections, sys
from PIL import Image,ImageDraw,ImageOps,ImageChops,ImageStat
root=pathlib.Path.cwd();o=root/"final_qc";o.mkdir(parents=True,exist_ok=True)
master=root/"output/HIA_LAKE_PEIGNEUR_V4_FINAL_UPLOAD_MASTER_1920x1080_25FPS.mp4"
original=root/"output/HIA_LAKE_PEIGNEUR_V4_ACCENTS_REVIEW_MASTER_1080P25.mp4"
p=pathlib.Path(sys.argv[1]); mp=json.loads((p/"public/v4_accents.json").read_text())
j=json.loads((p/"public/timeline.json").read_text())
facts=json.loads((p/"public/facts.json").read_text())
def run(cmd,path=None):
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if path: path.write_text(r.stdout+r.stderr)
 if r.returncode: raise RuntimeError(str(cmd)+" : "+r.stderr[-1600:])
 return r.stdout+r.stderr
def probe(f):
 return json.loads(run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(f)]))
def sha(f):
 h=hashlib.sha256()
 with f.open("rb") as fd:
  for b in iter(lambda:fd.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def audiohash(f):
 p=subprocess.run(["ffmpeg","-v","error","-i",str(f),"-map","0:a:0","-vn","-c:a","copy","-f","adts","-"],capture_output=True,check=True)
 return hashlib.sha256(p.stdout).hexdigest()
assert master.is_file() and original.is_file()
d=probe(master);v=next(x for x in d["streams"] if x["codec_type"]=="video")
a=next(x for x in d["streams"] if x["codec_type"]=="audio")
assert (v["codec_name"],v["profile"],v["width"],v["height"],v["r_frame_rate"],int(v["nb_frames"]))==("h264","High",1920,1080,"25/1",24711),v
assert (v.get("color_primaries"),v.get("color_transfer"),v.get("color_space"),v.get("color_range"))==("bt709","bt709","bt709","tv"),v
assert a['codec_name']=="aac" and a['sample_rate']=="48000",a
assert abs(float(d["format"]["duration"])-988.44)<.16,d["format"]["duration"]
assert not [x for x in d["streams"] if x["codec_type"]=="subtitle"]
assert len(j["beats"])==87 and sum(len(x["slots"]) for x in j["beats"])==99 and len(mp["items"])==100
active=[x for x in mp["items"] if x["effect"] not in ("HOLD","QC_HOLD")]
assert len(active)==36
assert not any(x["asset_id"] in ["LP-GFX-002","LP-GFX-022","LP-GFX-026","LP-REC-005","LP-REC-008","LP-REC-010","LP-REC-012","LP-REC-038","LP-REC-041"] for x in mp["items"])
cnt=collections.Counter(x["asset_id"] for x in mp["items"])
assert max(cnt.values())<=2
assert not re.search(r"<Caption\b|CleanEndScreen", (p/"src/index.jsx").read_text())
ft=json.dumps(facts)
for s in ["~68 ACRES","52 PEOPLE UNDERGROUND","7 DRILL WORKERS","ZERO FATALITIES"]: assert s in ft,s
audio1=audiohash(master);audio2=audiohash(original)
assert audio1==audio2,"Original Arthur AAC bitstream unexpectedly changed!"
run(["ffmpeg","-nostdin","-v","error","-xerror","-i",str(master),"-f","null","-"],o/"FULL_DECODE.log")
black=run(["ffmpeg","-nostdin","-hide_banner","-i",str(master),"-vf","blackdetect=d=0.4:pix_th=0.10:pic_th=0.98","-an","-f","null","-"],o/"BLACKDETECT.log")
assert not re.search("black_start:",black),"Black frames >=0.4 seconds detected; investigate"
sil=run(["ffmpeg","-nostdin","-hide_banner","-i",str(master),"-af","silencedetect=noise=-50dB:d=0.75","-vn","-f","null","-"],o/"SILENCEDETECT.log")
silent_starts=[float(z) for z in re.findall(r"silence_start: ([0-9.]+)",sil)]
assert not any(z<960 for z in silent_starts),("Unexpected narration silence",silent_starts)
stills=o/"stills";stills.mkdir(exist_ok=True)
def take(asset,beat,phase,frame,group):
    t=frame/25
    fn=f"{group}_{asset}_{beat}_{phase}_{frame:05d}.jpg".replace("/","_")
    path=stills/fn
    run(["ffmpeg","-nostdin","-v","error","-ss",f"{t:.4f}","-i",str(master),"-frames:v","1","-q:v","3","-vf","scale=960:-2","-y",str(path)])
    return {"group":group,"asset_id":asset,"beat":beat,"phase":phase,"frame":frame,"seconds":round(t,3),"image":fn,"editorial_qc":"OPEN"}
rows=[]
for x in active:
    a=int(x["accent_in_frame"]);b=int(x["accent_out_frame_exclusive"])-1
    for phase,f in [("start",min(b,a+3)),("middle",(a+b)//2),("end",max(a,b-3))]:
        rows.append(take(x["asset_id"],x["beat_id"],phase,f,"ACCENT"))
rep=json.loads((root/"output/V5_REPLACEMENTS_AND_PROVENANCE.json").read_text())
for x in rep["replacements"]:
    s=next(y for y in mp["items"] if y["beat_id"]==x["beat"] and y["asset_id"]==x["replacement"])
    a=int(s["slot_in_frame"]);b=int(s["slot_out_frame_exclusive"])-1
    for phase,f in [("start",min(b,a+3)),("middle",(a+b)//2),("end",max(a,b-3))]:
        rows.append(take(x["replacement"],x["beat"],phase,f,"REPAIR"))
for s in [0,5,10,30,90,330,460,540,615,750,885,965,970,980,987]:
    rows.append(take("MASTER","",str(s)+"sec",int(s*25),"SAFETY"))
with (o/"FRAME_EVIDENCE_MANIFEST.csv").open("w",newline="") as f:
 writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
for kind in ["ACCENT","REPAIR","SAFETY"]:
    r=[x for x in rows if x["group"]==kind]
    for start in range(0,len(r),20):
        sh=Image.new("RGB",(5*390,4*260),"#171A1C");dr=ImageDraw.Draw(sh)
        for i,x in enumerate(r[start:start+20]):
            pic=Image.open(stills/x["image"]).convert('RGB').resize((385,217))
            px=(i%5)*390;py=(i//5)*260;sh.paste(pic,(px,py))
            dr.text((px+4,py+221),x["asset_id"]+" "+x["phase"],fill="white")
            dr.text((px+4,py+241),str(x["seconds"])+"s "+x["beat"],fill="#E6DDC8")
        sh.save(o/f"{kind}_FRAMES_CONTACT_{start//20+1:02d}.jpg",quality=88)
tech={"verdict":"TECHNICAL MASTER QC PASS. Human editorial/audio listening, source/provenance, YouTube Unlisted still OPEN.",
 "master":master.name,"master_sha256":sha(master),"bytes":master.stat().st_size,
 "frames":24711,"duration_sec":float(d["format"]["duration"]),"video":"H264 High, 1920x1080 25fps BT709 TV range",
 "audio":"Original Arthur AAC stereo 48000 Hz packet-bitstream identical to prior review master","audio_packet_sha256":audio1,
 "no_subtitle_streams":True,"ffmpeg_full_decode":"PASS","black_events_0p4s":0,"unexpected_audio_silences_before_960s":0,
 "accents_sampled":len(active),"repairs_checked":len(rep["replacements"]),"max_reuse":max(cnt.values()),
 "original_endscreen_sha256":rep["unchanged_endscreen_sha256"],"all_87_beats":True,
 "next":"Owner frame/audio listening and Unlisted YouTube transcode review; DO NOT PUBLIC"}
(o/"FINAL_QC_TECHNICAL.json").write_text(json.dumps(tech,indent=2))
print(json.dumps(tech,indent=2))
