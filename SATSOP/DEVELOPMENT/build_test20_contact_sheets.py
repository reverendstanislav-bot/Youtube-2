from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
folder = sys.argv[1] if len(sys.argv) > 1 else "TEST20"
prefix = "TEST20_V2" if folder == "TEST20_V2" else "TEST20"
TEST_DIR = ROOT / "STAGE_6" / folder
entries = json.loads((TEST_DIR / f"{prefix}_JOBS.json").read_text(encoding="utf-8"))

report = []
paths = []
for entry in entries:
    path = TEST_DIR / f"{entry['prompt_id']}.png"
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=codec_name,width,height,pix_fmt", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    stream = json.loads(probe.stdout)["streams"][0]
    report.append({
        **entry,
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        **stream,
    })
    paths.append(path)

(TEST_DIR / f"{prefix}_TECHNICAL_QC.json").write_text(
    json.dumps(report, indent=2) + "\n", encoding="utf-8"
)

for page in range(2):
    batch = paths[page * 10 : (page + 1) * 10]
    command = ["ffmpeg", "-y"]
    for path in batch:
        command += ["-i", str(path)]
    scales = ";".join(
        f"[{index}:v]scale=768:432:force_original_aspect_ratio=decrease,"
        f"pad=768:432:(ow-iw)/2:(oh-ih)/2:black[v{index}]"
        for index in range(10)
    )
    layout = "|".join(f"{(index % 2) * 768}_{(index // 2) * 432}" for index in range(10))
    stack_inputs = "".join(f"[v{index}]" for index in range(10))
    command += [
        "-filter_complex", f"{scales};{stack_inputs}xstack=inputs=10:layout={layout}[out]",
        "-map", "[out]", "-frames:v", "1", "-q:v", "2",
        str(TEST_DIR / f"{prefix}_CONTACT_{page + 1}.jpg"),
    ]
    subprocess.run(command, check=True, capture_output=True)

print(f"TECH_QC_PASS={len(report)}")
print(sorted({(item["width"], item["height"], item["codec_name"]) for item in report}))
