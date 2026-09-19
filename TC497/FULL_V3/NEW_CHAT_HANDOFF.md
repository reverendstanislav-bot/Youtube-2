# TC497 FULL_V3 — NEW CHAT HANDOFF

Current state: **FULL_V3 retention/directorial review cut is rendered and passed QA.**

Primary build source:
- `TC497/FULL_V3/full_v3_build.py`
- `TC497/FULL_V3/make_overlay_v3_ass.py`
- `TC497/FULL_V3/README.md`
- `TC497/FULL_V3/FULL_V3_QC.md`

Workflow:
- `.github/workflows/build_tc497_full_v3.yml`

Accepted QA:
- orange edge blocks: 0
- max consecutive full TC-497 shots: 2
- AR-SNO: 1 use after cold open
- AR-A01: 1 use after cold open
- standalone graphics: 0
- generic split screens: 0
- median shot duration: 6.705 s
- 170 shots after cold open

Next action: user reviews the FULL_V3 MP4. Patch only timecoded remaining defects into FULL_V4. Do not rebuild the whole film unless requested.

After approval, render 1920x1080 upload master and perform final subtitle/audio/upload QC.
