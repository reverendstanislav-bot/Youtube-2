# VIDEO 006 Project Pluto — R3 independent editorial QC
Date: 2026-10-22. Overrides previous R2 unconditional "15:44" framing.

## Actual physical result
- New source bank in current conversation: `HIA_VIDEO006_PLUTO_R3_EDITORIAL_QC_SOURCE_BANK.zip`, exactly **120,954,345 bytes**, SHA256 **8ef7c1c582ac8afa38b17bdc42af519e752a7f77dbebb5bc03b8e3bf2982e8ad**. ZIP CRC/testzip PASS. This file is local conversation download **not a GitHub Release**; do not invent a GitHub download URL.
- `01_PRIMARY_PERIOD_MOTION_QC_PASS`: **24** muted full-frame H.264 1280×720/24fps clips, **783 seconds (13:03)**. Strongly relevant original 1963 USAF LASV-N1/Project Pluto program R&D, with working model/wind tunnel/mechanical tests and electronic/computer research footage. This is **source-selection/editorial subject PASS**, not final line-by-line film continuity PASS.
- `02_SUPPORT_ONLY_GRAPHICS_SLOW_SHOTS`: **5 clips 109 seconds (1:49)**. Slow model or still-heavy sequences; not counted as strong motion coverage. May be used only when voice exactly discusses that original detail.
- Total packaged actual video candidates: **29 MP4, 892 seconds (14:52)**. This is not 14:52 of guaranteed final documentary coverage.
- Previous R2: 29 files, 944 sec (15:44), now superseded as editing bank. Removed/shortened **52 sec** low-value/road/slate/dark/overlong footage.

## Specific corrections, verified on real frames
1. SLAM-07: 45s historical test slate / near-blank section at end; now first **28s**, source 09:30–09:58. Actual wind tunnel equipment and technicians remain.
2. SLAM-16: trimmed first 5s of near-black leader, now source 17:07–17:44, **37s**.
3. SLAM-19: original cut included **unrelated city-road footage** within a radiation electronics chapter; split into **SLAM-19A (19:22–19:44, 22s)** and **SLAM-19B (19:58–20:05, 7s)**. Verified via images and MP4 probe that roadway absent.
4. SLAM-15: removed final unrelated demonstration transition, now **16:06–16:21, 15s**.
5. SLAM-10: rejected, very dark 15s wind-tunnel scene showing little intelligible apparatus.
6. SLAM-01,03,09,22A,22C: moved to limited supporting bin, not falsely counted as dynamic main coverage.
7. During source screening 29 clips sampled at 8 real still frames each (with 5 additional frames on 25/26/27), first 13 strongest cuts previously passed full decode in FFmpeg; all R3 clips pass ffprobe duration/resolution/FPS/H264/audio-free SHA evidence and changed 19A/19B fully decoded. Source PTS had gaps; using frame-count trim for 19A/19B was necessary to preserve exact length and 24fps. No synthetic footage.

## Chapter balance / what remains impossible to PASS
- The **13:03 primary footage** is drawn almost entirely from 1963 *SLAM model/aerodynamics (Chapter 2)* and *radiation hardening, electronic/mechanical R&D (Chapter 5)*. Good evidence for those story beats **if narrated accurately**.
- Authentic **Tory II-C full-power ground-test footage, May 1964**: **0 confirmed seconds**. The 1963 report film is not the 1964 Tory running test. No SLAM ever flew.
- Actual end-of-program/political-decision/archive footage (chapters 1, 4, 6, 7, 8) is not covered by the 13:03. Government period report photos/engineering documents exist, but user wants film-based treatment and minimum stills.
- No owner-approved precise final narration/voice timestamp map in repository yet. Final timeline/coverage pass cannot be truthfully set.

## Copyright / provenance
- Historic USAF origin is supported by historical film catalog **USAF 38912**, but working digital copy obtained from a third-party mirror, not an independently supplied NARA original. Embedded footage/restoration/third-party rights cannot be certified from the copy alone.
- NARA specifically states it cannot certify PD, commercial clearance or freedom from restrictions per item, even for its holdings: https://www.archives.gov/research/motion-pictures/order . 17 USC 105 applies to work originally produced by US federal officers/employees as official duties; it does not magically clear any incorporated externally owned footage or all modern uploads.
- **RIGHTS PASS = HOLD**. YouTube Content ID / copyright-claim/strike risk cannot be guaranteed zero. Muting audio alone does not clear picture rights.
- An original-copy/rightsholder inquiry is prepared separately. It must be sent by a person with email access, and a response/documentation obtained. It has **not** been sent.

## Final decisions
SOURCE_RELATION_TO_PLUTO_1963 = PASS
PHYSICAL_FILE_29_MP4_TECH_QC = PASS
PRIMARY_EDITORIAL_SHOT_SELECTION = PASS (24 scenes; 13:03), **only source rough-cut selection**
SECONDARY_SUPPORT = LIMITED (5 scenes; 1:49)
CONTENT_ACCURACY_1964_TORY_TEST = HOLD (not depicted)
FULL_16_TO_22_MIN_NARRATIVE_COVERAGE = HOLD
PUBLICATION_RIGHTS_AND_STRIKE_RESILIENCE = HOLD
FINAL_HIA_VIDEO006_UPLOAD_MASTER = NOT BUILT

No paid generations, no new footage synthesized, original history clearly classified.
