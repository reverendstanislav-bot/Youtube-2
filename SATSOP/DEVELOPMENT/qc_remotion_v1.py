from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "SATSOP/REMOTION_V1/out/SATSOP_ROUGH_CUT_V1.mp4"
OUT = ROOT / "SATSOP/REMOTION_V1/REVIEW_QC"


def main() -> None:
    if not VIDEO.exists() or VIDEO.stat().st_size == 0:
        raise SystemExit("Rendered video is missing or empty")
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(VIDEO)
    ], text=True))
    OUT.mkdir(parents=True, exist_ok=True)
    samples = [5, 180, 360, 580, 800, 1000, 1155]
    for i, t in enumerate(samples, 1):
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(t), "-i", str(VIDEO), "-frames:v", "1", "-q:v", "2",
            str(OUT / f"sample_{i:02d}_{t:04d}s.jpg")
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    digest = hashlib.sha256(VIDEO.read_bytes()).hexdigest()
    streams = probe["streams"]
    video = next(x for x in streams if x["codec_type"] == "video")
    audio = next(x for x in streams if x["codec_type"] == "audio")
    duration = float(probe["format"]["duration"])
    report = {
        "status": "PASS" if abs(duration - 1163.92) <= 0.08 else "FAIL",
        "file": str(VIDEO.relative_to(ROOT)).replace("\\", "/"),
        "size_bytes": VIDEO.stat().st_size,
        "sha256": digest,
        "duration_seconds": duration,
        "expected_duration_seconds": 1163.92,
        "video": {k: video.get(k) for k in ["codec_name", "width", "height", "r_frame_rate", "pix_fmt", "nb_frames"]},
        "audio": {k: audio.get(k) for k in ["codec_name", "sample_rate", "channels", "channel_layout"]},
        "sample_frames": [p.name for p in sorted(OUT.glob("sample_*.jpg"))],
    }
    (OUT / "TECHNICAL_QC.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
