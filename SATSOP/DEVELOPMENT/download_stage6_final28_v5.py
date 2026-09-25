from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "STAGE_6" / "FINAL28_V5"
queue = json.loads((OUT / "SATSOP_FINAL28_PROMPTS_V5.json").read_text(encoding="utf-8"))
submitted = json.loads((OUT / "FINAL28_V5_SUBMISSIONS.json").read_text(encoding="utf-8"))
by_index = {item["index"]: item for item in queue["items"]}
records = []

for job in submitted["jobs"]:
    index = job["index"]
    meta = by_index[index]
    name = f"{index:02d}_{meta['prompt_id']}_{meta['beat_id']}.png"
    path = OUT / name
    if not path.exists():
        urllib.request.urlretrieve(job["result_url"], path)
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError(f"Not PNG: {path}")
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,pix_fmt", "-of", "json", str(path)], check=True, capture_output=True, text=True)
    stream = json.loads(probe.stdout)["streams"][0]
    records.append({**meta, **job, "filename": name, "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "width": stream["width"], "height": stream["height"], "mode": stream["pix_fmt"]})

(OUT / "SATSOP_FINAL28_V5_JOBS.json").write_text(json.dumps({"jobs": records}, indent=2) + "\n", encoding="utf-8")
status = "PASS" if len(records) == 28 and all(r["status"] == "completed" and r["width"] == 1344 and r["height"] == 752 for r in records) else "FAIL"
(OUT / "SATSOP_FINAL28_V5_TECHNICAL_QC.json").write_text(json.dumps({"status": status, "count": len(records), "items": [{k: r[k] for k in ("index", "prompt_id", "filename", "size_bytes", "sha256", "width", "height", "mode")} for r in records]}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"downloaded": len(records), "technical_status": status, "output": str(OUT)}, indent=2))
