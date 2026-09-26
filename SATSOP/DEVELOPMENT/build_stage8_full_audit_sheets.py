from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REM = ROOT / "SATSOP/REMOTION_V1"
VIDEO = REM / "out/SATSOP_ROUGH_CUT_V1.mp4"
TIMELINE = REM / "public/timeline.json"
OUT = REM / "REVIEW_QC/FULL_AUDIT"
THUMBS = OUT / "thumbs"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    beats = json.loads(TIMELINE.read_text(encoding="utf-8"))["beats"]
    if OUT.exists():
        shutil.rmtree(OUT)
    THUMBS.mkdir(parents=True)
    index = []
    for i, beat in enumerate(beats, 1):
        t = (beat["start"] + beat["end"]) / 2
        thumb = THUMBS / f"{i:03d}_{beat['beat']}.jpg"
        run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", str(VIDEO), "-frames:v", "1", "-vf", "scale=448:252", "-q:v", "3", "-update", "1", str(thumb)])
        index.append({"index": i, "beat": beat["beat"], "time": round(t, 3), "kind": beat["kind"], "chapter": beat["chapter"], "narration": beat["narration"], "thumbnail": thumb.name})
    for sheet_no, offset in enumerate(range(0, len(index), 12), 1):
        chunk = index[offset:offset + 12]
        sheet = OUT / f"AUDIT_SHEET_{sheet_no:02d}.jpg"
        if len(chunk) == 1:
            shutil.copy2(THUMBS / chunk[0]["thumbnail"], sheet)
            continue
        cmd = ["ffmpeg", "-loglevel", "error", "-y"]
        for item in chunk:
            cmd += ["-i", str(THUMBS / item["thumbnail"])]
        layout = "|".join(f"{(i%3)*448}_{(i//3)*252}" for i in range(len(chunk)))
        inputs = "".join(f"[{i}:v]" for i in range(len(chunk)))
        cmd += ["-filter_complex", f"{inputs}xstack=inputs={len(chunk)}:layout={layout}:fill=171A1C[out]", "-map", "[out]", "-frames:v", "1", "-update", "1", str(sheet)]
        run(cmd)
    (OUT / "AUDIT_INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"beats": len(index), "sheets": (len(index)+11)//12, "output": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
