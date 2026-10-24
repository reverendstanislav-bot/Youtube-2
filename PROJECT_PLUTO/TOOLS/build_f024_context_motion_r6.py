#!/usr/bin/env python3
"""Cut useful 1956 aerospace-engineering context scenes from verified F024."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


REPO = Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
BANK = Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_V2")
SOURCE = BANK / "00_ACQUISITION" / "new_video_audit" / "F024_source" / "F024.webm"
OUT = BANK / "11_CONTEXT_F024_AEROSPACE_INDUSTRY"
SHEETS = BANK / "12_F024_SELECTED_CONTACT_SHEETS"
MANIFEST = REPO / "PROJECT_PLUTO" / "SOURCE_BANK_V2" / "F024_CONTEXT_MOTION_R6_MANIFEST.csv"

# These ranges intentionally exclude generic bomber flight padding and titles.
CLIPS = [
    ("F024-R6-01", 12, 27, "Overhead crane moving a large aircraft structure", "PLUTO-CH03-B01"),
    ("F024-R6-02", 36, 51, "Close work on aircraft structural hardware", "PLUTO-CH03-B01"),
    ("F024-R6-03", 54, 69, "Technicians assembling a large wing structure", "PLUTO-CH03-B01"),
    ("F024-R6-04", 72, 87, "Engineer marking and inspecting aircraft structure", "PLUTO-CH03-B01"),
    ("F024-R6-05", 90, 105, "Engineering group working over plans", "PLUTO-CH03-B01"),
    ("F024-R6-06", 108, 123, "Scale aircraft model used in design discussion", "PLUTO-CH03-B01"),
    ("F024-R6-07", 126, 141, "Engineers discussing a configuration model", "PLUTO-CH03-B01"),
    ("F024-R6-08", 144, 159, "Period computing and electronics room", "PLUTO-CH03-B03"),
    ("F024-R6-09", 162, 177, "Rows of period electronic computing equipment", "PLUTO-CH03-B03"),
    ("F024-R6-10", 180, 195, "Close operation of electronic patch panel", "PLUTO-CH03-B03"),
    ("F024-R6-11", 500, 515, "Engineer operating an aerodynamic test installation", "PLUTO-CH03-B03"),
    ("F024-R6-12", 522, 537, "Model and operator in aerodynamic laboratory", "PLUTO-CH03-B03"),
    ("F024-R6-13", 540, 555, "Instrumentation work in an aerodynamic laboratory", "PLUTO-CH03-B03"),
    ("F024-R6-14", 558, 573, "Engineers conferring around laboratory hardware", "PLUTO-CH07-B04"),
    ("F024-R6-15", 576, 591, "Large laboratory test machinery under operation", "PLUTO-CH07-B04"),
    ("F024-R6-16", 594, 609, "Technicians monitoring a complex test installation", "PLUTO-CH07-B04"),
    ("F024-R6-17", 630, 645, "Technical photographic sheets under review", "PLUTO-CH07-B04"),
    ("F024-R6-18", 648, 663, "Engineer comparing photographic test records", "PLUTO-CH07-B04"),
]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    expected = "0b94728eb1b6317738aec49812aca3c03a6a2c833a1b1f7e6548473b47fb6174"
    actual = sha256(SOURCE)
    if actual != expected:
        raise SystemExit(f"F024 SHA mismatch: {actual}")
    OUT.mkdir(parents=True, exist_ok=True)
    SHEETS.mkdir(parents=True, exist_ok=True)
    rows = []
    for clip_id, start, end, context, beat in CLIPS:
        target = OUT / f"{clip_id}.mp4"
        duration = end - start
        run([
            "ffmpeg", "-y", "-ss", str(start), "-i", str(SOURCE), "-t", str(duration),
            "-map", "0:v:0", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(target),
        ])
        run(["ffmpeg", "-v", "error", "-xerror", "-i", str(target), "-f", "null", "-"])
        black = run([
            "ffmpeg", "-hide_banner", "-i", str(target), "-vf",
            "blackdetect=d=0.40:pix_th=0.10", "-an", "-f", "null", "-",
        ]).stderr
        black_intervals = " | ".join(line.strip() for line in black.splitlines() if "black_start:" in line)
        probe = json.loads(run([
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=codec_name,width,height,r_frame_rate:format=duration", "-of", "json", str(target),
        ]).stdout)
        stream = probe["streams"][0]
        run([
            "ffmpeg", "-y", "-i", str(target), "-vf",
            "fps=1/3,scale=320:-2,tile=5x1:padding=6:margin=6:color=0x101820",
            "-frames:v", "1", str(SHEETS / f"{clip_id}.jpg"),
        ])
        rows.append({
            "clip_id": clip_id,
            "file": str(target),
            "source_master": "F024_Boeing_Aircraft_Wichita_Bomber_Maintenance_and_Development_1956",
            "source_sha256": actual,
            "source_in_sec": f"{start:.3f}",
            "source_out_sec": f"{end:.3f}",
            "duration_sec": f"{float(probe['format']['duration']):.3f}",
            "historical_context": context,
            "editorial_purpose": "Period aerospace engineering context; never evidence of Project Pluto or Tory testing",
            "suggested_beat_id": beat,
            "rights_status": "HOLD_ITEM_SPECIFIC_COMMONS_DERIVATIVE_AI_UPSCALE_WARNING",
            "screen_label": "CONTEXT — BOEING WICHITA, 1956 / NOT PROJECT PLUTO",
            "sha256": sha256(target),
            "bytes": target.stat().st_size,
            "codec": stream["codec_name"],
            "width": stream["width"],
            "height": stream["height"],
            "fps": stream["r_frame_rate"],
            "decode_qc": "PASS",
            "black_intervals": black_intervals,
        })
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(json.dumps({"clips": len(rows), "duration_sec": sum(float(r["duration_sec"]) for r in rows), "source_sha256": actual}, indent=2))


if __name__ == "__main__":
    main()
