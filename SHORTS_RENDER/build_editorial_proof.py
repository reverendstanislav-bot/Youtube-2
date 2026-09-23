#!/usr/bin/env python3
import argparse,json,subprocess,re
from pathlib import Path

CHARCOAL="0x171A1C"
IRON="0x30363A"
PAPER="0xF3EBDD"
ORANGE="0xF28A3A"
BLUE="0x5F747D"

def esc(s):
    return str(s).replace("\\","\\\\").replace(":","\\:").replace("'","\\'").replace("%","\\%")

def ass_time(sec):
    cs=round(sec*100); h=cs//360000; cs%=360000; m=cs//6000; cs%=6000; s=cs//100; cs%=100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def ass_escape(s):
    return str(s).replace("\\",r"\\").replace("{",r"\{").replace("}",r"\}")

def make_ass(words,out):
    # readable 2-line max phrases
    groups=[]; buf=[]
    def flush():
        nonlocal buf
        if buf: groups.append(buf); buf=[]
    for w in words:
        if buf and (w["short_s"]-buf[-1]["short_e"]>.42): flush()
        buf.append(w)
        chars=sum(len(x["w"])+1 for x in buf)
        if len(buf)>=7 or chars>=40 or re.search(r'[.!?]$',w["w"]): flush()
    flush()
    hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,72,&H00FFFFFF,&H00FFFFFF,&H00101416,&H90000000,-1,0,0,0,100,100,0,0,1,4.8,1.6,2,72,72,92,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev=[]
    for g in groups:
        for i,w in enumerate(g):
            s=w["short_s"]; e=max(w["short_e"],s+.055)
            parts=[]
            for j,x in enumerate(g):
                token=ass_escape(x["w"])
                if j==i: token=r"{\c&H003A8AF2&}"+token+r"{\c&HFFFFFF&}"
                parts.append(token)
            ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{' '.join(parts)}")
    Path(out).write_text(hdr+"\n".join(ev)+"\n",encoding="utf-8")

def build(plan,mapj,source,out,qc):
    sid=plan["id"]; sh=next(x for x in mapj["shorts"] if x["id"]==sid)
    fps=int(plan["fps"]); dur=float(sh["duration_sec"])
    ass=Path(qc)/f"{sid}.ass"; make_ass(sh["source_words"],ass)

    inputs=[]; fc=[]; vids=[]
    for i,seg in enumerate(plan["segments"]):
        od=float(seg["out_end"]-seg["out_start"])
        ss=float(seg["visual_source_in"])
        inputs += ["-ss",f"{ss:.3f}","-t",f"{od:.3f}","-i",source]
        mode=seg.get("mode","wide")
        if mode=="wide":
            # Preserve substantially more horizontal context than a 9:16 crop.
            # Slow pan across a ~1:1 crop; source stays recognizable.
            cw=1120
            prog=f"min(1,max(0,t/{max(.2,od):.3f}))"
            if seg.get("direction","lr")=="lr":
                x=f"(iw-{cw})*({prog})"
            else:
                x=f"(iw-{cw})*(1-({prog}))"
            vf=(
                f"crop={cw}:1080:x='{x}':y=0,"
                "scale=1080:1042:flags=lanczos,"
                f"pad=1080:1920:0:70:color={CHARCOAL},"
                "drawbox=x=0:y=1112:w=1080:h=808:color=0x171A1C@0.98:t=fill,"
                f"drawbox=x=54:y=1110:w=972:h=5:color={ORANGE}:t=fill"
            )
        else:
            cw=720
            x=f"(iw-{cw})*{seg.get('x',.5):.2f}"
            vf=(
                f"crop={cw}:1080:x='{x}':y=0,"
                "scale=1080:1620:flags=lanczos,"
                f"pad=1080:1920:0:0:color={CHARCOAL},"
                "drawbox=x=0:y=1460:w=1080:h=460:color=0x171A1C@0.93:t=fill,"
                f"drawbox=x=54:y=1455:w=972:h=5:color={ORANGE}:t=fill"
            )
        # editorial GFX fills the non-video area for wide shots: not empty black
        metric=esc(seg.get("metric",""))
        label=esc(seg.get("label",""))
        title=esc(plan.get("title",""))
        vf += (
            f",drawtext=font='DejaVu Sans':text='HIDDEN INDUSTRIAL AMERICA':x=54:y=26:fontsize=22:fontcolor={PAPER}:borderw=2:bordercolor=black@0.7"
        )
        if i==0 and title:
            vf += f",drawtext=font='DejaVu Sans':text='{title}':x=(w-text_w)/2:y=122:fontsize=42:fontcolor={PAPER}:borderw=3:bordercolor=black@0.9"
        if mode=="wide":
            if label:
                vf += f",drawtext=font='DejaVu Sans':text='{label}':x=54:y=1180:fontsize=29:fontcolor={BLUE}:borderw=2:bordercolor=black@0.7"
            if metric:
                vf += f",drawtext=font='DejaVu Sans':text='{metric}':x=54:y=1240:fontsize=72:fontcolor={PAPER}:borderw=3:bordercolor=black@0.8"
        fc.append(f"[{i}:v]{vf},fps={fps},setsar=1[v{i}]")
        vids.append(f"[v{i}]")

    fc.append("".join(vids)+f"concat=n={len(vids)}:v=1:a=0[vcat]")
    fc.append(f"[vcat]ass='{str(ass).replace(':','\\:')}'[vout]")

    # audio is exact locked long-form excerpt
    inputs += ["-ss",f"{sh['source_in_sec']:.3f}","-t",f"{dur:.3f}","-i",source]
    audio_idx=len(plan["segments"])
    cmd=["ffmpeg","-y","-loglevel","error"]+inputs+[
        "-filter_complex",";".join(fc),
        "-map","[vout]","-map",f"{audio_idx}:a:0",
        "-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p",
        "-r",str(fps),"-c:a","aac","-b:a","192k","-ar","48000","-ac","2",
        "-movflags","+faststart",out
    ]
    subprocess.run(cmd,check=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--plan",required=True); ap.add_argument("--map",required=True)
    ap.add_argument("--source",required=True); ap.add_argument("--out",required=True); ap.add_argument("--qc",required=True)
    a=ap.parse_args()
    Path(a.qc).mkdir(parents=True,exist_ok=True); Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    plan=json.loads(Path(a.plan).read_text()); mp=json.loads(Path(a.map).read_text())
    build(plan,mp,a.source,a.out,a.qc)

if __name__=="__main__": main()
