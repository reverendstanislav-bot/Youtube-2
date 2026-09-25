from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "STAGE_5" / "SATSOP_STAGE_5_VISUAL_BEAT_MAP_V1.csv"
OUT = ROOT / "STAGE_6"
OUT.mkdir(exist_ok=True)

MODEL = {
    "model": "gpt_image_2_5",
    "variant": "flare",
    "quality": "low",
    "resolution": "1k",
    "aspect_ratio": "16:9",
    "count": 1,
    "use_unlim": False,
}

REFERENCE_PACKAGES = {
    "R01": "Verified present-day Satsop cooling-tower and exterior identity references; establishes tower form, wooded Washington setting, scale, and weather.",
    "R02": "Authenticated Satsop unit/site plan separating Project Three, Project Five, turbine buildings, cooling systems, roads, and common infrastructure.",
    "R03": "Authenticated WPPSS-era construction references: 1970s–1980s heavy concrete work, cranes, rebar, period vehicles, clothing, and safety equipment.",
    "R04": "Verified incomplete-nuclear-plant technical references: PWR containment/turbine/cooling-system geometry used only as engineering grounding, never as proof Satsop operated.",
    "R05": "Pacific Northwest industrial landscape references: wet evergreen terrain, overcast light, transmission corridors, hydro context, and period regional infrastructure.",
    "R06": "Source-grounded combined-cycle and power-system references used for comparison scenes; no invented exact Satsop conversion design.",
    "R07": "Verified present-day Satsop Business Park reuse references: turbine building, roads, warehouses, training spaces, and active industrial context.",
}

GLOBAL_SUFFIX = (
    "Hidden Industrial America visual canon. Cinematic 16:9 industrial documentary AI reconstruction, historically grounded and serious, "
    "naturalistic western Washington light, restrained charcoal / iron / warm-paper / faded-rust / blueprint-gray-blue grade. "
    "The Satsop nuclear projects were never fueled and never operated: no active reactor, no nuclear glow, no steam plume implying operation, "
    "no radioactive-hazard spectacle, no completed control room, and no finished plant passed off as real history. "
    "Preserve Project Three versus Project Five identity from supplied references. Do not invent readable logos, dates, signs, gauges, documents, "
    "technical labels, or named people. No faux archive border, scratches, dust, sepia, horror, neon, glossy concept art, or disaster-movie treatment. "
    "Use physically plausible concrete, steel, cranes, roads, transmission equipment, weather, clothing, and construction methods for the stated period. "
    "Keep the lower 15 percent and lower center quiet and low-detail for subtitles; keep faces, essential machinery, maps, and key action above it. "
    "No on-image title text. Production metadata and the edit must label the generated layer AI RECONSTRUCTION for its complete on-screen duration."
)

CAMERAS = [
    "wide elevated establishing composition",
    "ground-level three-quarter composition with strong human scale",
    "medium-wide lateral composition with layered foreground machinery",
    "long-lens compressed industrial composition",
    "high oblique site composition",
    "low architectural composition emphasizing concrete mass",
    "restrained interior-to-exterior composition",
    "asymmetrical wide composition with negative space",
]


def references(text: str, asset_class: str) -> list[str]:
    t = text.lower()
    refs = {"R01"}
    if asset_class == "AI_RECONSTRUCTION_MAP" or any(k in t for k in ["side by side", "site", "road", "hanford", "northwest"]):
        refs.add("R02")
    if any(k in t for k in ["construction", "worker", "built", "concrete", "crane", "suspended", "terminated", "1982", "1983"]):
        refs.add("R03")
    if asset_class == "AI_RECONSTRUCTION_GFX" or any(k in t for k in ["reactor", "turbine", "cooling system", "steam", "megawatt"]):
        refs.add("R04")
    if any(k in t for k in ["northwest", "hydroelectric", "transmission", "region", "utilities"]):
        refs.add("R05")
    if any(k in t for k in ["combined-cycle", "gas option", "repowering", "gas-fired"]):
        refs.add("R06")
    if any(k in t for k in ["business park", "redevelopment", "reuse", "warehouse", "training", "roads", "another job"]):
        refs.add("R07")
    return sorted(refs)


def scene_direction(text: str, asset_class: str, index: int) -> str:
    t = text.lower()
    camera = CAMERAS[(index - 1) % len(CAMERAS)]
    if "two cooling towers" in t or "towers still look like twins" in t:
        subject = "Show the two real-proportioned unfinished Satsop cooling towers rising separately above wet evergreen forest, with distinct spatial identity and no operating vapor."
    elif "project five" in t and "project three" in t:
        subject = "Separate Project Three and Project Five spatially and narratively: two neighboring unfinished construction zones with visibly different completion states, never one completed twin-unit station."
    elif "project five" in t:
        subject = "Focus on the less-complete Project Five construction zone: partial foundations, incomplete structural work, stored materials, and stopped activity, without borrowing Project Three's advanced structures."
    elif "project three" in t and any(k in t for k in ["seventy-four", "mostly built", "much of it existed", "close to finished"]):
        subject = "Show Project Three as substantially built from the outside yet visibly incomplete: cooling tower, major buildings, open construction areas, unfinished connections, and no operational signs."
    elif any(k in t for k in ["five nuclear projects", "entire portfolio", "competing for engineering", "organization"]):
        subject = "Construct a period planning-room and multi-site infrastructure montage in one coherent scene: maps, scale models, engineers, and five-project ambition, with all readable data reserved for later editorial overlays."
    elif any(k in t for k in ["take-or-pay", "contracts", "bonds", "capability shares", "net billing"]):
        subject = "Use a physical institutional scene rather than fake paperwork: period utility boardroom, bond/contract folders without readable text, regional power map, and participants connected through restrained editorial lines added later."
    elif any(k in t for k in ["construction", "built", "concrete", "crane", "workers"]):
        subject = "Show a specific Satsop construction operation with period cranes, rebar cages, formwork, concrete pours, and a small crew for scale; the plant remains incomplete and the equipment follows 1970s–early-1980s practice."
    elif any(k in t for k in ["suspended", "preservation", "mothballed", "inspection", "corrosion", "weather"]):
        subject = "Show preservation after suspension: silent unfinished industrial spaces under inspection, protected equipment, temporary weather barriers, damp Washington air, and a small maintenance crew preventing deterioration."
    elif any(k in t for k in ["reactor heat", "steam", "turbine generator", "cooling system"]):
        subject = "Create a cutaway-style generated industrial base showing the intended reactor-to-steam-to-turbine-to-cooling chain, with incomplete links visibly broken; exact arrows and labels will be added as vector GFX."
    elif any(k in t for k in ["combined-cycle", "gas-fired", "gas option", "repowering"]):
        subject = "Contrast the massive unfinished nuclear site with modular combined-cycle equipment in a physically plausible comparison scene; treat the gas plant as an alternative, not as something built at Satsop."
    elif any(k in t for k in ["surplus", "load", "demand", "power when"]):
        subject = "Visualize regional supply exceeding demand through a generated Pacific Northwest power landscape and modular generation blocks, leaving exact quantities to clean editorial GFX."
    elif any(k in t for k in ["capital at risk", "fixed costs", "future risk", "sunk cost", "money was already gone"]):
        subject = "Use an industrial-scale visual metaphor grounded in the site: unfinished concrete mass in one direction and smaller modular commitments in another; no coins, casino imagery, or generic finance icons."
    elif any(k in t for k in ["permit", "regulation", "decision", "administrator", "board"]):
        subject = "Stage a restrained institutional decision environment with the unfinished site visible through photographs or windows, keeping all documents unreadable so verified source excerpts can be composited separately."
    elif any(k in t for k in ["business park", "redevelopment", "reuse", "warehouse", "training", "another job"]):
        subject = "Show credible adaptive reuse of the former nuclear-site infrastructure: active industrial building, maintained roads, training activity, and reused heavy spaces, without portraying the whole site as abandoned."
    elif any(k in t for k in ["road", "building", "electrical connections", "tunnel"]):
        subject = "Isolate one reusable infrastructure element—heavy road, turbine building, tunnel, or electrical connection—in an active industrial composition that explains value beyond the abandoned reactor plan."
    elif asset_class == "AI_RECONSTRUCTION_MAP":
        subject = "Create a clean generated aerial/site context of Satsop with forests, roads, towers, and unfinished plant zones; factual unit boundaries and labels will be supplied only by the authenticated vector overlay."
    elif asset_class == "AI_RECONSTRUCTION_GFX":
        subject = "Create a technically restrained generated industrial base for the named system or comparison, leaving clean space and clear geometry for exact HIA vector explanation."
    else:
        subject = "Create a concrete historical-industrial scene that makes this narration visually legible through people, structures, machinery, weather, and spatial relationships rather than written text."

    return (
        f"{camera}. {subject} The exact narration beat is: {text} "
        "Interpret the beat literally and economically; one dominant visual idea, one secondary layer at most, and a composition materially different from neighboring beats. "
        + GLOBAL_SUFFIX
    )


with SOURCE.open(encoding="utf-8-sig", newline="") as f:
    beats = list(csv.DictReader(f))

generated = [row for row in beats if row["asset_class"].startswith("AI_")]
items = []
for index, row in enumerate(generated, 1):
    refs = references(row["narration"], row["asset_class"])
    items.append(
        {
            "prompt_id": f"SAT-GEN{index:03}",
            "beat_id": row["beat_id"],
            "start": row["start"],
            "end": row["end"],
            "duration_seconds": float(row["duration_seconds"]),
            "asset_class": row["asset_class"],
            "narration": row["narration"],
            "references": refs,
            "model": MODEL["model"],
            "variant": MODEL["variant"],
            "quality": MODEL["quality"],
            "resolution": MODEL["resolution"],
            "aspect_ratio": MODEL["aspect_ratio"],
            "count": MODEL["count"],
            "preflight_cost_credits": 0.25,
            "provenance": "AI RECONSTRUCTION",
            "prompt": scene_direction(row["narration"], row["asset_class"], index),
            "status": "COST PREFLIGHT PASS — NOT GENERATED",
        }
    )

assert len(items) == 68
assert len({item["prompt_id"] for item in items}) == 68
assert len({item["beat_id"] for item in items}) == 68
assert all(item["references"] for item in items)

json_path = OUT / "SATSOP_GENERATION_PROMPT_PACK_V1.json"
json_path.write_text(
    json.dumps(
        {
            "status": "COST PREFLIGHT PASS — NOT GENERATED",
            "model_defaults": MODEL,
            "reference_packages": REFERENCE_PACKAGES,
            "global_suffix": GLOBAL_SUFFIX,
            "prompt_count": len(items),
            "items": items,
        },
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

csv_path = OUT / "SATSOP_GENERATION_PROMPT_PACK_V1.csv"
with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
    fields = [
        "prompt_id", "beat_id", "start", "end", "duration_seconds", "asset_class", "references",
        "model", "variant", "quality", "resolution", "aspect_ratio", "count", "preflight_cost_credits",
        "provenance", "prompt", "status",
    ]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for item in items:
        out = dict(item); out["references"] = "+".join(item["references"]); out.pop("narration")
        writer.writerow({k: out[k] for k in fields})

md = [
    "# SATSOP — GENERATION PROMPT PACK V1",
    "",
    "Status: **68/68 PROMPTS READY — EXACT COST 17.00 CREDITS — NO GENERATION AUTHORIZED**",
    "",
    "## Model lock",
    "",
    "- model: `gpt_image_2_5` / GPT Image 2.5",
    "- variant: `flare`",
    "- quality: `low`",
    "- resolution: `1k`",
    "- aspect ratio: `16:9`",
    "- outputs per prompt: `1`",
    "- payment mode for future approved generation: credits (`use_unlim:false`)",
    "- exact provider preflight: `0.25 × 68 = 17.00 credits`",
    "",
    "## Reference packages",
    "",
]
for key, value in REFERENCE_PACKAGES.items():
    md.append(f"- **{key}:** {value}")
md += ["", "## Global guardrail", "", GLOBAL_SUFFIX, "", "## Individual prompts", ""]
for item in items:
    md += [
        f"## {item['prompt_id']} / {item['beat_id']} — {item['start']} → {item['end']}",
        "",
        f"- Asset class: `{item['asset_class']}`",
        f"- References: `{' + '.join(item['references'])}`",
        f"- Provenance: `AI RECONSTRUCTION`",
        f"- Narration: {item['narration']}",
        "",
        "### Production prompt",
        "",
        item["prompt"],
        "",
        "### QC",
        "",
        "- one distinct composition for this beat;",
        "- references assigned before submission;",
        "- no readable invented text;",
        "- no false operating/completed-reactor implication;",
        "- caption-safe lower 15 percent;",
        "- label `AI RECONSTRUCTION` for the full generated shot.",
        "",
    ]
md += [
    "## Pack audit",
    "",
    "- prompts: **68**;",
    "- unique prompt IDs: **68**;",
    "- unique mapped beat IDs: **68**;",
    "- unassigned reference packages: **0**;",
    "- generated jobs submitted while building this pack: **0**.",
    "- exact authorized image spend at this stage: **0.00 credits**.",
]
(OUT / "SATSOP_GENERATION_PROMPT_PACK_V1.md").write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

print(json.dumps({"prompt_count": len(items), "model": MODEL, "reference_packages": REFERENCE_PACKAGES}, indent=2))
