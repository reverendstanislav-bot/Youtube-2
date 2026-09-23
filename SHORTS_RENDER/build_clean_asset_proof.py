#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ORANGE = "0xF28A3A"
CHARCOAL = "0x171A1C"
PAPER = "0xF3EBDD"
BLUE = "0x5F747D"

def ass_time(sec):
    cs = round(float(sec) * 100)
    h = cs // 360000
    cs %= 360000
    m = cs // 6000
    cs %= 6000
    s = cs // 100
    cs %= 100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def ass_escape(value):
    return str(value).replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")

def draw_escape(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("%", "\\%")
    )

def is_sentence_end(token):
    return str(token).rstrip('"”').endswith((".", "!", "?"))

def caption_groups(words):
    groups = []
    buf = []

    def flush():
        nonlocal buf
        if buf:
            groups.append(buf)
            buf = []

    for word in words:
        if buf and float(word["short_s"]) - float(buf[-1]["short_e"]) > 0.36:
            flush()
        buf.append(word)
        chars = sum(len(str(x["w"])) + 1 for x in buf)
        if len(buf) >= 5 or chars >= 29 or is_sentence_end(word["w"]):
            flush()

    flush()
    return groups

def balanced_split(group):
    if len(group) <= 3:
        return len(group)
    total = sum(len(str(x["w"])) + 1 for x in group)
    best_score = 10**9
    best_index = len(group)
    for i in range(1, len(group)):
        left = sum(len(str(x["w"])) + 1 for x in group[:i])
        right = total - left
        score = abs(left - right)
        if score < best_score:
            best_score = score
            best_index = i
    return best_index

def make_ass(words, out_path):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,66,&H00FFFFFF,&H00FFFFFF,&H00101416,&H90000000,-1,0,0,0,100,100,0,0,1,4.6,1.5,2,104,104,315,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    events = []

    for group in caption_groups(words):
        visible_chars = sum(len(str(x["w"])) + 1 for x in group)
        split = balanced_split(group) if visible_chars > 21 else len(group)

        for active_index, active_word in enumerate(group):
            parts = []
            for index, item in enumerate(group):
                token = ass_escape(item["w"])
                if index == active_index:
                    token = r"{\c&H003A8AF2&}" + token + r"{\c&HFFFFFF&}"
                parts.append(token)

            if split < len(parts):
                rendered = " ".join(parts[:split]) + r"\N" + " ".join(parts[split:])
            else:
                rendered = " ".join(parts)

            start = float(active_word["short_s"])
            if active_index + 1 < len(group):
                end = max(float(group[active_index + 1]["short_s"]), start + 0.055)
            else:
                end = max(float(active_word["short_e"]) + 0.08, start + 0.055)
            events.append(
                f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Cap,,0,0,0,,{rendered}"
            )

    Path(out_path).write_text(header + "\n".join(events) + "\n", encoding="utf-8")

def build(plan, mapping, asset_dir, audio_source, output, qc_dir):
    short = next(x for x in mapping["shorts"] if x["id"] == plan["id"])
    fps = int(plan["fps"])
    duration = float(short["duration_sec"])

    qc_dir = Path(qc_dir)
    qc_dir.mkdir(parents=True, exist_ok=True)
    ass_path = qc_dir / f"{plan['id']}.ass"
    make_ass(short["source_words"], ass_path)

    inputs = []
    filters = []
    video_labels = []

    for index, segment in enumerate(plan["segments"]):
        segment_duration = float(segment["out_end"]) - float(segment["out_start"])
        asset = Path(asset_dir) / segment["asset"]
        if not asset.exists():
            raise FileNotFoundError(asset)

        inputs += [
            "-loop", "1",
            "-framerate", str(fps),
            "-t", f"{segment_duration:.3f}",
            "-i", str(asset),
        ]

        # Clean-source vertical composition:
        # exact 9:16 crop from the CLEAN 16:9 source asset,
        # fixed focal point, no left-right travel, no duplicated panel.
        focal = float(segment.get("x", 0.5))
        x_expr = f"(iw-ow)*{focal:.3f}"

        motion = str(segment.get("motion", "static")).lower()
        base_picture = (
            f"crop=ih*9/16:ih:x='{x_expr}':y=0,"
            "scale=1080:1920:flags=lanczos"
        )
        if motion == "push":
            # ~1.2% total push across the segment. No x/y travel.
            frames = max(1, round(segment_duration * fps))
            step = 0.012 / frames
            base_picture += (
                f",zoompan=z='min(zoom+{step:.8f},1.012)':"
                "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d=1:s=1080x1920:fps={fps}"
            )

        vf = (
            base_picture
            + ",drawbox=x=0:y=1380:w=1080:h=540:color=0x171A1C@0.48:t=fill"
            + ",drawbox=x=0:y=1680:w=1080:h=240:color=0x171A1C@0.88:t=fill"
            + f",drawbox=x=54:y=1374:w=972:h=4:color={ORANGE}:t=fill"
        )

        # All assets in this proof are generated reconstructions; label them truthfully.
        vf += (
            ",drawtext=font='DejaVu Sans':text='AI RECONSTRUCTION':"
            "x=w-text_w-42:y=46:fontsize=19:fontcolor=0xF3EBDD:"
            "borderw=2:bordercolor=black@0.72"
        )

        metric = draw_escape(segment.get("metric", ""))

        if metric:
            vf += (
                f",drawtext=font='DejaVu Sans':text='{metric}':"
                f"x=54:y=1286:fontsize=42:fontcolor={PAPER}:"
                "borderw=3:bordercolor=black@0.82"
            )

        if index == 0:
            title_1 = draw_escape(plan["title_lines"][0])
            title_2 = draw_escape(plan["title_lines"][1])
            vf += (
                f",drawtext=font='DejaVu Sans':text='{title_1}':"
                f"x=(w-text_w)/2:y=150:fontsize=44:fontcolor={PAPER}:"
                "borderw=4:bordercolor=black@0.90:enable='between(t,0,2.6)',"
                f"drawtext=font='DejaVu Sans':text='{title_2}':"
                f"x=(w-text_w)/2:y=202:fontsize=44:fontcolor={PAPER}:"
                "borderw=4:bordercolor=black@0.90:enable='between(t,0,2.6)'"
            )

        filters.append(f"[{index}:v]{vf},fps={fps},setsar=1[v{index}]")
        video_labels.append(f"[v{index}]")

    filters.append(
        "".join(video_labels)
        + f"concat=n={len(video_labels)}:v=1:a=0[vcat]"
    )

    ass_filter_path = str(ass_path).replace(":", r"\:")
    filters.append(f"[vcat]ass='{ass_filter_path}'[vout]")

    # Exact locked long-form audio excerpt.
    inputs += [
        "-ss", f"{float(short['source_in_sec']):.3f}",
        "-t", f"{duration:.3f}",
        "-i", audio_source,
    ]
    audio_input_index = len(plan["segments"])

    command = [
        "ffmpeg", "-y", "-loglevel", "error",
        *inputs,
        "-filter_complex", ";".join(filters),
        "-map", "[vout]",
        "-map", f"{audio_input_index}:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-ac", "2",
        "-movflags", "+faststart",
        output,
    ]
    subprocess.run(command, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--map", required=True)
    parser.add_argument("--asset-dir", required=True)
    parser.add_argument("--audio-source", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--qc", required=True)
    args = parser.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    mapping = json.loads(Path(args.map).read_text(encoding="utf-8"))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    build(plan, mapping, args.asset_dir, args.audio_source, args.out, args.qc)

if __name__ == "__main__":
    main()
