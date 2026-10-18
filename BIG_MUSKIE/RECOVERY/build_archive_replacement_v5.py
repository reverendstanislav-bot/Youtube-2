#!/usr/bin/env python3
"""BIG MUSKIE V5 — replace *all 55* FX001..FX055 primitive vector shots
with production-cleared authentic archival photographic documentary picture.
No full-screen node-diagrams, arrows, orange bar collages or fake pictograms.

Other shots are taken from V4 high-quality no-subtitles work master, without
cropping; approved B051/B052 technical reconstruction and true end hold retained.
Arthur AAC copied from source bit-for-bit. No video/image/voice generation credits.
"""
import collections,csv,hashlib,json,os,pathlib,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image,ImageOps,ImageEnhance

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=pathlib.Path(os.environ["BM_V4_SOURCE"])
ARCHIVE=pathlib.Path(os.environ["BM_V5_ARCHIVE_ROOT"])
WORK=pathlib.Path(os.environ.get("BM_V5_WORK","/tmp/bm_v5"))
OUTPUT=WORK/"BIG_MUSKIE_V5_AUTHENTIC_ARCHIVE_NO_SUBTITLES_1080P25.mp4"
fps=25
total=35660
FACES=WORK/"source_frames"
CLIPS=WORK/"clips"
for p in [WORK,FACES,CLIPS]:p.mkdir(parents=True,exist_ok=True)
# Every asset in the following map has production-cleared NARA/DOE/public-licensed provenance.
# C* refer to southeastern Ohio regional CONTEXT, NOT claimed to depict Big Muskie.
pairs={
"FX001":("R01","R05"),"FX002":("R05","R06"),"FX003":("R09","R06"),"FX004":("C10","C01"),
"FX005":("C07","C10"),"FX006":("C07","C19"),"FX007":("C10","C09"),"FX008":("C02","C19"),
"FX009":("C02","C19"),"FX010":("C19","R01"),"FX011":("C02","R02"),"FX012":("C07","R03"),
"FX013":("R02","R01"),"FX014":("R03","R02"),"FX015":("C19","C02"),"FX016":("R01","R02"),
"FX017":("R03","R01"),"FX018":("R01","R03"),"FX019":("R02","R03"),"FX020":("R03","R05"),
"FX021":("R01","R02"),"FX022":("C19","R03"),"FX023":("C19","C07"),"FX024":("C02","C19"),
"FX025":("R02","C02"),"FX026":("R01","C10"),"FX027":("R03","R02"),"FX028":("R02","R01"),
"FX029":("R03","C10"),"FX030":("R05","C19"),"FX031":("C02","C10"),"FX032":("R01","C19"),
"FX033":("R03","R02"),"FX034":("R03","C02"),"FX035":("R05","R01"),"FX036":("R05","C01"),
"FX037":("R02","R11"),"FX038":("C09","C10"),"FX039":("C02","C12"),"FX040":("R05","R11"),
"FX041":("R05","C01"),"FX042":("C10","C12"),"FX043":("R03","C07"),"FX044":("R03","R05"),
"FX045":("R05","C12"),"FX046":("C12","R06"),"FX047":("R05","C09"),"FX048":("R05","R06"),
"FX049":("R02","R06"),"FX050":("R07","R09"),"FX051":("R10","R09"),"FX052":("R01","C19"),
"FX053":("R06","R07"),"FX054":("R01","R05"),"FX055":("R05","R06")
}
assert len(pairs)==55
CODES=("R01","R02","R03","R05","R06","R07","R09","R10","R11","C01","C02","C07","C09","C10","C12","C19")
def sh(args,timeout=300):
 r=subprocess.run(args,timeout=timeout,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if r.returncode:
  raise RuntimeError("COMMAND FAILED "+ " ".join(map(str,args))[:400] + "\n"+r.stderr[-1200:])
 return r.stdout
def sec(t):
 h,m,s=t.split(":");return round((int(h)*3600+int(m)*60+float(s))*fps)
with (ROOT/"FINAL_ASSET_LOCK/FINAL_116_BEAT_ASSET_LOCK_V1.csv").open(newline="") as f: rows=list(csv.DictReader(f))
assert len(rows)==116
timeline=[]
for i,r in enumerate(rows):
 a=sec(r["start"]);b=sec(rows[i+1]["start"]) if i+1<len(rows) else total
 timeline.append(dict(idx=i+1,first=a,after=b,frames=b-a,asset=r["asset_id"],klass=r["final_class"],beat=r["beat"],purpose=r["shot_lock"]))
assert timeline[0]["first"]==0 and timeline[-1]["after"]==total
assert all(x["after"]==y["first"] for x,y in zip(timeline,timeline[1:]))
oldgfx=[x for x in timeline if x["asset"] in pairs]
assert len(oldgfx)==55,(len(oldgfx),[x["asset"] for x in oldgfx])
assert not any(x["asset"] in pairs for x in timeline if x["asset"] in {"B051_TECH_RECON","B052_TECH_RECON"})
# The intentionally missing RECON B028 in V4 is partially damaged by previous inpainting.
# Here its actual authentic assembly-related archived machinery replaces the damaged pixel source.
OVERRIDES={28:("R01","R03")}
index={}
for code in CODES:
 d=ARCHIVE/"01_PRODUCTION_CLEARED"
 candidates=list(d.rglob(code+"_*.tif"))+list(d.rglob(code+"_*.jpg"))+list(d.rglob(code+"_*.JPG"))
 if not candidates:raise RuntimeError("MISSING VERIFIED PRODUCTION ASSET "+code)
 # Preserve native maximum detail for historical NARA 554830 / 555644.
 index[code]=sorted(candidates,key=lambda p:(p.suffix.lower()!=".tif",len(str(p))))[0]
print("VERIFIED ARCHIVE SOURCES",json.dumps({k:str(v) for k,v in index.items()}),flush=True)
print("REPLACE_COUNT",len(oldgfx), "OLD FX SCENES;",len(OVERRIDES),"ADDITIONAL QUALITY REPAIR",flush=True)
# Camera language varies in focus, speed and cut; not a vector slideshow.
CAMERA=[
 ((0.49,0.49),(0.51,0.50),(0.0,0.0)),
 ((0.35,0.45),(0.52,0.50),(0.0,0.0)),
 ((0.66,0.46),(0.50,0.51),(0.0,0.0)),
 ((0.48,0.34),(0.51,0.55),(0.0,0.0)),
 ((0.51,0.62),(0.49,0.47),(0.0,0.0)),
 ((0.58,0.53),(0.42,0.46),(0.0,0.0))
]
def prep_frame(code,beat_i,shot):
 inpath=index[code]
 # Asymmetric shot designs; editorial camera + crop are selected at prep time.
 style=(beat_i*3+shot*5)%len(CAMERA)
 focal=CAMERA[style][shot%2]
 with Image.open(inpath) as im:
  im=ImageOps.exif_transpose(im).convert("RGB")
  # true full frame with source image (no graphic tile/collage).
  # 2 editorial shots per beat, contrast wide vs detail; unique reframings.
  z=1.045+(0.060 if shot else 0.008)+(.008*(beat_i%4))
  w=int(2068*z);h=int(1164*z)
  out=ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=focal)
  out=ImageEnhance.Color(out).enhance(.91)
  out=ImageEnhance.Contrast(out).enhance(1.065)
  dest=FACES/f"B{beat_i:03d}_S{shot+1}_{code}.jpg"
  out.save(dest,quality=95,subsampling=0,optimize=True)
  return dest

def render_beat(t):
 n=t["frames"];i=t["idx"];outfile=CLIPS/f"{i:03d}.mp4"
 if outfile.exists() and outfile.stat().st_size>150000:
  try:
   p=json.loads(sh(["ffprobe","-v","error","-show_streams","-of","json",str(outfile)],25))
   if int(p["streams"][0].get("nb_frames",0))==n:return (i,outfile.stat().st_size)
  except Exception:pass
 shotpair=pairs.get(t["asset"],OVERRIDES.get(i))
 if shotpair:
  # two different rights-cleared visuals for each replaced FX beat, paced inside narration.
  refs=[prep_frame(code,i,j) for j,code in enumerate(shotpair)]
  n1=max(1,round(n*(.44 if (i%3==0) else .55)))
  n2=n-n1
  if n2<1:raise RuntimeError("Bad duration")
  a=[]
  for j,nframes in enumerate((n1,n2)):
   # move within overscanned genuine photo without expanding subtitles;
   # small, smooth tracking, no brutal screen-wide slides.
   w,h=Image.open(refs[j]).size
   maxx=w-1920;maxy=h-1080
   if (i+j)%4==0:x=f"{maxx}/2 + min(n/{max(1,nframes-1)},1)*{maxx}/5"
   elif (i+j)%4==1:x=f"{maxx}*0.67-min(n/{max(1,nframes-1)},1)*{maxx}/4"
   elif (i+j)%4==2:x=f"{maxx}*0.33+min(n/{max(1,nframes-1)},1)*{maxx}/4"
   else:x=f"{maxx}/2"
   if (i+j)%3==0:y=f"{maxy}*0.60-min(n/{max(1,nframes-1)},1)*{maxy}/5"
   elif (i+j)%3==1:y=f"{maxy}*0.40+min(n/{max(1,nframes-1)},1)*{maxy}/5"
   else:y=f"{maxy}/2"
   a+=["-loop","1","-framerate","25","-t",f"{(nframes+2)/fps:.3f}","-i",str(refs[j])]
   if j==0:filtera=f"[0:v]crop=1920:1080:x='{x}':y='{y}',trim=duration={nframes/fps:.3f},setpts=PTS-STARTPTS,format=yuv420p[a]"
   else:filterb=f"[1:v]crop=1920:1080:x='{x}':y='{y}',trim=duration={nframes/fps:.3f},setpts=PTS-STARTPTS,format=yuv420p[b]"
  # Different handoff per beat, but no distracting repetitive swipe graphics.
  filt=filtera+";"+filterb+";[a][b]concat=n=2:v=1:a=0,format=yuv420p[v]"
  cmd=["ffmpeg","-nostdin","-hide_banner","-v","error","-y",*a,"-filter_complex",filt,"-map","[v]"]
 else:
  cmd=["ffmpeg","-nostdin","-hide_banner","-v","error","-y","-ss",f'{t["first"]/fps:.3f}',"-i",str(SOURCE),"-map","0:v:0"]
 cmd+=["-frames:v",str(n),"-r","25","-fps_mode","cfr","-an","-c:v","libx264","-preset","fast","-crf","13","-threads","2","-pix_fmt","yuv420p","-profile:v","high","-level","4.2","-g","100","-movflags","+faststart",str(outfile)]
 sh(cmd,900)
 return (i,outfile.stat().st_size)
def main():
 assert SOURCE.exists() and SOURCE.stat().st_size==545860241,(str(SOURCE),SOURCE.stat().st_size if SOURCE.exists() else None)
 rev=json.loads(sh(["ffprobe","-v","error","-show_streams","-of","json",str(SOURCE)],80))
 vs=next(x for x in rev["streams"] if x["codec_type"]=="video")
 assert int(vs["nb_frames"])==35660 and vs["width"]==1920 and vs["height"]==1080
 aa=[x for x in rev["streams"] if x["codec_type"]=="audio"];assert len(aa)==1
 usage=collections.Counter()
 for t in timeline:
  if t["asset"] in pairs or t["idx"] in OVERRIDES:
   usage.update(pairs.get(t["asset"],OVERRIDES.get(t["idx"])))
 (WORK/"V5_ASSET_PROVENANCE_QC.json").write_text(json.dumps({
  "source_archive_sha256":"7e453f165e72ad608324fd285195211d8b3eb20d45844b15850ab17ad510c979",
  "target_duration_seconds":1426.4,"original_narration":"Arthur AAC stream copied unchanged",
  "FX_removed":sorted(pairs),"FX_count":len(pairs),
  "also_replaced_problem_scene":sorted(OVERRIDES),
  "rights_held_assets_excluded":["R04","R08","R12","R13"],
  "source_usage_across_replacement_shots":dict(usage),
  "regional_context_not_Big_Muskie":["C01","C02","C07","C09","C10","C12","C19"],
  "new_video_generation":False,"paid_credits":0,
  "shots":[dict(beat=t["beat"],source_pair=list(pairs.get(t["asset"],OVERRIDES.get(t["idx"])))) for t in timeline if t["asset"] in pairs or t["idx"] in OVERRIDES]
 },indent=2))
 start=time.time()
 with ThreadPoolExecutor(max_workers=3) as pool:
  futs=[pool.submit(render_beat,x) for x in timeline]
  done=0
  for f in as_completed(futs):
   i,s=f.result();done+=1
   if done%10==0 or done==len(timeline):print("RENDER V5",done,"/",len(timeline),"elapsed",round(time.time()-start),flush=True)
 mani=WORK/"concat.txt"
 mani.write_text("".join("file '"+str(CLIPS/f"{i:03d}.mp4")+"'\n" for i in range(1,117)))
 silent=WORK/"V5_PICTURE_ONLY.mp4"
 sh(["ffmpeg","-nostdin","-v","error","-y","-f","concat","-safe","0","-i",str(mani),"-c:v","copy","-movflags","+faststart",str(silent)],300)
 sh(["ffmpeg","-nostdin","-v","error","-y","-i",str(silent),"-i",str(SOURCE),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","copy","-t","1426.400","-movflags","+faststart",str(OUTPUT)],300)
 chk=json.loads(sh(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(OUTPUT)],50))
 v=next(x for x in chk["streams"] if x["codec_type"]=="video")
 audio=[x for x in chk["streams"] if x["codec_type"]=="audio"]
 assert int(v["nb_frames"])==total and v["width"]==1920 and v["height"]==1080 and v["r_frame_rate"]=="25/1"
 assert len(audio)==1 and audio[0]["codec_name"]=="aac"
 print("V5 FULL DECODE START",flush=True)
 sh(["ffmpeg","-nostdin","-v","error","-xerror","-i",str(OUTPUT),"-f","null","-"],1800)
 sha=hashlib.sha256()
 with OUTPUT.open("rb") as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b""):sha.update(chunk)
 data={"technical_decode":"PASS","visual_editorial_qc":"REVIEW_REQUIRED","picture_source":"V4 1080p master for unaffected beats; 55 original-GFX beats replaced by approved photo-source clips","replaced_gfx_count":55,"repaired_other":sorted(OVERRIDES),"frames":total,"fps":25,"duration_seconds":1426.4,"bytes":OUTPUT.stat().st_size,"sha256":sha.hexdigest(),"audio_reencoded":False,"new_paid_generations":0}
 (WORK/"FINAL_V5_QC.json").write_text(json.dumps(data,indent=2))
 print("FULL V5 RENDER DONE",json.dumps(data),flush=True)
if __name__=="__main__":main()
