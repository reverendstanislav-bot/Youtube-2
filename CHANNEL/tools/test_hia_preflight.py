#!/usr/bin/env python3
"""Regression tests for read-only Glomar gate; no video or paid jobs."""
import csv
import json
import tempfile
import unittest
from pathlib import Path

from hia_preflight import run


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        p = self.root / "GLOMAR_EXPLORER"
        q = p / "RECHECK_R3"
        q.mkdir(parents=True)
        (p / "PROJECT_STATE.json").write_text(json.dumps({
            "status": "EDIT_PREP_REJECTED_AFTER_R3_RECHECK",
            "script_lock": "HOLD_OWNER_REVIEW",
            "current_visual_timeline": "RECHECK_R3/CORRECTED_TIMELINE_NOT_EDIT_READY.csv",
            "new_moving_sources_acquired": 0
        }))
        (q / "AUDIT_RESULT.json").write_text(json.dumps({
            "editorial_readiness": "REJECT_R2_AS_READY_FOR_ASSEMBLY",
            "rights": "HOLD_NOT_CLEARED"
        }))
        with (q / "STAGE_READINESS.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, ["stage", "status", "evidence", "next_required"])
            w.writeheader()
            w.writerow({"stage": "archive", "status": "HOLD", "next_required": "Acquire moving footage"})
        self.csvpath = q / "CORRECTED_TIMELINE_NOT_EDIT_READY.csv"
        self.write_shots([
            {"shot_id": "SH001", "start_seconds": "0", "end_seconds": "3", "duration_seconds": "3", "asset_id": "A", "visual_type": "PHOTO", "story_ready": "False"},
            {"shot_id": "SH002", "start_seconds": "3", "end_seconds": "6", "duration_seconds": "3", "asset_id": "A", "visual_type": "PHOTO", "story_ready": "False"}])

    def write_shots(self, items):
        with self.csvpath.open("w", newline="") as f:
            w = csv.DictWriter(f, ["shot_id", "start_seconds", "end_seconds",
                                  "duration_seconds", "asset_id", "visual_type", "story_ready"])
            w.writeheader()
            w.writerows(items)

    def test_audit_truthfully_reports_hold_without_failing_integrity(self):
        result = run(self.root, gate="audit")
        self.assertEqual(result["result"], "HOLD")
        self.assertEqual(result["stats"]["shots"], 2)
        self.assertFalse(any(x["level"] == "ERROR" for x in result["findings"]))

    def test_edit_ready_blocks_holds(self):
        result = run(self.root, gate="edit-ready")
        self.assertEqual(result["result"], "FAIL")
        self.assertIn("EDIT_READY_BLOCKED", [x["code"] for x in result["findings"]])

    def test_gap_is_structural_failure(self):
        text = self.csvpath.read_text().replace("SH002,3,6,3", "SH002,4,7,3")
        self.csvpath.write_text(text)
        result = run(self.root, gate="audit")
        self.assertEqual(result["result"], "FAIL")
        self.assertIn("TIMELINE_GAP_OR_OVERLAP", [x["code"] for x in result["findings"]])

    def test_false_ready_is_failure(self):
        text = self.csvpath.read_text().replace("SH002,3,6,3,A,PHOTO,False", "SH002,3,6,3,A,PHOTO,True")
        self.csvpath.write_text(text)
        result = run(self.root, gate="audit")
        self.assertEqual(result["result"], "FAIL")
        self.assertIn("FALSE_STORY_READY", [x["code"] for x in result["findings"]])

    def test_missing_state_fails_closed(self):
        (self.root / "GLOMAR_EXPLORER/PROJECT_STATE.json").unlink()
        self.assertEqual(run(self.root)["result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
