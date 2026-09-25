from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "STAGE_6" / "REMAINING_V4"
QUEUE = OUT / "SATSOP_REMAINING_GENERATION_V4.json"

JOBS = [
    (1, "7746e441-4fb0-40eb-9086-c4fd968a98eb", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203555_7746e441-4fb0-40eb-9086-c4fd968a98eb.png"),
    (2, "5562eebc-ea4f-4f3e-8e33-7560b5e00812", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203555_5562eebc-ea4f-4f3e-8e33-7560b5e00812.png"),
    (3, "649dc8a5-9148-4175-be5a-723bdd0e62d7", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203555_649dc8a5-9148-4175-be5a-723bdd0e62d7.png"),
    (4, "5c5095ec-1d44-40a2-a115-8c65c571b312", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203555_5c5095ec-1d44-40a2-a115-8c65c571b312.png"),
    (5, "092604c9-cd05-4c4a-b3b4-2bd1af3aa9be", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203555_092604c9-cd05-4c4a-b3b4-2bd1af3aa9be.png"),
    (6, "d4776e94-f721-4784-a140-78914b1115e6", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203555_d4776e94-f721-4784-a140-78914b1115e6.png"),
    (7, "ba9aa469-bdd7-4095-a86c-906e30e95543", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203600_ba9aa469-bdd7-4095-a86c-906e30e95543.png"),
    (8, "611abda6-9c4e-43b7-9aeb-7df48c4e9374", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203600_611abda6-9c4e-43b7-9aeb-7df48c4e9374.png"),
    (9, "9e29de39-47ad-44d7-aea9-156264e7d8ad", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203600_9e29de39-47ad-44d7-aea9-156264e7d8ad.png"),
    (10, "baa4fc57-964d-4d82-88aa-04bca3d07c83", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203600_baa4fc57-964d-4d82-88aa-04bca3d07c83.png"),
    (11, "cc002375-1df5-4372-afa8-15e089e926c0", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203600_cc002375-1df5-4372-afa8-15e089e926c0.png"),
    (12, "7724c6ae-c692-482a-a71e-fcf8a05364b8", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203601_7724c6ae-c692-482a-a71e-fcf8a05364b8.png"),
    (13, "13b9b664-1e2b-454f-9ef8-eab02820e020", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203606_13b9b664-1e2b-454f-9ef8-eab02820e020.png"),
    (14, "effa83b5-e250-492f-b099-ce99acb6fd65", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203606_effa83b5-e250-492f-b099-ce99acb6fd65.png"),
    (15, "6b332e8e-1797-4c1d-ab35-ad71341812ac", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203606_6b332e8e-1797-4c1d-ab35-ad71341812ac.png"),
    (16, "55ac4a60-fad7-4729-b346-76a8561df9e2", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203606_55ac4a60-fad7-4729-b346-76a8561df9e2.png"),
    (17, "caf608a2-35d1-48c9-a186-f1e42c01d731", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203606_caf608a2-35d1-48c9-a186-f1e42c01d731.png"),
    (18, "4e3fc7cb-16c8-494b-8811-33f3716567d0", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_203606_4e3fc7cb-16c8-494b-8811-33f3716567d0.png"),
]

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
by_index = {item["index"]: item for item in queue["items"]}
records = []
for index, job_id, url in JOBS:
    meta = by_index[index]
    name = f"{index:02d}_{meta['prompt_id']}_{meta['beat_id']}.png"
    path = OUT / name
    if not path.exists():
        urllib.request.urlretrieve(url, path)
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError(f"Not PNG: {path}")
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,pix_fmt", "-of", "json", str(path)], check=True, capture_output=True, text=True)
    stream = json.loads(probe.stdout)["streams"][0]
    records.append({**meta, "job_id": job_id, "status": "completed", "result_url": url, "filename": name, "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "width": stream["width"], "height": stream["height"], "mode": stream["pix_fmt"]})

(OUT / "SATSOP_REMAINING_V4_JOBS.json").write_text(json.dumps({"jobs": records}, indent=2) + "\n", encoding="utf-8")
status = "PASS" if len(records) == 18 and all(r["width"] == 1344 and r["height"] == 752 for r in records) else "FAIL"
(OUT / "SATSOP_REMAINING_V4_TECHNICAL_QC.json").write_text(json.dumps({"status": status, "count": len(records), "items": [{k: r[k] for k in ("index", "prompt_id", "filename", "size_bytes", "sha256", "width", "height", "mode")} for r in records]}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"downloaded": len(records), "technical_status": status, "output": str(OUT)}, indent=2))
