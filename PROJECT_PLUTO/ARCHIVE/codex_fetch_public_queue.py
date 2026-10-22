#!/usr/bin/env python3
"""HIA Project Pluto — Codex-only, public, minimal verified downloader.

NO archive requests, no paid media, no credentials/anti-bot bypass, no AI.
By default downloads only one curated Pluto primary-bank ZIP + the 1964 report.
Context movies and the original USAF film are explicit opt-ins.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import urllib.request
import zipfile

REPO = "reverendstanislav-bot/Youtube-2"
BASE = Path(__file__).resolve().parent
QUEUE = BASE / "CODEX_PUBLIC_ONLY_MINIMAL_SOURCE_QUEUE_2026-10-22.csv"
HASH_R5 = "897cddf56a8299f7ca995cf5a94cca19d965bcc0cdca764e70ddf81272572b66"
ORIGINAL = "3d9305615472a3ac7a18c50b1d7a3649d20d34f1e1aab93439f535650191114e"

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def inspect_video(path):
    if not shutil.which("ffprobe"):
        return {"technical_check": "FFPROBE_MISSING"}
    p = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams",
                        "-of", "json", str(path)], capture_output=True, text=True)
    if p.returncode:
        return {"technical_check": "FFPROBE_FAILED", "error": p.stderr[-500:]}
    d = json.loads(p.stdout)
    return {"technical_check": "FFPROBE_PASS", "duration": d.get("format", {}).get("duration"),
            "streams": [{k: s.get(k) for k in ("codec_type", "codec_name", "width",
                        "height", "r_frame_rate")} for s in d.get("streams", [])]}

def download(row, root):
    url = row["public_url"]
    name = url.rsplit("/", 1)[-1]
    target = root / "verified" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    want = row["known_sha256"]
    rec = {"id": row["asset_id"], "url": url, "file": str(target),
           "role": row["asset_role"], "rights": row["publication_rights"]}
    if target.exists():
        found = digest(target)
        if found == want:
            rec.update(status="PASS_ALREADY_PRESENT", size=target.stat().st_size, sha256=found)
            return rec
        rec.update(status="HOLD_EXISTING_FILE_HASH_MISMATCH", sha256=found)
        return rec

    tmp = target.with_suffix(target.suffix + ".partial")
    try:
        headers = {"User-Agent": "HIA public archival research downloader (public sources only)"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=50) as resp, tmp.open("wb") as output:
            for block in iter(lambda: resp.read(1024 * 1024), b""):
                output.write(block)
        got = digest(tmp)
        if got != want:
            rec.update(status="REJECT_SHA256_MISMATCH", sha256=got)
            tmp.unlink(missing_ok=True)
            return rec
        tmp.rename(target)
        rec.update(status="PASS_DOWNLOAD_AND_HASH", size=target.stat().st_size, sha256=got)
        if target.suffix.lower() == ".mp4":
            rec.update(inspect_video(target))
        elif target.suffix.lower() == ".zip":
            with zipfile.ZipFile(target) as z:
                problem = z.testzip()
                rec["zip_crc"] = "PASS" if problem is None else f"FAIL:{problem}"
        return rec
    except Exception as ex:
        rec.update(status="HOLD_DOWNLOAD_FAILED", error=str(ex)[:500])
        tmp.unlink(missing_ok=True)
        return rec

def recover_usaf(root):
    loc = root / "raw_USAF_38912"
    loc.mkdir(parents=True, exist_ok=True)
    if not shutil.which("gh"):
        return {"id": "LASVN1_ORIGINAL", "status": "HOLD_GH_CLI_MISSING"}
    cmd = ["gh", "run", "download", "39782104767", "-R", REPO, "-n",
           "LASVN1_Primary_1963_Research_Mirror_Rights_PENDING", "-D", str(loc)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    original = loc / "USAF38912_LASVN1_1963.mp4"
    if p.returncode or not original.exists():
        return {"id": "LASVN1_ORIGINAL", "status": "HOLD_ACTION_ARTIFACT_RETRIEVAL_FAILED",
                "details": (p.stderr or p.stdout)[-700:]}
    actual = digest(original)
    return {"id": "LASVN1_ORIGINAL", "file": str(original),
            "status": "PASS_USAF_SOURCE_BINARY" if actual == ORIGINAL else "REJECT_SHA256_MISMATCH",
            "sha256": actual, "bytes": original.stat().st_size, **inspect_video(original)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dest", default="PROJECT_PLUTO/CODEX_REAL_MEDIA")
    p.add_argument("--context", action="store_true", help="F015 Hound Dog and F013 Minuteman")
    p.add_argument("--x15", action="store_true", help="EXCEPTION: separate-program NASA film")
    p.add_argument("--doc2", action="store_true", help="EXCEPTION: large engineering PDF")
    p.add_argument("--original", action="store_true", help="Use gh CLI to recover 1963 original")
    p.add_argument("--r5", help="Local path to user-provided 34-clip R5 zip; not in GitHub Release")
    args = p.parse_args()
    root = Path(args.dest)
    root.mkdir(parents=True, exist_ok=True)
    with QUEUE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    choices = {"PLUTO_PRIMARY_EDITOR_BANK", "PLUTO_Q2_1964_REPORT"}
    if args.context:
        choices |= {"HOUND_DOG_B52", "MINUTEMAN_1962"}
    if args.x15:
        choices.add("NASA_X15_LAB")
    if args.doc2:
        choices.add("PLUTO_TORY_ENGINEERING_DESIGN")
    report = []
    for row in rows:
        if row["asset_id"] in choices:
            rec = download(row, root)
            report.append(rec)
            print(rec["id"], rec["status"], flush=True)
    if args.original:
        rec = recover_usaf(root)
        report.append(rec)
        print(rec["id"], rec["status"], flush=True)
    if args.r5:
        path = Path(args.r5)
        if path.is_file() and digest(path) == HASH_R5:
            report.append({"id": "R5_34_CLIPS", "status": "PASS_LOCAL_R5_HASH",
                           "file": str(path), "bytes": path.stat().st_size})
        else:
            report.append({"id": "R5_34_CLIPS", "status": "HOLD_R5_NOT_PRESENT_OR_HASH_MISMATCH"})
    report.append({"id": "VOICE_SCRIPT_TIMING", "status": "AUDIO_TIMING_HOLD_UNLESS_LOCKED_AUDIO_PROVIDED"})
    log = root / "SOURCE_DOWNLOAD_REPORT.json"
    log.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("WRITTEN", log)
    n = sum(v.get("status", "").startswith("PASS_") for v in report)
    print("VERIFIED", n, "OF", len(report), "records; do not claim missing resources acquired.")

if __name__ == "__main__":
    main()
