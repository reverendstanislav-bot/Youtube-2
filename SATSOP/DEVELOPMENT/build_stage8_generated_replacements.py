from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAT = ROOT / "SATSOP"
OUT = SAT / "STAGE_8_GENERATED_REPLACEMENTS"

CONCEPTS = {
"SAT-B007": "A wide, grounded Pacific Northwest planning-room scene: two separate scale-model construction sites sit far apart on one long table, one surrounded by dry eastern Washington terrain references and the other by wet coastal forest references; a financial adviser stands between them studying a closed funding portfolio, no wall map and no labels.",
"SAT-B009": "A 1982 municipal bond closing room after activity has stopped: dense stacks of blank bond certificates, ledger binders and adding machines fill the foreground while an unfinished industrial construction photograph sits soft and secondary in the distance.",
"SAT-B010": "An overwhelmed project-estimating office in 1982: an enormous wall of stacked blank cost binders and unopened contractor boxes dwarfs a much smaller original planning folder on a desk, with exhausted estimators reviewing the scale of the increase.",
"SAT-B013": "A monumental mid-century Pacific Northwest hydroelectric powerhouse interior with turbines, penstocks and operators at analog controls, emphasizing that the region's electrical system was built around federal hydropower.",
"SAT-B014": "A late-1960s regional utility planning conference: engineers and public-power officials gather around a large blank physical relief model of rivers, cities and future demand corridors, with hydro infrastructure models visibly insufficient for the expanding built landscape.",
"SAT-B018": "A restrained 1984 commissioning scene at the completed Hanford nuclear plant: workers in period safety gear stand beside a functioning turbine hall control boundary while four distant unfinished project models remain covered on a planning table, no steam spectacle.",
"SAT-B020": "A close documentary still of a utility executive signing a thick long-term payment contract at a plain institutional desk, the unfinished plant visible through a window behind the document; every page is blank and unreadable.",
"SAT-B022": "A small public utility billing office after construction stopped: ratepayer envelopes and payment trays continue moving across a counter while a framed photograph of an unfinished plant hangs in the background, making the continuing obligation tangible.",
"SAT-B028": "A Bonneville-era public power finance office: hydroelectric dispatch photographs, wholesale billing folders and a preserved nuclear-project model share one worktable, showing project costs flowing through a federal regional power system without using a diagram.",
"SAT-B030": "An institutional wholesale billing department with rows of public-utility account folders passing through credit trays toward one large preserved-project file; the composition gives most of the physical desk space to the public side and keeps all paper blank.",
"SAT-B033": "A giant unfinished cooling tower fills the background while, in sharp foreground, anonymous utility finance officers examine a heavy sealed capital-risk case that the structure itself cannot reveal.",
"SAT-B034": "A physically accurate industrial model-room view showing the separate major systems required for a large pressurized-water power station: unfinished containment-area model, turbine hall model, cooling works, transmission yard and support buildings arranged as distinct physical components, no labels.",
"SAT-B036": "A cutaway-like but fully physical training exhibit photographed in a 1970s engineering hall: four separate scale models show a heat source vessel, steam piping, turbine generator and cooling-water return loop in a clear left-to-right sequence, no arrows, labels or readable text.",
"SAT-B045": "A 1994 decision table: a carefully maintained model of the mostly built Project Three sits behind glass, while the foreground holds an unopened new-investment case and a closed preservation ledger, showing that past preservation does not justify the next commitment.",
"SAT-B050": "A formal late-1993 public-power boardroom after two separate meetings: two rows of empty chairs face a central evidence table with four blank analysis folders and one preserved-project model, no identifiable people or readable documents.",
"SAT-B051": "Four senior utility analysts occupy four separate stations around a single project model, each examining a different blank evidence package: competitiveness, completion, need and risk, composed as one serious decision process rather than an infographic.",
"SAT-B055": "A utility customer-choice scene in the early 1990s: industrial customers compare several competing energy proposals at a table while the costly preserved nuclear project remains visible through the window, isolated from the new alternatives.",
"SAT-B057": "A household and small-business billing counter where a thick legacy-project cost file physically weighs down a stack of current rate envelopes; the cooling towers appear only as a small distant photograph.",
"SAT-B059": "A utility resource-planning warehouse containing one enormous fixed nuclear plant scale model beside several smaller modular combined-cycle equipment models, with planners measuring how each fits the system; no numeric labels.",
"SAT-B063": "A hydroelectric dispatch center during changing river conditions: operators coordinate flexible gas-generation controls beside live analog water-flow instruments, with generation units responding at different scales, no screens with readable data.",
"SAT-B064": "A quiet combined-cycle plant at partial dispatch: modular turbine equipment rests while fuel delivery and operating crews are visibly scaled back, conveying costs that can be avoided when the plant is not producing.",
"SAT-B065": "A preserved unfinished nuclear facility during a shutdown period: security, maintenance, inspections and protected equipment continue across the site despite no power production, making unavoidable fixed costs visible.",
"SAT-B069": "A 1993 project-estimating room dominated by a vast unfinished construction model and heavy new-capital cases waiting beside it; one analyst studies the remaining commitment rather than the money already spent.",
"SAT-B072": "A risk committee compares two physical investment paths on a long table: one path uses a very large locked steel capital case leading to the preserved nuclear project, the other several smaller modular equipment cases leading to a compact gas plant.",
"SAT-B073": "An early-termination exercise in a utility planning room: the nuclear route leaves behind two large unrecoverable equipment cases while the modular alternative leaves one smaller case, shown through physical props rather than charts.",
"SAT-B074": "A regional grid planning room where an oversized nuclear plant model overwhelms the available customer-load blocks and hydro-system model, leaving a substantial group of power blocks with nowhere to go.",
"SAT-B075": "A wholesale power sales office with surplus-generation folders stacked unsold beside a large preserved-project cost case; even the most optimistic sales desk remains visibly unable to clear the accumulated obligation.",
"SAT-B079": "A mostly completed industrial complex model occupies nearly the entire planning floor while the actual regional demand is represented by a sparse group of customer contracts on one small desk, emphasizing the mismatch without numbers.",
"SAT-B082": "A sober 1994 risk-review archive: separate blank folders for construction uncertainty, aging upgrades, operations, maintenance, waste, decommissioning, regulation and public response surround the preserved project model.",
"SAT-B083": "An engineering evaluation bay compares repowering the preserved nuclear site with building a clean new combined-cycle plant on an empty industrial parcel; both options are shown as realistic physical models under equal neutral light.",
"SAT-B085": "A May 1994 federal public-power decision room after the final determination: the preserved Project Three model is being covered and the next-investment case is closed, with empty board chairs and blank official folders.",
"SAT-B089": "A late-1990s regulatory records room: the Project Three construction-permit folder is removed from an active-file shelf and placed into a closed archive box while an unfinished cooling tower photograph remains in the background.",
"SAT-B097": "A fiscal-year-2000 property transfer scene at the industrial site: keys, facility drawings with blank title blocks and asset inventory binders pass across a table from utility representatives to local development officials.",
"SAT-B098": "A present-day adaptive-reuse transition at the former nuclear site: existing heavy industrial buildings, roads, substations and utility corridors support active non-nuclear tenants while the unfinished cooling tower remains distant and inactive.",
"SAT-B099": "A present-day ground-level view through an active industrial park showing paved heavy-haul roads, occupied large buildings, electrical infrastructure, water-service structures and transmission access in one coherent real environment.",
}

FIX_IDS = {"SAT-GEN022", "SAT-GEN043", "SAT-GEN046", "SAT-GEN050", "SAT-GEN053", "SAT-GEN064"}


def main() -> None:
    timeline = json.loads((SAT / "REMOTION_V1/public/timeline.json").read_text(encoding="utf-8"))["beats"]
    items = []
    for beat in timeline:
        manual = beat["kind"] in {"gfx", "document"} or beat.get("promptId") in FIX_IDS
        if not manual:
            continue
        beat_id = beat["beat"]
        concept = CONCEPTS[beat_id]
        prompt = (
            f"SUBJECT AND COMPOSITION: {concept} "
            "Create one photorealistic 16:9 documentary still with a clear foreground, middle ground and background, realistic scale, restrained natural or institutional light, and a calm lower 18 percent for burned English subtitles. "
            "HISTORICAL AND FACTUAL BOUNDARY: Match the era stated in the subject. Treat the scene as an interpretive documentary reconstruction, with anonymous non-identifiable adults and plausible period materials. Do not claim exact geography unless the subject explicitly describes the present Satsop site. "
            "ABSOLUTE EXCLUSIONS: no words, letters, dates, numbers, logos, captions, title cards, maps, arrows, charts, graphs, diagrams, split screens, UI panels, infographic blocks, readable paper, nuclear glow, disaster imagery, operating Satsop reactor, fuel, smoke, dramatic steam, cinematic spectacle, painterly illustration or 3D infographic style."
        )
        items.append({
            "index": len(items) + 1,
            "replacement_id": f"SAT-RPL-{len(items)+1:03d}",
            "beat_id": beat_id,
            "start": beat["start"], "end": beat["end"],
            "replaces_kind": beat["kind"],
            "narration": beat["narration"],
            "model": "gpt_image_2", "aspect_ratio": "16:9",
            "cost_credits": 0.5, "prompt": prompt,
            "status": "PROMPT_READY_NOT_SUBMITTED",
        })
    assert len(items) == 35 and set(CONCEPTS) == {x["beat_id"] for x in items}
    OUT.mkdir(parents=True, exist_ok=True)
    package = {
        "status": "PROMPTS_READY_NOT_SUBMITTED",
        "count": len(items), "unit_cost_credits": 0.5,
        "maximum_cost_credits": round(sum(x["cost_credits"] for x in items), 2),
        "ai_reconstruction_badge": "REMOVED_FROM_REMOTION_SOURCE",
        "items": items,
    }
    (OUT / "SATSOP_35_GENERATED_REPLACEMENTS.json").write_text(json.dumps(package, indent=2, ensure_ascii=False), encoding="utf-8")
    with (OUT / "SATSOP_35_GENERATED_REPLACEMENTS.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(items[0]))
        w.writeheader(); w.writerows(items)
    lines = [
        "# SATSOP — 35 generated visual replacements", "",
        "Status: **PROMPTS READY — NOT SUBMITTED**", "",
        "These prompts replace every hand-built editorial GFX, Remotion document card and deterministic Stage 6 GFX used in the current rough cut.", "",
        f"Count: **{len(items)}**  ", "Unit cost: **0.50 credits**  ", "Maximum batch cost: **17.50 credits**", "",
    ]
    for x in items:
        lines += [f"## {x['replacement_id']} — {x['beat_id']}", "", f"**Narration:** {x['narration']}", "", f"**Prompt:** {x['prompt']}", ""]
    (OUT / "SATSOP_35_GENERATED_REPLACEMENTS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"count": len(items), "maximum_cost_credits": 17.5, "output": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
