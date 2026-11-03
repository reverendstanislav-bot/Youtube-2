from pathlib import Path
import json,csv,shutil,hashlib,xml.etree.ElementTree as E,argparse,math
pa=argparse.ArgumentParser();pa.add_argument("--first60",action="store_true");args=pa.parse_args()
L=Path(r"C:\YOUTUBE\Youtube 2\VIDEO 10");R=L/"IMAGEGEN_FULL_FILM_R2";W=Path(r"C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3");M=W/"MEDIA";M.mkdir(parents=True,exist_ok=True);(W/"RENDERS").mkdir(exist_ok=True)
plan=list(csv.DictReader((R/"SHOT_PLAN_193.csv").open(encoding="utf-8-sig")));queue={x["asset_id"]:x for x in json.loads((R/"GENERATION_QUEUE_ASSEMBLY_R4.json").read_text())};mix=json.loads((L/"AUDIO/FILM_MIX_R3/MIX_MANIFEST.json").read_text());limit=1440 if args.first60 else 21310;voice_end=min(20830,limit)
def cp(src):
 src=Path(src);dest=M/src.name
 if dest.exists() and hashlib.sha256(dest.read_bytes()).digest()!=hashlib.sha256(src.read_bytes()).digest():
  dest=M/(src.stem+'_'+hashlib.sha256(src.read_bytes()).hexdigest()[:12]+src.suffix)
 if not dest.exists():shutil.copy2(src,dest)
 assert hashlib.sha256(dest.read_bytes()).digest()==hashlib.sha256(src.read_bytes()).digest()
 return dest
shots=[]
for row in plan:
 s=int(row["start_frame"]);e=min(int(row["end_frame_exclusive"]),limit)
 if s>=limit:break
 if row["asset_type"]=="NEW_IMAGE":
  q=queue[row["asset_id"]];assert q["status"]=="GENERATED",row["asset_id"];src=R/q["output"]
 else:src=Path(row["existing_path"])
 if row["asset_id"] in ("DOC_HIGHJUMP_P347","DOC_HIGHJUMP_P396"):
  page="347" if row["asset_id"].endswith("347") else "396"
  row["original_document_path"]=str(src)
  src=L/"EDIT_PREP/R5_1/DOCUMENT_FOCUS_R3"/("HIGHJUMP_1947_P"+page+"_FOCUS_R3.png")
 assert src.exists(),src
 shots.append(dict(row,path=str(cp(src)),s=s,e=e))
assert shots[0]["s"]==0 and shots[-1]["e"]==voice_end
assert all(a["e"]==b["s"] for a,b in zip(shots,shots[1:]))
root=E.Element("xmeml",version="5");seq=E.SubElement(root,"sequence",id="VIDEO010_R3");name="VIDEO010_R5_1_FIRST60_R3_CANARY" if args.first60 else "VIDEO010_R5_1_193SHOTS_R3_REVIEW"
def tag(p,n,v):E.SubElement(p,n).text=str(v)
def rate(p,f=24):q=E.SubElement(p,"rate");tag(q,"timebase",f);tag(q,"ntsc","FALSE")
def sc(p):
 s=E.SubElement(p,"samplecharacteristics");rate(s);tag(s,"width",1920);tag(s,"height",1080);tag(s,"pixelaspectratio","square");tag(s,"fielddominance","none")
tag(seq,"name",name);tag(seq,"duration",limit);rate(seq);tc=E.SubElement(seq,"timecode");rate(tc);tag(tc,"string","00:00:00:00");tag(tc,"frame",0);tag(tc,"displayformat","NDF");media=E.SubElement(seq,"media");video=E.SubElement(media,"video");sc(E.SubElement(video,"format"));vt=E.SubElement(video,"track");au=E.SubElement(media,"audio");at=E.SubElement(au,"track");fx=E.SubElement(au,"track");counter=0
# Explicit XML still durations, never native AppendToTimeline five-second defaults.
def clip(track,path,start,end,audio=False,source_end=None,source_fps=24,source_duration=None):
 global counter
 counter+=1;path=Path(path);c=E.SubElement(track,"clipitem",id="clip"+str(counter));tag(c,"name",path.name);tag(c,"duration",source_end or end-start);rate(c,source_fps)
 for k,v in [("start",start),("end",end),("in",0),("out",source_end or end-start)]:tag(c,k,v)
 still=path.suffix.lower() in [".png",".jpg",".jpeg"]
 if still:tag(c,"stillframe","TRUE")
 f=E.SubElement(c,"file",id="file"+str(counter));tag(f,"name",path.name);tag(f,"pathurl",path.as_uri());rate(f,source_fps);d=86400 if still else source_duration or source_end or end-start;tag(f,"duration",d);fm=E.SubElement(f,"media")
 if audio:
  a=E.SubElement(fm,"audio");cs=E.SubElement(a,"samplecharacteristics");tag(cs,"depth",24);tag(cs,"samplerate",48000);tag(a,"channelcount",1);st=E.SubElement(c,"sourcetrack");tag(st,"mediatype","audio");tag(st,"trackindex",1)
 else:v=E.SubElement(fm,"video");tag(v,"duration",d);sc(v)
for row in shots:
 clip(vt,row["path"],row["s"],row["e"]);m=E.SubElement(seq,"marker");tag(m,"name",row["shot_id"]+" "+row["asset_id"]);tag(m,"comment",row["paragraph_id"]+" | "+row["visual_action"]);tag(m,"in",row["s"]);tag(m,"out",row["e"])
if not args.first60:
 end=cp(L/"EDIT_PREP/R5_1/ENDSCREEN_CANDIDATE/VIDEO010_TEXTLESS_20S_1080P25_CANDIDATE.mp4");clip(vt,end,20830,21310,source_end=500,source_fps=25)
clip(at,cp(mix["derived_voice"]),0,voice_end,audio=True,source_duration=20830)
cues=[("WOOD",30),("METAL_SWITCH",122)]
if not args.first60:
 for row in shots:
  a=row["visual_action"].lower()
  if row["paragraph_id"] in ["A04-P05","A04-P09","A05-P08","A07-P05"] and any(k in a for k in ["repair","fuse","electrical"]):cues.append(("METAL_SWITCH",row["s"]+12))
  elif any(k in a for k in ["digging","shovelling","laying"]):cues.append(("SNOW",row["s"]+8))
stems={x["name"]:x for x in mix["sfx"]};events=[]
for typ,start in cues:
 if typ not in stems or start>=limit:continue
 st=stems[typ];d=min(math.floor(st["duration"]*24),limit-start);clip(fx,cp(st["path"]),start,start+d,audio=True);events.append(dict(kind=typ,start=start,end=start+d,source=st["source"]))
xml=W/(name+".xml");E.ElementTree(root).write(xml,encoding="utf-8",xml_declaration=True);(W/(name+"_MANIFEST.json")).write_text(json.dumps(dict(name=name,frames=limit,shots=shots,sfx=events,voice=mix,status="PREVIEW_NOT_FULL_AV_PASS" if args.first60 else "ASSEMBLY_NOT_FINAL_QC"),indent=2));print(json.dumps(dict(xml=str(xml),name=name,frames=limit,video_items=len(shots)+(not args.first60),audio_sfx=len(events))))
