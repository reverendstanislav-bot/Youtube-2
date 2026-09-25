from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "STAGE_6" / "V3" / "SATSOP_GENERATION_PROMPT_PACK_V3.json"
OUT = ROOT / "STAGE_6" / "REMAINING_V4"
OUT.mkdir(parents=True, exist_ok=True)

V3_PASSES = {
    "SAT-GEN005", "SAT-GEN007", "SAT-GEN010", "SAT-GEN015", "SAT-GEN019",
    "SAT-GEN026", "SAT-GEN029", "SAT-GEN035", "SAT-GEN040", "SAT-GEN059",
    "SAT-GEN062",
}

CORRECTIONS = {
    "SAT-GEN008": "1969 regional planning room with five clearly separate abstract blank project maquettes on five tables, small staff dwarfed by the portfolio; no map, coastline, reactor model, site layout or modern screen.",
    "SAT-GEN009": "Single continuous wide frame, not a diptych: one modest nearly empty pre-1968 utility office transitions naturally into a crowded 1979 engineering floor through an open doorway. No divider, white panel, black panel, border or matte.",
    "SAT-GEN013": "Period public-utility counter with blank household bills and court-file boxes in foreground and worried customers waiting; one small generic construction photograph behind the clerk. Full-bleed image to every edge, with no border, matte or blank band.",
    "SAT-GEN017": "A branching chain of modest municipal utility offices represented by distinct service counters and blank folders leading toward one closed project folder. No plant, foundation, map, diagram, arrows or geographic relationship.",
    "SAT-GEN033": "Long empty industrial access road toward an uncertain forest horizon, with one maintenance barrier and a few aging equipment crates in foreground; no plant or active construction. Full-bleed image to every edge, with no border, matte or blank band.",
    "SAT-GEN037": "Top-down tabletop metaphor using two parallel material strips: one long strip with many unfinished physical checkpoints and one short strip with fewer modular blocks. No landscape, site, reactor, foundation, building, map, road or engineering claim.",
    "SAT-GEN038": "Generic late-1980s regional power dispatch room with reservoir photography, transmission paperwork and small modular thermal planning blocks; all documents blank, no identifiable geography or real facility layout.",
    "SAT-GEN041": "Balanced tabletop comparison with two equal neutral work areas: one holds a large long-lead commitment block and maintenance folder, the other holds smaller fuel-contract and emissions folders. No reactor, turbine, plant, landscape or heroic lighting.",
    "SAT-GEN042": "Utility planning tabletop with one rigid heavy straight commitment bar beside several smaller movable resource blocks being rearranged by human hands. No river shape, map, coastline, road, landscape or site geometry.",
    "SAT-GEN045": "Abstract decision tabletop: two equal distant outcome blocks, but the near path to one carries a single much larger locked-capital block. No plant, reactor, dome, water, coastline, landscape, map or site.",
    "SAT-GEN047": "Abstract capacity-versus-demand tabletop: one complete large neutral block feeds into a visibly narrower empty receiving lane, leaving part of the block unmatched. No power plant, grid, pipes, map, numbers or real site.",
    "SAT-GEN049": "Circular utility decision table with one large abstract commitment block at center and separate blank load, customer and finance folders around it. No reactor model, dome, plant, transmission tower or site geometry.",
    "SAT-GEN051": "One huge immovable neutral commitment block contrasted with several smaller distributed resource blocks, with a thin existing-assets layer beneath the large block. No plant, reactor, machinery, map or landscape.",
    "SAT-GEN055": "June 1994 administrative decision aftermath inside a quiet office: one newly closed project folder behind a simple barrier arm model, preserved-asset keys untouched beside it. No exterior site, reactor, building, gate landscape or demolition.",
}

GLOBAL = (
    "Create a full-bleed restrained 16:9 documentary frame with one clear primary subject and no competing secondary story. "
    "Use realistic materials and neutral natural light. Keep the image continuous to all four edges: no white or black bars, borders, mattes, frames, split-screen dividers or artificial blank panels. "
    "Never render readable words, dates, numbers, logos, maps, arrows, diagrams, captions or document text. "
    "No nuclear glow, operating steam, disaster imagery, active reactor, completed Satsop plant, faux archival damage or cinematic spectacle."
)

source = json.loads(SOURCE.read_text(encoding="utf-8"))
queue = []
for item in source["items"]:
    if item["production_route"] != "CONTROLLED_TEXT_GENERATION" or item["prompt_id"] in V3_PASSES:
        continue
    proposition = CORRECTIONS.get(item["prompt_id"], item["visual_proposition"])
    prompt = (
        f"SUBJECT AND COMPOSITION: {proposition} "
        "EVIDENCE BOUNDARY: This is an explicitly interpretive reconstruction. Avoid identifiable real people and keep every document surface blank for editorial replacement. "
        f"{GLOBAL}"
    )
    queue.append({
        "index": len(queue) + 1,
        "prompt_id": item["prompt_id"],
        "beat_id": item["beat_id"],
        "prompt_grammar": item["prompt_grammar"],
        "model": "gpt_image_2",
        "aspect_ratio": "16:9",
        "cost_credits": 0.5,
        "prompt": prompt,
    })

assert len(queue) == 18
assert len({item["prompt"] for item in queue}) == 18
assert all("calm lower" not in item["prompt"].lower() for item in queue)
assert all("no white or black bars" in item["prompt"].lower() for item in queue)

payload = {
    "status": "AUTHORIZED REMAINING REFERENCE-FREE IMAGE QUEUE",
    "generation_count": 18,
    "expected_cost_credits": 9.0,
    "no_retries": True,
    "items": queue,
}
(OUT / "SATSOP_REMAINING_GENERATION_V4.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"count": len(queue), "cost": 9.0, "output": str(OUT)}, indent=2))
