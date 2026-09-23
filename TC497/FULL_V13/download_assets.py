#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

MANIFEST = Path(__file__).with_name("asset_urls.json")

def curl(url, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["curl", "-fL", "--retry", "4", "--retry-all-errors", url, "-o", str(out)],
        check=True,
    )
    if not out.exists() or out.stat().st_size == 0:
        raise RuntimeError(f"empty download: {out}")

def download_group(items, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for name, url in sorted(items.items()):
        curl(url, outdir / name)

def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    v4 = data.get("v4_extra", {})
    v5 = data.get("v5_patch", {})
    v6 = data.get("v6_patch", {})

    if len(v4) != 39:
        raise SystemExit(f"Expected exactly 39 V4 extras, found {len(v4)}")
    if len(v5) != 7:
        raise SystemExit(f"Expected exactly 7 V5 patch assets, found {len(v5)}")
    if set(v6) != {"electric_human_v6.png", "electric_wheel_v6.png"}:
        raise SystemExit(f"Unexpected V6 patch manifest: {sorted(v6)}")

    download_group(v4, "/tmp/v13/v4extra")
    download_group(v5, "/tmp/v13/v5patch")
    download_group(v6, "/tmp/v13/patch")

    print("downloaded", len(v4), "V4 extras and", len(v5) + len(v6), "patch assets")

if __name__ == "__main__":
    main()
