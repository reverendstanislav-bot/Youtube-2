#!/usr/bin/env python3
"""Build and verify the local Project Pluto editor source bank.

The script preserves source binaries, creates Resolve-friendly photo proxies,
copies only explicitly selected comparison footage, and writes fresh manifests
from the physical files instead of trusting historic package metadata.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


REPO = Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
BANK = Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_V2")
OUT = REPO / "PROJECT_PLUTO" / "SOURCE_BANK_V2"
DIRECT = BANK / "04_DIRECT_PLUTO_MOTION_1963"
CONTEXT_ROOT = BANK / "03_CONTEXT_SCENE_BANK_40" / "PROJECT_PLUTO_DELIVERY" / "02_SELECTED_SCENES"
PHOTO_ROOT = BANK / "02_HISTORICAL_PHOTOS_39" / "PROJECT_PLUTO_HIA_PHOTO_ARCHIVE"
PRIMARY_ROOT = BANK / "01_PRIMARY_EDITOR_BANK" / "PROJECT_PLUTO_REAL_VISUAL_EDITOR_BANK"
R5 = REPO / "PROJECT_PLUTO" / "ARCHIVE" / "LASVN1_R5_VERIFIED_VIDEO_SOURCE_MANIFEST_2026-10-22.csv"
CONTEXT_CSV = CONTEXT_ROOT / "SCENE_BANK_40_SOURCE_IN_OUT.csv"
PHOTO_CSV = PHOTO_ROOT / "PHOTO_MASTER_INDEX.csv"

SELECT_CONTEXT = {
    "SC019", "SC020", "SC021", "SC022", "SC023", "SC024", "SC025", "SC026",
    "SC027", "SC028", "SC029", "SC030", "SC031", "SC032",
    "SC033", "SC034", "SC035", "SC036", "SC037", "SC038",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe_video(path: Path) -> dict:
    p = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate",
        "-of", "json", str(path),
    ])
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    data = json.loads(p.stdout)
    video = next(s for s in data["streams"] if s.get("codec_type") == "video")
    return {
        "duration_sec": round(float(data["format"]["duration"]), 3),
        "codec": video.get("codec_name", ""),
        "width": video.get("width", ""),
        "height": video.get("height", ""),
        "fps": video.get("avg_frame_rate") or video.get("r_frame_rate", ""),
    }


def qc_video(path: Path) -> dict:
    meta = probe_video(path)
    dec = run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-map", "0:v:0", "-f", "null", "-"])
    black = run([
        "ffmpeg", "-hide_banner", "-i", str(path), "-vf",
        "blackdetect=d=0.40:pix_th=0.10", "-an", "-f", "null", "-",
    ])
    black_lines = [line.strip() for line in black.stderr.splitlines() if "black_start:" in line]
    return {
        **meta,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "decode_qc": "PASS" if dec.returncode == 0 else "FAIL",
        "black_intervals": " | ".join(black_lines),
    }


def contact_sheet(path: Path, out: Path, label: str, duration: float) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    interval = max(duration / 6.0, 0.2)
    tmp = out.with_suffix(".raw.jpg")
    p = run([
        "ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf",
        f"fps=1/{interval:.6f},scale=426:-2,tile=3x2:padding=4:margin=4",
        "-frames:v", "1", "-q:v", "3", str(tmp),
    ])
    if p.returncode or not tmp.exists():
        return
    with Image.open(tmp) as im:
        canvas = Image.new("RGB", (im.width, im.height + 42), "#111820")
        canvas.paste(im.convert("RGB"), (0, 42))
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 12), f"{label}  |  {duration:.2f}s", fill="#f2f1ea", font=ImageFont.load_default())
        canvas.save(out, quality=92)
    tmp.unlink(missing_ok=True)


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def load_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def make_photo_proxy(src: Path, dst: Path) -> dict:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        original = im.size
        if max(im.size) > 3840:
            scale = 3840 / max(im.size)
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        im.save(dst, "JPEG", quality=95, subsampling=0, optimize=True)
        return {"source_width": original[0], "source_height": original[1], "proxy_width": im.width, "proxy_height": im.height}


def aggregate_contacts(source_dir: Path, output_dir: Path, prefix: str) -> int:
    files = sorted(source_dir.glob("*.jpg"))
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for page_no, offset in enumerate(range(0, len(files), 9), 1):
        batch = files[offset:offset + 9]
        canvas = Image.new("RGB", (1290, 3 * 284), "#0d141a")
        draw = ImageDraw.Draw(canvas)
        for idx, path in enumerate(batch):
            with Image.open(path) as im:
                im = im.convert("RGB")
                im.thumbnail((420, 250), Image.Resampling.LANCZOS)
                x = (idx % 3) * 430 + 5
                y = (idx // 3) * 284 + 28
                canvas.paste(im, (x, y))
                draw.text((x + 5, y - 20), path.stem, fill="#f2f1ea", font=ImageFont.load_default())
        canvas.save(output_dir / f"{prefix}_{page_no:02d}.jpg", quality=92)
        count += 1
    return count


def photo_review_pages(source_dir: Path, output_dir: Path) -> int:
    files = sorted(source_dir.glob("*.jpg"))
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for page_no, offset in enumerate(range(0, len(files), 9), 1):
        canvas = Image.new("RGB", (1290, 810), "#0d141a")
        draw = ImageDraw.Draw(canvas)
        for idx, path in enumerate(files[offset:offset + 9]):
            with Image.open(path) as src:
                im = src.convert("RGB")
                im.thumbnail((410, 230), Image.Resampling.LANCZOS)
                x = (idx % 3) * 430 + 8
                y = (idx // 3) * 270 + 28
                canvas.paste(im, (x, y))
                draw.text((x, y - 18), path.stem, fill="#f2f1ea", font=ImageFont.load_default())
        canvas.save(output_dir / f"PHOTO_REVIEW_{page_no:02d}.jpg", quality=92)
        count += 1
    return count


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    contact_root = BANK / "07_CONTACT_SHEETS"

    r5_by_id = {r["clip_id"]: r for r in load_csv(R5)}
    direct_files = sorted(DIRECT.glob("SLAM-*.mp4"))
    direct_qc: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(qc_video, p): p for p in direct_files}
        for fut in as_completed(futures):
            p = futures[fut]
            direct_qc[p.stem] = fut.result()

    direct_rows = []
    for p in direct_files:
        old = r5_by_id[p.stem]
        q = direct_qc[p.stem]
        contact_sheet(p, contact_root / "DIRECT" / f"{p.stem}.jpg", p.stem, q["duration_sec"])
        direct_rows.append({
            "clip_id": p.stem,
            "file": str(p),
            "source_master": "USAF38912_LASVN1_1963",
            "source_in_sec": old["origin_1963_sec_in"],
            "source_out_sec_selected": round(float(old["origin_1963_sec_in"]) + float(q["duration_sec"]), 3),
            "source_out_sec_r5_candidate": old["origin_1963_sec_out"],
            "historical_context": old["what_is_visibly_shown"],
            "chapter": old["chapter_provisional"],
            "editorial_role": "DIRECT_PROJECT_PLUTO_LASVN1_ENGINEERING_MOTION",
            "rights_status": "HOLD_THIRD_PARTY_MIRROR_ITEM_REVIEW_REQUIRED",
            "screen_label": "PROJECT PLUTO RESEARCH FILM — 1963",
            **q,
        })
    write_csv(OUT / "DIRECT_PLUTO_MOTION_MANIFEST_V2.csv", direct_rows, list(direct_rows[0]))

    context_meta = {r["scene_id"]: r for r in load_csv(CONTEXT_CSV)}
    selected_dir = BANK / "05_CONTEXT_MOTION_LABELLED"
    selected_dir.mkdir(parents=True, exist_ok=True)
    context_rows = []
    for scene_id in sorted(SELECT_CONTEXT):
        matches = list(CONTEXT_ROOT.glob(f"*/{scene_id}_*.mp4"))
        if len(matches) != 1:
            raise RuntimeError(f"Expected one file for {scene_id}, got {matches}")
        src = matches[0]
        dst = selected_dir / src.name
        if not dst.exists() or sha256(dst) != sha256(src):
            shutil.copy2(src, dst)
        q = qc_video(dst)
        meta = context_meta[scene_id]
        contact_sheet(dst, contact_root / "CONTEXT" / f"{scene_id}.jpg", scene_id, q["duration_sec"])
        context_rows.append({
            "scene_id": scene_id,
            "file": str(dst),
            "source_film_id": meta["source_id"],
            "source_in_sec": meta["start_seconds"],
            "source_out_sec": meta["end_seconds"],
            "historical_context": meta["description"],
            "editorial_purpose": meta["possible_use"],
            "editorial_role": "REAL_DIFFERENT_PROGRAM_CONTEXT",
            "rights_status": "HOLD_ITEM_SPECIFIC_SOURCE_REVIEW",
            "screen_label": "CONTEXT — DIFFERENT U.S. PROGRAM",
            **q,
        })
    write_csv(OUT / "CONTEXT_MOTION_MANIFEST_V2.csv", context_rows, list(context_rows[0]))

    inventory_rows = []
    for meta in load_csv(CONTEXT_CSV):
        scene_id = meta["scene_id"]
        matches = list(CONTEXT_ROOT.glob(f"*/{scene_id}_*.mp4"))
        if len(matches) != 1:
            continue
        p = matches[0]
        inventory_rows.append({
            "scene_id": scene_id,
            "file": str(p),
            "source_film_id": meta["source_id"],
            "source_in_sec": meta["start_seconds"],
            "source_out_sec": meta["end_seconds"],
            "historical_context": meta["description"],
            "editorial_purpose": meta["possible_use"],
            "selection_status": "EDITOR_READY_CONTEXT" if scene_id in SELECT_CONTEXT else "RESERVE_CONTEXT_ONLY",
            "provenance_guard": meta["source_subject_qualification"],
            "bytes": p.stat().st_size,
            "sha256": sha256(p),
        })
    write_csv(OUT / "CONTEXT_ALL_40_INVENTORY_V2.csv", inventory_rows, list(inventory_rows[0]))

    photo_index = load_csv(PHOTO_CSV)
    proxy_root = BANK / "06_EDITOR_READY_PHOTOS_4K_JPEG"
    photo_rows = []
    for row in photo_index:
        src = PHOTO_ROOT / row["file"]
        dst = proxy_root / (src.stem + "_4K.jpg")
        dims = make_photo_proxy(src, dst)
        photo_rows.append({
            "asset_id": src.stem,
            "source_file": str(src),
            "editor_proxy": str(dst),
            "source_sha256": sha256(src),
            "proxy_sha256": sha256(dst),
            "historical_context": row["class"],
            "date_context": row["date"],
            "rights_status": row["rights"],
            **dims,
        })
    write_csv(OUT / "HISTORICAL_PHOTO_MANIFEST_V2.csv", photo_rows, list(photo_rows[0]))

    figures = sorted((PRIMARY_ROOT / "02_PRIMARY_ENGINEERING_REPORT_FIGURES").glob("*.png"))
    figure_rows = []
    for src in figures:
        with Image.open(src) as im:
            figure_rows.append({
                "asset_id": src.stem,
                "file": str(src),
                "bytes": src.stat().st_size,
                "sha256": sha256(src),
                "width": im.width,
                "height": im.height,
                "historical_context": "ORIGINAL_ENGINEERING_REPORT_FIGURE",
                "rights_status": "FEDERAL_REPORT_SOURCE_ITEM_REVIEW_RETAIN_CITATION",
            })
    write_csv(OUT / "ENGINEERING_FIGURE_MANIFEST_V2.csv", figure_rows, list(figure_rows[0]))

    aggregate_pages = aggregate_contacts(contact_root / "DIRECT", contact_root / "REVIEW_PAGES", "DIRECT_REVIEW")
    aggregate_pages += aggregate_contacts(contact_root / "CONTEXT", contact_root / "REVIEW_PAGES", "CONTEXT_REVIEW")
    aggregate_pages += photo_review_pages(proxy_root, contact_root / "REVIEW_PAGES")
    summary = {
        "direct_motion": len(direct_rows),
        "direct_duration_sec": round(sum(float(r["duration_sec"]) for r in direct_rows), 3),
        "direct_decode_pass": sum(r["decode_qc"] == "PASS" for r in direct_rows),
        "selected_context_motion": len(context_rows),
        "selected_context_duration_sec": round(sum(float(r["duration_sec"]) for r in context_rows), 3),
        "selected_context_decode_pass": sum(r["decode_qc"] == "PASS" for r in context_rows),
        "all_context_inventory": len(inventory_rows),
        "historical_photos": len(photo_rows),
        "engineering_figures": len(figure_rows),
        "contact_sheets": len(list(contact_root.rglob("*.jpg"))),
        "aggregate_review_pages": aggregate_pages,
        "note": "Context motion is visually labelled as a different program; no context clip may depict a Tory test.",
    }
    (OUT / "EDITOR_BANK_V2_TECHNICAL_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
