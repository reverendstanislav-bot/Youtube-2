import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAT = ROOT / "SATSOP"
PUBLIC = SAT / "REMOTION_V1" / "public"
MASTER = SAT / "DELIVERY" / "SATSOP_FINAL_UPLOAD_MASTER.mp4"
BUILDER = ROOT / "SHORTS_RENDER" / "build_locked_native_vertical.py"
OUT = SAT / "SHORTS" / "out"
QC = SAT / "SHORTS" / "qc"
PLANS = SAT / "SHORTS" / "plans"
MAP_PATH = SAT / "SHORTS" / "satsop_shorts_map.json"

SHORTS = [
    {
        "id": "SAT-S01",
        "title": "Two Towers, Two Different Failures",
        "source_in": 0.000,
        "source_out": 54.920,
        "beats": ["SAT-B001", "SAT-B002", "SAT-B003", "SAT-B004", "SAT-B005"],
        "focals": [0.54, 0.50, 0.54, 0.50, 0.50],
    },
    {
        "id": "SAT-S02",
        "title": "Pay Even If It Never Runs",
        "source_in": 203.280,
        "source_out": 249.640,
        "beats": ["SAT-B020", "SAT-B021", "SAT-B022", "SAT-B023", "SAT-B024"],
        "focals": [0.50, 0.48, 0.53, 0.50, 0.50],
    },
    {
        "id": "SAT-S03",
        "title": "74% Complete — Still Cancelled",
        "source_in": 807.618,
        "source_out": 855.808,
        "beats": ["SAT-B076", "SAT-B077", "SAT-B078", "SAT-B079", "SAT-B080"],
        "focals": [0.50, 0.55, 0.50, 0.50, 0.48],
    },
    {
        "id": "SAT-S04",
        "title": "The Nuclear Plant That Found Another Job",
        "source_in": 1039.568,
        "source_out": 1095.811,
        "beats": ["SAT-B098", "SAT-B099", "SAT-B100", "SAT-B101", "SAT-B102"],
        "focals": [0.50, 0.50, 0.50, 0.53, 0.50],
    },
]


def run(command, capture=False):
    result = subprocess.run(
        command,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    return result.stdout if capture else ""


def probe(path):
    return json.loads(
        run(
            [
                "ffprobe", "-v", "error", "-show_entries",
                "stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels:format=duration,size",
                "-of", "json", str(path),
            ],
            capture=True,
        )
    )


def flatten_words(captions):
    words = []
    for cue in captions:
        words.extend(cue["words"])
    return words


def main():
    for folder in (OUT, QC, PLANS):
        folder.mkdir(parents=True, exist_ok=True)

    timeline = json.loads((PUBLIC / "timeline.json").read_text(encoding="utf-8"))
    captions = json.loads((PUBLIC / "captions.json").read_text(encoding="utf-8"))
    beat_lookup = {beat["beat"]: beat for beat in timeline["beats"]}
    all_words = flatten_words(captions)

    mapping = {"source_fps": 30, "shorts": []}
    plan_paths = []
    for item in SHORTS:
        start = item["source_in"]
        end = item["source_out"]
        duration = round(end - start, 3)
        source_words = []
        for word in all_words:
            if float(word["s"]) >= start - 0.001 and float(word["e"]) <= end + 0.001:
                source_words.append(
                    {
                        "w": word["w"],
                        "short_s": round(float(word["s"]) - start, 3),
                        "short_e": round(float(word["e"]) - start, 3),
                    }
                )
        mapping["shorts"].append(
            {
                "id": item["id"],
                "title": item["title"],
                "source_in_sec": start,
                "source_out_sec": end,
                "duration_sec": duration,
                "source_words": source_words,
            }
        )

        segments = []
        for beat_id, focal in zip(item["beats"], item["focals"]):
            beat = beat_lookup[beat_id]
            seg_start = max(start, float(beat["start"]))
            seg_end = min(end, float(beat["end"]))
            if seg_end <= seg_start:
                continue
            segments.append(
                {
                    "out_start": round(seg_start - start, 3),
                    "out_end": round(seg_end - start, 3),
                    "asset": Path(beat["file"]).name,
                    "x": focal,
                    "motion": "static",
                    "provenance": "",
                }
            )
        plan = {
            "id": item["id"],
            "fps": 30,
            "title": item["title"],
            "version": "SATSOP_LOCKED_NATIVE_V1",
            "segments": segments,
        }
        plan_path = PLANS / f"{item['id']}.json"
        plan_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
        plan_paths.append(plan_path)

    MAP_PATH.write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")

    end_source = Path(r"C:\Users\KK\Desktop\Новая папка (3)\Youtube 2\VIDEO 1\HIA_YOUTUBE_UPLOAD_FINAL_COMPLETE\02_SHORTS\CHICAGO\CHI-S01.mp4")
    end_frame = QC / "HIA_VERTICAL_END_SCREEN.png"
    if not end_frame.exists():
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "35.500", "-i", str(end_source), "-frames:v", "1", str(end_frame)])

    results = []
    for item, plan_path in zip(SHORTS, plan_paths):
        sid = item["id"]
        duration = round(item["source_out"] - item["source_in"], 3)
        audio = QC / f"{sid}_audio.wav"
        story = QC / f"{sid}_story.mp4"
        final = OUT / f"{sid}.mp4"
        run(
            [
                "ffmpeg", "-y", "-loglevel", "error", "-ss", f"{item['source_in']:.3f}",
                "-t", f"{duration:.3f}", "-i", str(MASTER), "-vn", "-c:a", "pcm_s16le",
                "-ar", "48000", "-ac", "2", str(audio),
            ]
        )
        print(f"BUILD {sid}", flush=True)
        run(
            [
                "python", str(BUILDER), "--plan", str(plan_path), "--map", str(MAP_PATH),
                "--asset-dir", str(PUBLIC / "assets"), "--audio-source", str(audio),
                "--out", str(story), "--qc", str(QC / sid),
            ]
        )
        run(
            [
                "ffmpeg", "-y", "-loglevel", "error", "-i", str(story),
                "-loop", "1", "-framerate", "30", "-t", "2.400", "-i", str(end_frame),
                "-f", "lavfi", "-t", "2.400", "-i", "anullsrc=r=48000:cl=stereo",
                "-filter_complex",
                "[0:v]fps=30,format=yuv420p[v0];[1:v]scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v1];"
                "[v0][0:a][v1][2:a]concat=n=2:v=1:a=1[v][a]",
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k",
                "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(final),
            ]
        )
        run(["ffmpeg", "-v", "error", "-xerror", "-i", str(final), "-f", "null", "-"])
        info = probe(final)
        actual_duration = float(info["format"]["duration"])
        result = {
            "id": sid,
            "title": item["title"],
            "source_in": item["source_in"],
            "source_out": item["source_out"],
            "story_duration": duration,
            "final_duration": actual_duration,
            "sha256": hashlib.sha256(final.read_bytes()).hexdigest(),
            "size_bytes": final.stat().st_size,
            "probe": info,
            "decode": "PASS",
        }
        results.append(result)
        sample_times = [1.0, duration / 2, max(1.0, duration - 1.0), duration + 1.2]
        sheet_dir = QC / sid / "frames"
        sheet_dir.mkdir(parents=True, exist_ok=True)
        for index, sample in enumerate(sample_times, 1):
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{sample:.3f}", "-i", str(final), "-frames:v", "1", str(sheet_dir / f"{index:02d}_{sample:.3f}.jpg")])
        print(f"PASS {sid} {actual_duration:.3f}s", flush=True)

    (QC / "SATSOP_SHORTS_QC.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = ["# Satsop Shorts QC", "", "Status: **4 / 4 PASS**", "", "| Short | Story | Final | Decode | SHA-256 |", "|---|---:|---:|---|---|"]
    for result in results:
        lines.append(f"| {result['id']} | {result['story_duration']:.3f}s | {result['final_duration']:.3f}s | PASS | `{result['sha256']}` |")
    lines += ["", "- 1080x1920, 30 fps, H.264 High, yuv420p.", "- Approved narration excerpts only; no music and no new TTS.", "- Existing approved Satsop assets only; no new image or video generation.", "- White mobile captions with orange active word.", "- Static full-screen vertical reframes and hard cuts.", "- Approved reusable HIA end screen appended for 2.4 seconds with silent audio."]
    (QC / "SATSOP_SHORTS_QC.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("ALL PASS", flush=True)


if __name__ == "__main__":
    main()
