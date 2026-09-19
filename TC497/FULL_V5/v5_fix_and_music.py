#!/usr/bin/env python3
import argparse, json, math, os, shutil, subprocess, sys, tempfile
from pathlib import Path
from collections import Counter

SAFE_SOURCES={"original","youtube_audio_library"}
TOTAL_DEFAULT=1236.533333
COLD_OPEN_END=82.6

def sh(cmd):
    print("+"," ".join(map(str,cmd)))
    subprocess.run(list(map(str,cmd)),check=True)

def ffprobe_duration(path):
    out=subprocess.check_output([
        "ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nw=1:nk=1",str(path)
    ],text=True).strip()
    return float(out)

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def audit_shots(shots_path):
    shots=load_json(shots_path)
    counts=Counter(x.get("code","") for x in shots)
    cats=Counter(x.get("category","") for x in shots)
    durs=[float(x["e"])-float(x["s"]) for x in shots]
    long=[x for x in shots if float(x["e"])-float(x["s"])>9.0]
    max_cat=0; cur=0; prev=None
    for x in shots:
        c=x.get("category")
        if c==prev: cur+=1
        else: prev=c; cur=1
        max_cat=max(max_cat,cur)
    return {
        "shot_count":len(shots),
        "median_shot_sec":sorted(durs)[len(durs)//2] if durs else 0,
        "long_shots_over_9s":len(long),
        "max_visual_category_streak":max_cat,
        "top_assets":counts.most_common(15),
        "category_counts":cats.most_common()
    }

def validate_music_manifest(manifest_path, base_dir):
    m=load_json(manifest_path)
    tracks=m.get("tracks",{})
    if not tracks:
        raise SystemExit("Music manifest has no tracks.")
    credits=[]
    for key,t in tracks.items():
        src=t.get("source")
        if src not in SAFE_SOURCES:
            raise SystemExit(f"Track {key}: unsafe/unverified source {src!r}. Allowed: {sorted(SAFE_SOURCES)}")
        p=(base_dir/t["file"]).resolve()
        if not p.exists():
            raise SystemExit(f"Track {key}: file not found: {p}")
        t["_path"]=str(p)
        if src=="youtube_audio_library":
            if t.get("attribution_required") and not str(t.get("credit","")).strip():
                raise SystemExit(f"Track {key}: attribution is required but credit text is empty.")
            if t.get("attribution_required"):
                credits.append(str(t["credit"]).strip())
            else:
                title=t.get("title","Unknown title")
                artist=t.get("artist","Unknown artist")
                credits.append(f"YouTube Audio Library — {title} — {artist} (attribution not required)")
        elif src=="original":
            credits.append(f"Original music — {t.get('title',key)} — owned/created by channel")
    return m,credits

def make_cue_wav(track_path,start,end,gain_db,fade_in,fade_out,total,tmpdir,idx):
    dur=end-start
    fade_out_start=max(0,dur-fade_out)
    delay_ms=round(start*1000)
    out=tmpdir/f"cue_{idx:02d}.wav"
    af=(
        f"atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d={fade_in:.3f},"
        f"afade=t=out:st={fade_out_start:.3f}:d={fade_out:.3f},"
        f"volume={gain_db}dB,"
        f"adelay={delay_ms}|{delay_ms},"
        f"apad=pad_dur={total:.3f},atrim=0:{total:.3f}"
    )
    sh(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",track_path,
        "-af",af,"-ac",2,"-ar",48000,"-c:a","pcm_s16le",out])
    return out

def make_music_bed(manifest,base_dir,total,tmpdir,shots_path=None):
    cues=manifest.get("cues",[])
    if not cues:
        raise SystemExit("Music manifest has no cues.")

    out=tmpdir/"music_bed.wav"
    cmd=["ffmpeg","-y","-loglevel","error"]
    # One looping input per cue, but mix everything in one graph: no multi-GB
    # per-cue PCM intermediates.
    for c in cues:
        t=manifest["tracks"][c["track"]]
        cmd += ["-stream_loop","-1","-i",t["_path"]]

    fc=[]
    labels=[]
    for i,c in enumerate(cues):
        start=float(c["start"]); end=float(c["end"]); dur=end-start
        gain=float(c.get("gain_db",-31))
        fi=float(c.get("fade_in",2)); fo=float(c.get("fade_out",2))
        fo_start=max(0,dur-fo)
        delay=round(start*1000)
        lab=f"q{i}"
        fc.append(
            f"[{i}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d={fi:.3f},"
            f"afade=t=out:st={fo_start:.3f}:d={fo:.3f},"
            f"volume={gain}dB,adelay={delay}|{delay}[{lab}]"
        )
        labels.append(f"[{lab}]")
    fc.append("".join(labels)+f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,apad=pad_dur={total:.3f},atrim=0:{total:.3f}[m]")

    chain="[m]"; step=0
    if shots_path:
        shots=load_json(shots_path)
        for x in shots:
            if x.get("category") not in {"document","archive"}:
                continue
            a=max(COLD_OPEN_END,float(x["s"])); b=float(x["e"])
            nxt=f"d{step}"
            fc.append(f"{chain}volume=0.40:enable='between(t,{a:.3f},{b:.3f})'[{nxt}]")
            chain=f"[{nxt}]"; step+=1

    nxt=f"d{step}"
    fc.append(f"{chain}volume=0.25:enable='between(t,1190,{total:.3f})'[{nxt}]")
    chain=f"[{nxt}]"

    cmd += ["-filter_complex",";".join(fc),"-map",chain,
            "-t",f"{total:.3f}","-ac",2,"-ar",48000,
            "-c:a","pcm_s16le",str(out)]
    sh(cmd)
    return out

def make_visual_patch_video(input_video,patch_manifest,base_dir,tmpdir):
    if not patch_manifest:
        return Path(input_video)
    p=load_json(patch_manifest)
    patches=p.get("patches",[])
    existing=[]
    for x in patches:
        img=(base_dir/x["image"]).resolve()
        if img.exists():
            y=dict(x); y["_path"]=str(img); existing.append(y)
        else:
            print(f"WARN: visual replacement missing, skipping: {img}",file=sys.stderr)
    if not existing:
        return Path(input_video)

    out=tmpdir/"visual_patched.mp4"
    cmd=["ffmpeg","-y","-loglevel","error","-i",str(input_video)]
    for x in existing:
        cmd += ["-loop","1","-framerate","30","-i",x["_path"]]
    fc=[]
    prev="[0:v]"
    for i,x in enumerate(existing, start=1):
        scaled=f"img{i}"
        nxt=f"v{i}"
        fc.append(f"[{i}:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540[{scaled}]")
        fc.append(f"{prev}[{scaled}]overlay=0:0:shortest=1:enable='between(t,{float(x['start']):.3f},{float(x['end']):.3f})'[{nxt}]")
        prev=f"[{nxt}]"
    if os.getenv("V5_FASTCHECK")=="1":
        venc=["-c:v","mpeg4","-q:v","5","-pix_fmt","yuv420p"]
    else:
        venc=["-c:v","libx264","-preset","ultrafast","-crf","20","-pix_fmt","yuv420p"]
    cmd += ["-filter_complex",";".join(fc),"-map",prev,"-map","0:a?"] + venc + [
            "-c:a","copy","-t",f"{ffprobe_duration(input_video):.3f}","-movflags","+faststart",str(out)]
    sh(cmd)
    return out


def ass_time_to_sec(x):
    h,m,ss=x.split(":")
    return int(h)*3600+int(m)*60+float(ss)

def extract_patch_ass(src_ass,patch_manifest,out_ass):
    if not src_ass or not Path(src_ass).exists():
        return None
    patches=load_json(patch_manifest).get("patches",[])
    txt=Path(src_ass).read_text(encoding="utf-8",errors="replace")
    head,_,events=txt.partition("[Events]")
    keep=[]
    lines=events.splitlines()
    fmt=None
    for line in lines:
        if line.startswith("Format:"):
            fmt=line
        if not line.startswith("Dialogue:"):
            continue
        parts=line.split(",",9)
        if len(parts)<10: continue
        s0=ass_time_to_sec(parts[1]); e0=ass_time_to_sec(parts[2])
        if any(e0>float(p["start"]) and s0<float(p["end"]) for p in patches):
            keep.append(line)
    if not keep:
        return None
    out=Path(out_ass)
    out.write_text(head+"[Events]\n"+(fmt or "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text")+"\n"+"\n".join(keep)+"\n",encoding="utf-8")
    return out

def reburn_patch_overlays(video,src_ass,patch_manifest,tmpdir):
    ass=extract_patch_ass(src_ass,patch_manifest,tmpdir/"patch_events.ass")
    if not ass:
        return Path(video)
    out=tmpdir/"visual_patched_text.mp4"
    sh(["ffmpeg","-y","-loglevel","error","-i",str(video),
        "-vf",f"ass={ass}","-map","0:v","-map","0:a?",
        "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",
        "-c:a","copy","-movflags","+faststart",str(out)])
    return out

def mix_final(video,music_bed,out,total):
    # The existing V4/V5 program audio acts as sidechain; music ducks under narration and SFX.
    fc=(
        "[0:a]aresample=48000,asplit=2[base][sc];"
        "[1:a]aresample=48000[music];"
        "[music][sc]sidechaincompress="
        "threshold=0.030:ratio=10:attack=18:release=420:makeup=1[duck];"
        "[base][duck]amix=inputs=2:weights='1 1':normalize=0,"
        "alimiter=limit=0.794,"
        "loudnorm=I=-14:TP=-2:LRA=6[outa]"
    )
    sh(["ffmpeg","-y","-loglevel","error","-i",str(video),"-i",str(music_bed),
        "-filter_complex",fc,"-map","0:v","-map","[outa]","-t",f"{total:.3f}",
        "-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",str(out)])


def mix_final_from_stems(video,music_bed,vo_path,sfx_path,out,total,tmpdir):
    rest=max(0.1,total-COLD_OPEN_END)
    # Input 0: patched V4 video/audio (cold-open audio source)
    # Input 1: full VO
    # Input 2: post-cold-open procedural sound-design bed
    # Input 3: full-timeline music bed
    fc=(
        f"[0:a]atrim=0:{COLD_OPEN_END:.3f},asetpts=PTS-STARTPTS,aresample=48000[cold];"
        f"[1:a]atrim=start={COLD_OPEN_END:.3f}:end={total:.3f},asetpts=PTS-STARTPTS,"
        "aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[vo_mix][vo_sc];"
        f"[2:a]atrim=0:{rest:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
        "pan=stereo|c0=c0|c1=c0,volume=0.62,"
        f"volume=0.22:enable='between(t,{1115.376-COLD_OPEN_END:.3f},{rest:.3f})'[sfx];"
        f"[3:a]atrim=start={COLD_OPEN_END:.3f}:end={total:.3f},asetpts=PTS-STARTPTS,aresample=48000[music];"
        "[music][vo_sc]sidechaincompress=threshold=0.020:ratio=12:attack=15:release=480:makeup=1[duck];"
        "[vo_mix][sfx][duck]amix=inputs=3:weights='1 0.75 1':normalize=0,alimiter=limit=0.89[rest];"
        "[cold][rest]concat=n=2:v=0:a=1[full];"
        "[full]loudnorm=I=-14:TP=-2:LRA=6[outa]"
    )
    sh(["ffmpeg","-y","-loglevel","error",
        "-i",str(video),"-i",str(vo_path),"-i",str(sfx_path),"-i",str(music_bed),
        "-filter_complex",fc,"-map","0:v","-map","[outa]",
        "-t",f"{total:.3f}","-c:v","copy",
        "-c:a","aac","-b:a","192k","-movflags","+faststart",str(out)])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-video",required=True)
    ap.add_argument("--music-manifest",required=True)
    ap.add_argument("--shots-json")
    ap.add_argument("--visual-patches")
    ap.add_argument("--source-ass",help="Burn back only V4 ASS events overlapped by replacement intervals")
    ap.add_argument("--output",required=True)
    ap.add_argument("--vo",help="Original full VO file; enables stem-based post-cold-open remix")
    ap.add_argument("--sfx-bed",help="Post-cold-open original sound-design/underscore WAV; enables stem-based remix")
    ap.add_argument("--report-dir",default="V5_REPORT")
    args=ap.parse_args()

    input_video=Path(args.input_video).resolve()
    if not input_video.exists(): raise SystemExit(f"Input video not found: {input_video}")
    manifest_path=Path(args.music_manifest).resolve()
    base_dir=manifest_path.parent
    total=ffprobe_duration(input_video)

    report=Path(args.report_dir).resolve()
    report.mkdir(parents=True,exist_ok=True)
    if args.shots_json:
        audit=audit_shots(args.shots_json)
        (report/"V5_SHOT_AUDIT.json").write_text(json.dumps(audit,indent=2),encoding="utf-8")
        print("SHOT AUDIT",json.dumps(audit,indent=2))

    manifest,credits=validate_music_manifest(manifest_path,base_dir)
    (report/"YOUTUBE_DESCRIPTION_MUSIC_CREDITS.txt").write_text("\n".join(credits)+"\n",encoding="utf-8")
    (report/"MUSIC_MANIFEST_USED.json").write_text(json.dumps(manifest,indent=2,default=str),encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="tc497_v5_") as td:
        td=Path(td)
        patched=make_visual_patch_video(
            input_video,args.visual_patches,
            Path(args.visual_patches).resolve().parent if args.visual_patches else base_dir,td
        )
        if args.visual_patches and args.source_ass:
            patched=reburn_patch_overlays(patched,args.source_ass,args.visual_patches,td)
        bed=make_music_bed(manifest,base_dir,total,td,args.shots_json)
        if args.vo and args.sfx_bed:
            mix_final_from_stems(
                patched,bed,Path(args.vo).resolve(),Path(args.sfx_bed).resolve(),
                Path(args.output).resolve(),total,td
            )
        else:
            mix_final(patched,bed,Path(args.output).resolve(),total)

    # Final objective QC.
    sh(["ffprobe","-v","error","-show_entries","format=duration,size,bit_rate",
        "-show_entries","stream=index,codec_name,width,height,r_frame_rate",
        "-of","json",str(Path(args.output).resolve())])
    subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",str(Path(args.output).resolve()),
                    "-af","ebur128=peak=true","-f","null","-"],
                   stdout=subprocess.DEVNULL,stderr=open(report/"V5_EBUR128.txt","w"))

if __name__=="__main__":
    main()
