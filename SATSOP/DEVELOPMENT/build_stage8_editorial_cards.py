from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMELINE = ROOT / "SATSOP/REMOTION_V1/public/timeline.json"
OUT = ROOT / "SATSOP/REMOTION_V1/public/overlays.json"

# Deliberately limited to the story's main turns and quantitative anchors.
# This matches the editorial-card density of the earlier channel episodes.
CARDS = {
    "SAT-B002": ("PROJECT 5", "14% COMPLETE", "TERMINATED IN 1982"),
    "SAT-B003": ("PROJECT 3", "74% COMPLETE", "PRESERVED UNTIL 1994"),
    "SAT-B006": ("THE FIRST BREAK", "JANUARY 22, 1982", "PROJECTS 4 + 5 TERMINATED"),
    "SAT-B009": ("BONDS ALREADY SOLD", "$2.25 BILLION", "PROJECTS 4 + 5"),
    "SAT-B010": ("COMPLETION ESTIMATE", "$12 BILLION", "~$8.5B ABOVE THE ORIGINAL ESTIMATE"),
    "SAT-B015": ("THE BUILDOUT", "FIVE NUCLEAR PROJECTS", "ONE WOULD EVENTUALLY OPERATE"),
    "SAT-B016": ("ORGANIZATIONAL SCALE", "FEWER THAN 100 → 1,471", "EMPLOYEES, 1968–1979"),
    "SAT-B019": ("PROJECT 4 + 5 PARTICIPANTS", "88 BPA CUSTOMERS", "+ 1 PRIVATE UTILITY"),
    "SAT-B021": ("TAKE OR PAY", "PAY WHETHER COMPLETED", "OPERABLE OR OPERATING"),
    "SAT-B025": ("THE DEFAULT", "JULY 22, 1983", "PROJECT 4 + 5 BONDS"),
    "SAT-B026": ("TWO FINANCING PATHS", "PROJECT 5 ≠ PROJECT 3", "PARTICIPANT DEBT / BPA NET BILLING"),
    "SAT-B031": ("PROJECT 3 FINANCING", "70% / 30%", "PUBLIC NET BILLING / FOUR IOUs"),
    "SAT-B032": ("PLANNED OUTPUT", "1,240 MW EACH", "PRESSURIZED-WATER REACTORS"),
    "SAT-B038": ("PROJECT 3", "SUSPENDED ≠ TERMINATED", "THE COMPLETION OPTION REMAINED OPEN"),
    "SAT-B046": ("CAPITAL ALREADY INVESTED", "$2.6 BILLION", "1993 DOLLARS"),
    "SAT-B047": ("VISIBLE SCALE", "~500-FOOT COOLING TOWERS", "MAJOR BUILDINGS ALREADY EXISTED"),
    "SAT-B048": ("THE COMPLETION TRAP", "VISIBLE CONCRETE", "DOES NOT REVEAL THE COST TO FINISH"),
    "SAT-B054": ("THE DECISION RULE", "PAST SPEND / NEXT DECISION", "SUNK COST IS NOT FUTURE VALUE"),
    "SAT-B058": ("CAPACITY COMPARISON", "1,240 MW / 240 MW", "NUCLEAR / COMBINED-CYCLE REFERENCE"),
    "SAT-B060": ("CONSTRUCTION WINDOW", "FIVE YEARS / THREE YEARS", "PROJECT 3 / COMBINED CYCLE"),
    "SAT-B068": ("THE ALTERNATIVE'S VALUE", "FLEXIBILITY", "SMALLER STEPS, SHORTER COMMITMENT"),
    "SAT-B069": ("BASE COMPLETION ESTIMATE", "$1.55 BILLION", "PROJECT 3 — 1993 DOLLARS"),
    "SAT-B074": ("SYSTEM POSITION", "1,240 MW", "+600 AVERAGE-MW SURPLUS FORECAST"),
    "SAT-B079": ("THE 1994 CONTRADICTION", "74% BUILT", "POWER NO LONGER NEEDED"),
    "SAT-B083": ("THE STRATEGIC CHOICE", "REPOWER / NEW BUILD", "EXISTING ASSETS VS FLEXIBILITY"),
    "SAT-B086": ("FINAL DECISION", "TERMINATED", "PAST INVESTMENT DID NOT CONTROL THE FUTURE"),
    "SAT-B088": ("FOUR ENDINGS", "1982 / 1983 / 1983 / 1994", "P5 / DEFAULT / P3 SUSPENSION / P3 TERMINATION"),
    "SAT-B090": ("AFTER TERMINATION", "FOUR DIFFERENT CLOCKS", "PERMIT / PROPERTY / REMEDIATION / DEBT"),
    "SAT-B093": ("THE DEBT CLOCK", "DECADES LATER", "BUDGETING CONTINUED AFTER TERMINATION"),
    "SAT-B098": ("THE RECOVERY", "INFRASTRUCTURE", "NOT THE NUCLEAR INVESTMENT"),
    "SAT-B102": ("TODAY'S SITE", "300,000 SQ FT", "SATSOP BUSINESS PARK"),
    "SAT-B103": ("ADAPTIVE REUSE", "CONFINED-SPACE TRAINING", "INDUSTRIAL AND RESCUE OPERATIONS"),
    "SAT-B106": ("WHAT SATSOP BECAME", "A WORKING INDUSTRIAL SITE", "WITHOUT GENERATING NUCLEAR POWER"),
}


def main() -> None:
    beats = {b["beat"]: b for b in json.loads(TIMELINE.read_text(encoding="utf-8"))["beats"]}
    cards = []
    for beat_id, (kicker, title, subline) in CARDS.items():
        beat = beats[beat_id]
        start = beat["start"] + 0.45
        end = min(beat["end"] - 0.35, start + 4.6)
        cards.append({
            "beat": beat_id,
            "s": round(start, 3),
            "e": round(end, 3),
            "kicker": kicker,
            "title": title,
            "subline": subline,
        })
    OUT.write_text(json.dumps({"cards": cards}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"cards": len(cards), "first": cards[0], "last": cards[-1]}, indent=2))


if __name__ == "__main__":
    main()
