from __future__ import annotations

import json
import re
import subprocess
from difflib import SequenceMatcher
from pathlib import Path

from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "AUDIO" / "TTS_CHUNKS_V1"
TEXT = ROOT / "SCRIPT" / "TTS_CHUNKS_V1"
OUT = ROOT / "AUDIO" / "SATSOP_WORD_ALIGNMENT_V1.json"


def duration(path: Path) -> float:
    ffprobe = (
        ROOT.parents[1]
        / "skills"
        / "remotion"
        / "node_modules"
        / "@remotion"
        / "compositor-win32-x64-msvc"
        / "ffprobe.exe"
    )
    value = subprocess.check_output(
        [str(ffprobe), "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(path)],
        text=True,
    )
    return float(value.strip())


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())


model = WhisperModel("tiny", device="cpu", compute_type="int8", local_files_only=True)
report: dict = {
    "method": "local faster-whisper tiny; word_timestamps=true",
    "language": "en",
    "chunks": [],
    "words": [],
}
offset = 0.0
all_expected: list[str] = []
all_recognized: list[str] = []

for index in range(1, 5):
    audio_path = AUDIO / f"CHUNK_{index:02}.mp3"
    expected_text = (TEXT / f"CHUNK_{index:02}.txt").read_text(encoding="utf-8")
    segments, info = model.transcribe(
        str(audio_path),
        language="en",
        beam_size=5,
        word_timestamps=True,
        vad_filter=False,
        condition_on_previous_text=True,
    )
    chunk_segments = []
    recognized_parts = []
    chunk_words = []
    for segment in segments:
        recognized_parts.append(segment.text.strip())
        words = []
        for word in segment.words or []:
            item = {
                "word": word.word,
                "start": round(offset + word.start, 3),
                "end": round(offset + word.end, 3),
                "probability": round(word.probability, 5),
            }
            words.append(item)
            chunk_words.append(item)
            report["words"].append(item)
        chunk_segments.append(
            {
                "start": round(offset + segment.start, 3),
                "end": round(offset + segment.end, 3),
                "text": segment.text.strip(),
                "words": words,
            }
        )
    recognized_text = " ".join(part for part in recognized_parts if part)
    expected_tokens = tokens(expected_text)
    recognized_tokens = tokens(recognized_text)
    matcher = SequenceMatcher(a=expected_tokens, b=recognized_tokens, autojunk=False)
    matching = sum(block.size for block in matcher.get_matching_blocks())
    similarity = matching / max(1, len(expected_tokens))
    chunk_duration = duration(audio_path)
    report["chunks"].append(
        {
            "index": index,
            "offset_seconds": round(offset, 6),
            "duration_seconds": round(chunk_duration, 6),
            "expected_word_count": len(expected_tokens),
            "recognized_word_count": len(recognized_tokens),
            "sequence_match_ratio": round(similarity, 6),
            "recognized_text": recognized_text,
            "segments": chunk_segments,
        }
    )
    all_expected.extend(expected_tokens)
    all_recognized.extend(recognized_tokens)
    offset += chunk_duration

matcher = SequenceMatcher(a=all_expected, b=all_recognized, autojunk=False)
matching = sum(block.size for block in matcher.get_matching_blocks())
report["total_duration_seconds"] = round(offset, 6)
report["expected_word_count"] = len(all_expected)
report["recognized_word_count"] = len(all_recognized)
report["sequence_match_ratio"] = round(matching / max(1, len(all_expected)), 6)
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in report.items() if k not in {"chunks", "words"}}, indent=2))
for chunk in report["chunks"]:
    print(
        f"chunk {chunk['index']}: expected={chunk['expected_word_count']} "
        f"recognized={chunk['recognized_word_count']} ratio={chunk['sequence_match_ratio']}"
    )
print(f"output={OUT}")
