#!/usr/bin/env python3
import argparse,json,subprocess,re,os
from pathlib import Path

ORANGE="0xF28A3A"
CHARCOAL="0x171A1C"
PAPER="0xF3EBDD"

def ass_time(sec):
    cs=round(sec*100); h=cs//360000; cs%=360000; m=cs//6000; cs%=6000; s=cs//100; cs%=100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def ass_escape(s):
    return str(s).replace("\\",r"\\").replace("{",r"\{").replace("}",r"\}")

def make_ass(words,out):
    groups=[]; buf=[]
    def flush():
        nonlocal buf
        if buf: groups.append(buf); buf=[]
    for w in words:
        if buf and w["short_s"]-buf[-1]["short_e"]>.42: flush()
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
Style: Cap,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00101416,&H90000000,-1,0,0,0,100,100,0,0,1,4.8,1.6,2,70,70,110,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev=[]
    for g in groups:
        for i,w in enumerate(g):
            s=w["short_s"]; e=max(w["short_e"],s+.055)
            parts=[]
            for j,x in enumerate(g):
                tok=ass_escape(x["w"])
                if j==i: tok=r"{\c&H003A8AF2&}"+tok+r"{\c&HFFFFFF&}"
                parts.append(tok)
            ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{' '.join(parts)}")
    Path(out).write_text(hdr+"\n".join(ev)+"\n",encoding="utf-8")

def esc_draw(s):
    return str(s).replace("\\","\\\\").replace(":","\\:").replace("'","\\'").replace("%","\\%")

def build(plan,mapj,asset_dir,audio_source,out,qc):
    sid=plan["id"]; sh=next(x for x in mapj["shorts"] if x["id"]==sid)
    fps=int(plan["fps"]); dur=float(sh["duration_sec"])
    ass=Path(qc)/f"{sid}.ass"; make_ass(sh["source_words"],ass)

    inputs=[]; filters=[]; vids=[]
    for i,seg in enumerate(plan["segments"]):
        segdur=float(seg["out_end"]-seg["out_start"])
        asset=Path(asset_dir)/seg["asset"]
        if not asset.exists(): raise FileNotFoundError(asset)
        inputs += ["-loop","1","-framerate",str(fps),"-t",f"{segdur:.3f}","-i",str(asset)]

        # Full-bleed vertical crop from CLEAN source asset, never from caption-burned long-form video.
        # A 608px crop maps 1920x1080 -> exact 9:16.
        x=seg.get("x",.5)
        motion=seg.get("motion","static")
        if motion=="scan_lr":
            xexpr=f"(iw-608)*min(1,max(0,t/{max(.2,segdur):.3f}))"
        elif motion=="scan_rl":
            xexpr=f"(iw-608)*(1-min(1,max(0,t/{max(.2,segdur):.3f})))"
        else:
            xexpr=f"(iw-608)*{float(x):.3f}"

        vf=(
            f"crop=608:1080:x='{xexpr}':y=0,"
            "scale=1080:1920:flags=lanczos,"
            "drawbox=x=0:y=1450:w=1080:h=470:color=0x171A1C@0.76:t=fill,"
            "drawbox=x=0:y=1660:w=1080:h=260:color=0x171A1C@0.94:t=fill,"
            f"drawbox=x=54:y=1444:w=972:h=5:color={ORANGE}:t=fill"
        )
        metric=esc_draw(seg.get("metric",""))
        label=esc_draw(seg.get("label",""))
        if label:
            vf += f",drawtext=font='DejaVu Sans':text='{label}':x=54:y=1320:fontsize=26:fontcolor=0x5F747D:borderw=2:bordercolor=black@0.65"
        if metric:
            vf += f",drawtext=font='DejaVu Sans':text='{metric}':x=54:y=1360:fontsize=48:fontcolor={PAPER}:borderw=3:bordercolor=black@0.8"

        if i==0:
            l1=esc_draw(plan["title_lines"][0]); l2=esc_draw(plan["title_lines"][1])
            vf += (
                f",drawtext=font='DejaVu Sans':text='{l1}':x=(w-text_w)/2:y=60:fontsize=46:fontcolor={PAPER}:borderw=4:bordercolor=black@0.9,"
                f"drawtext=font='DejaVu Sans':text='{l2}':x=(w-text_w)/2:y=114:fontsize=46:fontcolor={PAPER}:borderw=4:bordercolor=black@0.9"
            )
        filters.append(f"[{i}:v]{vf},fps={fps},setsar=1[v{i}]")
        vids.append(f"[v{i}]")

    filters.append("".join(vids)+f"concat=n={len(vids)}:v=1:a=0[vcat]")
    filters.append(f"[vcat]ass='{str(ass).replace(':','\\:')}'[vout]")

    # Locked original long-form audio excerpt.
    inputs += ["-ss",f"{sh['source_in_sec']:.3f}","-t",f"{dur:.3f}","-i",audio_source]
    ai=len(plan["segments"])
    cmd=["ffmpeg","-y","-loglevel","error"]+inputs+[
        "-filter_complex",";".join(filters),"-map","[vout]","-map",f"{ai}:a:0",
        "-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p","-r",str(fps),
        "-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-movflags","+faststart",out
    ]
    subprocess.run(cmd,check=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--plan",required=True); ap.add_argument("--map",required=True)
    ap.add_argument("--asset-dir",required=True); ap.add_argument("--audio-source",required=True)
    ap.add_argument("--out",required=True); ap.add_argument("--qc",required=True)
    a=ap.parse_args(); Path(a.qc).mkdir(parents=True,exist_ok=True)
    plan=json.loads(Path(a.plan).read_text()); mp=json.loads(Path(a.map).read_text())
    build(plan,mp,a.asset_dir,a.audio_source,a.out,a.qc)

if __name__=="__main__": main()
