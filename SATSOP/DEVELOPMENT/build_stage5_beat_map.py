from __future__ import annotations

import csv
import difflib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALIGNMENT = json.loads((ROOT / "AUDIO" / "SATSOP_WORD_ALIGNMENT_V1.json").read_text(encoding="utf-8"))
OUT = ROOT / "STAGE_5"
OUT.mkdir(exist_ok=True)


def norm_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())


def tc(seconds: float) -> str:
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"


def chapter(mid: float) -> str:
    if mid < 105:
        return "ACT I — two towers, two failures"
    if mid < 335:
        return "ACT II — the five-project system"
    if mid < 575:
        return "ACT III — financing split and collapse"
    if mid < 755:
        return "ACT IV — preservation and the completion question"
    if mid < 1025:
        return "ACT V — Bonneville's risk decision"
    return "ACT VI — transfer, reuse, and meaning"


def classify(text: str, mid: float) -> tuple[str, str, str, str, str]:
    t = text.lower()
    if "hydroelectric system whose generation changed" in t:
        asset = "MAP_GFX"
        req = "Regional hydro-system/load-shaping map showing variable water-driven generation and modular combined-cycle additions without inventing plant locations."
        prov = "No historical label; cite system/load sources"
        motion = "Water-generation band changes while modular supply blocks enter; restrained and explanatory."
        risk = "Do not imply exact dispatch quantities beyond the cited comparison."
    elif "variable and avoidable" in t:
        asset = "GFX"
        req = "Fixed-versus-variable cost graphic showing why non-producing combined-cycle capacity avoided more cost than Project Three."
        prov = "No historical label; cite Bonneville comparison"
        motion = "Two cost stacks separate into avoidable and continuing portions."
        risk = "Conceptual proportions only unless exact values are sourced."
    elif "held capability shares" in t:
        asset = "DOCUMENT"
        req = "Verified capability-share/net-billing agreement excerpt showing the assignment relationship among public utilities and Bonneville."
        prov = "DOCUMENT"
        motion = "Highlight the parties and assignment clause; keep the rest of the page quiet."
        risk = "Use the correct Project Three agreement; do not substitute Project Four/Five participant contracts."
    elif "major siting permits were in place" in t:
        asset = "DOCUMENT"
        req = "Verified siting/permit record paired with an authenticated construction-state image; show existing advantages without implying readiness to operate."
        prov = "DOCUMENT for the record; HISTORICAL SOURCE only for authenticated period image"
        motion = "Hard cut from permit excerpt to one period structural detail."
        risk = "Existing permits and structures must not be framed as proof the plant was operationally complete."
    elif "listed uncertainty in completion cost" in t:
        asset = "GFX"
        req = "Source-grounded risk field grouping completion, upgrades, operations, maintenance, waste, decommissioning, regulation, and opposition."
        prov = "No historical label; cite Bonneville source"
        motion = "Risks enter in three semantic groups, then resolve to one cumulative field."
        risk = "Do not assign invented weights or probabilities."
    elif "repowering project three" in t:
        asset = "TECH_GFX"
        req = "Conceptual site/system comparison between repowering the existing site and a new combined-cycle plant, limited to options actually examined."
        prov = "CONCEPT"
        motion = "Simple side-by-side system blocks; no photoreal unbuilt plant."
        risk = "Do not imply the repowering concept was selected or engineered for construction."
    elif "analysis asked four practical questions" in t:
        asset = "GFX"
        req = "Four-question decision framework: competitiveness, need, alternatives, and risk, revealed one at a time from the sourced Bonneville analysis."
        prov = "No historical label; cite the Bonneville source"
        motion = "Four restrained branches enter sequentially, then hold as a complete decision frame."
        risk = "Keep wording faithful to the source and narration."
    elif "human-scale center" in t or "household or a small business" in t:
        asset = "CURRENT_BROLL"
        req = "Cleared contemporary regional utility/customer imagery that connects wholesale decisions to ordinary ratepayers without implying a specific person's testimony."
        prov = "No historical label; retain stock/creator attribution"
        motion = "Two purposeful human-scale cuts; natural movement, no staged reaction close-up."
        risk = "Treat as illustrative present-day B-roll, not evidence of a named historical customer."
    elif "pressure to control its rates" in t:
        asset = "DOCUMENT"
        req = "Bonneville source excerpt documenting competitiveness/rate pressure, paired with a restrained regional power-context background."
        prov = "DOCUMENT while verified page is visible"
        motion = "Static source crop with one highlighted clause, then hard cut away."
        risk = "Do not generalize beyond the cited customer and rate context."
    elif "push bonneville's costs upward" in t:
        asset = "GFX"
        req = "Minimal cost-pressure graphic: completion commitment rising while customer alternatives open, with no invented price series."
        prov = "No historical label; cite source logic in manifest"
        motion = "Opposing directional lines timed to the two clauses; no dashboard UI."
        risk = "Conceptual relationship only; do not fabricate quantitative axes."
    elif any(k in t for k in ["1970", "1971", "1972", "1973", "1974", "1975", "1976", "1977", "1978", "1979", "1980", "1981", "1982", "1983", "1993", "1994", "1995", "1999", "2000"]):
        asset = "DOCUMENT"
        req = "Authenticated government/owner record page or dated period source tied to the stated event; highlight only the cited date, decision, or figure."
        prov = "DOCUMENT"
        motion = "Hard cut into a restrained page crop; one highlight/reveal, no generic document carousel."
        risk = "Verify page, agency, date, and embedded third-party rights before edit."
    elif any(k in t for k in ["net billing", "take or pay", "capability shares", "fixed costs", "capital at risk", "deficit", "billion", "million dollars", "bonds", "wholesale power"]):
        asset = "GFX"
        req = "Source-grounded finance-flow or comparison graphic using the exact parties, percentages, and dollar basis stated in narration."
        prov = "No historical label; cite source data in asset manifest"
        motion = "Remotion line/shape reveal keyed to spoken clauses; one comparison at a time."
        risk = "Do not imply nominal-dollar equivalence or merge Project Three and Project Five financing."
    elif any(k in t for k in ["northwest", "hanford", "satsop", "site", "regional", "transmission", "map", "side by side"]):
        asset = "MAP_GFX"
        req = "Original HIA map/site-plan GFX grounded in official geography and unit layout; distinguish Project Three, Project Five, Hanford, and shared infrastructure."
        prov = "No historical label; cite map/data sources"
        motion = "Clean map trace or plan reveal; static labels, restrained camera, no fake satellite UI."
        risk = "Unit placement and common-system geometry must be authenticated before final lock."
    elif any(k in t for k in ["reactor", "turbine", "cooling system", "steam", "pressurized-water", "system 80", "megawatt output"]):
        asset = "TECH_GFX"
        req = "Source-grounded simplified plant/system diagram showing only the components named in narration."
        prov = "DOCUMENT if a verified drawing is visible; otherwise no historical label"
        motion = "Component-by-component reveal; no decorative gauges or invented engineering detail."
        risk = "Do not depict either Satsop unit as fueled, operating, or completed."
    elif mid < 105 or mid >= 1025 or any(k in t for k in ["today", "business park", "roads", "warehouse", "training", "redevelopment", "current"]):
        asset = "CURRENT_FOOTAGE"
        req = "Cleared present-day Satsop exterior/interior footage or stills showing scale, empty infrastructure, and active reuse without implying total abandonment."
        prov = "No HISTORICAL SOURCE label; retain creator/license attribution"
        motion = "Hard cuts among distinct viewpoints; stable footage or restrained static reframe, never repeated oscillating zooms."
        risk = "Port material requires permission; restricted structures and active tenants must be represented accurately."
    elif any(k in t for k in ["construction", "workers", "built", "concrete", "tower", "suspended", "terminated"]):
        asset = "ARCHIVE_PHOTO"
        req = "Authenticated period construction photograph/film tied to the correct Satsop unit and date; use documents/GFX if rights remain unclear."
        prov = "HISTORICAL SOURCE only while verified archive is actually visible"
        motion = "Hard cut; static or ≤3% restrained crop; alternate scale, labor, structure, and site views."
        risk = "Do not misidentify Unit Three/Five or reuse one image as fake visual progression."
    else:
        asset = "DOCUMENT_GFX"
        req = "Relevant official-source excerpt, restrained typographic pull-quote, or factual HIA diagram that makes the clause visually specific."
        prov = "DOCUMENT only for the verified source page; otherwise no historical label"
        motion = "One purposeful reveal or hard cut; avoid generic cards and wallpaper text."
        risk = "Every visible number and label must remain traceable to the claim-source map."

    gfx = "None beyond captions unless a number/date named in narration materially improves comprehension."
    if re.search(r"\b(percent|billion|million|megawatt|years?|project (three|five)|19\d\d|20\d\d)\b", t):
        gfx = "Use one restrained factual overlay for the named number/date; remove it before the next unrelated claim."
    return asset, req, prov, motion, risk + " Caption-safe lower 15% required.", gfx


units: list[dict] = []
for chunk in ALIGNMENT["chunks"]:
    idx = chunk["index"]
    source = (ROOT / "SCRIPT" / "TTS_CHUNKS_V1" / f"CHUNK_{idx:02}.txt").read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in source.split("\n\n") if p.strip()]
    narration_units = [
        sentence.strip()
        for paragraph in paragraphs
        for sentence in re.split(r"(?<=[.!?])\s+", paragraph)
        if sentence.strip()
    ]
    expected = norm_tokens(source)
    recognized_words = [w for seg in chunk["segments"] for w in seg["words"]]
    recognized = norm_tokens(" ".join(w["word"] for w in recognized_words))
    matcher = difflib.SequenceMatcher(a=expected, b=recognized, autojunk=False)
    anchors: dict[int, int] = {}
    for block in matcher.get_matching_blocks():
        for n in range(block.size):
            anchors[block.a + n] = block.b + n

    def mapped(pos: int) -> int:
        if not recognized_words:
            return 0
        if pos in anchors:
            return min(anchors[pos], len(recognized_words) - 1)
        left = [k for k in anchors if k < pos]
        right = [k for k in anchors if k > pos]
        if left and right:
            lo, hi = max(left), min(right)
            frac = (pos - lo) / max(1, hi - lo)
            guess = round(anchors[lo] + frac * (anchors[hi] - anchors[lo]))
        elif left:
            lo = max(left); guess = anchors[lo] + (pos - lo)
        elif right:
            hi = min(right); guess = anchors[hi] - (hi - pos)
        else:
            guess = round(pos * len(recognized_words) / max(1, len(expected)))
        return max(0, min(guess, len(recognized_words) - 1))

    cursor = 0
    for paragraph in narration_units:
        p_tokens = norm_tokens(paragraph)
        start_token = cursor
        end_token = cursor + len(p_tokens) - 1
        cursor += len(p_tokens)
        start_word = mapped(start_token)
        end_word = mapped(end_token)
        start = recognized_words[start_word]["start"]
        end = recognized_words[end_word]["end"]
        units.append({"text": paragraph, "start": start, "end": end})

# Group short adjacent paragraphs without crossing long semantic units.
beats: list[dict] = []
current: list[dict] = []
for unit in units:
    if not current:
        current = [unit]
        continue
    proposed = unit["end"] - current[0]["start"]
    current_duration = current[-1]["end"] - current[0]["start"]
    if current_duration < 7.0 and proposed <= 17.0:
        current.append(unit)
    else:
        beats.append({"start": current[0]["start"], "end": current[-1]["end"], "text": " ".join(x["text"] for x in current)})
        current = [unit]
if current:
    beats.append({"start": current[0]["start"], "end": current[-1]["end"], "text": " ".join(x["text"] for x in current)})

# Close timeline gaps at phrase midpoints while preserving first/last exact bounds.
for i in range(len(beats) - 1):
    boundary = round((beats[i]["end"] + beats[i + 1]["start"]) / 2, 3)
    beats[i]["end"] = boundary
    beats[i + 1]["start"] = boundary
beats[0]["start"] = 0.0
beats[-1]["end"] = 1163.92

rows = []
for i, beat in enumerate(beats, 1):
    mid = (beat["start"] + beat["end"]) / 2
    asset, req, prov, motion, risk, gfx = classify(beat["text"], mid)
    lower = beat["text"].lower()
    evidence_markers = [
        "gao",
        "bonneville described",
        "1994 exhibits",
        "executive board",
        "board of directors",
        "administrator made the final determination",
        "construction permit",
        "fiscal year 2000",
        "record of decision",
        "the analysis asked",
    ]
    evidence_document = asset == "DOCUMENT" and any(marker in lower for marker in evidence_markers)
    if asset in {"ARCHIVE_PHOTO", "DOCUMENT_GFX"} or (asset == "DOCUMENT" and not evidence_document):
        asset = "AI_RECONSTRUCTION"
        req = (
            "Purpose-built, historically grounded non-photoreal reconstruction of this exact narration beat. "
            "Use verified Satsop/WPPSS references for structures, period, weather, clothing, equipment, and geography; "
            "do not invent readable signs, documents, reactor operation, fuel, steam, smoke, or completed systems."
        )
        prov = "AI RECONSTRUCTION for the complete on-screen duration"
        motion = "Use a distinct composition and restrained depth/motion treatment; hard cut by default; no repeated plate or oscillating zoom."
        risk = "Reference package must substantiate every historical/technical detail. Caption-safe lower 15% required."
    elif asset == "MAP_GFX" and not any(
        marker in lower
        for marker in ["pacific northwest", "regional", "hanford", "hydroelectric system", "transmission", "geography"]
    ):
        asset = "AI_RECONSTRUCTION_MAP"
        req = (
            "Generated, historically grounded Satsop/site base composition paired with a precise HIA map or site-plan overlay. "
            "The generated layer supplies scale and atmosphere; the vector overlay carries every factual location and unit relationship."
        )
        prov = "AI RECONSTRUCTION while generated base is visible; map overlay cites authenticated plan/geography"
        motion = "Restrained spatial reveal from generated site context into exact vector geometry; no fake satellite interface."
        risk = "Generated geography is illustrative; factual placement comes only from the authenticated overlay. Caption-safe lower 15% required."
    elif asset == "TECH_GFX":
        asset = "AI_RECONSTRUCTION_GFX"
        req = (
            "Historically grounded generated industrial base frame for the named Satsop system, combined with an exact HIA vector overlay "
            "for the explanatory relationships. Generated base must not imply an operating or completed reactor."
        )
        prov = "AI RECONSTRUCTION while generated base is visible; overlay is explanatory GFX"
        motion = "Subtle generated depth only; explanatory vector reveal follows narration and remains technically traceable."
        risk = "No invented piping labels, gauges, fuel, steam plume, or completed-system claim. Caption-safe lower 15% required."
    rows.append({
        "beat_id": f"SAT-B{i:03}",
        "start": tc(beat["start"]),
        "end": tc(beat["end"]),
        "duration_seconds": round(beat["end"] - beat["start"], 3),
        "chapter": chapter(mid),
        "narration": beat["text"],
        "asset_class": asset,
        "specific_asset_requirement": req,
        "provenance": prov,
        "motion_editing": motion,
        "gfx": gfx,
        "rights_qc": risk,
        "status": "PLANNED — ASSET NOT YET CLEARED",
    })

csv_path = OUT / "SATSOP_STAGE_5_VISUAL_BEAT_MAP_V1.csv"
with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)

counts: dict[str, int] = {}
for row in rows:
    counts[row["asset_class"]] = counts.get(row["asset_class"], 0) + 1

md = [
    "# SATSOP — STAGE 5 VISUAL BEAT MAP V1",
    "",
    "Status: **COMPLETE TIMING MAP — ASSETS NOT YET CLEARED OR GENERATED**",
    "",
    f"- Canonical runtime: **00:19:23.920**",
    f"- Beats: **{len(rows)}**",
    f"- Average beat: **{sum(r['duration_seconds'] for r in rows)/len(rows):.2f} s**",
    "- Timing source: local word-level alignment against the locked Arthur VO",
    "- Renderer target: Remotion",
    "- Paid generation performed in Stage 5: **none**",
    "",
    "## Planned class count",
    "",
]
for key in sorted(counts):
    md.append(f"- `{key}`: **{counts[key]}**")
md += ["", "## Beats", ""]
for row in rows:
    md += [
        f"## {row['beat_id']} — {row['start']} → {row['end']} ({row['duration_seconds']:.3f}s)",
        "",
        f"**Narration:** {row['narration']}",
        "",
        f"- Narrative function: {row['chapter']}",
        f"- Main asset class: `{row['asset_class']}`",
        f"- Specific asset requirement: {row['specific_asset_requirement']}",
        f"- Provenance: {row['provenance']}",
        f"- Motion/editing: {row['motion_editing']}",
        f"- GFX: {row['gfx']}",
        f"- Rights/QC: {row['rights_qc']}",
        f"- Status: {row['status']}",
        "",
    ]
(OUT / "SATSOP_STAGE_5_VISUAL_BEAT_MAP_V1.md").write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

summary = {
    "runtime_seconds": 1163.92,
    "beat_count": len(rows),
    "average_beat_seconds": round(sum(r["duration_seconds"] for r in rows) / len(rows), 3),
    "class_counts": counts,
    "first_start": rows[0]["start"],
    "last_end": rows[-1]["end"],
    "coverage_seconds": round(sum(r["duration_seconds"] for r in rows), 3),
}
(OUT / "SATSOP_STAGE_5_BEAT_MAP_AUDIT.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
