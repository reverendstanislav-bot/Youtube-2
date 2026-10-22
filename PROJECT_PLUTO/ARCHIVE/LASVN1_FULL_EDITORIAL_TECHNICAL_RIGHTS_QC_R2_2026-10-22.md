# HIA / Project Pluto VIDEO 006 — Independent Full QC R2
Date: 2026-10-22. **Overrides** earlier unqualified descriptions of 17:45 as montage-ready original film.

## Decision
- **Source identity:** USAF film 38912, LASV-N1 Progress Report (1963), actual period program report: source subject **PASS**, however source digitization received from a third-party mirror; do not mistake this title for film of **Tory II-C's May 1964 hot run** or a flight of an SLAM cruise missile.
- **Original 27 MP4 technical QC:** **PASS 27/27**. Each physical file exists. All original first-batch SHA256 values agree with source CSV, 1280x720/24fps H.264, no audio, lengths match, all 27 decode through FFmpeg, ZIP CRC checked, total exactly **1065 seconds = 17:45**. 3 source-to-clip frame samples per original were compared; all clips correspond to original, with one short boundary discrepancy described below.
- **Original 27 MP4 editorial QC:** **REJECT as a clean continuous live-action package.** Original film includes unrelated roadway footage, static presentation animation, black transition frames, repetitive poor-visibility test footage, and a large amount of evidence from early1963 laboratory/electronics phase rather than 1964 reactor testing. Thumbnail spot-checks alone were insufficient.
- **R2 re-edited cut bank:** **29 distinct correctly-encapsulated MP4s, precisely 944 seconds = 15:44**. 20 existing good cuts reused without re-encoding, 9 cutouts corrected; seven source segments assessed for trim/reject. All 29 files tested for duration, true MP4 container, H264, 720p, 24fps, and absence of extra audio: **29/29 TECHNICAL PASS**. ZIP CRC PASS and per-MP4 SHA256 logs. These files are generated in this ChatGPT conversation sandbox (not currently a GitHub Release). Filename `HIA_PROJECT_PLUTO_LASVN1_QC_V2_29_SCENES_15M44S.zip`, size **133,570,226 bytes**; SHA256 `88eed4884252285095ba2d1a33ac65e23bc95f9bda369a78e6f188540a46e4a8`. It also includes decisions CSV and per-clip JSON/CSV source cutlists.
- **Full film container error FIXED:** downloaded file `USAF38912_LASVN1_1963.mp4` looked MP4 by suffix but was actual **MPEG-TS**, with AAC and timed ID3. Verified by ffprobe. Created separate `USAF38912_LASVN1_1963_PROPER_MP4_REMUX.mp4` using stream-copy without repeating video or audio compression. True MP4, 1280x720 H264 24fps, AAC sound, **1658.333s (27:38.333)**, size **92,111,526 bytes**, SHA256 `f0ffe68e0395738d191f53132b70d412b98b8d44236496f9db5fe58eedbd16e3`. Original first binary preserved SHA256 `3d9305615472a3ac7a18c50b1d7a3649d20d34f1e1aab93439f535650191114e`.
- **PTS concern:** Source originally MPEG-TS had discontinuities on some transitions. Source vs original-cut frame crosscheck found one major mismatch exactly at boundary of SLAM-14 ~15:38, while surrounding frames matched. Therefore do not promise subframe-perfect historic source IN/OUT; video-action content is genuine and R2 cuts preserve correct durations, but exact source frame boundary should be aligned in edit if material is selected.

## Decisions for all 27 first-version source segments
- **Keep as is (20):** SLAM-02, 03, 04, 05, 06, 07, 08, 09, 13, 14, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26. These are source-derived genuinely moving laboratory, engineering, model and equipment footage, yet some footage is repetitive and must match the actual narration.
- **Trim (6 source segments):**
  - SLAM-01: model/product turntable; 30s initial reduced to **05:31–05:43** (12s).
  - SLAM-10: poor visibility/repetition; 48s initial reduced to **11:51–12:06** (15s).
  - SLAM-12: original historical animation removed; **13:49–14:09** (20s) retains original lab.
  - SLAM-15: equipment operator separated from demonstrative model; **16:06–16:22** (16s).
  - SLAM-22: remove short black intercut, split into **21:43–21:52 / 21:56–22:04 / 22:08–22:22** (9+8+14s). Ceramic sample demonstration remains period MOVING image, not AI.
  - SLAM-27: exclude company-building establishing shot and last black frames; **26:18–26:45 / 26:53–27:01** (27+8s).
- **Reject as live-action archive:** SLAM-11 12:57–13:27 (30s): generic road footage and illustrative AEC-era diagrams of shielding rather than actual lab work. Historical animation is truthful but may only be used in a separately labelled technical-graphics section, not counted as live period lab footage.
- Earlier claim that SLAM-08 was poor/empty was **incorrect**; detailed review confirmed continuous genuine mechanical component fabrication.
- Source film 1963 cannot show May 1964 Tory II-C engine hot test. Actual May 1964 direct reactor-operation film **0 seconds acquired**.
- The LASV-N1 record is highly relevant, but it disproportionately covers planned Chapter 2 (SLAM design) and Chapter 5 (testing electronics/components). Do not claim 15:44 narratively covers the whole 16–22-minute documentary. Narration/beat timeline has not been locked; chapters 1/4/6/7/8 need direct visuals and reports.

## Law, copyright and claims
- **RIGHTS PASS: NO.** The archival film originated in the U.S. federal USAF series, but copy supplied by third-party mirror; provenance/restoration/upload rights, embedded images, soundtrack and third-party insert copyright not independently cleared. Muted MP4s reduce sound claims but do not ensure picture rights. Do not guarantee absence of YouTube Content ID or strikes.
- NARA advises most of its holdings can be reproduced without restriction, but it will not guarantee public-domain status, commercial-use rights, or clearances for individual items: https://www.archives.gov/research/motion-pictures/order .
- Other AEC films from DOE are not automatically all government-produced: DOE lists *Atomic Energy for Space* (1966) as produced by private Handel Film Corporation in cooperation with AEC/NASA (https://www.energy.gov/lm/atomic-energy-commission-films-available-online). Even if a mirror marks it Public Domain, rights need producer and embedded-frame checks; do not count AEC film status as global rights PASS.
- AEC/NARA context film shortlist was scoped, but originals **except previously collected seven other-program films and this LASV-N1** are not confirmed physically acquired/rights cleared. Do not count candidate film durations as completed project footage.

## Final release gates
**Source historical relation = PASS with restriction; original and corrected MP4 technical = PASS; in-motion semantic review = CONDITIONAL/REQUIRES SCRIPT-SPECIFIC SELECTION; timeline coverage = HOLD; provenance/licensing = HOLD; final film = NOT BUILT.**

New ZIP and normalized MP4 are available as downloadable current-conversation sandbox files, NOT public GitHub Releases. Do not invent a GitHub release URL for them.
