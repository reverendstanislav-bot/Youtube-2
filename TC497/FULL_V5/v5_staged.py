#!/usr/bin/env python3
import argparse, json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v5_fix_and_music as v

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("mode",choices=["visual","music","mix"])
    ap.add_argument("--input-video")
    ap.add_argument("--visual-patches")
    ap.add_argument("--source-ass")
    ap.add_argument("--music-manifest")
    ap.add_argument("--shots-json")
    ap.add_argument("--music-bed")
    ap.add_argument("--vo")
    ap.add_argument("--sfx-bed")
    ap.add_argument("--output",required=True)
    ap.add_argument("--work-dir",required=True)
    args=ap.parse_args()

    work=Path(args.work_dir).resolve()
    work.mkdir(parents=True,exist_ok=True)
    out=Path(args.output).resolve()
    out.parent.mkdir(parents=True,exist_ok=True)

    if args.mode=="visual":
        src=Path(args.input_video).resolve()
        pm=Path(args.visual_patches).resolve()
        built=v.make_visual_patch_video_concat(src,str(pm),pm.parent,work,args.source_ass)
        if built.resolve()!=out:
            shutil.copy2(built,out)
        print("V5_STAGE_VISUAL_DONE",out,flush=True)
        return

    if args.mode=="music":
        manifest_path=Path(args.music_manifest).resolve()
        manifest,_=v.validate_music_manifest(manifest_path,manifest_path.parent)
        total=v.ffprobe_duration(args.input_video)
        built=v.make_music_bed(manifest,manifest_path.parent,total,work,args.shots_json)
        if built.resolve()!=out:
            shutil.copy2(built,out)
        print("V5_STAGE_MUSIC_DONE",out,flush=True)
        return

    total=v.ffprobe_duration(args.input_video)
    v.mix_final_from_stems(
        Path(args.input_video).resolve(),
        Path(args.music_bed).resolve(),
        Path(args.vo).resolve(),
        Path(args.sfx_bed).resolve(),
        out,total,work
    )
    print("V5_STAGE_MIX_DONE",out,flush=True)

if __name__=="__main__":
    main()
