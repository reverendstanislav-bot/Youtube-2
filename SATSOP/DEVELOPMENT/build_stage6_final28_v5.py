from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "STAGE_6" / "V3" / "SATSOP_GENERATION_PROMPT_PACK_V3.json"
OUT = ROOT / "STAGE_6" / "FINAL28_V5"
OUT.mkdir(parents=True, exist_ok=True)

SUBJECTS = {
    "SAT-GEN001": "Ground-level close shot of two early-1980s surveyors beside a single low concrete footing and sparse rebar in a wet Pacific Northwest clearing. Frame below the horizon; no reactor, tower or site layout.",
    "SAT-GEN002": "Preservation-era close detail of an unfinished poured-concrete wall junction, sealed access opening and weathered construction joint. Tight crop only; no dome, tower or panorama.",
    "SAT-GEN003": "Tactile editorial map base made from dark paper, one subtle grid and two differently sized empty footprint zones. No real coastline, river, road, building or geographic shape.",
    "SAT-GEN004": "Two-panel tactile chronology base: sparse unfinished material field on the left and a denser preserved-construction field on the right, divided by a clean central time lane. No real site geometry.",
    "SAT-GEN006": "Tight close shot of one abandoned early foundation bay with stopped formwork, bundled rebar and large surrounding emptiness. No skyline, tower, reactor building or identifiable geography.",
    "SAT-GEN016": "Two-lane financial comparison board built from neutral paper and wood: one branching participant lane and one single institutional lane, with empty label areas. No map or plant imagery.",
    "SAT-GEN020": "Two equal abstract technical envelopes built from cut paper, each containing the same four empty component slots. No machinery, reactor vessel, dome, piping, digits or labels.",
    "SAT-GEN021": "Low-angle close view from inside the base of a monumental unfinished concrete cooling structure, with one worker for scale and visible open sky. Treat it only as heat-rejection infrastructure; no reactor or steam.",
    "SAT-GEN022": "Four-stage tactile process base made from four distinct empty industrial-shaped frames arranged left to right with clear gaps. No arrows, labels, machinery or reactor details.",
    "SAT-GEN023": "Abstract chain-of-completion board: a sequence of neutral physical blocks stops abruptly before the final empty destination slot, with an earlier side branch ending first. No map, plant or readable text.",
    "SAT-GEN024": "Close preservation scene inside a generic unfinished industrial hall: protected equipment crate, inspection tags turned away, dry floor and a small maintenance crew. No active construction or operating machinery.",
    "SAT-GEN027": "Regional demand-change base using a broad empty paper band that narrows across time while a separate unused capacity block remains stationary. No geography, grid, plant, values or labels.",
    "SAT-GEN028": "Maintenance crew performing a careful visual inspection of sealed generic industrial equipment in a quiet unfinished concrete hall. No reactor components, active construction, readable forms or exact site geometry.",
    "SAT-GEN030": "Tactile capital-cost base with one large stack of blank bond-like paper expanding across three empty milestone wells. No currency symbols, numbers, words or plant imagery.",
    "SAT-GEN034": "Late-1980s small Northwest workshop after hours: owner studies a blank utility invoice beside an open operating ledger, dim workbench and closed storefront visible behind. Full-bleed, no newspaper or plant photograph.",
    "SAT-GEN038": "Late-1980s regional power dispatch room with reservoir photographs, transmission paperwork and three plain rectangular planning blocks. No plant model, dome, reactor, turbine, smokestack or identifiable geography.",
    "SAT-GEN043": "Tactile completion-cost base with one existing sunk-cost block and a second slightly larger future-completion block separated by a narrow decision gap. No numbers, words, currency or plant.",
    "SAT-GEN046": "Clean capacity-versus-demand base: one large neutral block above a visibly shorter receiving band, plus a separate empty surplus zone. No digits, labels, plant, landscape or machinery.",
    "SAT-GEN048": "Extreme close-up of massive weathered poured concrete curving out of frame, with a tiny maintenance worker and ordinary service door for scale. No full tower, dome, reactor or invented site layout.",
    "SAT-GEN050": "Two-field evidence-safe comparison base: dense built-asset blocks on the left and a much smaller demand field on the right, separated by an empty annotation lane. No plant, map, values or labels.",
    "SAT-GEN052": "Close still life of reusable industrial advantages: heavy electrical conduit, intact service rail, blank permit folders and an empty emissions folder slot. No plant exterior, reactor or readable text.",
    "SAT-GEN053": "Two-path repower-versus-new-build base: one path begins with several existing neutral asset blocks while the other begins from an empty foundation plane. No machinery, plant, arrows, words or numbers.",
    "SAT-GEN057": "Four-column tactile chronology base with distinct blank icon wells: stopped barrier, bond folder, preservation cover and closed permit file. No dates, words, landscapes or plant imagery.",
    "SAT-GEN060": "Long-lived debt base: a sealed project folder at far left connects through a sequence of empty annual budget trays extending deep into frame. No people, plant, digits, labels or currency symbols.",
    "SAT-GEN064": "Present-day reuse-map base made from neutral paper parcels, one maintained road strip and several empty industrial footprint blocks. No real geography, labels, reactor forms or nuclear symbols.",
    "SAT-GEN065": "Representative present-day adaptive-reuse interior: maintained high-bay industrial workspace, ordinary logistics activity, clean floor and active non-nuclear equipment. No abandoned debris, reactor components or exact Satsop claim.",
    "SAT-GEN067": "Representative working industrial site: maintained warehouse frontage, delivery vehicle and small crew during an ordinary shift, with no nuclear structures, logos or readable signs.",
    "SAT-GEN068": "Representative infrastructure-afterlife composition: active modest industrial building and maintained access road in foreground, one distant anonymous concrete legacy wall reduced to context. No reactor, dome, tower or exact site layout.",
}

GLOBAL = (
    "Create a full-bleed restrained 16:9 documentary frame with one dominant visual idea. Use realistic materials, neutral natural light and period-appropriate details where relevant. "
    "Continue the image to every edge: no white or black bars, borders, mattes, split screens or artificial blank panels. "
    "Never render readable words, dates, numbers, logos, captions, watermarks or document text. "
    "No nuclear glow, operating steam, disaster imagery, active reactor, completed Satsop plant, faux archival damage or cinematic spectacle."
)

source = json.loads(SOURCE.read_text(encoding="utf-8"))
wanted = [item for item in source["items"] if item["production_route"] in {"REFERENCE_CONDITIONED_GENERATION", "EDITORIAL_GFX_BASE_ONLY"}]
wanted += [next(item for item in source["items"] if item["prompt_id"] == prompt_id) for prompt_id in ("SAT-GEN034", "SAT-GEN038")]
queue = []
for item in wanted:
    subject = SUBJECTS[item["prompt_id"]]
    route = "HIGGSFIELD_GFX_BASE" if item["production_route"] == "EDITORIAL_GFX_BASE_ONLY" else "HIGGSFIELD_SAFE_RECONSTRUCTION"
    if item["prompt_id"] in {"SAT-GEN034", "SAT-GEN038"}:
        route = "HIGGSFIELD_CORRECTION"
    prompt = (
        f"SUBJECT AND COMPOSITION: {subject} "
        "EVIDENCE BOUNDARY: This image is a reconstruction or editorial base, not documentary proof of exact Satsop geometry. "
        f"{GLOBAL}"
    )
    queue.append({
        "index": len(queue) + 1,
        "prompt_id": item["prompt_id"],
        "beat_id": item["beat_id"],
        "route": route,
        "overlay_plan": item["overlay_plan"],
        "model": "gpt_image_2",
        "aspect_ratio": "16:9",
        "cost_credits": 0.5,
        "prompt": prompt,
    })

assert len(queue) == 28
assert len({item["prompt_id"] for item in queue}) == 28
assert len({item["prompt"] for item in queue}) == 28
assert all("calm lower" not in item["prompt"].lower() for item in queue)

payload = {
    "status": "AUTHORIZED FINAL 28 HIGGSFIELD GENERATION",
    "generation_count": 28,
    "expected_cost_credits": 14.0,
    "reference_note": "No authenticated R01-R07 identity mapping was available; site-sensitive frames were reframed as non-identifying close or representative reconstructions.",
    "items": queue,
}
(OUT / "SATSOP_FINAL28_PROMPTS_V5.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"count": len(queue), "cost": 14.0, "output": str(OUT)}, indent=2))
