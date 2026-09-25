from __future__ import annotations

import difflib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
alignment = json.loads((ROOT / "AUDIO" / "SATSOP_WORD_ALIGNMENT_V1.json").read_text(encoding="utf-8"))


def normalize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())


for chunk in alignment["chunks"]:
    expected = normalize((ROOT / "SCRIPT" / "TTS_CHUNKS_V1" / f"CHUNK_{chunk['index']:02}.txt").read_text(encoding="utf-8"))
    recognized = normalize(chunk["recognized_text"])
    matcher = difflib.SequenceMatcher(a=expected, b=recognized, autojunk=False)
    changes = [item for item in matcher.get_opcodes() if item[0] != "equal"]
    print(f"CHUNK {chunk['index']} differences={len(changes)}")
    for tag, i1, i2, j1, j2 in changes[:20]:
        print(f"  {tag}: EXP={' '.join(expected[i1:i2])!r} GOT={' '.join(recognized[j1:j2])!r}")

full = " ".join(chunk["recognized_text"] for chunk in alignment["chunks"]).lower()
print("KEY TERMS")
for term in [
    "satsop",
    "bonneville",
    "chehalis",
    "grays harbor",
    "take or pay",
    "seventy-four percent",
    "fourteen percent",
    "supply system",
    "project three",
    "project five",
    "project two",
]:
    print(f"  {term}: {term in full}")

print("LOW CONFIDENCE")
for word in sorted(alignment["words"], key=lambda item: item["probability"])[:30]:
    print(f"  {word['start']:8.3f} {word['probability']:.5f} {word['word']!r}")
