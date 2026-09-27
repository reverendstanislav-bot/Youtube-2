from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMELINE = ROOT / "SATSOP/REMOTION_V1/public/timeline.json"
OUT = ROOT / "SATSOP/REMOTION_V1/public/motion.json"

# Twelve-beat directing phrase. Holds interrupt continuous movement; pushes,
# pulls and pans never repeat on adjacent beats.
PHRASE = [
    "hold",
    "push_left",
    "pan_right",
    "pull",
    "push",
    "hold_then_push",
    "pan_left",
    "tilt_up",
    "push_right",
    "pull",
    "hold",
    "tilt_down",
]

# Reflective pivots and chapter openings receive a short true crossfade.
# Every other boundary remains a clean documentary cut.
DISSOLVE_IN = {
    "SAT-B002", "SAT-B006", "SAT-B012", "SAT-B018", "SAT-B026",
    "SAT-B033", "SAT-B038", "SAT-B046", "SAT-B050", "SAT-B055",
    "SAT-B063", "SAT-B069", "SAT-B075", "SAT-B080", "SAT-B087",
    "SAT-B090", "SAT-B097", "SAT-B101", "SAT-B106",
}

OVERRIDES = {
    # Portrait tower source: movement would expose the large white sky field.
    "SAT-B056": "hold",
    # Strong authentic present-day stills work best as observational holds.
    "SAT-B092": "hold",
    "SAT-B109": "pull",
}


def main() -> None:
    beats = json.loads(TIMELINE.read_text(encoding="utf-8"))["beats"]
    items = []
    previous = None
    for i, beat in enumerate(beats):
        style = OVERRIDES.get(beat["beat"], PHRASE[i % len(PHRASE)])
        if style == previous:
            style = "hold" if style != "hold" else "push"
        previous = style
        items.append({
            "beat": beat["beat"],
            "style": style,
            "transition_in": "dissolve" if beat["beat"] in DISSOLVE_IN else "cut",
            "dissolve_frames": 8 if beat["beat"] in DISSOLVE_IN else 0,
        })
    counts = Counter(item["style"] for item in items)
    payload = {
        "version": 2,
        "principle": "varied restrained documentary motion; hard cuts dominate",
        "items": items,
        "counts": dict(sorted(counts.items())),
        "transitions": {
            "cut": sum(x["transition_in"] == "cut" for x in items),
            "dissolve": sum(x["transition_in"] == "dissolve" for x in items),
        },
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"beats": len(items), "motion": payload["counts"], "transitions": payload["transitions"]}, indent=2))


if __name__ == "__main__":
    main()
