#!/usr/bin/env python3
"""Read-only, dependency-free HIA stage preflight. Never grants owner approval."""
import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def run(root, episode="GLOMAR_EXPLORER", gate="audit"):
    project = root / episode
    findings = []
    stats = {}
    def add(level, code, detail):
        findings.append({"level": level, "code": code, "detail": detail})
    if episode != "GLOMAR_EXPLORER":
        add("ERROR", "UNSUPPORTED_EPISODE", "Only Glomar is wired; no implied pass for other episodes")
        return {"gate": gate, "result": "FAIL", "findings": findings, "stats": stats}
    paths = {
        "state": project / "PROJECT_STATE.json",
        "audit": project / "RECHECK_R3/AUDIT_RESULT.json",
        "stages": project / "RECHECK_R3/STAGE_READINESS.csv",
        "timeline": project / "RECHECK_R3/CORRECTED_TIMELINE_NOT_EDIT_READY.csv",
    }
    for key, p in paths.items():
        if not p.is_file():
            add("ERROR", "MISSING_CURRENT_" + key.upper(), str(p.relative_to(root)))
    if any(f["level"] == "ERROR" for f in findings):
        return {"gate": gate, "result": "FAIL", "findings": findings, "stats": stats}
    try:
        state = json.loads(paths["state"].read_text(encoding="utf-8-sig"))
        audit = json.loads(paths["audit"].read_text(encoding="utf-8-sig"))
        stages = read_csv(paths["stages"])
        shots = read_csv(paths["timeline"])
    except (ValueError, UnicodeError, OSError) as exc:
        add("ERROR", "INPUT_PARSE", str(exc))
        return {"gate": gate, "result": "FAIL", "findings": findings, "stats": stats}

    if not shots:
        add("ERROR", "EMPTY_TIMELINE", "Current map has no rows")
    shot_ids, used = set(), Counter()
    type_seconds = defaultdict(float)
    prev_end = None
    timeline_end = 0.0
    for i, shot in enumerate(shots, 1):
        sid = shot.get("shot_id", "")
        if not sid or sid in shot_ids:
            add("ERROR", "DUPLICATE_OR_MISSING_SHOT", f"row {i}: {sid}")
        shot_ids.add(sid)
        try:
            start = float(shot["start_seconds"])
            end = float(shot["end_seconds"])
            dur = float(shot["duration_seconds"])
            if not all(map(math.isfinite, [start, end, dur])) or start < 0 or end <= start:
                raise ValueError("invalid interval")
            if abs(end - start - dur) > .07:
                add("ERROR", "DURATION_MISMATCH", f"{sid}: {start} to {end} != {dur}")
            if prev_end is not None and abs(start - prev_end) > .08:
                add("ERROR", "TIMELINE_GAP_OR_OVERLAP", f"{sid}: previous end {prev_end}, start {start}")
            prev_end, timeline_end = end, max(timeline_end, end)
            kind = (shot.get("visual_type") or "UNASSIGNED").strip().upper()
            type_seconds[kind] += dur
            asset = (shot.get("asset_id") or "").strip()
            if asset:
                used[asset] += dur
            if shot.get("story_ready", "").strip().lower() in ("true", "yes", "1") and audit.get("editorial_readiness", "").startswith("REJECT"):
                add("ERROR", "FALSE_STORY_READY", f"{sid} marked ready during rejected R3")
        except (KeyError, ValueError, TypeError) as exc:
            add("ERROR", "BAD_SHOT_TIME", f"{sid or i}: {exc}")
    stats["shots"] = len(shots)
    stats["timeline_seconds"] = round(timeline_end, 2)
    stats["visual_seconds_by_type"] = {k: round(v, 2) for k,v in sorted(type_seconds.items())}
    stats["most_reused_assets_seconds"] = [
        {"asset_id": k, "seconds": round(v, 2)} for k,v in used.most_common(5)
    ]
    if used:
        for asset, seconds in used.items():
            if seconds > 60:
                add("HOLD", "HEAVY_REUSE", f"{asset}: {seconds:.2f}s; review actual visual variety")
    if state.get("current_visual_timeline") != "RECHECK_R3/CORRECTED_TIMELINE_NOT_EDIT_READY.csv":
        add("ERROR", "STALE_CURRENT_TIMELINE", str(state.get("current_visual_timeline")))
    status = str(state.get("status", ""))
    if "REJECT" in str(audit.get("editorial_readiness", "")) and "REJECT" not in status:
        add("ERROR", "REJECT_NOT_REFLECTED_IN_STATE", status)
    if state.get("new_moving_sources_acquired", 0) == 0:
        add("HOLD", "NO_NEW_MOVING_ARCHIVE", "No additional real motion source acquired")
    if state.get("script_lock") != "LOCKED" and state.get("script_lock") != "PASS":
        add("HOLD", "SCRIPT_LOCK", str(state.get("script_lock")))
    if audit.get("rights", "").startswith("HOLD"):
        add("HOLD", "RIGHTS", str(audit.get("rights")))
    if audit.get("editorial_readiness", "").startswith("REJECT"):
        add("HOLD", "EDITORIAL", str(audit.get("editorial_readiness")))
    unresolved = []
    for row in stages:
        st = str(row.get("status", "")).strip()
        if st not in ("PASS", "KEEP_ACCEPTED"):
            unresolved.append({"stage": row.get("stage"), "status": st, "next_required": row.get("next_required")})
    stats["unresolved_stages"] = unresolved
    if not stages:
        add("ERROR", "EMPTY_STAGE_REGISTRY", "No stage rows")
    if gate == "edit-ready" and unresolved:
        add("ERROR", "EDIT_READY_BLOCKED", f"{len(unresolved)} unresolved current stages")
    if gate == "edit-ready" and any(f["level"] == "HOLD" for f in findings):
        add("ERROR", "UNRESOLVED_HOLDS", "Stage not ready for edit/release")
    result = "FAIL" if any(f["level"] == "ERROR" for f in findings) else ("HOLD" if any(f["level"] == "HOLD" for f in findings) else "PASS")
    return {"episode": episode, "gate": gate, "result": result, "findings": findings, "stats": stats,
            "disclaimer": "Only structural evidence and declared statuses checked; no semantic AV, authenticity, licensing, or owner approval."}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--episode", default="GLOMAR_EXPLORER")
    ap.add_argument("--gate", choices=("audit", "edit-ready"), default="audit")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = run(args.repo, args.episode, args.gate)
    data = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data + "\n", encoding="utf-8")
    print(data)
    return 2 if result["result"] == "FAIL" else 0

if __name__ == "__main__":
    raise SystemExit(main())
