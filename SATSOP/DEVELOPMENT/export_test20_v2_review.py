from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "Youtube-2" / "SATSOP" / "STAGE_6" / "TEST20_V2"
DEST = ROOT / "SATSOP_V2_TEST20_REVIEW"
DEST.mkdir(parents=True, exist_ok=True)

VERDICTS = {
    "SAT-GEN001": ("CONDITIONAL", "Early construction reads, but Project Five identity is not reference-verified."),
    "SAT-GEN002": ("FAIL", "Invented domed reactor building; cannot represent Project Three."),
    "SAT-GEN003": ("FAIL", "Fabricated geography, roads, rivers and completed domes."),
    "SAT-GEN006": ("CONDITIONAL", "Improved sparse works, but exact Project Five identity is unverified."),
    "SAT-GEN011": ("PASS", "Clear non-factual utility-node graphic base with usable overlay space."),
    "SAT-GEN012": ("PASS", "Three-state payment-obligation mechanism reads without generated text."),
    "SAT-GEN016": ("FAIL", "Fabricated coastal geography and reactor geometry."),
    "SAT-GEN020": ("CONDITIONAL", "Clear technical comparison, but engineering geometry needs R04 validation."),
    "SAT-GEN022": ("CONDITIONAL", "System chain reads, but generated engineering layout is not exact."),
    "SAT-GEN025": ("PASS", "Covered equipment and inspection-only activity clearly communicate preservation."),
    "SAT-GEN032": ("PASS", "Missing systems dominate the frame and explain remaining completion work."),
    "SAT-GEN036": ("PASS", "One large commitment versus modular units reads immediately."),
    "SAT-GEN044": ("PASS", "Low/base/high comparison is expressed as a clean physical-model graphic."),
    "SAT-GEN046": ("CONDITIONAL", "Capacity metaphor reads, but exact surplus claim depends on overlay."),
    "SAT-GEN050": ("CONDITIONAL", "Demand context is improved; identity and comparison axis remain implicit."),
    "SAT-GEN057": ("FAIL", "Four landscapes do not distinguish four chronology events."),
    "SAT-GEN058": ("PASS", "Four post-termination workstreams read as distinct physical objects."),
    "SAT-GEN063": ("PASS", "Civic reuse meeting fixes the false renewed-construction interpretation."),
    "SAT-GEN065": ("CONDITIONAL", "Industrial reuse reads, but it is not verified as the Satsop turbine building."),
    "SAT-GEN068": ("CONDITIONAL", "Useful afterlife reads, but present-day Satsop identity is unverified."),
}

jobs = json.loads((SOURCE / "TEST20_V2_JOBS.json").read_text(encoding="utf-8"))
records = []
for entry in jobs:
    prompt_id = entry["prompt_id"]
    verdict, reason = VERDICTS[prompt_id]
    source = SOURCE / f"{prompt_id}.png"
    target = DEST / f"{entry['index']:02d}_{verdict}_{prompt_id}_{entry['beat_id']}.png"
    shutil.copy2(source, target)
    assert source.read_bytes() == target.read_bytes()
    records.append({
        "index": entry["index"],
        "verdict": verdict,
        "prompt_id": prompt_id,
        "beat_id": entry["beat_id"],
        "prompt_grammar": entry["prompt_grammar"],
        "reason": reason,
        "filename": target.name,
        "size_bytes": target.stat().st_size,
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "job_id": entry["job_id"],
    })

for page in (1, 2):
    shutil.copy2(SOURCE / f"TEST20_V2_CONTACT_{page}.jpg", DEST / f"CONTACT_SHEET_{page}.jpg")

with (DEST / "QC_VERDICTS.csv").open("w", newline="", encoding="utf-8-sig") as handle:
    writer = csv.DictWriter(handle, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

summary = [
    "SATSOP V2 TEST20 — MANUAL REVIEW PACKAGE",
    "",
    "20 original PNG files copied bit-for-bit from the local Higgsfield downloads.",
    "Filename format: INDEX_VERDICT_PROMPT_BEAT.png",
    "",
    "My strict verdict: 8 PASS / 8 CONDITIONAL / 4 FAIL.",
    "This was a text-only prompt test. R01-R07 reference media were not attached.",
    "QC_VERDICTS.csv contains my exact reason, SHA-256 and provider job ID for every file.",
    "",
    "PASS files:",
]
summary += [f"- {record['filename']}: {record['reason']}" for record in records if record["verdict"] == "PASS"]
summary += ["", "No source image was modified or deleted."]
(DEST / "README.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")

assert len(list(DEST.glob("*.png"))) == 20
assert sum(record["verdict"] == "PASS" for record in records) == 8
assert sum(record["verdict"] == "CONDITIONAL" for record in records) == 8
assert sum(record["verdict"] == "FAIL" for record in records) == 4

print(DEST)
print("EXPORTED=20 PASS=8 CONDITIONAL=8 FAIL=4")
