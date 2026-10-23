#!/usr/bin/env python3
"""Build the locked-input, no-generation Voicebox package for Pluto Stage 04 V2."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = SCRIPT_DIR.parent
FULL_SCRIPT = SCRIPT_DIR / "STAGE04_PROJECT_PLUTO_FULL_NARRATION_V2_EN.md"
VOICE_TEXT = SCRIPT_DIR / "STAGE04_PROJECT_PLUTO_VOICE_TEXT_V2_EN.txt"
CLAIMS = SCRIPT_DIR / "STAGE04_CLAIM_BY_CLAIM_EVIDENCE_LEDGER_V1.csv"
QC = SCRIPT_DIR / "STAGE04_FINAL_FACT_EDITORIAL_LEGAL_QC_2026-10-22.md"
BEATS = SCRIPT_DIR / "STAGE04_PROJECT_PLUTO_EVIDENCE_ALIGNED_BEATS_V2.csv"
OUT = PROJECT_DIR / "AUDIO" / "VOICEBOX_ARTHUR_V2_PREP"
JOBS_DIR = OUT / "JOBS"

PROFILE_ID = "49119911-6b96-4db0-87fe-8a976ccc6b91"
PROFILE_NAME = "HIA Arthur Multi-Source"
MODEL = "Qwen3-TTS 1.7B"
SEED = 20261022
PAUSE_MS = 600
INSTRUCT = (
    "Calm, factual American industrial-history documentary narration. "
    "Measured medium cadence, restrained emphasis, clear technical terms, "
    "no trailer voice or melodrama."
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def parse_chapters(markdown: str) -> list[dict]:
    pattern = re.compile(
        r"^## (CH\d{2})\s+[^\n]*\n(.*?)(?=^---\s*$|^## CH\d{2}|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    chapters = []
    for match in pattern.finditer(markdown):
        chapter = match.group(1)
        body = re.sub(r"<!--.*?-->\s*", "", match.group(2), flags=re.DOTALL).strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        title_match = re.search(rf"^## {chapter}\s+—\s+(.+)$", markdown, re.MULTILINE)
        chapters.append(
            {
                "chapter": chapter,
                "title": title_match.group(1).strip() if title_match else chapter,
                "text": body,
            }
        )
    return chapters


def count_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def main() -> None:
    required = [FULL_SCRIPT, VOICE_TEXT, CLAIMS, QC, BEATS]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing Stage 04 inputs: " + ", ".join(missing))

    full = read_text(FULL_SCRIPT)
    voice = read_text(VOICE_TEXT).strip()
    chapters = parse_chapters(full)
    if len(chapters) != 8:
        raise SystemExit(f"Expected 8 chapters, found {len(chapters)}")
    reconstructed = "\n\n".join(item["text"] for item in chapters)
    if reconstructed != voice:
        raise SystemExit("Chapter bodies do not reconstruct the V2 voice text exactly")
    if len(voice.split()) != 2955:
        raise SystemExit(f"Expected 2955 whitespace words, found {len(voice.split())}")
    if count_rows(CLAIMS) != 54:
        raise SystemExit("Claim ledger does not contain exactly 54 rows")
    if count_rows(BEATS) != 30:
        raise SystemExit("Evidence-aligned beat map does not contain exactly 30 rows")

    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    request_jobs = []
    for index, chapter in enumerate(chapters, 1):
        text = chapter["text"]
        filename = f"PROJECT_PLUTO_V2_JOB_{index:02d}_{chapter['chapter']}.txt"
        path = JOBS_DIR / filename
        path.write_text(text + "\n", encoding="utf-8", newline="\n")
        words = len(text.split())
        characters = len(text)
        manifest_rows.append(
            {
                "job_number": index,
                "chapter": chapter["chapter"],
                "chapter_title": chapter["title"],
                "text_file": f"JOBS/{filename}",
                "words": words,
                "characters": characters,
                "utf8_bytes_without_terminal_newline": len(text.encode("utf-8")),
                "estimated_seconds_at_135_wpm": f"{words / 135 * 60:.3f}",
                "estimated_seconds_at_145_wpm": f"{words / 145 * 60:.3f}",
                "estimated_seconds_at_155_wpm": f"{words / 155 * 60:.3f}",
                "text_sha256": sha_bytes(text.encode("utf-8")),
                "file_sha256": file_sha(path),
                "generation_status": "HOLD_OWNER_SCRIPT_LOCK",
                "generation_id": "",
                "expected_wav": f"GENERATED_WAV/PROJECT_PLUTO_V2_JOB_{index:02d}_{chapter['chapter']}.wav",
            }
        )
        request_jobs.append(
            {
                "job_number": index,
                "chapter": chapter["chapter"],
                "text_file": f"JOBS/{filename}",
                "payload_template": {
                    "profile_id": PROFILE_ID,
                    "language": "en",
                    "model_size": "1.7B",
                    "engine": "qwen",
                    "seed": SEED,
                    "instruct": INSTRUCT,
                    "personality": False,
                    "max_chunk_chars": 800,
                    "crossfade_ms": 50,
                    "normalize": True,
                },
                "submit": False,
                "status": "HOLD_OWNER_SCRIPT_LOCK",
            }
        )

    manifest_path = OUT / "JOB_MANIFEST.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest_rows[0]))
        writer.writeheader()
        writer.writerows(manifest_rows)

    total_chars_jobs = sum(int(row["characters"]) for row in manifest_rows)
    total_words = sum(int(row["words"]) for row in manifest_rows)
    qc_data = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "READY_FOR_OWNER_SCRIPT_LOCK__GENERATION_NOT_STARTED",
        "authoritative_script": str(FULL_SCRIPT.relative_to(PROJECT_DIR)).replace("\\", "/"),
        "authoritative_voice_text": str(VOICE_TEXT.relative_to(PROJECT_DIR)).replace("\\", "/"),
        "v1_status": "SUPERSEDED_DO_NOT_USE",
        "source_bank_r1_status": "REJECT_DO_NOT_USE",
        "chapter_count": len(chapters),
        "voice_word_count_whitespace": total_words,
        "voice_text_characters_including_7_double_newline_chapter_separators": len(voice),
        "billable_job_characters_excluding_inter_job_separators": total_chars_jobs,
        "sentence_loss_check": "PASS_EXACT_RECONSTRUCTION",
        "claim_rows": count_rows(CLAIMS),
        "evidence_aligned_beats": count_rows(BEATS),
        "job_count": len(manifest_rows),
        "chapter_pause_ms": PAUSE_MS,
        "estimated_narration_seconds": {
            "at_135_wpm": round(total_words / 135 * 60, 3),
            "at_145_wpm": round(total_words / 145 * 60, 3),
            "at_155_wpm": round(total_words / 155 * 60, 3),
            "assembly_pause_total": round((len(manifest_rows) - 1) * PAUSE_MS / 1000, 3),
        },
        "cost": {
            "local_voicebox_external_api_credits_usd": 0.0,
            "paid_provider_cost": "NOT_CALCULATED_NO_PROVIDER_OR_RATE_AUTHORIZED",
            "paid_provider_formula": f"{total_chars_jobs} / 1000 * provider_rate_per_1000_characters",
        },
        "profile": {
            "name": PROFILE_NAME,
            "id": PROFILE_ID,
            "source_scope": "Youtube-2 Big Muskie and Lake Peigneur verified narration only",
            "youtube_3_audio_used": False,
            "reference_sample_count": 4,
        },
        "input_sha256": {path.name: file_sha(path) for path in required},
    }
    (OUT / "PREGENERATION_QC.json").write_text(
        json.dumps(qc_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    (OUT / "VOICEBOX_REQUESTS_HOLD.json").write_text(
        json.dumps(
            {
                "status": "DO_NOT_SUBMIT_UNTIL_OWNER_SCRIPT_LOCK",
                "job_count": len(request_jobs),
                "profile_id": PROFILE_ID,
                "jobs": request_jobs,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    concat = []
    for index, row in enumerate(manifest_rows):
        concat.append(row["expected_wav"])
        if index != len(manifest_rows) - 1:
            concat.append(f"SILENCE_{PAUSE_MS}MS.wav")
    (OUT / "MASTER_CONCAT_ORDER.txt").write_text("\n".join(concat) + "\n", encoding="utf-8", newline="\n")

    tracked = [
        manifest_path,
        OUT / "PREGENERATION_QC.json",
        OUT / "VOICEBOX_REQUESTS_HOLD.json",
        OUT / "MASTER_CONCAT_ORDER.txt",
        OUT / "README.md",
        OUT / "MASTER_ASSEMBLY_PLAN.md",
        OUT / "merge_voicebox_jobs.ps1",
        *sorted(JOBS_DIR.glob("*.txt")),
    ]
    (OUT / "SHA256SUMS.txt").write_text(
        "".join(f"{file_sha(path)}  {path.relative_to(OUT).as_posix()}\n" for path in tracked),
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(qc_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
