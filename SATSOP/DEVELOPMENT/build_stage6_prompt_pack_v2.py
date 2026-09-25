from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "STAGE_5" / "SATSOP_STAGE_5_VISUAL_BEAT_MAP_V1.csv"
OUT = ROOT / "STAGE_6" / "V2"
OUT.mkdir(parents=True, exist_ok=True)

MODEL = {"model": "gpt_image_2", "quality": "low", "resolution": "1k", "aspect_ratio": "16:9", "count": 1, "use_unlim": False}

TEST_GRADES = {
    "SAT-GEN001": "CONDITIONAL", "SAT-GEN002": "CONDITIONAL", "SAT-GEN003": "FAIL",
    "SAT-GEN006": "CONDITIONAL", "SAT-GEN011": "FAIL", "SAT-GEN016": "FAIL",
    "SAT-GEN018": "PASS", "SAT-GEN020": "FAIL", "SAT-GEN025": "FAIL",
    "SAT-GEN031": "PASS", "SAT-GEN032": "CONDITIONAL", "SAT-GEN039": "PASS",
    "SAT-GEN044": "FAIL", "SAT-GEN046": "FAIL", "SAT-GEN050": "CONDITIONAL",
    "SAT-GEN054": "PASS", "SAT-GEN057": "CONDITIONAL", "SAT-GEN063": "FAIL",
    "SAT-GEN066": "PASS", "SAT-GEN068": "CONDITIONAL",
}

SECOND_TEST_GRADES = {
    "SAT-GEN001": "CONDITIONAL", "SAT-GEN002": "FAIL", "SAT-GEN003": "FAIL",
    "SAT-GEN006": "CONDITIONAL", "SAT-GEN011": "PASS", "SAT-GEN012": "PASS",
    "SAT-GEN016": "FAIL", "SAT-GEN020": "CONDITIONAL", "SAT-GEN022": "CONDITIONAL",
    "SAT-GEN025": "PASS", "SAT-GEN032": "PASS", "SAT-GEN036": "PASS",
    "SAT-GEN044": "PASS", "SAT-GEN046": "CONDITIONAL", "SAT-GEN050": "CONDITIONAL",
    "SAT-GEN057": "FAIL", "SAT-GEN058": "PASS", "SAT-GEN063": "PASS",
    "SAT-GEN065": "CONDITIONAL", "SAT-GEN068": "CONDITIONAL",
}

PLANS = {
    "SAT-B002": ("CONSTRUCTION_PHASE", "Project Five at an unmistakably early phase: low foundations and sparse formwork only, one survey crew for scale; no reactor dome, cooling tower, turbine hall, or completed switchyard.", "R02+R03", "1982", "14% / 1982"),
    "SAT-B003": ("SITE_IDENTITY", "Reference-matched Project Three exterior in preservation condition: cooling tower and major shells present, open unfinished interfaces visible, no cranes working and no operating vapor.", "R01+R02", "1983-1994 preservation", "74% / preserved to 1994"),
    "SAT-B004": ("MAP_BASE", "Near-orthographic site-plan plate matching the authenticated plan exactly; Project Three and Project Five footprints separated, all labels and status marks omitted for vector overlay.", "R02", "neutral factual map", "P3 / P5 / NEVER OPERATED"),
    "SAT-B005": ("MAP_BASE", "Split-site orthographic plate with Project Five visually sparse and Project Three substantially built; preserve exact plan geometry and reserve the center seam for a twelve-year timeline overlay.", "R01+R02", "1982-1994 comparison", "1982 → 1994"),
    "SAT-B006": ("INSTITUTIONAL", "January 1982 utility-board decision room after a vote: closed folders, empty chairs and a stopped-project site photograph on an easel; no readable invented documents.", "R03", "1982", "JAN 22 1982 / P4+P5 TERMINATED"),
    "SAT-B011": ("CONSTRUCTION_PHASE", "Project Five early works viewed from ground level: isolated concrete foundations and stored rebar separated by large empty tracts; make limited physical progress the dominant fact.", "R02+R03", "1981-1982", "14% / rising estimate"),
    "SAT-B012": ("FINANCIAL_METAPHOR", "A period utility desk where a signed payment obligation in the foreground visually blocks the road toward the distant unfinished site; documents remain blank for editorial replacement.", "R03", "1982", "PROMISE TO PAY / REWIND"),
    "SAT-B015": ("PLANNING_ROOM", "1969 regional planning room with five separate plant models arranged around a Pacific Northwest wall map, small staff dwarfed by the expansion plan; no modern screens.", "R03+R05", "1969", "5 PROJECTS"),
    "SAT-B016": ("WORKFORCE_SCALE", "Diptych base: a modest pre-1968 utility office on the left and a crowded 1979 engineering floor on the right, matched camera height and blank center for exact employee numbers.", "R03", "1968 vs 1979", "<100 → 1,471"),
    "SAT-B017": ("PORTFOLIO_SYSTEM", "Five distinct project worktables competing for the same limited pool of engineers, contractor schedules, component crates and permit trays in one overhead institutional composition.", "R03+R05", "late 1970s", "portfolio competition"),
    "SAT-B019": ("NETWORK_GFX_BASE", "Dark warm-paper regional map base with many small utility nodes converging on Projects Four and Five; no text, no fake boundaries, ample negative space for 88+1 overlay.", "R05", "1976", "88 BPA customers + 1 private utility"),
    "SAT-B021": ("CONTRACT_MECHANISM", "Three-state triptych using the same payment folder in front of an unfinished plant, an inoperable plant and an idle plant; the obligation remains visually unchanged in all panels.", "R03", "late 1970s-1980s", "PAY WHETHER COMPLETED OR OPERATING"),
    "SAT-B023": ("RATEPAYER_SCALE", "Period public-utility counter with household bills and court-file boxes in foreground, worried customers waiting, unfinished project photograph small in the background; all paper text blank.", "R03", "early 1980s", "RATE INCREASES / COURT"),
    "SAT-B024": ("LIABILITY_METAPHOR", "A stopped industrial gate at dusk with one heavy contract case being passed from project officials toward local utility representatives; no active construction.", "R03", "1982-1983", "WHO CARRIES THE BILL?"),
    "SAT-B025": ("FINANCIAL_COLLAPSE", "Empty bond-market trading desk and stacked blank bond certificates under a single extinguished task lamp, with the halted Project Five foundation visible only through a window.", "R03", "July 1983", "JUL 22 1983 / DEFAULT"),
    "SAT-B026": ("MAP_BASE", "Exact plan-matched two-project diagram plate divided into two clean financial lanes while retaining true site adjacency; no invented architecture or labels in the generated layer.", "R02", "neutral factual map", "P5 PARTICIPANT FINANCE / P3 BPA PATH"),
    "SAT-B027": ("FINANCE_NETWORK", "Project Five foundation at the end of a branching chain of municipal utility offices, each connected by restrained empty line paths reserved for editorial graphics.", "R02+R03", "late 1970s", "P4+P5 participant system"),
    "SAT-B029": ("INSTITUTIONAL", "Period utility boardroom with capability-share folders moving toward a central Bonneville representative; preserve the accepted TEST20 composition and do not regenerate.", "R03+R05", "late 1970s", "capability shares → BPA"),
    "SAT-B031": ("OWNERSHIP_SPLIT", "One clean tabletop divided 70/30 by physical folder stacks, public-utility side larger and four investor-owned utility chairs on the smaller side; blank overlay space above.", "R03", "agreement-era", "70% / 30% / 4 IOUs"),
    "SAT-B032": ("TECHNICAL_GFX_BASE", "Two simplified cutaway silhouettes of pressurized-water project systems derived from authenticated technical references, side by side on neutral blueprint-gray; no photoreal domes, labels, pipes to nowhere or operating effects.", "R02+R04", "design comparison", "PWR / 1,240 MW EACH"),
    "SAT-B035": ("COMPONENT_SCALE", "Low-angle exterior where the cooling tower occupies one edge while reactor, turbine and auxiliary building shells recede separately across the site, making the tower only one component.", "R01+R02+R04", "construction-era", "tower = heat rejection only"),
    "SAT-B036": ("TECHNICAL_GFX_BASE", "Clean horizontal four-stage engineering plate: reactor vessel silhouette, steam line, turbine-generator, cooling loop; unfinished broken link at Satsop, no labels or arrows rendered by the model.", "R04", "intended system", "HEAT → STEAM → TURBINE → COOLING"),
    "SAT-B037": ("MAP_BASE", "Plan-matched Satsop systems plate with the intended generation chain stopping before completion and Project Five highlighted as the first financial stop; generated layer contains no labels.", "R02+R04", "1982-1983", "CHAIN NEVER COMPLETED / P5 FIRST"),
    "SAT-B038": ("PRESERVATION", "Project Three immediately after suspension: locked work zone, idle crane booms lowered, weather covers being installed and a two-person inspection team; no pouring concrete or active build.", "R01+R03", "July 1983", "SUSPENDED ≠ TERMINATED"),
    "SAT-B039": ("PRESERVATION", "Protected stored equipment inside an unfinished turbine space, tagged but unreadable crates, desiccation covers and a small inspection crew; no active construction.", "R01+R03+R04", "1983-1994", "preserve optionality"),
    "SAT-B040": ("OPTION_COST", "A preserved machine under a clean protective cover in a vast unfinished hall while a maintenance crew works under one pool of light; show time being purchased, not construction progress.", "R01+R03", "preservation era", "OPTION ALIVE / COST CONTINUES"),
    "SAT-B042": ("REGIONAL_GFX_BASE", "Pacific Northwest power-system landscape at low water with one silent preserved Satsop site at the edge; large clean sky and water areas reserved for demand-forecast overlay.", "R01+R05", "late 1980s-early 1990s", "demand changed / zero output"),
    "SAT-B043": ("PRESERVATION", "Close operational inspection of corrosion protection, sealed penetrations and stored equipment records inside an unfinished plant; three workers only, no cranes or fresh concrete.", "R01+R03+R04", "preservation era", "inspect / protect / evaluate"),
    "SAT-B044": ("OPTION_COST", "Symmetrical corridor of preserved equipment with recurring inspection stations disappearing into depth, each station consuming labor while nothing produces power.", "R01+R03", "preservation era", "spend to keep option alive"),
    "SAT-B046": ("CAPITAL_GFX_BASE", "Reference-matched Project Three concrete mass isolated against a clean warm-paper field, with one empty lower-third scale lane for the verified invested-dollar overlay; no cash, coins or charts generated.", "R01+R02", "1993 valuation", "$2.6B / 1993 dollars"),
    "SAT-B047": ("SITE_IDENTITY", "Preserve the accepted road-level cooling-tower scale frame; use authenticated tower proportions and keep the reactor and turbine shells visibly incomplete.", "R01+R02", "1993-1994", "~500 FT / major buildings existed"),
    "SAT-B048": ("FUTURE_COST", "Foreground unfinished cable trays, open penetrations and missing systems lead toward the apparently complete exterior shell; the absent work dominates over the visible concrete.", "R01+R04", "1993-1994", "VISIBLE CONCRETE ≠ COST TO FINISH"),
    "SAT-B049": ("RISK_HORIZON", "Long empty access road from preserved Project Three toward a distant uncertain horizon, with maintenance barriers and aging equipment in foreground; no active build.", "R01", "1993-1994", "TIME + CAPITAL AT RISK"),
    "SAT-B052": ("RATEPAYER_SCALE", "A small Northwest business after hours with utility invoice and operating ledger on a counter, Satsop image only as a secondary newspaper photograph; no readable invented amounts.", "R05", "1993-1994", "agency decision → monthly rate"),
    "SAT-B054": ("SUNK_COST", "A closed archival vault containing past-project folders behind glass while an open decision table in foreground remains empty, separating money already spent from the next commitment.", "R03", "1994", "PAST SPEND / NEXT DECISION"),
    "SAT-B058": ("COMPARISON_GFX_BASE", "Clean scale comparison plate: one large reference-controlled Project Three mass on the left and five smaller modular combined-cycle blocks on the right, neutral background, no labels or fake site placement.", "R01+R04+R06", "1994 alternatives", "1,240 MW / 240 MW"),
    "SAT-B060": ("LEAD_TIME", "Two parallel construction paths seen from above: long preserved nuclear restart path with many unfinished stages versus a short modular gas path with fewer stages; no text in generated layer.", "R01+R06", "1994 comparison", "5 YEARS / 3 YEARS"),
    "SAT-B061": ("HYDRO_SYSTEM", "Pacific Northwest hydro control context with reservoir, transmission and dispatch room reflections; modular thermal blocks remain secondary and geographically non-specific.", "R05+R06", "1994 system context", "hydro variability / flexible dispatch"),
    "SAT-B062": ("MODULAR_COMPARISON", "Preserve the accepted conceptual composite of one unfinished nuclear commitment versus several small modular combined-cycle units, explicitly non-geographic and free of Satsop site claims.", "R01+R06", "1994 alternatives", "add capacity in increments"),
    "SAT-B066": ("RISK_PAIR", "Balanced tabletop still life: gas-fuel contract and emissions-policy folder on one side, nuclear completion-risk folder on the other, all text blank and equal visual weight.", "R03+R06", "1994", "fuel price / carbon risk"),
    "SAT-B067": ("BALANCED_COMPARISON", "Split composition giving nuclear and combined-cycle advantages and liabilities equal physical space; neither side heroic or catastrophic, no site merger.", "R01+R06", "1994", "risk-free claim rejected"),
    "SAT-B068": ("DECISION_FLEXIBILITY", "A rigid single heavy commitment path beside several smaller movable resource blocks on a utility planning table; human hands can rearrange only the modular side.", "R03+R06", "1994", "FLEXIBILITY"),
    "SAT-B069": ("COST_GFX_BASE", "Project Three silhouette behind one large empty cost bar area on warm-paper background; no digits generated, exact $1.55B overlay added later.", "R01", "1993 dollars", "$1.55B base completion estimate"),
    "SAT-B070": ("COST_GFX_BASE", "Three empty vertical case lanes—low, base, high—beside one shorter combined-cycle lane, using physical model blocks and no generated numbers or labels.", "R06", "1994 analysis", "LOW / BASE / HIGH / CC"),
    "SAT-B071": ("LIFETIME_RISK", "Two alternatives appear similar at the far operating-life horizon, but the Project Three path carries a much larger locked capital block in the foreground.", "R01+R06", "1994 analysis", "lifetime cost comparable ≠ decision equivalent"),
    "SAT-B074": ("QUANT_GFX_BASE", "Clean regional supply-demand plate with one large Project Three block visibly exceeding a lower demand band; no site photograph, no numbers, no labels, ample overlay space.", "R05", "1994 forecast", "1,240 MW / +600 aMW surplus"),
    "SAT-B076": ("ECONOMIC_MISMATCH", "A technically complete power block feeds into a visibly undersized regional demand channel, causing unused capacity to terminate in an empty lane; conceptual, not a real site.", "R05", "1994 forecast", "technical success / economic failure"),
    "SAT-B077": ("TOWER_REVEAL", "Reference-controlled cooling tower fills foreground while the wider regional grid and demand landscape remains visible through an opening, revealing the system hidden by the monument.", "R01+R05", "1994 reflection", "megaproject beyond engineering"),
    "SAT-B078": ("SYSTEM_TEST", "Project Three scale model sits at the center of a circular table surrounded by load forecast, customer and finance stations; all station text reserved for overlay.", "R03+R05", "1994", "CAN SYSTEM USE AND PAY?"),
    "SAT-B079": ("NEED_GFX_BASE", "Reference-matched mostly built Project Three on left and a deliberately sparse regional demand field on right; no cranes, no active construction, clean central overlay lane.", "R01+R05", "1994", "74% BUILT / POWER NOT NEEDED"),
    "SAT-B080": ("CAPITAL_CONCENTRATION", "One huge immovable Project Three commitment block contrasted with several smaller distributed alternatives, while a subtle existing-assets layer remains behind the nuclear side.", "R01+R06", "1994", "capital concentration / real advantages"),
    "SAT-B081": ("EXISTING_ADVANTAGES", "Quiet preserved Project Three exterior with completed access, major shells and permit binders represented as blank physical folders; no operating plant or emissions spectacle.", "R01+R02", "1994", "existing assets / permits / no combustion emissions"),
    "SAT-B083": ("REPOWER_GFX_BASE", "Three-panel neutral engineering plate: preserved Project Three, hypothetical gas repower, and clean-sheet combined-cycle plant; no physical claim that repowering occurred.", "R01+R04+R06", "1994 alternatives", "REPOWER / NEW BUILD"),
    "SAT-B084": ("THIRD_PARTY_OPTION", "Preserve the accepted image of protected unfinished infrastructure as an uncertain third-party option; no map claim and no active nuclear construction.", "R01+R07", "1994", "third party insufficient"),
    "SAT-B086": ("TERMINATION_DECISION", "June 1994 preserved site behind a newly closed administrative gate, with the built structures unchanged and the future path visibly ending; no demolition.", "R01", "June 1994", "TERMINATED / past ≠ future"),
    "SAT-B087": ("MULTIPLE_CLOCKS", "Four physical clocks mounted over permit files, property keys, debt ledgers and redevelopment plans, each showing a different phase; exact dates added only in overlay.", "R03+R07", "1982-2000", "project ends on several clocks"),
    "SAT-B088": ("CHRONOLOGY_GFX_BASE", "Four clean horizontal event stations with distinct physical symbols—Project Five stop, bond default, Project Three suspension, Project Three termination—no generated dates or text.", "R01+R02+R03", "1982-1994", "1982 / 1983 / 1983 / 1994"),
    "SAT-B090": ("MULTIPLE_CLOCKS", "Permit stamp, property key, remediation field kit and debt ledger arranged as four independent workstreams on a neutral table; no readable invented wording.", "R03+R07", "post-termination", "permit / property / remediation / debt"),
    "SAT-B091": ("CONTRACT_AFTERLIFE", "Maintained concrete building outside a window while property keys and long-lived finance folders occupy separate foreground planes, making visible asset and invisible contract coexist.", "R01+R03", "post-termination", "property clock / debt clock"),
    "SAT-B093": ("DEBT_GFX_BASE", "Present-day institutional budget workspace with legacy project folder linked visually to a long receding timeline; no new construction imagery and no generated numbers.", "R01+R07", "present-day debt administration", "legacy budgeting decades later"),
    "SAT-B094": ("ADMINISTRATION", "Contemporary finance office managing legacy obligations: spreadsheets visible only as unreadable shapes, archived project folders, no hard hats, cranes, plant operation or construction.", "R07", "FY2021", "debt administration only"),
    "SAT-B095": ("VISIBLE_INVISIBLE", "Close exterior concrete wall reflected in glass over a table of sealed contracts, pairing durable structure and durable obligation in one restrained composition.", "R01+R03", "post-termination", "CONCRETE / CONTRACTS"),
    "SAT-B096": ("REDEVELOPMENT_INSTITUTIONAL", "1995 civic redevelopment meeting with county, port and public-utility representatives around a reuse site model; no cranes, nuclear construction or operating reactor.", "R02+R07", "1995", "three public partners"),
    "SAT-B098": ("REUSE_MAP_BASE", "Exact plan-matched site plate showing reusable roads, turbine space, grid connection and heavy foundations as isolated zones; reactor-completion path visibly absent, labels reserved for overlay.", "R02+R07", "reuse era", "recover infrastructure, not nuclear investment"),
    "SAT-B102": ("MODERN_REUSE", "Present-day active turbine-building industrial interior with maintained floor, ordinary logistics activity and reusable open volume; no reactor work, cranes, dereliction or nuclear props.", "R01+R07", "present day", "300,000 SQ FT / BUSINESS PARK"),
    "SAT-B103": ("TRAINING", "Preserve the accepted confined-space rescue-training frame: modern PPE, organized exercise team and safe industrial tunnel, clearly training rather than emergency or construction.", "R07", "present day", "confined-space / rescue training"),
    "SAT-B106": ("MODERN_REUSE", "Present-day maintained business-park roadway during a normal workday with occupied industrial buildings, delivery vehicles and controlled access; no tourists, ruins or cranes.", "R01+R07", "present day", "WORKING INDUSTRIAL SITE"),
    "SAT-B107": ("REUSE_RESOLUTION", "Elevated present-day view anchored on active reused buildings and maintained infrastructure, with the cooling tower secondary in the distance; show useful afterlife, not abandoned spectacle.", "R01+R02+R07", "present day", "WHAT REMAINS USEFUL"),
}

def global_guard(era: str) -> str:
    return (
        f"Respect the exact stated era and state ({era}); do not import construction activity, clothing, vehicles or technology from another period. "
        "Historically grounded 16:9 documentary reconstruction with restrained natural light and realistic materials. "
        "The Satsop projects never operated: no fuel, nuclear glow, operating steam, radioactive spectacle or completed plant presented as fact. "
        "Do not render titles, dates, numbers, logos, maps, signs, document text, arrows or labels; exact information is added later as editorial vector graphics. "
        "Keep the lower 15 percent calm for captions. One visual proposition only."
    )

with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
    beats = [row for row in csv.DictReader(handle) if row["asset_class"].startswith("AI_")]

v1 = json.loads((ROOT / "STAGE_6" / "SATSOP_GENERATION_PROMPT_PACK_V1.json").read_text(encoding="utf-8"))
prompt_by_beat = {item["beat_id"]: item["prompt_id"] for item in v1["items"]}
test_jobs = json.loads((ROOT / "STAGE_6" / "TEST20" / "TEST20_JOBS.json").read_text(encoding="utf-8"))
test_tech = json.loads((ROOT / "STAGE_6" / "TEST20" / "TEST20_TECHNICAL_QC.json").read_text(encoding="utf-8"))
second_jobs = json.loads((ROOT / "STAGE_6" / "TEST20_V2" / "TEST20_V2_JOBS.json").read_text(encoding="utf-8"))
second_tech = json.loads((ROOT / "STAGE_6" / "TEST20_V2" / "TEST20_V2_TECHNICAL_QC.json").read_text(encoding="utf-8"))
job_by_prompt = {item["prompt_id"]: item for item in test_jobs + second_jobs}
tech_by_prompt = {item["prompt_id"]: item for item in test_tech + second_tech}

assert len(beats) == len(PLANS) == 68
assert {row["beat_id"] for row in beats} == set(PLANS)

items = []
for row in beats:
    prompt_id = prompt_by_beat[row["beat_id"]]
    grammar, proposition, references, era, overlay = PLANS[row["beat_id"]]
    locked = TEST_GRADES.get(prompt_id) == "PASS" or SECOND_TEST_GRADES.get(prompt_id) == "PASS"
    prompt = f"VISUAL PROPOSITION: {proposition} ERA/STATE: {era}. {global_guard(era)}"
    old_prompt = next(item["prompt"] for item in v1["items"] if item["prompt_id"] == prompt_id)
    assert prompt != old_prompt
    item = {
        "prompt_id": prompt_id,
        "beat_id": row["beat_id"],
        "start": row["start"],
        "end": row["end"],
        "duration_seconds": float(row["duration_seconds"]),
        "asset_class": row["asset_class"],
        "prompt_grammar": grammar,
        "narration": row["narration"],
        "visual_proposition": proposition,
        "era_state": era,
        "required_reference_packages": references.split("+"),
        "reference_gate": "LOCKED_PASS_REUSE" if locked else "BLOCKED_UNTIL_REAL_MEDIA_IDS_ATTACHED",
        "overlay_plan": overlay,
        **MODEL,
        "cost_if_generated_credits": 0.0 if locked else 0.5,
        "queue_status": "LOCKED_PASS_REUSE" if locked else "REWRITTEN_NOT_AUTHORIZED",
        "test_grade_v1": TEST_GRADES.get(prompt_id, "NOT_TESTED"),
        "test_grade_v2": SECOND_TEST_GRADES.get(prompt_id, "NOT_TESTED"),
        "prompt": prompt,
    }
    if locked:
        item["locked_asset"] = {
            "job_id": job_by_prompt[prompt_id]["job_id"],
            "filename": tech_by_prompt[prompt_id]["filename"],
            "sha256": tech_by_prompt[prompt_id]["sha256"],
        }
    items.append(item)

assert len({item["prompt"] for item in items}) == 68
assert sum(item["queue_status"] == "LOCKED_PASS_REUSE" for item in items) == 13
assert sum(item["queue_status"] == "REWRITTEN_NOT_AUTHORIZED" for item in items) == 55
assert sum(item["cost_if_generated_credits"] for item in items) == 27.5

payload = {
    "status": "V2 TESTED — 13 LOCKED PASS / 55 REQUIRE REFERENCES AND NEW APPROVAL",
    "model_defaults": MODEL,
    "locked_pass_count": 13,
    "rewritten_queue_count": 55,
    "maximum_remaining_cost_credits": 27.5,
    "generation_authorized": False,
    "items": items,
}
(OUT / "SATSOP_GENERATION_PROMPT_PACK_V2.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

fields = ["prompt_id", "beat_id", "start", "end", "duration_seconds", "asset_class", "prompt_grammar", "required_reference_packages", "reference_gate", "overlay_plan", "model", "quality", "resolution", "aspect_ratio", "cost_if_generated_credits", "queue_status", "test_grade_v1", "test_grade_v2", "prompt"]
with (OUT / "SATSOP_GENERATION_PROMPT_PACK_V2.csv").open("w", newline="", encoding="utf-8-sig") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for item in items:
        flat = dict(item)
        flat["required_reference_packages"] = "+".join(item["required_reference_packages"])
        writer.writerow({field: flat[field] for field in fields})

lines = [
    "# SATSOP — GENERATION PROMPT PACK V2", "",
    "Status: **SECOND TEST COMPLETE — 13 LOCKED PASS / 55 PENDING REFERENCES / NO FURTHER GENERATION AUTHORIZED**", "",
    "V2 replaces the V1 prompt system. Every non-passing beat has a new visual proposition, era/state control, prompt grammar, reference gate, and overlay plan. Reference package names are requirements; a job remains blocked until real Higgsfield media IDs are attached.", "",
    "- model: GPT Image 2 / low / 1k / 16:9", "- locked accepted images: 13", "- rewritten pending images: 55",
    "- maximum cost if all 55 were later approved: 27.50 credits", "- current authorization: 0.00 credits", "",
]
for item in items:
    lines += [
        f"## {item['prompt_id']} / {item['beat_id']} — {item['queue_status']}", "",
        f"- Grammar: `{item['prompt_grammar']}`", f"- References: `{' + '.join(item['required_reference_packages'])}`",
        f"- Reference gate: `{item['reference_gate']}`", f"- Era/state: {item['era_state']}",
        f"- Overlay plan: {item['overlay_plan']}", f"- Narration: {item['narration']}", "", "### Prompt", "", item["prompt"], "",
    ]
(OUT / "SATSOP_GENERATION_PROMPT_PACK_V2.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

print(json.dumps({"total": 68, "locked_pass": 13, "rewritten": 55, "remaining_max_cost": 27.5}, indent=2))
