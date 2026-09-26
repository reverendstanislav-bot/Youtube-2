from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REM = ROOT / "SATSOP/REMOTION_V1"
VIDEO = REM / "out/SATSOP_ROUGH_CUT_V1.mp4"
OUT = REM / "REVIEW_QC/CARD_AUDIT"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    cards = json.loads((REM / "public/overlays.json").read_text(encoding="utf-8"))["cards"]
    if OUT.exists():
        shutil.rmtree(OUT)
    thumbs = OUT / "thumbs"
    thumbs.mkdir(parents=True)
    for i, card in enumerate(cards, 1):
        t = (card["s"] + card["e"]) / 2
        dst = thumbs / f"{i:02d}_{card['beat']}.jpg"
        run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", str(VIDEO), "-frames:v", "1", "-vf", "scale=448:252", "-q:v", "3", "-update", "1", str(dst)])
    images = sorted(thumbs.glob("*.jpg"))
    for sheet_no, offset in enumerate(range(0, len(images), 12), 1):
        chunk = images[offset:offset + 12]
        cmd = ["ffmpeg", "-loglevel", "error", "-y"]
        for path in chunk:
            cmd += ["-i", str(path)]
        layout = "|".join(f"{(i % 3) * 448}_{(i // 3) * 252}" for i in range(len(chunk)))
        inputs = "".join(f"[{i}:v]" for i in range(len(chunk)))
        cmd += ["-filter_complex", f"{inputs}xstack=inputs={len(chunk)}:layout={layout}:fill=171A1C[out]", "-map", "[out]", "-frames:v", "1", "-update", "1", str(OUT / f"CARD_AUDIT_{sheet_no:02d}.jpg")]
        run(cmd)
    print(json.dumps({"cards": len(cards), "sheets": (len(cards) + 11) // 12}))


if __name__ == "__main__":
    main()
