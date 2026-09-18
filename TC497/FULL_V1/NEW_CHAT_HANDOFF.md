# TC497 FULL V1 — NEW CHAT HANDOFF

Current state: **complete 20:36 full-episode review cut exists and has passed visual/audio QC.**

Start from:
- `TC497/FULL_V1/README.md`
- `TC497/FULL_V1/FULL_REVIEW_QC.md`
- `TC497/FULL_V1/full_build.py`
- `TC497/FULL_V1/index.jsx`

Full review build artifact workflow:
`.github/workflows/build_tc497_full_v1_fast.yml`

The user's next step is to review the full cut and give timecoded corrections.

Do not restart from V14 or rebuild the entire film unless the user asks. Patch only the criticized sections, then create FULL_V2.

After the full cut is approved:
1. Render final 1920x1080 master.
2. Run final subtitle-safe-area QC.
3. Normalize final YouTube audio near -14 LUFS with healthy true-peak headroom.
4. Export upload master plus final checksum/report.
