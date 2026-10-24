# Project Pluto VIDEO006 — R6 maximum-video source bank QC

## Result

**PASS for technical integrity and timeline construction.** R6 expands the editor bank to **122 unique video clips** with **1,817.020 seconds (30:17.020)** of usable motion. Every motion file passed a fresh SHA256 check and full `ffmpeg -v error -xerror` decode. No duplicate motion hashes, black intervals, missing media, timeline gaps, or local-clip overruns remain.

The locked Arthur narration remains unchanged at **18:41.600**. `VOICE_SYNCED_VISUAL_MAP_R6_MAX_VIDEO.csv` contains **261 edit rows**, **200 unique assets**, all **30 semantic beats**, and all **8 chapters**, ending exactly at 1121.600 seconds. It assigns **122 unique video assets** and 428.737 seconds of source-motion screen time; the remaining time uses historical photographs, engineering figures and official pages with restrained 2D motion.

## Motion bank

| Group | Clips | Usable duration | Status |
|---|---:|---:|---|
| Direct Project Pluto 1963 research film | 49 | 932.500 s | 49/49 hash + decode PASS; no black intervals |
| Previously selected Atlas/Minuteman/B-52 context | 20 | 270.000 s | 20/20 hash + decode PASS |
| Promoted X-15/Fort Belvoir reserve | 20 | 220.520 s | 20/20 hash + decode PASS; SC004 black tail removed |
| Boeing Wichita engineering context, F024 | 18 | 270.000 s | source SHA verified; 18/18 hash + decode PASS |
| Army Ordnance engineering context, F018 | 15 | 124.000 s | source SHA verified; 15/15 hash + decode PASS |

The earlier V2 direct-film package used only 737.375 seconds from the R5 selection. R6 restores every meaningful R5 range and reaches 932.500 seconds. The omitted 0.500 seconds are the detected black tail at the end of `SLAM-25B`.

## Editorial review

- Six aggregate pages were inspected for all 49 direct Project Pluto clips.
- The complete F024 source was screened; only manufacturing, engineering, computing and aerodynamic-laboratory material was retained. Generic flight padding was excluded.
- The complete F018 source was screened; only missile hardware, ranges, laboratories and industrial infrastructure were retained. Talking-head sections were removed from the selected cuts.
- All 20 previously reserved X-15 and Fort Belvoir clips were rechecked and promoted. They remain comparison material from different programs.
- F060 `Space Age Railroad` was reviewed through its contact sheets and left out. Its 1969 Holloman rail-test imagery creates a high risk of implying Nevada or Project Pluto activity.
- The separate X-15 batch-3 release was not downloaded: 14 of 16 ranges overlap the existing F020 bank, and the two unique pressure-suit ranges add little to this script.

## Timeline correction

V2 stored original-film IN/OUT values beside paths that already pointed to cut clip files. That could be misread by an editor as local clip time and cause an invalid source seek. R6 fixes the schema:

- `local_clip_in_sec` and `local_clip_out_sec` are the values to use against the supplied MP4.
- `original_source_in_sec` and `original_source_out_sec` preserve provenance against the full historical source.

All 261 rows were validated for continuity and all motion rows were checked against the physical file duration.

## Provenance and rights gates

No blanket legal clearance is claimed. Direct LASV-N1 material remains `HOLD_THIRD_PARTY_MIRROR_ITEM_REVIEW_REQUIRED`. Context sources retain per-shot or item-specific HOLD statuses. F024 and F018 are Commons derivatives with explicit AI-upscale warnings; they may provide period context but cannot be described as original film scans. Every other-program motion row has an explicit `NOT PROJECT PLUTO` screen label.

No generated video was used. The three optional explanatory graphics from V2 remain the only generation candidates.

## Primary R6 files

- `VOICE_SYNCED_VISUAL_MAP_R6_MAX_VIDEO.csv`
- `DIRECT_PLUTO_MOTION_R6_MAX_MANIFEST.csv`
- `CONTEXT_MOTION_PROMOTED_R6_MANIFEST.csv`
- `F024_CONTEXT_MOTION_R6_MANIFEST.csv`
- `F018_CONTEXT_MOTION_R6_MANIFEST.csv`
- `ADDITIONAL_VIDEO_SOURCE_AUDIT_R6_2026-10-23.csv`
- `EDITOR_BANK_R6_TECH_AUDIT.json`

