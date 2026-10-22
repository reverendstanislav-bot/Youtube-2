# Project Pluto Video 006 — R4 physically recovered and corrected video source bank

**Date:** 2026-10-22. **Supersedes R3's editorial source selection, not R3's history.** This R4 is not a finished movie or rights clearance.

## Confirmed binary acquisition

- The original GitHub Actions run [39782104767](https://github.com/reverendstanislav-bot/Youtube-2/actions/runs/39782104767) artifact 12427911346 was downloaded and its video was physically extracted.
- USAF 38912, LASV-N1 Progress Report (1963), 100,689,792 bytes, source SHA256 `3d9305615472a3ac7a18c50b1d7a3649d20d34f1e1aab93439f535650191114e`.
- The source file is actually MPEG-TS mislabeled .mp4. Independently stream-copy remuxed real H.264/AAC MP4, duration 27:38.333, 92,111,526 bytes, SHA256 `f0ffe68e0395738d191f53132b70d412b98b8d44236496f9db5fe58eedbd16e3` (matches prior remux).
- Rebuilt a NEW physical R4 source bank by re-cutting from this source with FFmpeg; do **not** claim these MP4s are byte-identical to missing R3 ZIP.

## R4 exact media facts

- **30 independent MP4**, **876 seconds = 14:36**.
- **25 primary 1963 LASV-N1 program-related moving-image scenes**: **767 sec = 12:47**.
- **5 supporting slow/model/graphic clips**: **109 sec = 1:49**, restricted use.
- Each R4 MP4: 1280x720, 24fps, H.264, **audio absent**, exact expected frame count and duration, checked individual SHA256. **30/30 entire MP4 streams decoded by FFmpeg without error**. ZIP CRC passed.
- FINAL R4 ZIP is **144,619,493 bytes**, SHA256 `9547f857a4a2ae56f82445b6f382d7d75cbf0a6e930eaf78cdaa6e58813b0521`.
- Complete per-file hashes/source IN/OUT in [LASVN1_R4_VERIFIED_VIDEO_SOURCE_MANIFEST_2026-10-22.csv](LASVN1_R4_VERIFIED_VIDEO_SOURCE_MANIFEST_2026-10-22.csv), with binaries accessible in the producing conversation sandbox only. **R4 ZIP is NOT uploaded to GitHub Release. Do not fabricate a GitHub download link.**

## Rechecked editorial defects and correction

Using original frame-strips for all 29 predecessor cuts and one-second contact sheets for flagged segments:

1. **SLAM-07** R3 28sec -> R4 **27sec**. Excluded final 1sec printed run-number slate. Source 570–597.
2. **SLAM-26** R3 46sec -> **SLAM-26A 1530–1543 (13sec)** and **SLAM-26B 1551–1570 (19sec)**. Excluded unrelated city street at ~1570+, cut low-motion padding and kept original instrumentation/site/technical sequence; chronological source order preserved.
3. **SLAM-27B** R3 8sec -> R4 **7sec**, source 1613–1620. Removed final near-black transition.
4. All other 26 predecessor selections preserved at same source IN/OUT, but freshly encoded source-derived R4 files. No synthetic video/paid generation.

## Gate verdict

| QC gate | Result |
|---|---|
| Source original physically acquired and hash matched | PASS |
| R4 binary file hashes, frame counts, decode and ZIP CRC | PASS 30/30 |
| R4 source footage is 1963 USAF LASV-N1 progress film | PASS (with dating restriction) |
| Original-film-derived rough shot selection | PASS, **only preselection** |
| 1964 Tory II-C actual hot-run motion | HOLD; 0 confirmed sec |
| Narrative coverage all eight chapters / actual locked voice | HOLD |
| Independent original official copy, third-party elements, image copyright | RIGHTS HOLD |
| Publishable 16–22min final film | NOT BUILT |
| GitHub release delivery of this R4 binary ZIP | HOLD, not uploaded |

This remains overwhelmingly footage for Chapter 2 and Chapter 5. Distinct events of May 1964, program cancellation, and the aftermath cannot be falsely depicted using this 1963 report. Do not claim zero-risk YouTube Content ID.

Official rights guidance: https://www.archives.gov/research/motion-pictures/permissions ; official DOE AEC-film leads: https://www.energy.gov/lm/atomic-energy-commission-films-available-online .
