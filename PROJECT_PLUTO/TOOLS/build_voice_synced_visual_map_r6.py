#!/usr/bin/env python3
"""Rebuild the locked VIDEO006 visual map with maximum verified motion coverage."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


REPO = Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
SRC = REPO / "PROJECT_PLUTO" / "SOURCE_BANK_V2"
BEATS = REPO / "PROJECT_PLUTO" / "AUDIO" / "AUDIO_LOCK_V2" / "STAGE05_PROJECT_PLUTO_AUDIO_LOCKED_BEATS_V1.csv"
OLD_MAP = SRC / "VOICE_SYNCED_VISUAL_MAP_V2.csv"
OUT = SRC / "VOICE_SYNCED_VISUAL_MAP_R6_MAX_VIDEO.csv"


def read(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def tc(seconds: float) -> str:
    frames = round(seconds * 25)
    hh, rem = divmod(frames, 25 * 3600)
    mm, rem = divmod(rem, 25 * 60)
    ss, ff = divmod(rem, 25)
    return f"{hh:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def main() -> None:
    old = read(OLD_MAP)
    beats = read(BEATS)
    purposes = {}
    plans: dict[str, list[str]] = defaultdict(list)
    assets: dict[str, dict] = {}
    for row in old:
        beat = row["beat_id"]
        purposes[beat] = row["editorial_purpose"]
        aid = row["asset_id"]
        if aid not in plans[beat]:
            plans[beat].append(aid)
        if aid not in assets:
            motion = "MOTION" in row["media_type"]
            duration = None
            if motion and row["source_in_sec"] and row["source_out_sec"]:
                duration = float(row["source_out_sec"]) - float(row["source_in_sec"])
            assets[aid] = {
                "type": row["media_type"], "file": row["file"],
                "duration": duration, "original_in": row["source_in_sec"],
                "original_out": row["source_out_sec"],
                "context": row["historical_context"], "rights": row["rights_status"],
                "label": row["required_screen_label"],
            }

    # Replace each old direct-film selection with every verified R6 part from that parent range.
    r6_by_parent: dict[str, list[str]] = defaultdict(list)
    for row in read(SRC / "DIRECT_PLUTO_MOTION_R6_MAX_MANIFEST.csv"):
        aid = row["clip_id"]
        r6_by_parent[row["parent_r5_clip_id"]].append(aid)
        assets[aid] = {
            "type": "DIRECT_PROJECT_PLUTO_MOTION", "file": row["file"],
            "duration": float(row["duration_sec"]), "original_in": row["source_in_sec"],
            "original_out": row["source_out_sec"], "context": row["historical_context"],
            "rights": row["rights_status"], "label": row["screen_label"],
        }
    for beat, ids in list(plans.items()):
        expanded = []
        for aid in ids:
            expanded.extend(r6_by_parent.get(aid, [aid]))
        plans[beat] = expanded

    # Add only the useful engineering portions of the 1956 Boeing context film.
    for row in read(SRC / "F024_CONTEXT_MOTION_R6_MANIFEST.csv"):
        aid = row["clip_id"]
        assets[aid] = {
            "type": "CONTEXT_MOTION_OTHER_PROGRAM", "file": row["file"],
            "duration": float(row["duration_sec"]), "original_in": row["source_in_sec"],
            "original_out": row["source_out_sec"], "context": row["historical_context"],
            "rights": row["rights_status"], "label": row["screen_label"],
        }
        plans[row["suggested_beat_id"]].append(aid)

    # Promote all twenty previously reserved, already-local context clips after fresh QC.
    for row in read(SRC / "CONTEXT_MOTION_PROMOTED_R6_MANIFEST.csv"):
        aid = row["scene_id"]
        assets[aid] = {
            "type": "CONTEXT_MOTION_OTHER_PROGRAM", "file": row["file"],
            "duration": float(row["duration_sec"]), "original_in": row["source_in_sec"],
            "original_out": row["source_out_sec"], "context": row["historical_context"],
            "rights": row["rights_status"], "label": row["screen_label"],
        }
        plans[row["suggested_beat_id"]].append(aid)

    for row in read(SRC / "F018_CONTEXT_MOTION_R6_MANIFEST.csv"):
        aid = row["clip_id"]
        assets[aid] = {
            "type": "CONTEXT_MOTION_OTHER_PROGRAM", "file": row["file"],
            "duration": float(row["duration_sec"]), "original_in": row["source_in_sec"],
            "original_out": row["source_out_sec"], "context": row["historical_context"],
            "rights": row["rights_status"], "label": row["screen_label"],
        }
        plans[row["suggested_beat_id"]].append(aid)

    rows = []
    scene_no = 0
    for beat in beats:
        beat_id = beat["beat_id"]
        ids = plans[beat_id]
        start, end = float(beat["audio_start_sec"]), float(beat["audio_end_sec"])
        weights = [min(8.0, assets[x]["duration"]) if assets[x]["duration"] else 7.0 for x in ids]
        scale = (end - start) / sum(weights)
        durations = [w * scale for w in weights]
        # A local motion file may never be extended beyond its physical duration.
        excess = 0.0
        flexible = []
        for i, aid in enumerate(ids):
            physical = assets[aid]["duration"]
            if physical is not None and durations[i] > physical:
                excess += durations[i] - physical
                durations[i] = physical
            else:
                flexible.append(i)
        if excess:
            capacity = [i for i in flexible if assets[ids[i]]["duration"] is None or durations[i] < assets[ids[i]]["duration"]]
            while excess > 0.0001 and capacity:
                share = excess / len(capacity)
                next_capacity = []
                spent = 0.0
                for i in capacity:
                    physical = assets[ids[i]]["duration"]
                    room = share if physical is None else min(share, physical - durations[i])
                    durations[i] += room
                    spent += room
                    if physical is None or durations[i] + 0.0001 < physical:
                        next_capacity.append(i)
                excess -= spent
                capacity = next_capacity
        cursor = start
        for i, aid in enumerate(ids):
            a = assets[aid]
            scene_no += 1
            scene_end = end if i == len(ids) - 1 else min(end, cursor + durations[i])
            local_out = "" if a["duration"] is None else f"{scene_end - cursor:.3f}"
            rows.append({
                "scene_id": f"R6-{scene_no:03d}", "beat_id": beat_id, "chapter": beat["chapter"],
                "timeline_in_sec": f"{cursor:.3f}", "timeline_out_sec": f"{scene_end:.3f}",
                "timeline_in_tc_25": tc(cursor), "timeline_out_tc_25": tc(scene_end),
                "asset_id": aid, "media_type": a["type"], "file": a["file"],
                "local_clip_in_sec": "0.000" if a["duration"] is not None else "",
                "local_clip_out_sec": local_out,
                "original_source_in_sec": a["original_in"], "original_source_out_sec": a["original_out"],
                "historical_context": a["context"], "editorial_purpose": purposes[beat_id],
                "rights_status": a["rights"], "required_screen_label": a["label"],
                "script_bit_excerpt": " ".join(beat["spoken_text"].split())[:280],
                "audio_lock_status": beat["audio_status"],
                "motion_treatment": "SOURCE_SPEED_100_PERCENT_CUT_ON_ACTION" if a["duration"] is not None else "SLOW_2D_PUSH_OR_DETAIL_CROP_NO_FAKE_3D",
            })
            cursor = scene_end
    with OUT.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    # Hard validation: exact coverage and no motion overrun.
    assert abs(float(rows[0]["timeline_in_sec"])) < 0.001
    assert abs(float(rows[-1]["timeline_out_sec"]) - 1121.6) < 0.001
    for prev, cur in zip(rows, rows[1:]):
        assert abs(float(prev["timeline_out_sec"]) - float(cur["timeline_in_sec"])) < 0.001
    for row in rows:
        if row["local_clip_out_sec"]:
            assert float(row["local_clip_out_sec"]) <= assets[row["asset_id"]]["duration"] + 0.001
    print(f"wrote {len(rows)} rows; {len(set(r['asset_id'] for r in rows))} unique assets; exact 1121.600 sec")


if __name__ == "__main__":
    main()
