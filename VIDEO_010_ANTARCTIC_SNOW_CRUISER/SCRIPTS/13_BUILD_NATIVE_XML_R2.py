from pathlib import Path
import json,csv,xml.etree.ElementTree as E
W=Path(r"C:\Users\KK\Movies\HIA_VIDEO010_ASSEMBLY_R1")
R=Path(r"C:\Users\KK\Youtube-2-editorial-lock-20261102\VIDEO_010_ANTARCTIC_SNOW_CRUISER")
A=Path(r"C:\YOUTUBE\Youtube 2\VIDEO 10\AUDIO\R5_1_MASTER_QC")
paths=json.loads((W/"MEDIA_PATHS.json").read_text());audio=list(csv.DictReader((A/"PARAGRAPH_AUDIO_TIMING.csv").open(encoding="utf-8-sig")));beats=list(csv.DictReader((R/"11_VISUAL_BEATS_R5_1.csv").open(encoding="utf-8-sig")))
def tag(p,n,v):E.SubElement(p,n).text=str(v)
def rate(p,fps=24):q=E.SubElement(p,"rate");tag(q,"timebase",fps);tag(q,"ntsc","FALSE")
def characteristics(p):
 s=E.SubElement(p,"samplecharacteristics");rate(s);tag(s,"width",1920);tag(s,"height",1080);tag(s,"pixelaspectratio","square");tag(s,"fielddominance","none")
root=E.Element("xmeml",version="5");seq=E.SubElement(root,"sequence",id="VIDEO010_R2");tag(seq,"name","VIDEO010_R5_1_ASSEMBLY_R2_COVERAGE_HOLD");voice_end=round(float(audio[-1]["end_seconds"])*24);tag(seq,"duration",voice_end+480);rate(seq);tc=E.SubElement(seq,"timecode");rate(tc);tag(tc,"string","00:00:00:00");tag(tc,"frame",0);tag(tc,"displayformat","NDF");media=E.SubElement(seq,"media");video=E.SubElement(media,"video");characteristics(E.SubElement(video,"format"));vt=E.SubElement(video,"track");at=E.SubElement(E.SubElement(media,"audio"),"track");shots=[];gaps=[];count=0
# Explicit XML durations avoid Resolve AppendToTimeline's five-second still cap.
def clip(track,aid,start,end,source_end=None,source_fps=24,audio_only=False):
 global count
 count+=1;c=E.SubElement(track,"clipitem",id="clip"+str(count));tag(c,"name",Path(paths[aid]).name);tag(c,"duration",source_end or end-start);rate(c,source_fps)
 for k,v in [("start",start),("end",end),("in",0),("out",source_end or end-start)]:tag(c,k,v)
 still=Path(paths[aid]).suffix.lower() in [".jpg",".png",".jpeg"]
 if still:tag(c,"stillframe","TRUE")
 f=E.SubElement(c,"file",id="file"+str(count));tag(f,"name",Path(paths[aid]).name);tag(f,"pathurl",Path(paths[aid]).as_uri());rate(f,source_fps);tag(f,"duration",86400 if still else (source_end or end-start));fm=E.SubElement(f,"media")
 if audio_only:
  au=E.SubElement(fm,"audio");sc=E.SubElement(au,"samplecharacteristics");tag(sc,"depth",24);tag(sc,"samplerate",48000);tag(au,"channelcount",1);src=E.SubElement(c,"sourcetrack");tag(src,"mediatype","audio");tag(src,"trackindex",1)
 else:
  v=E.SubElement(fm,"video");tag(v,"duration",86400 if still else (source_end or end-start));characteristics(v)
 return c
for b,a in zip(beats,audio):
 assert b["paragraph_id"]==a["paragraph_id"]
 s=round(float(a["start_seconds"])*24);e=round(float(a["end_seconds"])*24);ids=[x for x in b["primary_ready_asset_ids"].split(";") if x in paths]
 if not ids:gaps.append(dict(paragraph_id=b["paragraph_id"],start=s,end=e,need=b["required_graphic_or_held_source"],reason=b["purpose"]))
 for j,aid in enumerate(ids):
  cs=s+round((e-s)*j/len(ids));ce=s+round((e-s)*(j+1)/len(ids));native=24;sf=None
  if Path(paths[aid]).suffix.lower()==".mp4":
   import subprocess
   probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=r_frame_rate,nb_frames","-of","json",paths[aid]]));st=probe["streams"][0];n,d=st["r_frame_rate"].split("/");native=round(int(n)/int(d));sf=min(int(st["nb_frames"]),round((ce-cs)*native/24));ce=cs+round(sf*24/native)
   if ce<e:gaps.append(dict(paragraph_id=b["paragraph_id"],start=ce,end=e,need="CONTEXT_CLIP_TOO_SHORT",reason=b["purpose"]))
  clip(vt,aid,cs,ce,sf,native);shots.append(dict(paragraph_id=b["paragraph_id"],asset_id=aid,start=cs,end=ce,source_limit=b["director_limit"]))
 m=E.SubElement(seq,"marker");tag(m,"name",b["paragraph_id"]);tag(m,"comment",b["purpose"]+" | "+b["director_limit"]);tag(m,"in",s);tag(m,"out",e)
clip(vt,"ENDSCREEN",voice_end,voice_end+480,500,25);clip(at,"VOICE_MASTER",0,voice_end,audio_only=True)
x=W/"VIDEO010_R5_1_ASSEMBLY_R2.xml";E.ElementTree(root).write(x,encoding="utf-8",xml_declaration=True)
(W/"R2_SHOT_MANIFEST.json").write_text(json.dumps(shots,indent=2));(W/"R2_COVERAGE_GAPS.json").write_text(json.dumps(gaps,indent=2));print(json.dumps(dict(xml=str(x),shots=len(shots),gaps=len(gaps),uncovered_seconds=sum(g["end"]-g["start"] for g in gaps)/24,voice_frames=voice_end,total_frames=voice_end+480)))
