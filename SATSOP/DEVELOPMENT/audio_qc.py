from __future__ import annotations

import array
import json
import math
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "AUDIO" / "SATSOP_VO_MASTER_V1.wav"


def dbfs(value: float) -> float:
    return -120.0 if value <= 0 else 20.0 * math.log10(value / 32768.0)


with wave.open(str(MASTER), "rb") as wav:
    channels = wav.getnchannels()
    sample_rate = wav.getframerate()
    sample_width = wav.getsampwidth()
    frame_count = wav.getnframes()
    raw = wav.readframes(frame_count)

if channels != 1 or sample_width != 2:
    raise SystemExit(f"Unsupported PCM layout: channels={channels}, width={sample_width}")

samples = array.array("h")
samples.frombytes(raw)
peak = max(abs(x) for x in samples)
sum_sq = sum(x * x for x in samples)
rms = math.sqrt(sum_sq / len(samples))
clipped = sum(1 for x in samples if abs(x) >= 32767)

# Detect sustained quiet using 100 ms RMS windows. This avoids treating zero
# crossings inside speech as silence.
window = sample_rate // 10
quiet_threshold_db = -45.0
quiet = []
for start in range(0, len(samples), window):
    block = samples[start : start + window]
    block_rms = math.sqrt(sum(x * x for x in block) / len(block))
    quiet.append(dbfs(block_rms) <= quiet_threshold_db)

runs = []
run_start = None
for i, is_quiet in enumerate(quiet + [False]):
    if is_quiet and run_start is None:
        run_start = i
    elif not is_quiet and run_start is not None:
        start_sec = run_start * 0.1
        end_sec = min(i * 0.1, len(samples) / sample_rate)
        if end_sec - start_sec >= 1.5:
            runs.append({"start": round(start_sec, 3), "end": round(end_sec, 3), "duration": round(end_sec - start_sec, 3)})
        run_start = None

report = {
    "file": str(MASTER.relative_to(ROOT)),
    "duration_seconds": round(len(samples) / sample_rate, 6),
    "sample_rate": sample_rate,
    "channels": channels,
    "sample_width_bytes": sample_width,
    "peak_dbfs": round(dbfs(peak), 3),
    "rms_dbfs": round(dbfs(rms), 3),
    "clipped_samples": clipped,
    "sustained_quiet_threshold_dbfs": quiet_threshold_db,
    "sustained_quiet_min_seconds": 1.5,
    "sustained_quiet_runs": runs,
}
print(json.dumps(report, indent=2))
