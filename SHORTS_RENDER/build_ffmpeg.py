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
        if buf and (len(buf)>=5 or next_chars>28):
            flush()
        buf.append(w)
        if re.search(r"[.!?,;:]$",str(w["w"])) and len(buf)>=3:
            flush()
    flush()
    return out

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
Style: Cap,DejaVu Sans,68,&H00FFFFFF,&H00FFFFFF,&H00101416,&H90000000,-1,0,0,0,100,100,0,0,1,4.5,1.5,2,78,78,285,1

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

def visual_filter(beat):
    # V2 vertical design: ONE crisp source image only.
    # The previous layout duplicated the same landscape frame into two visible panels.
    # That is explicitly forbidden now.
    desc=(str(beat.get("visual",""))+" "+str(beat.get("action",""))+" "+str(beat.get("provenance",""))).lower()
    keep_full=bool(re.search(
        r"map|document|patent|publication|diagram|network|top-down|572|13 units|full.machine|long.profile|route|metric|gauge|archive|historical source",
        desc
    ))

    # Always remove the burned-in long-form caption strip.
    # Wide evidence shots preserve the full horizontal source.
    # Other shots get only a mild centered crop, never a second copy.
    if keep_full:
        picture=(
            "crop=iw:ih-180:0:0,"
            "scale=1040:-2:flags=lanczos,"
            "pad=1080:620:20:(620-ih)/2:color=0x171A1C"
        )
    else:
        picture=(
            "crop=1560:900:180:0,"
            "scale=1080:623:flags=lanczos"
        )

    # Neutral industrial background; no blurred duplicate of the source.
    # One warm-paper outline and one rust rule are the only framing devices.
    y=276 if keep_full else 268
    panel_h=620 if keep_full else 623
    return (
        f"color=c={CHARCOAL}:s=1080x1920:r=30[bg];"
        f"[in]{picture}[pic];"
        f"[bg][pic]overlay=0:{y},"
        f"drawbox=x=20:y={y}:w=1040:h={panel_h}:color=0xF3EBDD@0.28:t=2,"
        f"drawbox=x=54:y=1018:w=972:h=5:color={ORANGE}:t=fill,"
        f"drawbox=x=0:y=1023:w=1080:h=897:color={CHARCOAL}@0.98:t=fill"
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
        vf=visual_filter(b)
        fc.append(f"[{i}:v]null[in];{vf},fps={fps},setsar=1[v{i}]")
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
