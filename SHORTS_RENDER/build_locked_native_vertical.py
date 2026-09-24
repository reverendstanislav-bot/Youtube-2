#!/usr/bin/env python3
import argparse, json, subprocess, re, hashlib
from pathlib import Path
from PIL import Image

FPS_DEFAULT=25
ORANGE_ASS="&H003A8AF2&"
WHITE_ASS="&H00FFFFFF&"

GFX_REPLACEMENTS={
    ("CHI-S02","origin"):("A08_IllinoisTelephoneAndTelegraphAd.png",0.50,""),
    ("CHI-S02","evidence_uncertain"):("A05_IllinoisTunnelConstruction.jpg",0.50,"HISTORICAL SOURCE"),
    ("CHI-S02","gauge"):("A07_IllinoisTunnelTestTrain.jpg",0.50,"HISTORICAL SOURCE"),
    ("CHI-S03","obsolescence"):("A14_LOC_State_Street_1905_full_archive.png",0.50,"HISTORICAL SOURCE"),
    ("CHI-S04","network_flood"):("A02_IllinoisTunnelMap1910.png",0.50,"HISTORICAL SOURCE"),
    ("CHI-S05","court_allegation"):("S181_P122.png",0.50,""),
    ("CHI-S05","court_correction"):("S183_P124.png",0.50,""),
    ("TC497-S03","road_compare"):("V2_DUNE.png",0.50,""),
    ("TC497-S04","army1961_excerpt"):("V4_NUKE_TECH.png",0.50,""),
    ("TC497-S05","terrain_river"):("V2_DUNE.png",0.42,""),
    ("TC497-S05","terrain_ridge"):("V3_DUNE_LIMIT.png",0.56,""),
    ("TC497-S05","terrain_soft ground"):("V3_YUMA_TEST.png",0.48,""),
    ("TC497-S05","terrain_dunes"):("V2_DUNE.png",0.58,""),
}

def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:
        print(p.stdout)
        print(p.stderr[-12000:])
        raise subprocess.CalledProcessError(p.returncode,cmd)
    return p

def at(t):
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    s=int(t); cs=int(round((t-s)*100))
    if cs>=100: s+=1; cs-=100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def esc(s):
    return str(s).replace("\\",r"\\").replace("{",r"\{").replace("}",r"\}")

def normalize_words(words,replacements):
    out=[]
    for w in words:
        x=dict(w)
        token=str(x.get("w",""))
        if token in replacements: token=replacements[token]
        x["w"]=token
        out.append(x)
    merged=[]; i=0
    while i<len(out):
        cur=dict(out[i])
        if i+1<len(out) and str(out[i+1]["w"]).startswith("-") and cur["w"]:
            cur["w"]=cur["w"]+str(out[i+1]["w"])
            cur["short_e"]=out[i+1]["short_e"]
            merged.append(cur); i+=2
        else:
            merged.append(cur); i+=1
    return merged

def caption_groups(words):
    groups=[]; buf=[]
    def flush():
        nonlocal buf
        if buf: groups.append(buf); buf=[]
    for w in words:
        if buf and float(w["short_s"])-float(buf[-1]["short_e"])>0.38: flush()
        buf.append(w)
        chars=sum(len(str(x["w"]))+1 for x in buf)
        punct=str(w["w"]).rstrip('"”').endswith((".","!","?"))
        if len(buf)>=6 or chars>=34 or punct: flush()
    flush()
    return groups

def balanced_split(g):
    if len(g)<=3: return len(g)
    total=sum(len(str(x["w"]))+1 for x in g)
    best=(10**9,len(g))
    for i in range(1,len(g)):
        left=sum(len(str(x["w"]))+1 for x in g[:i])
        score=abs(left-(total-left))
        if score<best[0]: best=(score,i)
    return best[1]

def resolve_segment(short_id,seg):
    if seg.get("gfx_type"):
        key=(short_id,str(seg["gfx_type"]).lower())
        if key not in GFX_REPLACEMENTS:
            raise RuntimeError(f"No clean replacement for {key}")
        asset,x,prov=GFX_REPLACEMENTS[key]
        return asset,x,prov
    prov="HISTORICAL SOURCE" if seg.get("provenance")=="HISTORICAL SOURCE" else ""
    return seg["asset"],float(seg.get("x",0.5)),prov

def build_ass(short,plan,out):
    replacements=plan.get("caption_replacements",{})
    words=normalize_words(short["source_words"],replacements)
    header=r'''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,62,&H00FFFFFF,&H00FFFFFF,&H00110A05,&H00000000,-1,0,0,0,100,100,0,0,1,5,2,2,90,90,390,1
Style: Hist,DejaVu Sans,28,&H00DDE6F3,&H00DDE6F3,&H00110A05,&H00000000,-1,0,0,0,100,100,2,0,1,3,1,9,40,44,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events=[]
    for group in caption_groups(words):
        split=balanced_split(group) if sum(len(str(x["w"]))+1 for x in group)>21 else len(group)
        for ai,a in enumerate(group):
            parts=[]
            for i,w in enumerate(group):
                tok=esc(w["w"])
                if i==ai: tok=r"{\c&H003A8AF2&}"+tok+r"{\c&H00FFFFFF&}"
                parts.append(tok)
            body=(" ".join(parts[:split])+r"\N"+" ".join(parts[split:])) if split<len(parts) else " ".join(parts)
            start=float(a["short_s"])
            nxt=float(group[ai+1]["short_s"]) if ai+1<len(group) else float(a["short_e"])+.08
            events.append([start,nxt,f"Dialogue: 10,{at(start)},{at(nxt)},Cap,,0,0,0,,{body}"])
    # Exactly one HISTORICAL SOURCE event per verified historical segment.
    for seg in plan["segments"]:
        asset,x,prov=resolve_segment(plan["id"],seg)
        if prov=="HISTORICAL SOURCE":
            s=float(seg["out_start"]); e=min(float(seg["out_end"]),s+1.5)
            events.append([s,e,f"Dialogue: 20,{at(s)},{at(e)},Hist,,0,0,0,,— HISTORICAL SOURCE"])
    events.sort(key=lambda x:(x[0],x[1],0 if ",Cap," in x[2] else 1))
    out.write_text(header+"\n".join(x[2] for x in events)+"\n",encoding="utf-8")
    return {"caption_words":len(words),"historical_events":sum(1 for x in events if ",Hist," in x[2])}

def make_gradient(path):
    W,H=1080,1920
    img=Image.new("RGBA",(W,H),(0,0,0,0)); px=img.load()
    fade_start=1340; solid_start=1500; amax=245
    for y in range(fade_start,H):
        a=amax if y>=solid_start else int(amax*(((y-fade_start)/(solid_start-fade_start))**1.2))
        for x in range(W): px[x,y]=(0,0,0,a)
    img.save(path)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--plan",required=True)
    ap.add_argument("--map",required=True)
    ap.add_argument("--asset-dir",required=True)
    ap.add_argument("--audio-source",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--qc",required=True)
    args=ap.parse_args()

    plan=json.loads(Path(args.plan).read_text(encoding="utf-8"))
    mapping=json.loads(Path(args.map).read_text(encoding="utf-8"))
    short=next(x for x in mapping["shorts"] if x["id"]==plan["id"])
    fps=int(plan.get("fps",mapping.get("source_fps",FPS_DEFAULT)))
    duration=float(short["duration_sec"])
    qc=Path(args.qc); qc.mkdir(parents=True,exist_ok=True)
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    ass=qc/f"{plan['id']}.ass"
    assqc=build_ass(short,plan,ass)
    gradient=qc/"bottom_gradient.png"; make_gradient(gradient)

    inputs=[]; filters=[]; labels=[]
    for i,seg in enumerate(plan["segments"]):
        dur=float(seg["out_end"])-float(seg["out_start"])
        asset,x,prov=resolve_segment(plan["id"],seg)
        p=Path(args.asset_dir)/asset
        if not p.exists(): raise FileNotFoundError(p)
        inputs += ["-loop","1","-framerate",str(fps),"-t",f"{dur:.3f}","-i",str(p)]
        # Static full-screen portrait reframe only. No push/pan/zoom.
        cropx=f"(iw-ih*9/16)*{max(0,min(1,x)):.4f}"
        filters.append(
            f"[{i}:v]scale=-2:1080:flags=lanczos,crop=ih*9/16:ih:x='{cropx}':y=0,"
            f"scale=1080:1920:flags=lanczos,fps={fps},setsar=1,format=yuv420p[v{i}]"
        )
        labels.append(f"[v{i}]")
    n=len(plan["segments"])
    inputs += ["-loop","1","-framerate",str(fps),"-t",f"{duration:.3f}","-i",str(gradient)]
    grad_idx=n
    # Audio is already the exact Short cut from the GitHub 10-pack.
    inputs += ["-t",f"{duration:.3f}","-i",args.audio_source]
    audio_idx=n+1
    filters.append("".join(labels)+f"concat=n={n}:v=1:a=0[base]")
    filters.append(f"[{grad_idx}:v]format=rgba[grad]")
    filters.append("[base][grad]overlay=0:0:shortest=1[shade]")
    assp=str(ass).replace(":",r"\:")
    filters.append(f"[shade]ass='{assp}':fontsdir='/usr/share/fonts/truetype/dejavu'[vout]")

    cmd=["ffmpeg","-y","-hide_banner","-loglevel","error",*inputs,
         "-filter_complex",";".join(filters),"-map","[vout]","-map",f"{audio_idx}:a:0",
         "-r",str(fps),"-c:v","libx264","-preset","medium","-crf","17","-profile:v","high","-pix_fmt","yuv420p",
         "-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-movflags","+faststart",str(out)]
    run(cmd)
    run(["ffmpeg","-v","error","-xerror","-i",str(out),"-f","null","-"])
    probe=json.loads(run(["ffprobe","-v","error","-show_entries",
        "stream=codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels:format=duration,size",
        "-of","json",str(out)]).stdout)
    qcdata={
      "id":plan["id"],"status":"PASS","style":"CHI-S01 SAFE V2 SCALE",
      "new_generation":False,"editor_gfx":False,"motion":"STATIC ONLY",
      "visible_provenance":"HISTORICAL SOURCE ONLY",
      "ai_reconstruction_plaque":False,"document_plaque":False,"concept_plaque":False,
      "caption_margin_v":390,"bottom_darkening":"locked strong gradient",
      "duration_target":duration,"ass":assqc,
      "sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"probe":probe,
    }
    (qc/f"{plan['id']}_QC.json").write_text(json.dumps(qcdata,indent=2),encoding="utf-8")
    print(json.dumps(qcdata,indent=2))

if __name__=="__main__": main()
