#!/usr/bin/env python3
import argparse, json, subprocess
from pathlib import Path

FPS = 30.0

def sh(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(list(map(str, cmd)), check=True)

def ass_to_sec(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

def sec_to_ass(t):
    t = max(0.0, float(t))
    h = int(t // 3600)
    t -= h * 3600
    m = int(t // 60)
    t -= m * 60
    return f"{h}:{m:02d}:{t:05.2f}"

def load_manifest(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    patches = sorted(data["patches"], key=lambda p: float(p["start"]))
    if len(patches) != 7:
        raise SystemExit(f"Expected 7 patches, got {len(patches)}")
    return patches

def build_patch_ass(src_ass, patches, chunk_start, chunk_end, out_ass):
    txt = Path(src_ass).read_text(encoding="utf-8", errors="replace")
    head, sep, events = txt.partition("[Events]")
    if not sep:
        raise SystemExit("ASS has no [Events] section")

    fmt = None
    rendered = []
    for line in events.splitlines():
        if line.startswith("Format:"):
            fmt = line
            continue
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9)
        if len(parts) < 10:
            continue
        s0 = ass_to_sec(parts[1])
        e0 = ass_to_sec(parts[2])
        for p in patches:
            ps = float(p["start"])
            pe = float(p["end"])
            a = max(s0, ps, chunk_start)
            b = min(e0, pe, chunk_end)
            if b <= a:
                continue
            q = parts.copy()
            q[1] = sec_to_ass(a - chunk_start)
            q[2] = sec_to_ass(b - chunk_start)
            rendered.append(",".join(q))

    out = Path(out_ass)
    out.write_text(
        head + "[Events]\n" +
        (fmt or "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text") +
        "\n" + "\n".join(rendered) + ("\n" if rendered else ""),
        encoding="utf-8",
    )
    return len(rendered)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--source-ass", required=True)
    ap.add_argument("--replacement-dir", required=True)
    ap.add_argument("--start", type=float, required=True)
    ap.add_argument("--end", type=float, required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    start = round(args.start * FPS) / FPS
    end = round(args.end * FPS) / FPS
    if end <= start:
        raise SystemExit("Invalid chunk range")
    duration = end - start

    patches = load_manifest(args.manifest)
    active = [p for p in patches if float(p["end"]) > start and float(p["start"]) < end]
    out_ass = Path(args.output).with_suffix(".patch.ass")
    ass_count = build_patch_ass(args.source_ass, patches, start, end, out_ass)
    print(f"CHUNK {start:.3f}-{end:.3f}: active_patches={len(active)} ass_events={ass_count}", flush=True)

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", f"{start:.6f}", "-i", args.input,
    ]

    image_patches = []
    for p in active:
        image = p.get("overlay_image")
        if not image:
            continue
        path = (Path(args.replacement_dir) / image).resolve()
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"Missing overlay image: {path}")
        image_patches.append((p, path))
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(path)]

    fc = ["[0:v]setpts=PTS-STARTPTS[v0]"]
    prev = "[v0]"
    for idx, (p, path) in enumerate(image_patches, start=1):
        ps = max(start, float(p["start"])) - start
        pe = min(end, float(p["end"])) - start
        img = f"img{idx}"
        nxt = f"v{idx}"
        fc.append(
            f"[{idx}:v]scale=960:540:force_original_aspect_ratio=increase,"
            f"crop=960:540,setpts=PTS-STARTPTS[{img}]"
        )
        fc.append(
            f"{prev}[{img}]overlay=0:0:eof_action=pass:"
            f"enable='between(t,{ps:.6f},{pe:.6f})'[{nxt}]"
        )
        prev = f"[{nxt}]"

    if ass_count:
        fc.append(f"{prev}ass={out_ass}[vout]")
        prev = "[vout]"

    cmd += [
        "-filter_complex", ";".join(fc),
        "-map", prev,
        "-an",
        "-t", f"{duration:.6f}",
        "-r", "30",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-keyint_min", "60",
        "-sc_threshold", "0",
        "-movflags", "+faststart",
        args.output,
    ]
    sh(cmd)

    sh([
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_name,width,height,r_frame_rate:format=duration,size",
        "-of", "json", args.output,
    ])

if __name__ == "__main__":
    main()
