#!/usr/bin/env python3
import argparse, json, re, subprocess
from pathlib import Path

CHARCOAL="0x171A1C"
ORANGE="0xF28A3A"

def run(cmd):
    print("RUN", " ".join(str(x) for x in cmd[:20]), "..." if len(cmd)>20 else "")
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
        next_chars=sum(len(str(x["w"]))+1 for x in buf)+len(str(w["w"]))+1
        if buf and (len(buf)>=7 or next_chars>40):
            flush()
        buf.append(w)
        if re.search(r"[.!?,;:]$",str(w["w"])) and len(buf)>=3:
            flush()
    flush()
    return out

def hook_text(short):
    title=str(short.get("title","")).strip().upper()
    if not title:
        return ""
    words=title.split()
    if len(words)<=4:
        return ass_escape(title)
    best=(10**9,None)
    for i in range(2,len(words)):
        a=" ".join(words[:i]); b=" ".join(words[i:])
        score=abs(len(a)-len(b))
        if score<best[0]:
            best=(score,i)
    i=best[1] or max(1,len(words)//2)
    return ass_escape(" ".join(words[:i]))+r"\N"+ass_escape(" ".join(words[i:]))

def active_text(group,active):
    raw=[str(w["w"]) for w in group]
    total=sum(len(x)+1 for x in raw)
    split=None
    if total>20 and len(group)>=3:
        best=(10**9,None)
        for i in range(1,len(group)):
            a=sum(len(x)+1 for x in raw[:i])
            b=sum(len(x)+1 for x in raw[i:])
            score=abs(a-b)
            if score<best[0]:
                best=(score,i)
        split=best[1]

    chunks=[]
    for i,w in enumerate(group):
        token=ass_escape(w["w"])
        if i==active:
            token=r"{\c&H003A8AF2&}"+token+r"{\c&HFFFFFF&}"
        if split is not None and i==split:
            token=r"\N"+token
        chunks.append(token)
    return " ".join(chunks).replace(" \\N","\\N")

def make_ass(short,out):
    hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00101416,&H90000000,-1,0,0,0,100,100,0,0,1,4.8,1.6,2,74,74,165,1
Style: Hook,DejaVu Sans,46,&H00F3EBDD,&H00F3EBDD,&H00101416,&H70000000,-1,0,0,0,100,100,1.0,0,1,3.4,1.0,8,70,70,82,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev=[]
    hook=hook_text(short)
    if hook:
        ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(min(2.4,float(short['duration_sec'])))},Hook,,0,0,0,,{hook}")
    for group in phrases(short["source_words"]):
        ps=float(group[0]["short_s"])
        pe=float(group[-1]["short_e"])+.08
        for i,w in enumerate(group):
            s=max(ps,float(w["short_s"]))
            e=float(group[i+1]["short_s"]) if i+1<len(group) else pe
            if e<=s: e=s+.06
            ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{active_text(group,i)}")
    Path(out).write_text(hdr+"\n".join(ev)+"\n",encoding="utf-8")

def drawtext_filter(text,x,y,size,color="white"):
    safe=str(text).replace("\\","\\\\").replace(":","\\:").replace("'","\\'")
    return (
        "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text='{safe}':x={x}:y={y}:fontsize={size}:fontcolor={color}:"
        "shadowcolor=black@0.85:shadowx=2:shadowy=2"
    )

def provenance_label(beat):
    raw=str(beat.get("provenance","")).strip()
    # Only render a provenance tag when the extraction map is unambiguous.
    # Ambiguous instructions such as "match source visual" defer to the source frame.
    if "/" in raw or "if verified" in raw.lower() or "match source" in raw.lower() or "→" in raw:
        return ""
    u=raw.upper()
    for label in ("HISTORICAL SOURCE","AI RECONSTRUCTION","DOCUMENT","CONCEPT"):
        if u==label or u.startswith(label+" "):
            return label
    return ""

def visual_filter(beat, beat_index=0, beat_dur=4.0):
    # V4 vertical system: one source plane filling almost the entire 9:16 frame.
    # No stacked panels, no duplicated blur copy, no half-screen picture.
    desc=(str(beat.get("visual",""))+" "+str(beat.get("action",""))+" "+str(beat.get("provenance",""))).lower()

    wide=bool(re.search(
        r"map|document|patent|publication|diagram|network|top-down|572|13 units|full.machine|long.profile|route|metric|gauge|aircraft|helicopter|city|tunnel map|street",
        desc
    ))

    # 620 px crop -> ~1881 px tall in the 1080x1920 output.
    # 700 px crop -> ~1666 px tall for very wide evidence, still >86% of the canvas.
    cw=700 if wide else 620
    out_h=1666 if wide else 1881

    # Wide evidence gets a slow horizontal scan so the viewer can read the full machine/map
    # over the beat without ever showing a second copy of the frame.
    if wide:
        if beat_index % 2 == 0:
            xexpr=f"(iw-{cw})*min(1,max(0,t/{max(0.2,beat_dur):.3f}))"
        else:
            xexpr=f"(iw-{cw})*(1-min(1,max(0,t/{max(0.2,beat_dur):.3f})))"
    else:
        # Alternate center-left / center / center-right to keep consecutive vertical crops varied.
        pos=beat_index % 3
        if pos==0:
            xexpr=f"(iw-{cw})*0.38"
        elif pos==1:
            xexpr=f"(iw-{cw})*0.50"
        else:
            xexpr=f"(iw-{cw})*0.62"

    # Fill the screen from the top with one crisp crop. The small remaining lower strip is
    # reserved for captions; a bottom gradient/solid cover hides the original long-form caption.
    picture=(
        f"crop={cw}:1080:x='{xexpr}':y=0,"
        f"scale=1080:{out_h}:flags=lanczos,"
        f"pad=1080:1920:0:0:color=0x171A1C"
    )

    return (
        picture
        +",drawbox=x=0:y=1320:w=1080:h=600:color=0x171A1C@0.22:t=fill"
        +",drawbox=x=0:y=1500:w=1080:h=420:color=0x171A1C@0.90:t=fill"
        +f",drawbox=x=54:y=1494:w=972:h=5:color={ORANGE}:t=fill"
    )

def build_short(short,source,outdir,qcdir):
    sid=short["id"]; fps=int(short["source_fps"])
    beats=short["montage"]
    outdir=Path(outdir); qcdir=Path(qcdir)
    outdir.mkdir(parents=True,exist_ok=True); qcdir.mkdir(parents=True,exist_ok=True)
    ass=qcdir/f"{sid}.ass"; make_ass(short,ass)
    out=outdir/f"{sid}.mp4"

    cmd=["ffmpeg","-y","-hide_banner","-loglevel","warning"]
    for i,b in enumerate(beats):
        start=float(b["source_in"])
        end=float(beats[i+1]["source_in"]) if i+1<len(beats) else float(short["source_out_sec"])
        dur=max(.04,end-start)
        cmd += ["-ss",f"{start:.3f}","-t",f"{dur:.3f}","-i",str(source)]

    # One extra continuous input supplies uninterrupted original narration/audio.
    cmd += ["-ss",f"{float(short['source_in_sec']):.3f}","-t",f"{float(short['duration_sec']):.3f}","-i",str(source)]

    fc=[]; labels=[]
    for i,b in enumerate(beats):
        beat_dur=max(0.2, min(short["duration_sec"], b.get("_next_source", short["source_out_sec"])) - b["source_in"])
        vf=visual_filter(b, i, beat_dur)
        fc.append(f"[{i}:v]{vf},fps={fps},setsar=1[v{i}]")
        labels.append(f"[v{i}]")
    fc.append("".join(labels)+f"concat=n={len(beats)}:v=1:a=0[vc]")
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
