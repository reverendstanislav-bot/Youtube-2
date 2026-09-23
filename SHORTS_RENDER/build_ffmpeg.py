#!/usr/bin/env python3
import argparse, json, re, subprocess
from pathlib import Path

CHARCOAL="0x171A1C"
PAPER="0xF3EBDD"
ORANGE="0xF28A3A"
BLUE="0x5F747D"
RUST="0xA55235"

def run(cmd):
    print("RUN", " ".join(str(x) for x in cmd[:18]), "..." if len(cmd)>18 else "")
    subprocess.run(cmd,check=True)

def ass_time(t):
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def ass_escape(s):
    return str(s).replace("\\","\\\\").replace("{","\\{").replace("}","\\}").replace("\n"," ")

def phrases(words):
    out=[]; buf=[]
    def flush():
        nonlocal buf
        if buf:
            out.append(buf); buf=[]
    for w in words:
        if buf and float(w["short_s"])-float(buf[-1]["short_e"])>.42:
            flush()
        buf.append(w)
        chars=sum(len(str(x["w"]))+1 for x in buf)
        punct=bool(re.search(r"[.!?,;:]$",str(w["w"])))
        if len(buf)>=6 or chars>=34 or (punct and len(buf)>=3):
            flush()
    flush()
    return out

def active_text(group,active):
    chunks=[]
    for i,w in enumerate(group):
        token=ass_escape(w["w"])
        if i==active:
            chunks.append(r"{\c&H003AF2&}"+token+r"{\c&HFFFFFF&}")
        else:
            chunks.append(token)
    return " ".join(chunks)

def make_ass(short,out):
    hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,68,&H00FFFFFF,&H00FFFFFF,&H00101416,&H90000000,-1,0,0,0,100,100,0,0,1,4.2,1.4,2,72,72,330,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev=[]
    for group in phrases(short["source_words"]):
        ps=float(group[0]["short_s"])
        pe=float(group[-1]["short_e"])+.08
        for i,w in enumerate(group):
            s=max(ps,float(w["short_s"]))
            e=float(group[i+1]["short_s"]) if i+1<len(group) else pe
            if e<=s: e=s+.06
            ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{active_text(group,i)}")
    Path(out).write_text(hdr+"\n".join(ev)+"\n",encoding="utf-8")

def canonical_prov(text):
    text=str(text or "")
    for x in ("HISTORICAL SOURCE","AI RECONSTRUCTION","DOCUMENT","CONCEPT"):
        if x in text:
            return x
    return ""

def focus_mode(beat):
    s=(str(beat.get("visual",""))+" "+str(beat.get("action",""))+" "+str(beat.get("provenance",""))).lower()
    if re.search(r"wheel|motor|human scale|cargo|tunnel reveal|breach|steering|joint|locomotive",s) and not re.search(r"map|document|patent|publication|572|long-profile|network",s):
        return "focus"
    return "contain"

def drawtext_filter(text,x,y,size,color="white",extra=""):
    safe=str(text).replace("\\","\\\\").replace(":","\\:").replace("'","\\'")
    return f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{safe}':x={x}:y={y}:fontsize={size}:fontcolor={color}:shadowcolor=black@0.85:shadowx=2:shadowy=2{extra}"

def visual_filter(beat):
    mode=focus_mode(beat)
    if mode=="focus":
        chain=[
            "crop=iw:ih-180:0:0",
            "scale=1360:638:flags=lanczos",
            "crop=1080:638:140:0",
            f"pad=1080:1920:0:190:color={CHARCOAL}",
            f"drawbox=x=0:y=718:w=1080:h=110:color={CHARCOAL}:t=fill",
        ]
    else:
        chain=[
            "crop=iw:ih-180:0:0",
            "scale=1080:506:flags=lanczos",
            f"pad=1080:1920:0:230:color={CHARCOAL}",
            f"drawbox=x=0:y=641:w=1080:h=95:color={CHARCOAL}:t=fill",
        ]
    chain += [
        f"drawbox=x=0:y=1128:w=1080:h=792:color={CHARCOAL}@0.92:t=fill",
        f"drawbox=x=54:y=1128:w=972:h=5:color={ORANGE}:t=fill",
        drawtext_filter("HIDDEN INDUSTRIAL AMERICA","54","72","24","white"),
    ]
    prov=canonical_prov(beat.get("provenance",""))
    if prov:
        accent=ORANGE if prov=="HISTORICAL SOURCE" else BLUE if prov=="AI RECONSTRUCTION" else RUST
        chain += [
            f"drawbox=x=54:y=118:w=6:h=42:color={accent}:t=fill",
            drawtext_filter(prov,"76","122","22","white"),
        ]
    return ",".join(chain)

def build_short(short,source,outdir,qcdir):
    sid=short["id"]; fps=int(short["source_fps"])
    beats=short["montage"]
    outdir=Path(outdir); qcdir=Path(qcdir)
    outdir.mkdir(parents=True,exist_ok=True); qcdir.mkdir(parents=True,exist_ok=True)
    ass=qcdir/f"{sid}.ass"; make_ass(short,ass)
    out=outdir/f"{sid}.mp4"

    cmd=["ffmpeg","-y","-hide_banner","-loglevel","warning"]
    durations=[]
    for i,b in enumerate(beats):
        start=float(b["source_in"])
        end=float(beats[i+1]["source_in"]) if i+1<len(beats) else float(short["source_out_sec"])
        dur=max(.04,end-start); durations.append(dur)
        cmd += ["-ss",f"{start:.3f}","-t",f"{dur:.3f}","-i",str(source)]
    # One additional continuous source input supplies uninterrupted original narration/audio.
    cmd += ["-ss",f"{float(short['source_in_sec']):.3f}","-t",f"{float(short['duration_sec']):.3f}","-i",str(source)]

    fc=[]
    labels=[]
    for i,b in enumerate(beats):
        fc.append(f"[{i}:v]{visual_filter(b)},fps={fps},setsar=1[v{i}]")
        labels.append(f"[v{i}]")
    fc.append("".join(labels)+f"concat=n={len(beats)}:v=1:a=0[vc]")
    # Caption path has no spaces/colon in CI.
    fc.append(f"[vc]ass='{ass.as_posix()}'[vout]")
    cmd += [
        "-filter_complex",";".join(fc),
        "-map","[vout]","-map",f"{len(beats)}:a:0",
        "-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p",
        "-r",str(fps),"-c:a","aac","-b:a","192k","-ar","48000","-ac","2",
        "-movflags","+faststart","-shortest",str(out)
    ]
    run(cmd)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--map",required=True)
    ap.add_argument("--source",required=True)
    ap.add_argument("--episode-key",required=True)
    ap.add_argument("--fps",type=int,required=True)
    ap.add_argument("--outdir",required=True)
    ap.add_argument("--qcdir",required=True)
    a=ap.parse_args()
    data=json.loads(Path(a.map).read_text(encoding="utf-8"))
    shorts=data["shorts"] if "shorts" in data else data[a.episode_key]["shorts"]
    for sh in shorts:
        sh=dict(sh); sh["source_fps"]=a.fps
        build_short(sh,Path(a.source),a.outdir,a.qcdir)

if __name__=="__main__":
    main()
