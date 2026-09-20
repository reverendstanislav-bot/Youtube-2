#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

DROPBOX_BLOCK = 4 * 1024 * 1024

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def dropbox_content_hash(path: Path) -> str:
    overall = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(DROPBOX_BLOCK)
            if not block:
                break
            overall.update(hashlib.sha256(block).digest())
    return overall.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts-dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--output", default="HIA_CHICAGO_RECOVERED_SOURCE.bin")
    args = ap.parse_args()

    parts_dir = Path(args.parts_dir)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    output = Path(args.output)

    total = 0
    resolved = []
    for item in manifest["parts"]:
        p = parts_dir / item["name"]
        if not p.is_file():
            raise SystemExit(f"MISSING: {p}")
        size = p.stat().st_size
        if size != int(item["size_bytes"]):
            raise SystemExit(f"SIZE MISMATCH: {p.name}: {size} != {item['size_bytes']}")
        dbx = dropbox_content_hash(p)
        if dbx.lower() != item["dropbox_content_hash"].lower():
            raise SystemExit(f"DROPBOX HASH MISMATCH: {p.name}: {dbx}")
        print(f"OK {p.name} size={size} dropbox_hash={dbx}")
        total += size
        resolved.append(p)

    if total != int(manifest["total_bytes"]):
        raise SystemExit(f"TOTAL SIZE MISMATCH: {total} != {manifest['total_bytes']}")

    with output.open("wb") as dst:
        for p in resolved:
            with p.open("rb") as src:
                shutil.copyfileobj(src, dst, length=8 * 1024 * 1024)

    if output.stat().st_size != total:
        raise SystemExit("OUTPUT SIZE MISMATCH")

    digest = sha256_file(output)
    print(f"OUTPUT {output}")
    print(f"BYTES {output.stat().st_size}")
    print(f"SHA256 {digest}")

    try:
        probe = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries",
                "stream=index,codec_name,width,height,r_frame_rate:format=format_name,duration,size,bit_rate",
                "-of", "json", str(output),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0:
            print("FFPROBE_OK")
            print(probe.stdout)
        else:
            print("FFPROBE_NOT_MEDIA_OR_FAILED")
            print(probe.stderr)
    except FileNotFoundError:
        print("ffprobe not installed; binary integrity checks completed.")

if __name__ == "__main__":
    main()
