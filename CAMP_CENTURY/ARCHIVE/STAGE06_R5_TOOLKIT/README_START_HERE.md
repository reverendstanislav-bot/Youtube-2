# Camp Century VIDEO007 — Stage06 Codex FULL HANDOFF (R5)

**Goal:** REAL Camp Century historical moving-film clips, 5–20 seconds of meaningful continuous physical action, with true original IN/OUT, licensing receipts, no duplicates and coverage reporting for all eight locked V4 chapters. **No slideshow, no other bases, no invented visuals.**

## Quick start — Codex on a workstation WITH network access

1. Clone/open `reverendstanislav-bot/Youtube-2` repository, branch `main`. Read `SCRIPT_V4_LOCK.md` and read the referenced official Stage05 lock directly from GitHub.
2. Extract this ZIP somewhere local. Install system `ffmpeg` and `ffprobe`, Python 3.10+, and Python requirements with `python -m pip install -r requirements.txt`. Do not buy any voice, clips, stock or generation credits.
3. On Unix run `bash tools/run_workflow.sh /path/to/REAL_FILM_ARCHIVE` (initializes files, attempts to download F01B/F02 from Internet Archive metadata and builds source QC reports). On Windows use `python tools/download_ia_originals.py --root C:\CAMP_CENTURY_ARCHIVE`; then `python tools/stage06_real_footage.py init --root C:\CAMP_CENTURY_ARCHIVE`, `audit --full-decode`, and `sheets`. If Archive.org errors, record `DOWNLOAD_HOLD`; don't misstate a successful download.
4. Obtain F01 official 1963 film from USACE ContentDM (item says original filename 35.mp4, exact CDN path MUST be verified) and F03 separate 1964 PM2A removal from DVIDS if legitimate login allows. Save as `masters/F01.mp4` and `masters/F03.mp4`. IA originals go to `F01B.mpeg` and `F02.mpeg` automatically. For TV543/520/781 authenticated Army origin original reels use `F04`, `F05`, `F06` with true file extension.
5. Audit full native decoding and compare film. Analyze contact sheets and **actually watch** every candidate 5–20sec full-motion excerpt. Only REAL site or that exact operation's supply cargo is eligible. Mixed Camp Tuto, Site I/II, Thule, unrelated Arctic or missile footage is not.
6. Create a nonempty **real rights receipt file** under `rights_receipts` per used source. Copy `manifests/approved_ranges.csv` into archive working root. Fill only physically verified scene IN/OUT, script beat id, actual site class, rights filename, verified_by and `APPROVED`. Blank means NOT reviewed, not automatically approved. Do not claim source timecodes just from online scene descriptions.
7. Run: `python tools/stage06_real_footage.py cut --root /path/to/REAL_FILM_ARCHIVE`, then `duplicates`, review matched film frames and note duplicates; create `final_review.csv` with approvals/rejections and run `finalize`. The tool hashes exported clips; source must have **FULL_DECODE_PASS** and matching SHA256, or extraction refuses.
8. `report` outputs per-chapter actual unique seconds, separating `DIRECT_CAMP_CENTURY` and `SAME_PROJECT_SUPPLY_CHAIN`. Compare to the 32 V4 beats in the original repo. Chapters 05 (unbuilt missile network), 06 (creep) and 08 (core) may have genuine moving-video gaps. Never invent operational Iceworm film.
9. Commit **metadata only** to GitHub under `CAMP_CENTURY/ARCHIVE/`: acquired-film SHA256 records; actual frame-verified source cut list; confirmed duplicate list; **real 8-chapter unique-second report** and item-specific license receipt log. Upload raw original films and real MP4 excerpts into editing storage, **not ordinary Git**. Store a manifest with exact path and source SHA to recover binaries.
10. GO only if sufficient genuine unique footage demonstrated by actual scene records and relevant V4 coverage. Otherwise honest `HOLD`; don't start paid voice without explicit producer approval.

## Nonnegotiable stop rules

- **Do NOT purchase** voice, footage, music, licenses or credits.
- **Do NOT generate** new videos, fake base scenes, paid AI imagery, or unrelated stock B-roll.
- Original federal government films are generally U.S. public-domain, but **third-party inserts / restored re-edits / music** need independent checks; avoid monetized reusage of CBS, CriticalPast or Periscope licensable scan without permission.
- Never reidentify Camp Tuto / Site II / Thule as Camp Century. Distinguish transport of this *specific* camp's materials from shots inside the base.
- No HIA speech subtitles, SRT/VTT or burned text.
- Preserve genuine historic frame ratio, grain and interlace: final project may be 1920×1080/25fps; do not claim original film native 1080p.
- Audio VO V4 is LOCKED but remains **not generated**.

## Included

`tools/stage06_real_footage.py`: real-video audit, contact sheets, segment cuts, duplicate suggestions and manual final approval.
`tools/download_ia_originals.py`: IA API identifies real original MPEG file and writes actual receipt, resumable download and SHA.
`tools/run_workflow.sh`: first-phase local runner; pauses for human shot screening.
`manifests/`: actual source list, 32 spoken-beat coverage targets, 8 chapter baseline, blank permitted-source shot approvals and final reviews.
`rights/`: rights receipt template.
`records/`: detailed status that no real film is packaged.

**Current archive status:** physical original video acquisition HOLD. This ZIP contains preparation and tested technical tooling, **not real Camp Century footage**.
