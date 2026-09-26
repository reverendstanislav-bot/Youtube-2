from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "SATSOP/STAGE_8_GENERATED_REPLACEMENTS"
IMAGES = BASE / "IMAGES"


def main() -> None:
    images = sorted(IMAGES.glob("SAT-RPL-*.png"))
    if len(images) != 35:
        raise SystemExit(f"Expected 35 images, found {len(images)}")
    for sheet_no, offset in enumerate(range(0, len(images), 6), 1):
        chunk = images[offset:offset + 6]
        cmd = ["ffmpeg", "-y"]
        for image in chunk:
            cmd += ["-i", str(image)]
        filters = []
        for i, image in enumerate(chunk):
            filters.append(f"[{i}:v]scale=448:251[v{i}]")
        layout = "|".join(f"{(i%3)*448}_{(i//3)*251}" for i in range(len(chunk)))
        inputs = "".join(f"[v{i}]" for i in range(len(chunk)))
        filters.append(f"{inputs}xstack=inputs={len(chunk)}:layout={layout}:fill=171A1C[out]")
        cmd += ["-filter_complex", ";".join(filters), "-map", "[out]", "-frames:v", "1", "-update", "1", str(BASE / f"CONTACT_SHEET_{sheet_no}.jpg")]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Built 6 contact sheets")


if __name__ == "__main__":
    main()
