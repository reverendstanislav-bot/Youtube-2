from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "SATSOP/STAGE_8_GENERATED_REPLACEMENTS"
OUT = BASE / "IMAGES"


def main() -> None:
    prompts = json.loads((BASE / "SATSOP_35_GENERATED_REPLACEMENTS.json").read_text(encoding="utf-8"))["items"]
    jobs = json.loads((BASE / "HIGGSFIELD_RESULTS.json").read_text(encoding="utf-8-sig"))
    by_index = {int(x["index"]): x for x in jobs}
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for item in prompts:
        job = by_index[item["index"]]
        if job["status"] != "completed" or not job.get("result_url"):
            raise RuntimeError(f"Job {item['index']} is not downloadable: {job}")
        dst = OUT / f"{item['replacement_id']}_{item['beat_id']}.png"
        with urllib.request.urlopen(job["result_url"], timeout=120) as response, dst.open("wb") as fh:
            fh.write(response.read())
        raw = dst.read_bytes()
        if raw[:8] != b"\x89PNG\r\n\x1a\n":
            raise RuntimeError(f"Invalid PNG signature: {dst.name}")
        probe = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,pix_fmt", "-of", "json", str(dst)
        ], text=True))
        stream = probe["streams"][0]
        manifest.append({
            **{k: item[k] for k in ["index", "replacement_id", "beat_id"]},
            "job_id": job["job_id"], "result_url": job["result_url"],
            "filename": dst.name, "size_bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "width": stream["width"], "height": stream["height"], "pix_fmt": stream.get("pix_fmt"),
            "technical_status": "PASS",
        })
    (BASE / "TECHNICAL_QC.json").write_text(json.dumps({"count": len(manifest), "pass": len(manifest), "fail": 0, "items": manifest}, indent=2), encoding="utf-8")
    print(json.dumps({"downloaded": len(manifest), "pass": len(manifest), "directory": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
