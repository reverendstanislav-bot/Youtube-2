#!/usr/bin/env python3
"""Restore the usable R5 selection as 5-30 second editor clips."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
BANK = Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_V2")
SOURCE = BANK / "00_ACQUISITION" / "raw_USAF_38912" / "USAF38912_LASVN1_1963_PROPER_MP4_REMUX.mp4"
R5 = REPO / "PROJECT_PLUTO" / "ARCHIVE" / "LASVN1_R5_VERIFIED_VIDEO_SOURCE_MANIFEST_2026-10-22.csv"
OUT = BANK / "09_DIRECT_PLUTO_MOTION_R6_MAX_933S"
CONTACTS = BANK / "10_R6_CONTACT_SHEETS"
MANIFEST = REPO / "PROJECT_PLUTO" / "SOURCE_BANK_V2" / "DIRECT_PLUTO_MOTION_R6_MAX_MANIFEST.csv"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def split_range(start: float, end: float) -> list[tuple[float, float]]:
    duration = end - start
    parts = max(1, math.ceil(duration / 30.0))
    step = duration / parts
    return [(start + i * step, start + (i + 1) * step) for i in range(parts)]


def render(job: dict) -> dict:
    path = Path(job["file"])
    duration = job["source_out_sec"] - job["source_in_sec"]
    if not path.exists():
        p = run([
            "ffmpeg", "-y", "-v", "error", "-ss", f"{job['source_in_sec']:.6f}",
            "-i", str(SOURCE), "-t", f"{duration:.6f}", "-map", "0:v:0", "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(path),
        ])
        if p.returncode:
            raise RuntimeError(f"render failed {path.name}: {p.stderr}")
    probe = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_name,width,height,avg_frame_rate", "-of", "json", str(path),
    ])
    data = json.loads(probe.stdout)
    stream = data["streams"][0]
    actual = float(data["format"]["duration"])
    decode = run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"])
    black = run([
        "ffmpeg", "-hide_banner", "-i", str(path), "-vf",
        "blackdetect=d=0.40:pix_th=0.10", "-an", "-f", "null", "-",
    ])
    black_lines = [x.strip() for x in black.stderr.splitlines() if "black_start:" in x]
    return {
        **job,
        "duration_sec": round(actual, 3),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "codec": stream.get("codec_name", ""),
        "width": stream.get("width", ""),
        "height": stream.get("height", ""),
        "fps": stream.get("avg_frame_rate", ""),
        "decode_qc": "PASS" if decode.returncode == 0 else "FAIL",
        "black_intervals": " | ".join(black_lines),
    }


def contact(row: dict) -> None:
    path = Path(row["file"])
    raw = CONTACTS / "individual" / f"{row['clip_id']}.raw.jpg"
    out = CONTACTS / "individual" / f"{row['clip_id']}.jpg"
    raw.parent.mkdir(parents=True, exist_ok=True)
    interval = max(float(row["duration_sec"]) / 6, 0.2)
    p = run([
        "ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf",
        f"fps=1/{interval:.6f},scale=426:-2,tile=3x2:padding=4:margin=4",
        "-frames:v", "1", "-q:v", "3", str(raw),
    ])
    if p.returncode or not raw.exists():
        return
    with Image.open(raw) as im:
        canvas = Image.new("RGB", (im.width, im.height + 42), "#101820")
        canvas.paste(im.convert("RGB"), (0, 42))
        ImageDraw.Draw(canvas).text(
            (10, 12),
            f"{row['clip_id']} | source {row['source_in_sec']:.3f}-{row['source_out_sec']:.3f}",
            fill="#f2f1ea", font=ImageFont.load_default(),
        )
        canvas.save(out, quality=92)
    raw.unlink(missing_ok=True)


def aggregate() -> int:
    files = sorted((CONTACTS / "individual").glob("*.jpg"))
    review = CONTACTS / "review_pages"
    review.mkdir(parents=True, exist_ok=True)
    count = 0
    for page_no, offset in enumerate(range(0, len(files), 9), 1):
        canvas = Image.new("RGB", (1290, 852), "#0d141a")
        draw = ImageDraw.Draw(canvas)
        for idx, path in enumerate(files[offset:offset + 9]):
            with Image.open(path) as src:
                im = src.convert("RGB")
                im.thumbnail((420, 250), Image.Resampling.LANCZOS)
                x = (idx % 3) * 430 + 5
                y = (idx // 3) * 284 + 28
                canvas.paste(im, (x, y))
                draw.text((x + 5, y - 20), path.stem, fill="#f2f1ea", font=ImageFont.load_default())
        canvas.save(review / f"R6_DIRECT_REVIEW_{page_no:02d}.jpg", quality=92)
        count += 1
    return count


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with R5.open("r", newline="", encoding="utf-8-sig") as f:
        r5_rows = list(csv.DictReader(f))
    jobs = []
    for r in r5_rows:
        source_start = float(r["origin_1963_sec_in"])
        source_end = float(r["origin_1963_sec_out"])
        # The final 0.5 seconds of SLAM-25B contain a detected black tail.
        # Preserve the entire meaningful shot and reject that transition.
        if r["clip_id"] == "SLAM-25B":
            source_end = min(source_end, 1521.5)
        segments = split_range(source_start, source_end)
        for idx, (start, end) in enumerate(segments, 1):
            clip_id = f"R6-{r['clip_id']}-P{idx:02d}"
            jobs.append({
                "clip_id": clip_id,
                "parent_r5_clip_id": r["clip_id"],
                "file": str(OUT / f"{clip_id}.mp4"),
                "source_master": "USAF38912_LASVN1_1963",
                "source_in_sec": round(start, 6),
                "source_out_sec": round(end, 6),
                "chapter": r["chapter_provisional"],
                "historical_context": r["what_is_visibly_shown"],
                "r5_qc_class": r["QC_class"],
                "rights_status": "HOLD_THIRD_PARTY_MIRROR_ITEM_REVIEW_REQUIRED",
                "screen_label": "PROJECT PLUTO RESEARCH FILM — 1963",
            })
    rows = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(render, j): j for j in jobs}
        for fut in as_completed(futures):
            rows.append(fut.result())
    rows.sort(key=lambda r: (r["source_in_sec"], r["clip_id"]))
    for row in rows:
        contact(row)
    fields = list(rows[0])
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(json.dumps({
        "clips": len(rows),
        "duration_sec": round(sum(float(r["duration_sec"]) for r in rows), 3),
        "decode_pass": sum(r["decode_qc"] == "PASS" for r in rows),
        "black_free": sum(not r["black_intervals"] for r in rows),
        "review_pages": aggregate(),
    }, indent=2))


if __name__ == "__main__":
    main()
