from __future__ import annotations

import csv
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAT = ROOT / "SATSOP"
OUT = SAT / "REMOTION_V1"
PUBLIC = OUT / "public"
ASSETS = PUBLIC / "assets"
FPS = 30


def seconds(tc: str) -> float:
    h, m, s = tc.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def link(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def prompt_map() -> tuple[dict[str, str], dict[str, str]]:
    data = json.loads((SAT / "STAGE_6/V3/SATSOP_GENERATION_PROMPT_PACK_V3.json").read_text(encoding="utf-8"))
    items = data["items"]
    prompt_to_beat = {x["prompt_id"]: x["beat_id"] for x in items}
    beat_to_prompt = {v: k for k, v in prompt_to_beat.items()}
    return prompt_to_beat, beat_to_prompt


def choose_generated(beat: str, prompt: str) -> Path:
    fix_ids = {"SAT-GEN022", "SAT-GEN028", "SAT-GEN034", "SAT-GEN038", "SAT-GEN043", "SAT-GEN046", "SAT-GEN050", "SAT-GEN053", "SAT-GEN064"}
    roots = [
        SAT / "STAGE_6/FIX9_V6",
        SAT / "STAGE_6/FINAL28_V5",
        SAT / "STAGE_6/REMAINING_V4",
        SAT / "STAGE_6/TEST20_V3",
        SAT / "STAGE_6/TEST20_V2",
        SAT / "STAGE_6/TEST20",
    ]
    if prompt not in fix_ids:
        roots = roots[1:]
    for root in roots:
        candidates = [p for p in root.glob("*.png") if (prompt in p.stem or beat in p.stem) and "CONTACT" not in p.stem.upper()]
        if root.name == "FIX9_V6" and prompt == "SAT-GEN034":
            candidates = [p for p in candidates if "BLURRED" in p.stem]
        if candidates:
            return sorted(candidates, key=lambda p: ("FIX" not in p.stem, len(p.name)))[0]
    raise FileNotFoundError(f"No generated image for {beat} / {prompt}")


def captions() -> list[dict]:
    alignment = json.loads((SAT / "AUDIO/SATSOP_WORD_ALIGNMENT_V1.json").read_text(encoding="utf-8"))
    words = []
    for chunk in alignment["chunks"]:
        off = float(chunk["offset_seconds"])
        for segment in chunk["segments"]:
            for word in segment.get("words", []):
                text = word["word"].strip()
                if text:
                    words.append({"w": text, "s": round(off + float(word["start"]), 3), "e": round(off + float(word["end"]), 3)})
    cues, buf = [], []
    for w in words:
        if buf and (len(buf) >= 7 or w["s"] - buf[-1]["e"] > 0.42 or w["e"] - buf[0]["s"] > 3.2):
            cues.append({"s": buf[0]["s"], "e": buf[-1]["e"], "words": buf})
            buf = []
        buf.append(w)
        if re.search(r"[.!?]$", w["w"]) and len(buf) >= 3:
            cues.append({"s": buf[0]["s"], "e": buf[-1]["e"], "words": buf})
            buf = []
    if buf:
        cues.append({"s": buf[0]["s"], "e": buf[-1]["e"], "words": buf})
    return cues


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    p2b, b2p = prompt_map()
    beats = list(csv.DictReader((SAT / "STAGE_5/SATSOP_STAGE_5_VISUAL_BEAT_MAP_V1.csv").open(encoding="utf-8-sig", newline="")))
    assignment_data = json.loads((SAT / "STAGE_7/STAGE7_41_BEAT_ASSIGNMENT.json").read_text(encoding="utf-8"))
    assignments = {x["beat_id"]: x for x in assignment_data["assignments"]}
    timeline = []
    missing = []
    for i, row in enumerate(beats):
        beat = row["beat_id"]
        start, end = seconds(row["start"]), seconds(row["end"])
        klass = row["asset_class"]
        item = {
            "beat": beat, "start": start, "end": end,
            "a": round(start * FPS), "b": round(end * FPS),
            "chapter": row["chapter"], "narration": row["narration"],
            "assetClass": klass, "direction": -1 if i % 2 else 1,
        }
        try:
            if beat in assignments:
                a = assignments[beat]
                item.update({"sourceTitle": a["source_title"], "license": a["license"]})
                if a["asset_class"] == "DOCUMENT":
                    item["kind"] = "document"
                    item["documentName"] = Path(a["asset_path"]).stem.replace("DOC-", "").replace("-", " ")
                else:
                    src = SAT / "STAGE_7" / a["asset_path"]
                    ext = src.suffix.lower()
                    dst = ASSETS / f"{beat}{ext}"
                    link(src, dst)
                    item.update({"kind": "gfx" if ext == ".svg" else "current", "file": f"assets/{dst.name}"})
            else:
                prompt = b2p[beat]
                src = choose_generated(beat, prompt)
                dst = ASSETS / f"{beat}{src.suffix.lower()}"
                link(src, dst)
                item.update({"kind": "generated", "file": f"assets/{dst.name}", "promptId": prompt})
        except Exception as exc:
            missing.append(f"{beat}: {exc}")
        timeline.append(item)
    if missing:
        raise RuntimeError("\n".join(missing))

    link(SAT / "AUDIO/SATSOP_VO_MASTER_V1.wav", PUBLIC / "SATSOP_VO_MASTER_V1.wav")
    (PUBLIC / "timeline.json").write_text(json.dumps({"fps": FPS, "duration": seconds(beats[-1]["end"]), "beats": timeline}, indent=2), encoding="utf-8")
    (PUBLIC / "captions.json").write_text(json.dumps(captions(), indent=2), encoding="utf-8")
    report = {
        "beats": len(timeline),
        "counts": {k: sum(x["kind"] == k for x in timeline) for k in ["generated", "current", "gfx", "document"]},
        "captions": len(captions()), "duration_seconds": seconds(beats[-1]["end"]), "missing": missing,
    }
    (OUT / "BUILD_PREFLIGHT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
