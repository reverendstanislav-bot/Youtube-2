#!/usr/bin/env python3
"""Camp Century original-site footage QC pipeline. Requires physical ORIGINAL source binaries.

No source film / content is silently authenticated. A source location and rights receipt
must be signed off independently before an editor shot can be included.
"""
from __future__ import annotations
import argparse, csv, hashlib, itertools, json, math, os, re, shutil, subprocess, sys
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CHAPTER_WORDS = {"CH01":297,"CH02":332,"CH03":336,"CH04":409,"CH05":368,"CH06":441,"CH07":333,"CH08":415}
ALLOW_LOC = {"DIRECT_CAMP_CENTURY","SAME_PROJECT_SUPPLY_CHAIN"}
SOURCES = {
 "F01":{"title":"USACE original color Army Progress Report 6","original_url":"https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34","rights":"ORIGINAL_U.S._ARMY_PD_WORK_VERIFY_INSERTS"},
 "F01B":{"title":"Archive.org DoD color master alternate same content as F01","original_url":"https://archive.org/details/gov.dod.dimoc.26064","rights":"SAME_COLOR_WORK_AS_F01_DEDUP"},
 "F02":{"title":"NARA 111-TV-514 Army Big Picture City Under the Ice","original_url":"https://archive.org/details/gov.archives.arc.2569752","rights":"ORIGINAL_U.S._ARMY_PD_WORK_VERIFY_INSERTS"},
 "F03":{"title":"US Army actual PM-2A dismantling / relocation 1964","original_url":"https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv","rights":"OFFICIAL_DVIDS_PD_ITEM_VERIFY_MEDIA"},
 "F04":{"title":"US Army TV-543 Top of the World real Camp Century sections only","original_url":"https://campcentury.omeka.net/items/show/151","rights":"ORIGINAL_FEDERAL_ARMY_COPY_TO_VERIFY"},
 "F05":{"title":"US Army TV-520 Boy Scout visit real Camp Century only","original_url":"https://campcentury.omeka.net/items/show/144","rights":"ORIGINAL_FEDERAL_ARMY_COPY_TO_VERIFY"},
 "F06":{"title":"US Army TV-781 later partly reused actual Camp Century","original_url":"https://campcentury.omeka.net/items/show/161","rights":"ORIGINAL_FEDERAL_ARMY_COPY_TO_VERIFY"}
}
HEADERS=["scene_id","source_id","start_tc","end_tc","chapter","beat","site_class","actual_shot_description","rights_receipt","verified_by","status","duplicate_of","cut_filename","cut_sha256","cut_seconds","native_width","native_height","source_sha256"]

def process(args:list[str], *, check=True) -> subprocess.CompletedProcess:
    p=subprocess.run(args,capture_output=True,text=True)
    if check and p.returncode:raise RuntimeError(f"Exit {p.returncode}: {' '.join(args)}\n{p.stderr[-1400:]}")
    return p

def probe(src:Path)->dict:
    p=process(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(src)])
    return json.loads(p.stdout)

def digest(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(4<<20),b""):h.update(chunk)
    return h.hexdigest()

def parse_seconds(tc:str)->float:
    st=(tc or "").strip()
    if re.fullmatch(r"\d+(?:\.\d+)?",st):return float(st)
    pieces=st.split(":")
    if len(pieces) not in (2,3):raise ValueError(f"Bad timecode '{tc}', expected 00:00:00.000")
    if len(pieces)==2: pieces=["0"]+pieces
    h,m,s=map(float,pieces)
    if m>=60 or s>=60 or any(a<0 for a in [h,m,s]):raise ValueError(tc)
    return h*3600+m*60+s

def nice_time(t:float)->str:
    return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}"

def video_info(meta:dict)->dict:
    streams=[s for s in meta.get("streams",[]) if s.get("codec_type")=="video"]
    if not streams:raise ValueError("Not a video file")
    v=streams[0]
    return {"duration":float(meta.get("format",{}).get("duration") or v.get("duration") or 0),"width":int(v.get("width") or 0),"height":int(v.get("height") or 0),"fps":v.get("avg_frame_rate"),"pix_fmt":v.get("pix_fmt"),"field_order":v.get("field_order"),"sample_aspect_ratio":v.get("sample_aspect_ratio"),"video_codec":v.get("codec_name"),"audio_tracks":sum(1 for s in meta.get("streams",[]) if s.get("codec_type")=="audio")}

def init(root:Path):
    for sub in ["masters","clips","qc_sheets","reports","rights_receipts"]:(root/sub).mkdir(parents=True,exist_ok=True)
    out=root/"approved_ranges.csv"
    if not out.exists():
        with out.open("w",newline="",encoding="utf-8") as f:csv.DictWriter(f,fieldnames=HEADERS).writeheader()
    (root/"reports"/"SOURCE_CATALOG.json").write_text(json.dumps(SOURCES,indent=2),encoding="utf-8")
    return out

def load_sources(root:Path)->dict[str,Path]:
    # Users place physical authentic reels on disk, using F01.mp4 or F02.mpeg etc.
    ans={}
    for source in SOURCES:
        paths=[p for p in (root/"masters").glob(source+".*") if p.suffix.lower() in {".mp4",".mpeg",".mpg",".mov",".mkv"}]
        if len(paths)>1:raise ValueError(f"Ambiguous masters for {source}: {paths}")
        if paths:ans[source]=paths[0]
    return ans

def audit(root:Path, full_decode=False):
    init(root); originals=load_sources(root)
    report=[]
    for code,file in originals.items():
        p=probe(file);vi=video_info(p)
        ok="PROBE_PASS"
        if full_decode:
            dec=process(["ffmpeg","-nostdin","-v","error","-i",str(file),"-map","0:v:0","-an","-f","null","-"],check=False)
            ok="FULL_DECODE_PASS" if dec.returncode==0 else "DECODE_FAILED"
        report.append({"source_id":code,"path":str(file),"size_bytes":file.stat().st_size,"sha256":digest(file),"status":ok,**vi})
        print(code,ok,vi["duration"],vi["width"],vi["height"])
    with (root/"reports"/"physical_originals.json").open("w") as f:json.dump(report,f,indent=2)
    for sid in sorted(set(SOURCES)-set(originals)):print("NOT_ACQUIRED",sid,SOURCES[sid]["original_url"])
    return report

def sheets(root:Path,interval=20,cols=5,per_sheet=25):
    init(root)
    originals=load_sources(root)
    try:font=ImageFont.truetype("DejaVuSans.ttf",18)
    except Exception:font=ImageFont.load_default()
    for src_id,src in originals.items():
        duration=video_info(probe(src))["duration"]
        if not duration:print("SKIP_BAD_DURATION",src_id);continue
        temp=root/"qc_sheets"/f"_{src_id}_temp";temp.mkdir(parents=True,exist_ok=True)
        # time-text burned on SCREENING CONTACT SHEET ONLY, never the footage itself.
        cmd=["ffmpeg","-nostdin","-hide_banner","-loglevel","error","-i",str(src),"-an","-vf",f"fps=1/{interval},scale=320:-2", "-q:v","3","-y",str(temp/"frame_%06d.jpg")]
        process(cmd)
        frames=sorted(temp.glob("frame_*.jpg"))
        for start in range(0,len(frames),per_sheet):
            chunk=frames[start:start+per_sheet]
            canv=Image.new("RGB",(cols*330, math.ceil(len(chunk)/cols)*220),(22,22,22))
            drawer=ImageDraw.Draw(canv)
            for pos,path in enumerate(chunk):
                k=start+pos
                with Image.open(path) as frame:
                    f=frame.convert("RGB");f.thumbnail((318,184))
                    x=(pos%cols)*330+4;y=(pos//cols)*220+3
                    canv.paste(f,(x,y))
                drawer.text((x,y+187),f"{src_id} ~{nice_time(k*interval)}",fill="white",font=font)
            dest=root/"qc_sheets"/f"{src_id}_sheet_{start//per_sheet+1:03d}.jpg"
            canv.save(dest,quality=90)
        for item in frames:item.unlink()
        temp.rmdir()
        print("SHEETS",src_id,"frames",len(frames),"approx_times_only; inspect real movie in/out")

def read_rows(file:Path)->list[dict]:
    with file.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def write_rows(file:Path,rows:list[dict],fields:list[str]):
    with file.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)

def extract(root:Path):
    init(root);files=load_sources(root)
    records=read_rows(root/"approved_ranges.csv")
    audit_path=root/"reports"/"physical_originals.json"
    if records and not audit_path.exists():
        raise ValueError("First run audit --full-decode. No unverified source may be cut")
    audited={r["source_id"]:r for r in json.loads(audit_path.read_text(encoding="utf-8"))} if audit_path.exists() else {}
    if not records:
        print("NO_APPROVED_SHOTS: empty CSV (correct until an editor watches and signs real source timecodes)")
        summarize(root,records)
        return
    done=[];errors=[]
    approved_ids=[q.get("scene_id") for q in records if q.get("status")=="APPROVED"]
    if len(approved_ids)!=len(set(approved_ids)):
        raise ValueError("Duplicate scene_id in approved_ranges.csv")
    for row in records:
        sid=row.get("scene_id","").strip();src=row.get("source_id","").strip()
        try:
            if row.get("status","").strip() != "APPROVED":
                row["status"]="NOT_APPROVED";done.append(row);continue
            if not sid or not re.fullmatch(r"[A-Za-z0-9_-]{3,60}",sid):raise ValueError("Invalid scene ID")
            if src not in files:raise ValueError("Source binary missing")
            prior=audited.get(src)
            if not prior or prior.get("status")!="FULL_DECODE_PASS":
                raise ValueError("Full physical source decode QC not PASS")
            if digest(files[src])!=prior.get("sha256"):
                raise ValueError("Original source SHA256 changed since audit")
            if row.get("site_class") not in ALLOW_LOC:raise ValueError("Other-site/context footage forbidden")
            if not row.get("actual_shot_description") or not row.get("verified_by") or not row.get("rights_receipt"):
                raise ValueError("Missing manual subject/rights/verification evidence")
            evidence=Path(row["rights_receipt"])
            if not evidence.is_absolute(): evidence=root/"rights_receipts"/evidence
            if not evidence.is_file() or evidence.stat().st_size<30:
                raise ValueError("Missing actual rights receipt text file")
            if not row.get("beat","").strip().startswith("CC07-S4-"):
                raise ValueError("Beat ID must match locked Stage04 V4 manifest")
            if row.get("duplicate_of"):raise ValueError("Already declared duplicate")
            if row.get("chapter") not in CHAPTER_WORDS:raise ValueError("Invalid V4 chapter")
            st=parse_seconds(row.get("start_tc",""));en=parse_seconds(row.get("end_tc",""));length=en-st
            if not 4.99<=length<=20.01:raise ValueError(f"Rejected {length:.2f}s: require 5–20 sec of real continuous action")
            vi=video_info(probe(files[src]))
            if en>vi["duration"]+0.1:raise ValueError("IN/OUT outside source duration")
            dst=root/"clips"/(sid+".mp4")
            if dst.exists():raise ValueError("Existing clip, will not silently overwrite")
            # Accurate seek relative to input, preserve correct 4:3 source aspect rather than stretching.
            cmd=["ffmpeg","-nostdin","-v","error","-i",str(files[src]),"-ss",f"{st:.3f}","-t",f"{length:.3f}","-map","0:v:0","-an","-c:v","libx264","-preset","fast","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart",str(dst)]
            process(cmd)
            rendered=video_info(probe(dst))
            if abs(rendered["duration"]-length)>0.18:
                dst.unlink();raise ValueError("Decoded clip duration differs significantly from approved timecodes")
            row.update({"cut_filename":str(dst),"cut_sha256":digest(dst),"cut_seconds":f"{rendered['duration']:.3f}","native_width":vi["width"],"native_height":vi["height"],"source_sha256":digest(files[src]),"status":"PHYSICALLY_EXTRACTED_PENDING_DUP_QC"})
            done.append(row);print("EXTRACTED",sid,src,st,en,rendered["duration"])
        except Exception as e:
            row["status"]="ERROR_HOLD";done.append(row);errors.append({"scene_id":sid,"why":str(e)});print("ERROR",sid,str(e))
    write_rows(root/"reports"/"extraction_results.csv",done,HEADERS)
    (root/"reports"/"extraction_errors.json").write_text(json.dumps(errors,indent=2),encoding="utf-8")
    summarize(root,done)

def dhash(frame)->int:
    import cv2
    gry=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    scaled=cv2.resize(gry,(9,8),interpolation=cv2.INTER_AREA)
    bits=scaled[:,1:]>scaled[:,:-1]
    num=0
    for flag in bits.flat:num=(num<<1)|int(flag)
    return num

def get_clip_hashes(file:Path):
    import cv2
    cap=cv2.VideoCapture(str(file))
    if not cap.isOpened():raise ValueError(f"unreadable video {file}")
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));result=[]
    for fraction in [0.2,0.5,0.8]:
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(max(0,count-1)*fraction))
        ok,fr=cap.read()
        if ok:result.append(dhash(fr))
    cap.release()
    if len(result)!=3:raise ValueError(f"missing frames for {file}")
    return result

def duplicate_suggestions(root:Path):
    f=root/"reports"/"extraction_results.csv"
    if not f.exists():print("NO_EXTRACTS_TO_COMPARE");return
    rows=[r for r in read_rows(f) if r.get("cut_filename") and Path(r["cut_filename"]).exists()]
    hashes={}
    for r in rows:
        try:hashes[r["scene_id"]]=get_clip_hashes(Path(r["cut_filename"]))
        except Exception as e:print("HASH_HOLD",r["scene_id"],e)
    suggestions=[]
    for a,b in itertools.combinations(rows,2):
        if a["scene_id"] not in hashes or b["scene_id"] not in hashes:continue
        ha,hb=hashes[a["scene_id"]],hashes[b["scene_id"]]
        same_time_dist=sum((x^y).bit_count() for x,y in zip(ha,hb))/3
        best=min((x^y).bit_count() for x in ha for y in hb)
        if best<=12 or same_time_dist<=17:
            suggestions.append({"scene_A":a["scene_id"],"source_A":a["source_id"],"scene_B":b["scene_id"],"source_B":b["source_id"],"min_dhash_dist":best,"avg_sync_dist":round(same_time_dist,1),"outcome":"REVIEW_MANUALLY_NOT_AUTO_DUPLICATE"})
    cols=["scene_A","source_A","scene_B","source_B","min_dhash_dist","avg_sync_dist","outcome"]
    write_rows(root/"reports"/"duplicate_suggestions.csv",suggestions,cols)
    print("DUP_SUGGESTIONS",len(suggestions),"human confirmation required (color vs B/W and cropping can break automation)")

def summarize(root:Path,rows:list[dict]|None=None):
    if rows is None:
        final=root/"reports"/"final_verified_clips.csv"
        preliminary=root/"reports"/"extraction_results.csv"
        p=final if final.exists() else preliminary
        rows=read_rows(p) if p.exists() else []
        if p==final: rows=[x for x in rows if x.get("status")=="FINAL_APPROVED_NO_DUP"]
    counts=defaultdict(lambda:{"direct_sec":0.0,"own_supply_sec":0.0,"clips":0})
    for row in rows:
        if row.get("status") not in {"PHYSICALLY_EXTRACTED_PENDING_DUP_QC","FINAL_APPROVED_NO_DUP"}:continue
        if row.get("duplicate_of"):continue
        c=row.get("chapter")
        if c not in CHAPTER_WORDS:continue
        secs=float(row.get("cut_seconds") or 0)
        field="direct_sec" if row.get("site_class")=="DIRECT_CAMP_CENTURY" else "own_supply_sec"
        counts[c][field]+=secs;counts[c]["clips"]+=1
    report=[]
    lines=["# Camp Century Stage 06 — physical original footage coverage","","Only physical, editor-qualified clips count. Pending duplicates must be confirmed; this is not final release PASS.","", "| Chapter | VO estimate @145wpm | Direct site motion | Project supply chain motion | Unique clips pre-dedup |", "|---|---:|---:|---:|---:|"]
    for ch,words in CHAPTER_WORDS.items():
        d=counts[ch]
        report.append({"chapter":ch,"narration_words":words,"estimated_speech_seconds_145wpm":round(words*60/145,1),"physical_direct_sec":round(d["direct_sec"],2),"physical_supply_sec":round(d["own_supply_sec"],2),"prelim_clips":d["clips"]})
        lines.append(f"| {ch} | {words*60/145:.1f}s | {d['direct_sec']:.1f}s | {d['own_supply_sec']:.1f}s | {d['clips']} |")
    direct=sum(x["physical_direct_sec"] for x in report);supply=sum(x["physical_supply_sec"] for x in report)
    lines.extend(["",f"**Direct physically extracted video:** {direct:.1f}s.",f"**Own project supply footage:** {supply:.1f}s.",f"**Total preliminary moving footage:** {direct+supply:.1f}s (**before confirmed cross-film duplicate removal**).", "", "**GO/NO-GO:** HOLD until every clip is confirmed visually as Camp Century or the exact supply mission, scene-level rights checked, cross-film dupes resolved, and sufficient unique matching footage verified. No voice generation."])
    (root/"reports"/"coverage_by_chapter.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    (root/"reports"/"coverage_by_chapter.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("COVERAGE_PRELIM_DIRECT",direct,"SUPPLY",supply,"STATUS_HOLD")


def finalize(root:Path):
    """Separate human editorial signoff of factual location, rights and duplicates."""
    p=root/"reports"/"extraction_results.csv"
    reviews=root/"final_review.csv"
    if not p.exists():raise ValueError("First run cut on physically decoded originals")
    if not reviews.exists():
        with reviews.open("w",encoding="utf-8",newline="") as f:
            cols=["scene_id","site_verified_by","rights_verified_by","duplicate_reviewed_by","decision","duplicate_of"]
            csv.DictWriter(f,fieldnames=cols).writeheader()
        raise ValueError("Fill final_review.csv after reviewing ALL extracted real scenes")
    rows=read_rows(p)
    decisions={x["scene_id"]:x for x in read_rows(reviews)}
    accepted=0
    for row in rows:
        if row.get("status")!="PHYSICALLY_EXTRACTED_PENDING_DUP_QC":continue
        rev=decisions.get(row["scene_id"],{})
        if rev.get("decision")=="REJECT":row["status"]="REJECTED_AFTER_FINAL_QC";continue
        if rev.get("decision")=="DUPLICATE":
            if not rev.get("duplicate_of"):raise ValueError("DUPLICATE must identify duplicate_of")
            row["duplicate_of"]=rev["duplicate_of"]
            row["status"]="CONFIRMED_DUPLICATE_EXCLUDED"
            continue
        if rev.get("decision")!="APPROVE_UNIQUE":continue
        if not all(rev.get(k,"").strip() for k in ["site_verified_by","rights_verified_by","duplicate_reviewed_by"]):
            raise ValueError(f"Missing three independent review labels for {row['scene_id']}")
        clip=Path(row["cut_filename"])
        if not clip.is_file() or digest(clip)!=row.get("cut_sha256"):
            raise ValueError(f"Missing or changed physical clip {row['scene_id']}")
        row["status"]="FINAL_APPROVED_NO_DUP";accepted+=1
    write_rows(root/"reports"/"final_verified_clips.csv",rows,HEADERS)
    summarize(root,[x for x in rows if x.get("status")=="FINAL_APPROVED_NO_DUP"])
    print("FINAL_ACCEPTED_UNIQUE",accepted,"Not proof of sufficient coverage by itself")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cmd",choices=["init","audit","sheets","cut","duplicates","finalize","report"])
    parser.add_argument("--root",required=True,type=Path,help="Working directory containing masters/F01.mp4 etc")
    parser.add_argument("--full-decode",action="store_true",help="Decode every frame (can be slow)")
    parser.add_argument("--sample-interval",type=int,default=20)
    a=parser.parse_args();root=a.root.resolve()
    if a.cmd=="init": print("READY",init(root))
    elif a.cmd=="audit":audit(root,a.full_decode)
    elif a.cmd=="sheets":sheets(root,interval=a.sample_interval)
    elif a.cmd=="cut":extract(root)
    elif a.cmd=="duplicates":duplicate_suggestions(root)
    elif a.cmd=="finalize":finalize(root)
    elif a.cmd=="report":summarize(root)
if __name__=="__main__":main()
