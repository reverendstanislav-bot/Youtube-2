# HIA VIDEO006 PROJECT PLUTO — CODEX PUBLIC-ONLY NO-JUNK ACQUISITION HANDOFF
Prepared: 2026-10-22.
Authoritative queue: `ARCHIVE/CODEX_PUBLIC_ONLY_MINIMAL_SOURCE_QUEUE_2026-10-22.csv`.
**Do not begin by searching random stock or expanding into unrelated archive movies.**

## Critical gates from live main
- Episode has **Stage 02 working 8-chapter outline only**, not owner-locked Stage 03 full screenplay.
- **No verified final Harrison/Arthur/Alexey/other narration WAV or timed transcript for THIS Pluto episode in `PROJECT_PLUTO` GitHub.** Don't borrow audio from another HIA video. SEARCH accessible project media/release files. If audio exists outside repository, accept path as user-provided input; never fake it or invent voice timestamps.
- Current R5 bank **34 true 1963 LASV-N1 MP4, 15:33** (29 primary 13:44 + 5 slow/support 1:49), generated in prior ChatGPT conversation, **not a GitHub release**. If local R5 ZIP is provided, verify SHA256 `897cddf56a8299f7ca995cf5a94cca19d965bcc0cdca764e70ddf81272572b66`. If not, recover **original** from GitHub Actions; do not pretend a new recut is byte-identical to R5.
- Missing genuine filmed May 1964 Tory II-C reactor hot tests = **0 confirmed sec**.
- Rights on third-party copy / embedded elements = HOLD. Period US government origin may support US public domain, but cannot categorically clear unverified digitizations or other-program clips.
- All acquired source films must be labelled REAL_1963_PLUTO / REAL_DIFFERENT_PROGRAM_CONTEXT / DOCUMENT / AFTER-THE-FACT_SITE_PHOTO. No image/video generation, no external credit spends, no archive inquiries/emails/API-key requests/purchases.

## Start here — no duplicate downloads
1. `git pull`, inspect `PROJECT_PLUTO/CURRENT_STATUS_HANDOFF.md`, `DEVELOPMENT/ANGLE_AND_HOOKS_V1.md`, and `ARCHIVE/BEAT_VISUAL_MAP_V1.csv`. Search for `PROJECT_PLUTO` audio files/WAV/MP3 and timed VO transcript; absent => `AUDIO_TIMING_HOLD`, no fictional timings.
2. If R5 ZIP has been provided by the user, import as immutable and verify hash above. Else: use authenticated GitHub CLI to download existing **public-repository GitHub Actions** artifact:
   `gh run download 39782104767 -R reverendstanislav-bot/Youtube-2 -n LASVN1_Primary_1963_Research_Mirror_Rights_PENDING -D PROJECT_PLUTO/RAW_USAF38912`
   This contains historical film `USAF38912_LASVN1_1963.mp4` (100,689,792 B SHA256 `3d9305615472a3ac7a18c50b1d7a3649d20d34f1e1aab93439f535650191114e`). Despite .mp4 name original stream is MPEG-TS. If needed remux with `ffmpeg -i original -map 0:v:0 -map 0:a? -c copy -movflags +faststart clean.mp4` and check probe; no need to re-encode source.
3. Retrieve SMALL **already published authenticated direct Project Pluto document/image set** (58,440,612B ZIP) and technical report DOC-01 (13,180,638 B) from queue, SHA256 verify; do NOT separately fetch 723MB photo pack, 24MB duplicate figures or 69MB DOC-02 until a narrative beat demonstrates genuine need. 58MB bank includes 13 historic Pluto photos + 26 authentic engineering figures + 9 brief other-program comparisons, as published. They are NOT 9 direct Tory tests.
4. The existing real contextual footage release **F015 Hound Dog (284MB)** is only for chapter 3's bomber / cruise-missile systems comparison. **F013 Minuteman (159MB)** is only for chapters 3 / 7's strategic ICBM alternative. These already exist on GitHub Releases; download only if target segment absent from the 58MB bank or stronger action is required for actual story. **F020 X-15 (363MB)** optional ONLY for an explicit aerodynamic/analog lab comparison if LASV-N1 does not already show that (usually skip).
5. DOE officially indexes four publicly watchable historical films at https://www.energy.gov/lm/atomic-energy-commission-films-available-online (Project Rover 1963 NARA 88229, EBR-II Fuel Cycle NARA 88381, EBR-I Core Disassembly NARA 88380, ML-1 NARA 88191). Their YouTube mirrors are linked in queue. These are **strictly other nuclear programs, not Project Pluto**. On GitHub runner `yt-dlp` was already blocked by public YouTube anti-bot check 0/4 (run 39839095490). Do NOT pretend watch URLs are direct MP4 downloads. Only acquire if a public no-login binary is legally/technically reachable; no bypass/private cookies. Skip if blocked; do not count runtime.
6. Public same-era contemporary film scans can have embedded private copyrighted clips. Document item-specific rights and source producer, preserve link attribution, review Content ID risk. **Rights HOLD** is permitted; user wants not to risk strikes. Never set ZERO_RISK/PUBLISH_PASS without adequate rights facts.

## Exact chapter-level editorial visual intent (NO invented audio clock)
Ch 1 — 1964 successful Tory II-C ground-test claim then cancellation: actual Tory II-C authenticated photograph; DOC-01 page evidence. **NO actual moving hot test film available**.
Ch 2 — nuclear RAMJET vs unbuilt SLAM: 1963 LASV-N1 29 primary R5 clips (aerodynamic SLAM models/wind tunnel, `SLAM-02,04,05,06,07,08`). Authentic DOC-02 figures already extracted in primary editor bank. Mark proposed missile graphics as concepts, not historical flying footage.
Ch 3 — Cold War requirements and alternate weapons: limit to F015 `SC035` B52 src **690–697 s** if speaking of bomber/air-launched cruise missile; F013 `SC027` Minuteman stage **275–283 s** if solid-fuel ICBM; do not use launches as Pluto flight.
Ch 4 — Nevada actual site and Tory II-A (1961): authenticated Pluto site contemporary engineering documents + later HAER site photos visibly labeled retrospective, not Nevada footage of unrelated Area25 Rover. Avoid scenic generic desert.
Ch 5 — engineering hard problem: most R5 direct 1963 controls, ceramics, test/radiation-hardened electronics; clip IDs `SLAM-11A,12,12B,13,14,15,15B,16,17,18,19A,19B,20,21,22B,23,24,25,25B,26A,26B,27A,27B` as appropriate to verbal claims. Secondary R5 support bin use sparingly. Only OPTIONAL DOE Rover/EBR-I/EBR-II for explicitly named different-program comparisons; do not use fuel fabrication footage as literal Tory fuel fabrication.
Ch 6 — May 1964 Tory II-C hot run: original DOC-01 test data, true Tory engine photo, original report controls and technical figures. **No literal 1964 Tory operating motion**; no Rover/Atlas/X15 test pretending to be Tory.
Ch 7 — July 1964 cancellation and strategic alternatives: report + exact decision source; F013 `SC029` **487–493 s** and `SC032` **777–785 s** only when relevant to ICBM deployment and strategic context.
Ch 8 — legacy/site: official historic/retrospective HAER site photos and period project records; use minimal stills, no unrelated ruined factory or generic reactor.

## Hard clip / file QC for Codex
- Create `SOURCE_DOWNLOAD_REPORT.csv` with URL, final filepath, bytes, SHA256, codec, dimensions, FPS, final status; **only files that physically exist and hash PASS count**.
- For each newly acquired original, contact-sheet sample and IN/OUT shortlist (action >=5 seconds and can be 15–30 sec when continuously useful). Cut only relevant visible machinery/technicians, not animation/title card/blank/road/stills/repeated image.
- Export candidate true clips as silent original-resolution horizontal frames, preserve native quality, original source IN/OUT and full-decoding FFmpeg PASS. Do not manufacture 1080p historical masters. Final 1080p/25fps is for output edit, not source claims.
- Set `PUBLICATION_RIGHTS` explicitly PASS/HOLD/REJECT per item; no unsourced blanket PD.
- Generate `VOICE_SYNCED_VISUAL_MAP.csv` **ONLY WHEN actual locked WAV, script and transcript exist**, with columns `audio_start,audio_end,script_line_id,claim,clip_id,source_in,source_out,screen_role,rights_status`. Otherwise create `PROVISIONAL_CHAPTER_VISUAL_MAP.csv` without bogus audio times and record `AUDIO_TIMING_HOLD`.
- User wants real motion predominant, not still-photo slideshow; no black caption bars; HIA NO dialogue subtitles. No generated video or paid jobs.

## Acceptance
Deliver a real downloadable, tightly scoped `FINAL_VIDEO_SOURCE_BANK` from verified originals + per-shot rights and semantic QC, not just a plan. **Do not label COMPLETE/PASS merely because links are listed or clips downloaded.** Do not create a new master or claim exact film timeline before script/voice lock. Record discrepancies and update current handoff only with facts.
