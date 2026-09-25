from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "STAGE_6" / "V2" / "SATSOP_GENERATION_PROMPT_PACK_V2.json"
OUT = ROOT / "STAGE_6" / "V3"
OUT.mkdir(parents=True, exist_ok=True)

LOCKED = "LOCKED_PASS_REUSE"

# These twelve treatments directly replace every non-passing result from the V2 test.
CORRECTIONS = {
    "SAT-GEN001": ("Foundation-only close shot: two surveyors beside low concrete footings and sparse rebar, forest horizon soft and distant. Frame below the skyline so no reactor building, tower, switchyard or site layout can be invented.", "REFERENCE_CONDITIONED_GENERATION"),
    "SAT-GEN002": ("Preservation-era exterior detail controlled by the supplied Project Three photographs: crop to the verified cooling-tower base, unfinished wall junction and sealed access point. Do not show or invent a reactor dome or a complete site panorama.", "REFERENCE_CONDITIONED_GENERATION"),
    "SAT-GEN003": ("Generate only a flat, unlabeled charcoal-and-warm-paper topographic texture with a subtle orthographic grid and two empty translucent footprint zones. No coastline, river, road, building, tower, reactor, terrain landmark or site geometry. The authenticated R02 plan supplies every factual shape in editorial compositing.", "EDITORIAL_GFX_BASE_ONLY"),
    "SAT-GEN006": ("Tight ground-level view of a single early foundation bay, stacked rebar and stopped formwork with large surrounding emptiness. No skyline, reactor building, cooling tower or invented Project Five geography.", "REFERENCE_CONDITIONED_GENERATION"),
    "SAT-GEN016": ("Generate only a neutral two-lane financial comparison plate: two empty vertical zones separated by a thin center rule, restrained paper texture, no map, land, water, roads, buildings or reactor forms. R02 geometry and finance labels are added as exact vector overlays.", "EDITORIAL_GFX_BASE_ONLY"),
    "SAT-GEN020": ("Minimal technical comparison plate using two identical plain rectangular system envelopes and simple empty internal bays. No reactor vessels, domes, piping, machinery or engineering details generated. Verified R04 silhouettes and 1,240 MW labels are composited later.", "EDITORIAL_GFX_BASE_ONLY"),
    "SAT-GEN022": ("Minimal four-stage process plate made from four empty industrial frames connected only by clear spacing. No reactor vessel, turbine, cooling equipment, pipes, arrows or labels generated. Exact R04 components and flow arrows are added later.", "EDITORIAL_GFX_BASE_ONLY"),
    "SAT-GEN046": ("Clean quantitative plate: one large neutral capacity block above a clearly lower demand band, plus a separate empty surplus zone. No plant, landscape, grid, digits, labels or decorative machinery. Exact 1,240 MW and 600 aMW values are editorial overlays.", "EDITORIAL_GFX_BASE_ONLY"),
    "SAT-GEN050": ("Clean two-field comparison plate: a dense built-assets field on the left and a visibly smaller demand field on the right, separated by an empty overlay lane. No site image, map, reactor, landscape, number or label.", "EDITORIAL_GFX_BASE_ONLY"),
    "SAT-GEN057": ("Neutral four-column chronology plate with four physically distinct blank icon wells: stopped construction barrier, bond folder, preservation cover and closed permit file. No landscapes, plant images, dates, text or repeated scenery.", "EDITORIAL_GFX_BASE_ONLY"),
    "SAT-GEN065": ("Representative present-day adaptive-reuse interior: maintained high-bay industrial workspace, ordinary logistics, clean floor and active equipment. Do not claim exact Satsop architecture; no reactor components, abandoned debris, cranes or nuclear construction.", "REFERENCE_CONDITIONED_GENERATION"),
    "SAT-GEN068": ("Representative infrastructure-afterlife composition: active industrial building and maintained road in the foreground, one distant concrete legacy structure reduced to context. Do not imitate a specific Satsop layout without R01/R07.", "REFERENCE_CONDITIONED_GENERATION"),
}

EDITORIAL_GRAMMARS = {
    "MAP_BASE", "REUSE_MAP_BASE", "TECHNICAL_GFX_BASE", "NETWORK_GFX_BASE",
    "COMPARISON_GFX_BASE", "CAPITAL_GFX_BASE", "COST_GFX_BASE", "QUANT_GFX_BASE",
    "NEED_GFX_BASE", "CHRONOLOGY_GFX_BASE", "DEBT_GFX_BASE", "REGIONAL_GFX_BASE",
    "REPOWER_GFX_BASE",
}

EDITORIAL_BASES = {
    "MAP_BASE": "Build a flat, unlabeled charcoal-and-warm-paper map canvas with an empty plot area. Add all coastlines, rivers, roads, boundaries, site footprints and labels later as authenticated vectors.",
    "REUSE_MAP_BASE": "Build a flat, unlabeled present-day reuse-map canvas with an empty plot area. Add every road, parcel, building footprint and label later as authenticated vectors.",
    "TECHNICAL_GFX_BASE": "Build a neutral technical-comparison canvas with empty component wells. Add all equipment silhouettes, flow paths, arrows, values and labels later from verified engineering sources.",
    "NETWORK_GFX_BASE": "Build a neutral network canvas with empty nodes and clear routing space. Add all organizations, connections, arrows, dates and labels later as authenticated vectors.",
    "COMPARISON_GFX_BASE": "Build a clean two-field comparison canvas with an empty center lane. Add every factual category, icon, value and label later as editorial vectors.",
    "CAPITAL_GFX_BASE": "Build a restrained capital-flow canvas with empty source, project and obligation zones. Add all money flows, arrows, values and labels later as verified editorial graphics.",
    "COST_GFX_BASE": "Build a restrained cost-comparison canvas with empty bars and annotation lanes. Add every amount, scale, date and label later as verified editorial graphics.",
    "QUANT_GFX_BASE": "Build a restrained quantitative canvas with empty blocks and annotation lanes. Add every value, scale, relationship and label later as verified editorial graphics.",
    "NEED_GFX_BASE": "Build a restrained demand-versus-capacity canvas with empty bands and annotation lanes. Add all values, scales, relationships and labels later as verified editorial graphics.",
    "CHRONOLOGY_GFX_BASE": "Build a restrained chronology canvas with distinct empty milestone wells and a clear timing lane. Add every date, event, icon and label later as verified editorial graphics.",
    "DEBT_GFX_BASE": "Build a restrained debt-obligation canvas with empty issuer, obligation and payer zones. Add all amounts, flows, dates and labels later as verified editorial graphics.",
    "REGIONAL_GFX_BASE": "Build a flat, unlabeled regional canvas with empty geographic and network layers. Add all real geography, transmission paths, facilities and labels later as authenticated vectors.",
    "REPOWER_GFX_BASE": "Build a restrained old-versus-new power-system canvas with two empty equipment zones. Add verified plant silhouettes, capacities, dates and labels later as editorial vectors.",
}

REFERENCE_SENSITIVE = {
    "CONSTRUCTION_PHASE", "SITE_IDENTITY", "COMPONENT_SCALE", "PRESERVATION",
    "TOWER_REVEAL", "EXISTING_ADVANTAGES", "MODERN_REUSE", "REUSE_RESOLUTION",
}

GLOBAL = (
    "Create one restrained 16:9 documentary frame with a clear primary subject and no competing secondary story. "
    "Use realistic materials, neutral natural light and a calm lower 15 percent for captions. "
    "Never render words, dates, numbers, logos, maps, arrows, diagrams, captions or document text. "
    "No nuclear glow, operating steam, disaster imagery, active reactor, completed Satsop plant, faux archival damage or cinematic spectacle."
)

v2 = json.loads(SOURCE.read_text(encoding="utf-8"))
items = []
for old in v2["items"]:
    item = dict(old)
    item["v2_queue_status"] = old["queue_status"]
    if old["queue_status"] == LOCKED:
        item["production_route"] = "LOCKED_GENERATED_ASSET"
        item["v3_status"] = LOCKED
        item["v3_prompt"] = "DO NOT GENERATE — use the locked accepted asset recorded in locked_asset."
        item["reference_gate"] = "LOCKED_ASSET_NO_NEW_JOB"
        item["cost_if_generated_credits"] = 0.0
    else:
        proposition, forced_route = CORRECTIONS.get(old["prompt_id"], (old["visual_proposition"], None))
        grammar = old["prompt_grammar"]
        if forced_route:
            route = forced_route
        elif grammar in EDITORIAL_GRAMMARS or old["asset_class"] in {"AI_RECONSTRUCTION_MAP", "AI_RECONSTRUCTION_GFX"}:
            route = "EDITORIAL_GFX_BASE_ONLY"
        elif grammar in REFERENCE_SENSITIVE:
            route = "REFERENCE_CONDITIONED_GENERATION"
        else:
            route = "CONTROLLED_TEXT_GENERATION"

        if route == "EDITORIAL_GFX_BASE_ONLY":
            proposition = EDITORIAL_BASES.get(
                grammar,
                "Build a neutral editorial canvas with empty evidence zones. Add every factual shape, relationship, value and label later as verified editorial vectors.",
            )
            evidence = (
                "This is an editor-built non-factual design plate. It must contain no geographic, architectural, engineering or numeric claim; "
                "all evidence comes from deterministic editorial vectors."
            )
            gate = "EDITORIAL_BUILD_NO_IMAGE_JOB"
        elif route == "REFERENCE_CONDITIONED_GENERATION":
            evidence = (
                "Match only the supplied reference media for identifiable geometry. If those media are absent, do not submit this job. "
                "Do not infer unseen buildings, roads, water, machinery or site relationships."
            )
            gate = "BLOCKED_UNTIL_REAL_MEDIA_IDS_ATTACHED"
        else:
            evidence = (
                "This is an explicitly interpretive reconstruction. Avoid identifiable real people and keep every document surface blank for editorial replacement."
            )
            gate = "TEXT_ONLY_ALLOWED_AFTER_SMALL_BATCH_APPROVAL"

        if route == "EDITORIAL_GFX_BASE_ONLY":
            prompt = (
                f"EDITORIAL BUILD BRIEF FOR {old['beat_id']}: {proposition} "
                f"Reserve the factual overlay lane for: {old['overlay_plan']}. "
                f"EVIDENCE BOUNDARY: {evidence}"
            )
        else:
            prompt = f"SUBJECT AND COMPOSITION: {proposition} EVIDENCE BOUNDARY: {evidence} {GLOBAL}"
        item["visual_proposition"] = proposition
        item["production_route"] = route
        item["v3_status"] = "READY_FOR_TARGETED_VALIDATION_NOT_AUTHORIZED"
        item["v3_prompt"] = prompt
        item["reference_gate"] = gate
        item["cost_if_generated_credits"] = 0.5 if route != "EDITORIAL_GFX_BASE_ONLY" else 0.0
    items.append(item)

assert len(items) == 68
assert sum(item["v3_status"] == LOCKED for item in items) == 13
assert sum(item["v3_status"] != LOCKED for item in items) == 55
assert len({item["v3_prompt"] for item in items if item["v3_status"] != LOCKED}) == 55
assert all(item["v3_prompt"] != item["prompt"] for item in items if item["v3_status"] != LOCKED)

counts = {}
for item in items:
    counts[item["production_route"]] = counts.get(item["production_route"], 0) + 1
remaining_cost = sum(item["cost_if_generated_credits"] for item in items)

payload = {
    "status": "V3 DIRECTORIAL-RISK REDUCTION COMPLETE — NO GENERATION AUTHORIZED",
    "locked_pass_count": 13,
    "pending_count": 55,
    "route_counts": counts,
    "maximum_remaining_image_cost_credits": remaining_cost,
    "generation_authorized": False,
    "items": items,
}
(OUT / "SATSOP_GENERATION_PROMPT_PACK_V3.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

fields = [
    "prompt_id", "beat_id", "start", "end", "asset_class", "prompt_grammar",
    "production_route", "required_reference_packages", "reference_gate", "overlay_plan",
    "v3_status", "cost_if_generated_credits", "v3_prompt",
]
with (OUT / "SATSOP_GENERATION_PROMPT_PACK_V3.csv").open("w", newline="", encoding="utf-8-sig") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for item in items:
        flat = dict(item)
        flat["required_reference_packages"] = "+".join(item["required_reference_packages"])
        writer.writerow({field: flat[field] for field in fields})

lines = [
    "# SATSOP — GENERATION PROMPT PACK V3", "",
    "Status: **DIRECTORIAL-RISK REWRITE COMPLETE — 13 LOCKED / 55 ROUTED / NO GENERATION AUTHORIZED**", "",
    "V3 is designed to maximize usable outputs rather than force every beat through photoreal generation. Factual maps, chronology, technical diagrams and quantitative comparisons are routed to deterministic editorial GFX with no image-generation job. Site-specific reconstruction is blocked until real reference media are attached.", "",
    f"- locked accepted assets: **13**", f"- pending positions: **55**",
    f"- route counts: `{json.dumps(counts, sort_keys=True)}`",
    f"- maximum remaining image-generation cost under V3 routing: **{remaining_cost:.2f} credits**", "",
]
for item in items:
    lines += [
        f"## {item['prompt_id']} / {item['beat_id']}", "",
        f"- Route: `{item['production_route']}`", f"- Status: `{item['v3_status']}`",
        f"- References: `{' + '.join(item['required_reference_packages'])}`", f"- Gate: `{item['reference_gate']}`",
        f"- Overlay: {item['overlay_plan']}", "", "### V3 prompt", "", item["v3_prompt"], "",
    ]
(OUT / "SATSOP_GENERATION_PROMPT_PACK_V3.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

print(json.dumps({"total": 68, "locked": 13, "pending": 55, "routes": counts, "max_cost": remaining_cost}, indent=2))
