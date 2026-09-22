#!/usr/bin/env python3
import argparse, importlib.util, json, subprocess
from pathlib import Path

FPS=25

def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-6000:])
    return p.stdout

def load_v3(path):
    spec=importlib.util.spec_from_file_location("v3builder",path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def render_clean(v3,s,i,outdir):
    out=outdir/f"{i:03d}.mp4"
    width,height=1920,1080
    count=s["b"]-s["a"]
    args=["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate","25","-loop","1","-i",s["asset"]]
    graph=f"[0:v]scale={width}:{height}:flags=lanczos,format=yuv444p"
    if s.get("motion")!="static":
        graph+=","+v3.motion_filter(width,height,count,s["motion"])
    graph+=",setsar=1,format=yuv420p[v]"
    args += ["-filter_complex",graph,"-map","[v]","-frames:v",str(count),"-an",
             "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-r","25","-g","50",
             "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",str(out)]
    run(args)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--v3-builder",required=True)
    ap.add_argument("--shots",required=True)
    ap.add_argument("--assets-root",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--output-video",required=True)
    ap.add_argument("--plan-out",required=True)
    a=ap.parse_args()

    work=Path(a.work); work.mkdir(parents=True,exist_ok=True)
    clips=work/"clips"; clips.mkdir(exist_ok=True)
    gen=work/"generated"; gen.mkdir(exist_ok=True)
    v3=load_v3(a.v3_builder)
    assets=v3.resolve_assets(Path(a.assets_root))
    orig=json.loads(Path(a.shots).read_text(encoding="utf-8-sig"))
    plan=v3.patch_plan(orig,assets,gen)
    Path(a.plan_out).write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8")

    rendered=[]
    for i,s in enumerate(plan):
        rendered.append(render_clean(v3,s,i,clips))
        if i%20==0:
            print(f"1080p clean picture {i+1}/{len(plan)}",flush=True)

    listing=work/"concat.txt"
    listing.write_text("\n".join("file '"+str(p.resolve()).replace("'","'\\''")+"'" for p in rendered)+"\n",encoding="utf-8")
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(listing),
         "-c","copy","-movflags","+faststart",a.output_video])
    print(json.dumps({"shots":len(plan),"output":a.output_video,"size":"1920x1080"},indent=2))

if __name__=="__main__":
    main()
