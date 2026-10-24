#!/usr/bin/env python3
"""Create an audio-locked, provenance-aware visual plan for VIDEO006."""

from __future__ import annotations

import csv
from pathlib import Path


REPO = Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
BANK = Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_V2")
SRC = REPO / "PROJECT_PLUTO" / "SOURCE_BANK_V2"
BEATS = REPO / "PROJECT_PLUTO" / "AUDIO" / "AUDIO_LOCK_V2" / "STAGE05_PROJECT_PLUTO_AUDIO_LOCKED_BEATS_V1.csv"
DOC_PAGES = BANK / "08_EDITOR_READY_OFFICIAL_DOCUMENT_PAGES"


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def tc(seconds: float) -> str:
    frames = round(seconds * 25)
    hh, rem = divmod(frames, 25 * 3600)
    mm, rem = divmod(rem, 25 * 60)
    ss, ff = divmod(rem, 25)
    return f"{hh:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def main() -> None:
    assets: dict[str, dict] = {}
    for r in read_csv(SRC / "DIRECT_PLUTO_MOTION_MANIFEST_V2.csv"):
        assets[r["clip_id"]] = {
            "type": "DIRECT_PROJECT_PLUTO_MOTION", "file": r["file"],
            "source_in": float(r["source_in_sec"]), "duration": float(r["duration_sec"]),
            "context": r["historical_context"], "rights": r["rights_status"],
            "label": r["screen_label"],
        }
    for r in read_csv(SRC / "CONTEXT_MOTION_MANIFEST_V2.csv"):
        assets[r["scene_id"]] = {
            "type": "CONTEXT_MOTION_OTHER_PROGRAM", "file": r["file"],
            "source_in": float(r["source_in_sec"]), "duration": float(r["duration_sec"]),
            "context": r["historical_context"], "rights": r["rights_status"],
            "label": r["screen_label"],
        }
    for r in read_csv(SRC / "HISTORICAL_PHOTO_MANIFEST_V2.csv"):
        assets[r["asset_id"]] = {
            "type": "HISTORICAL_PHOTO", "file": r["editor_proxy"],
            "source_in": None, "duration": None, "context": r["historical_context"],
            "rights": r["rights_status"],
            "label": "AREA 26 — HAER SURVEY AFTER 1968" if r["asset_id"].startswith("HAER") else "ACTUAL TORY HARDWARE",
        }
    for r in read_csv(SRC / "ENGINEERING_FIGURE_MANIFEST_V2.csv"):
        assets[r["asset_id"]] = {
            "type": "ENGINEERING_REPORT_FIGURE", "file": r["file"],
            "source_in": None, "duration": None, "context": r["historical_context"],
            "rights": r["rights_status"], "label": "ORIGINAL ENGINEERING RECORD",
        }
    for r in read_csv(DOC_PAGES / "DOCUMENT_PAGE_MANIFEST.csv"):
        asset_id = Path(r["asset"]).stem
        assets[asset_id] = {
            "type": "OFFICIAL_DOCUMENT_PAGE", "file": str(DOC_PAGES / r["asset"]),
            "source_in": None, "duration": None,
            "context": f"Official publication page {r['pdf_page_index_1based']} from {r['source_pdf']}",
            "rights": "SOURCE_SPECIFIC_REVIEW_RETAIN_ONSCREEN_CITATION",
            "label": "OFFICIAL RECORD",
        }

    AEC67 = "AEC_PRESIDENT_REPORT_1964__PDFPAGE_067"
    CR54 = "CONGRESSIONAL_RECORD_1964_PT13_3_1__PDFPAGE_054"
    CR55 = "CONGRESSIONAL_RECORD_1964_PT13_3_1__PDFPAGE_055"
    CR56 = "CONGRESSIONAL_RECORD_1964_PT13_3_1__PDFPAGE_056"
    NASA221 = "NASA_AERONAUTICS_CHRONOLOGY_1964__PDFPAGE_221"
    NASA254 = "NASA_AERONAUTICS_CHRONOLOGY_1964__PDFPAGE_254"
    NASA325 = "NASA_AERONAUTICS_CHRONOLOGY_1964__PDFPAGE_325"
    AF = [f"AIR_FORCE_MAGAZINE_JULY_1964_PLUTO__PDFPAGE_{n:03d}" for n in range(1, 7)]

    plan: dict[str, tuple[str, list[str]]] = {
        "PLUTO-CH01-B01": ("May 1964 Tory II-C full-power milestone and July termination", ["P002", "DOC-01__P016__TORY_IIC_MAY_1964_TEST_RESULTS", AEC67, "DOC-01__P037__TORY_IIC_OPERATION_DATA", "P001", "P003"]),
        "PLUTO-CH01-B02": ("Separate the tested reactor from the unbuilt flying weapon", ["P001", "P002", "DOC-01__P007__END_OF_PROGRAM_1964_PREFACE", AEC67, "DOC-02__P049__REACTOR_CORE_CROSS_SECTION", "P003"]),
        "PLUTO-CH01-B03": ("Project Pluto thesis: engineering success versus weapon decision", ["P003", "DOC-05__P004__PLUTO_ACTUAL_SITE_HISTORY", "P002"]),

        "PLUTO-CH02-B01": ("Explain reactor-heated airflow and ground-tested engine", ["SLAM-02", "SLAM-04", "SLAM-05", "DOC-02__P049__REACTOR_CORE_CROSS_SECTION", "DOC-02__P051__TORY_DESIGN_SECTION_DETAILS", "DOC-02__P318__REACTOR_ENGINE_ANNOTATED_HARDWARE", "P001"]),
        "PLUTO-CH02-B02": ("Explain SLAM as the proposed vehicle and endurance concept", ["SLAM-01", "SLAM-03", "SLAM-06", "SLAM-09", "DOC-02__P210__FUEL_ASSEMBLY_DIAGRAM", "DOC-02__P219__REACTOR_SPRING_AND_CONSTRUCTION", "P003"]),
        "PLUTO-CH02-B03": ("Show what wind-tunnel and component tests proved and did not prove", ["SLAM-07", "SLAM-08", "DOC-02__P105__REACTOR_GRID_PLATE_PHOTOGRAPHS", "DOC-02__P110__TORY_CORE_HARDWARE_DETAIL", "DOC-02__P222__FUEL_SUPPORT_ASSEMBLY"]),

        "PLUTO-CH03-B01": ("Cold War bomber and airborne missile context", ["SC033", "SC034", "SC035", "SC036", "SC037", "SC038"]),
        "PLUTO-CH03-B02": ("Ballistic missile alternative and operational constraints", ["SC027", "SC028", "SC029", "SC030", "SC031", "SC032"]),
        "PLUTO-CH03-B03": ("Explicitly compare Atlas-era systems with the never-flown SLAM", ["SC019", "SC020", "SC021", "SC022", "SC023", "SC024", "SC025", "SC026"]),

        "PLUTO-CH04-B01": ("Establish the real Area 26 industrial site", [*[f"HAER-4A-{n:02d}" for n in range(1, 8)], "DOC-05__P002__PLUTO_REAL_SITE_GOV_SURVEY", "DOC-05__P004__PLUTO_ACTUAL_SITE_HISTORY"]),
        "PLUTO-CH04-B02": ("Explain the test site as substitute for a moving aircraft", [*[f"HAER-4A-{n:02d}" for n in range(8, 15)], "DOC-01__P073__TORY_TEST_GAS_SAMPLE_SCHEMATIC"]),
        "PLUTO-CH04-B03": ("Show disassembly, protected work areas, and post-test study", [*[f"HAER-4A-{n:02d}" for n in range(15, 22)], "DOC-02__P228__REACTOR_FABRICATION_IN_SHOP_PHOTOS"]),
        "PLUTO-CH04-B04": ("Tory II-A test as a ground demonstration rather than a flight", [*[f"HAER-4A-{n:02d}" for n in range(22, 29)], "P001", "P003", "DOC-01__P118__TORY_REACTOR_TEST_DATA"]),

        "PLUTO-CH05-B01": ("Airflow, heat, and reactor engineering burden", ["SLAM-11A", "SLAM-12", "SLAM-12B", "SLAM-13", "DOC-02__P049__REACTOR_CORE_CROSS_SECTION", "DOC-02__P324__CORE_REACTOR_ASSEMBLY_PHOTOGRAPHS"]),
        "PLUTO-CH05-B02": ("Ceramic fuel elements and material survival", ["SLAM-14", "SLAM-15", "SLAM-15B", "SLAM-16", "SLAM-17", "SLAM-22C", "DOC-02__P135__REACTOR_FUEL_ELEMENT_PHOTOGRAPHS", "DOC-02__P375__FUEL_ROD_COMPONENT_PHOTOS"]),
        "PLUTO-CH05-B03": ("Progression from Tory II-A fundamentals to Tory II-C engine burden", ["SLAM-18", "SLAM-19A", "SLAM-19B", "SLAM-20", "DOC-02__P374__FABRICATED_CORE_PHOTOS", "DOC-04__P041__TORY_CONTROL_ROD_CORE_LAYOUT", "P002"]),
        "PLUTO-CH05-B04": ("1963 film evidence of the real supporting development program", ["SLAM-21", "SLAM-22A", "SLAM-22B", "SLAM-23", "SLAM-24", "SLAM-25", "SLAM-25B"]),
        "PLUTO-CH05-B05": ("Guidance, telemetry, controls, and reliability demands", ["SLAM-26A", "SLAM-26B", "SLAM-27A", "SLAM-27B", "DOC-04__P005__PLUTO_CONTROL_REPORT_COVER", "DOC-04__P050__TORY_NUCLEAR_CONTROL_CIRCUIT", "DOC-04__P052__TORY_TEST_CONTROL_SIGNALS", "DOC-04__P063__ACTUAL_TORY_CONTROL_ACTUATOR", "DOC-04__P064__ACTUAL_TORY_CONTROL_ACTUATOR_PARTS"]),

        "PLUTO-CH06-B01": ("January to March 1964 test chronology", [AEC67, "P002", "DOC-01__P016__TORY_IIC_MAY_1964_TEST_RESULTS", "DOC-01__P037__TORY_IIC_OPERATION_DATA", "HAER-4A-03"]),
        "PLUTO-CH06-B02": ("May 20 full-power result at simulated Mach 2.8 sea-level conditions", ["P002", AEC67, "DOC-01__P016__TORY_IIC_MAY_1964_TEST_RESULTS", "DOC-01__P037__TORY_IIC_OPERATION_DATA", "DOC-01__P118__TORY_REACTOR_TEST_DATA"]),
        "PLUTO-CH06-B03": ("State the missing flight proof without fabricating flight footage", ["P001", "P002", "P003", "DOC-02__P318__REACTOR_ENGINE_ANNOTATED_HARDWARE", "DOC-04__P050__TORY_NUCLEAR_CONTROL_CIRCUIT"]),
        "PLUTO-CH06-B04": ("Use surviving reports and engine photographs as the evidence", [AEC67, "DOC-01__P016__TORY_IIC_MAY_1964_TEST_RESULTS", "P002", "DOC-01__P037__TORY_IIC_OPERATION_DATA"]),

        "PLUTO-CH07-B01": ("July 1 decision and end of the flight-test objective", [AEC67, "DOC-01__P007__END_OF_PROGRAM_1964_PREFACE", CR54, CR55, NASA254]),
        "PLUTO-CH07-B02": ("Congressional funding conflict and demand for a flight-test plan", [CR55, CR56, NASA221, AF[0], AF[1], AF[2]]),
        "PLUTO-CH07-B03": ("Frame later strategic explanations as interpretations", [AF[3], AF[4], AF[5], NASA325, "SC025", "SC027", "SC032"]),
        "PLUTO-CH07-B04": ("Show the scale of systems and infrastructure still required", ["SC022", "SC023", "SC029", "SC030", "SC035", "SC037", "DOC-04__P052__TORY_TEST_CONTROL_SIGNALS"]),
        "PLUTO-CH07-B05": ("Close the distinction: tested reactor, unflown missile", [AEC67, "DOC-01__P007__END_OF_PROGRAM_1964_PREFACE", "P002", "P001"]),

        "PLUTO-CH08-B01": ("Survey what physically survives at Area 26", [*[f"HAER-4A-{n:02d}" for n in range(29, 37)], "DOC-05__P004__PLUTO_ACTUAL_SITE_HISTORY"]),
        "PLUTO-CH08-B02": ("Summarize the demonstrated reactor and engineering record", ["P001", "P002", "P003", "DOC-02__P324__CORE_REACTOR_ASSEMBLY_PHOTOGRAPHS", "DOC-02__P228__REACTOR_FABRICATION_IN_SHOP_PHOTOS", "HAER-4A-31"]),
        "PLUTO-CH08-B03": ("Final image: real engine on the ground, the limit of the project", ["P002", "P001", "P003", "HAER-4A-03"]),
    }

    beats = read_csv(BEATS)
    rows: list[dict] = []
    scene_no = 0
    for beat in beats:
        purpose, ids = plan[beat["beat_id"]]
        start = float(beat["audio_start_sec"])
        end = float(beat["audio_end_sec"])
        weights = []
        for aid in ids:
            a = assets[aid]
            weights.append(min(8.0, a["duration"]) if a["duration"] else 7.0)
        scale = (end - start) / sum(weights)
        durations = [w * scale for w in weights]
        # Cap motion at physical duration, then redistribute any excess to still/document assets.
        excess = 0.0
        still_indices = []
        for i, aid in enumerate(ids):
            a = assets[aid]
            if a["duration"] is not None and durations[i] > a["duration"]:
                excess += durations[i] - a["duration"]
                durations[i] = a["duration"]
            elif a["duration"] is None:
                still_indices.append(i)
        if excess and still_indices:
            for i in still_indices:
                durations[i] += excess / len(still_indices)
        cursor = start
        for idx, aid in enumerate(ids):
            a = assets[aid]
            scene_no += 1
            scene_end = end if idx == len(ids) - 1 else min(end, cursor + durations[idx])
            source_in = a["source_in"]
            source_out = None if source_in is None else source_in + (scene_end - cursor)
            rows.append({
                "scene_id": f"V2-{scene_no:03d}",
                "beat_id": beat["beat_id"],
                "chapter": beat["chapter"],
                "timeline_in_sec": f"{cursor:.3f}",
                "timeline_out_sec": f"{scene_end:.3f}",
                "timeline_in_tc_25": tc(cursor),
                "timeline_out_tc_25": tc(scene_end),
                "asset_id": aid,
                "media_type": a["type"],
                "file": a["file"],
                "source_in_sec": "" if source_in is None else f"{source_in:.3f}",
                "source_out_sec": "" if source_out is None else f"{source_out:.3f}",
                "historical_context": a["context"],
                "editorial_purpose": purpose,
                "rights_status": a["rights"],
                "required_screen_label": a["label"],
                "script_bit_excerpt": " ".join(beat["spoken_text"].split())[:280],
                "audio_lock_status": beat["audio_status"],
                "motion_treatment": "SOURCE_SPEED_100_PERCENT_CUT_ON_ACTION" if "MOTION" in a["type"] else "SLOW_2D_PUSH_OR_DETAIL_CROP_NO_FAKE_3D",
            })
            cursor = scene_end
    write_csv(SRC / "VOICE_SYNCED_VISUAL_MAP_V2.csv", rows)

    gaps = [
        {
            "gap_id": "GEN-01", "beat_id": "PLUTO-CH02-B01", "duration_target_sec": "8-12",
            "need": "Simple explanatory airflow overlay through the documented Tory core cross-section",
            "reason": "No historical motion cleanly explains ramjet compression and reactor heating",
            "generation_limit": "Graphic arrows, labels and heat gradient only; base must remain the real report figure",
            "status": "OPTIONAL_MINIMAL_GENERATION",
        },
        {
            "gap_id": "GEN-02", "beat_id": "PLUTO-CH06-B03", "duration_target_sec": "6-10",
            "need": "Clear tested-reactor versus unbuilt-flight-vehicle comparison",
            "reason": "No actual SLAM flight footage exists",
            "generation_limit": "Diagrammatic silhouette and factual labels only; never present as archival footage",
            "status": "OPTIONAL_MINIMAL_GENERATION",
        },
        {
            "gap_id": "GEN-03", "beat_id": "PLUTO-CH07-B01", "duration_target_sec": "6-8",
            "need": "May 20 to July 1 decision timeline over official documents",
            "reason": "A concise date bridge improves comprehension without replacing source evidence",
            "generation_limit": "Typography and line animation over scanned official pages",
            "status": "OPTIONAL_MINIMAL_GENERATION",
        },
    ]
    write_csv(SRC / "MINIMAL_GENERATION_GAPS_V2.csv", gaps)
    print(f"wrote {len(rows)} visual timeline elements across {len(beats)} audio-locked beats")


if __name__ == "__main__":
    main()
