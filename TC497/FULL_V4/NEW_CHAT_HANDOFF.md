# TC497 FULL_V4 — NEW CHAT HANDOFF

Current state: **FULL_V4 review cut rendered successfully and passed structural, subtitle, source-label and copyright-independent audio QC.**

Primary sources:
- `TC497/FULL_V4/full_v4_build.py`
- `TC497/FULL_V4/make_overlay_v4_ass.py`
- `TC497/FULL_V4/README.md`
- `TC497/FULL_V4/FULL_V4_QC.md`

Workflow:
- `.github/workflows/build_tc497_full_v4.yml`

Accepted QA:
- 644 expected / 644 physical ASS Dialogue lines
- 478 caption phrases / 0 suspicious
- 0 blacklisted legacy uses
- 0 orange/rust edge-block flags
- no still asset >3 uses
- max 1 consecutive full-TC-497 shot
- max 2 identical visual categories
- no modern AR-A04 camera-operator shot
- no whole-TC-497 helicopter-lift implication
- source roles explicit: ARCHIVE / DOCUMENT / RECONSTRUCTION / CONCEPT

Next action: user reviews FULL_V4. If approved, choose whether to keep the original procedural underscore or substitute verified YouTube-safe music, then render 1920x1080 upload master.
