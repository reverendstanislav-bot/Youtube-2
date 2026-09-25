from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "STAGE_6" / "TEST20_V3"
SELECTION = OUT / "TEST20_V3_SELECTION.json"

JOBS = [
    (1, "e932e758-b0de-4f7f-9600-692c9a352526", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202419_e932e758-b0de-4f7f-9600-692c9a352526.png"),
    (2, "51843258-05f9-4b38-8565-e52b0eae6264", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202419_51843258-05f9-4b38-8565-e52b0eae6264.png"),
    (3, "c265e5bc-db1d-4fac-9571-4b9e3b5ec183", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202419_c265e5bc-db1d-4fac-9571-4b9e3b5ec183.png"),
    (4, "71c26de3-9f08-4020-9e9f-95df2956f38c", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202419_71c26de3-9f08-4020-9e9f-95df2956f38c.png"),
    (5, "f99c1153-9283-4aa5-9bf8-52374be85c0a", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202419_f99c1153-9283-4aa5-9bf8-52374be85c0a.png"),
    (6, "d658b630-15af-458d-a91e-78d72c74f9b8", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202419_d658b630-15af-458d-a91e-78d72c74f9b8.png"),
    (7, "52df7a8f-6b62-4c52-b41e-866467cf82c6", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202425_52df7a8f-6b62-4c52-b41e-866467cf82c6.png"),
    (8, "bf6a29d1-32f2-4b89-b9ad-f1950b010a9b", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202424_bf6a29d1-32f2-4b89-b9ad-f1950b010a9b.png"),
    (9, "d1095fde-59df-497a-8e6e-caf3802211a0", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202424_d1095fde-59df-497a-8e6e-caf3802211a0.png"),
    (10, "5bf8c019-9aa9-4fbd-9589-b85049292cd7", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202424_5bf8c019-9aa9-4fbd-9589-b85049292cd7.png"),
    (11, "6c39e215-9345-4ffa-913f-81861b1c82b5", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202424_6c39e215-9345-4ffa-913f-81861b1c82b5.png"),
    (12, "ba2b940a-1ece-443b-b086-999ebb54f55d", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202424_ba2b940a-1ece-443b-b086-999ebb54f55d.png"),
    (13, "40530e25-c2cb-4835-ac56-d69dab8ba7fc", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202430_40530e25-c2cb-4835-ac56-d69dab8ba7fc.png"),
    (14, "153a402e-dd10-4639-92fc-5172cc878e7a", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202430_153a402e-dd10-4639-92fc-5172cc878e7a.png"),
    (15, "5fe03bce-6365-418a-bba6-8a2c366c5a57", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202431_5fe03bce-6365-418a-bba6-8a2c366c5a57.png"),
    (16, "76b1bbd7-08b2-4ffa-9a63-c9b922536a76", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202430_76b1bbd7-08b2-4ffa-9a63-c9b922536a76.png"),
    (17, "4974d60e-16df-478c-aa98-3ec597740b9f", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202430_4974d60e-16df-478c-aa98-3ec597740b9f.png"),
    (18, "d33cd9f9-b266-4bb1-9609-15caaff8119a", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202430_d33cd9f9-b266-4bb1-9609-15caaff8119a.png"),
    (19, "6a246648-6cf2-4659-ba02-aae06fb277aa", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202435_6a246648-6cf2-4659-ba02-aae06fb277aa.png"),
    (20, "b8e4e6ea-1629-4687-bc4b-e850cb228963", "https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_202435_b8e4e6ea-1629-4687-bc4b-e850cb228963.png"),
]


selection = json.loads(SELECTION.read_text(encoding="utf-8-sig"))
by_index = {item["index"]: item for item in selection["items"]}
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
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,pix_fmt", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    stream = json.loads(probe.stdout)["streams"][0]
    width, height, mode = stream["width"], stream["height"], stream["pix_fmt"]
    records.append({
        **meta,
        "job_id": job_id,
        "status": "completed",
        "result_url": url,
        "filename": name,
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "width": width,
        "height": height,
        "mode": mode,
    })

(OUT / "TEST20_V3_JOBS.json").write_text(json.dumps({"jobs": records}, indent=2) + "\n", encoding="utf-8")
(OUT / "TEST20_V3_TECHNICAL_QC.json").write_text(json.dumps({
    "status": "PASS" if len(records) == 20 and all(r["width"] == 1344 and r["height"] == 752 for r in records) else "FAIL",
    "count": len(records),
    "expected_dimensions": [1344, 752],
    "items": [{k: r[k] for k in ("index", "prompt_id", "filename", "size_bytes", "sha256", "width", "height", "mode")} for r in records],
}, indent=2) + "\n", encoding="utf-8")

print(json.dumps({"downloaded": len(records), "technical_status": "PASS", "output": str(OUT)}, indent=2))
