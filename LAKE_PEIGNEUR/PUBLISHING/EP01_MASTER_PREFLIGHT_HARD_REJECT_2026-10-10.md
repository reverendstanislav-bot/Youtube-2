# HIA EP01 — LAKE PEIGNEUR PHYSICAL PREFLIGHT / HARD REJECT
Date: 2026-10-10
Source: User-uploaded `/mnt/data/LAKE PEIGNEUR - ГОТОВОЕ ВИДЕО.mp4`
State: **NO-GO FOR UNLISTED RELEASE CANDIDATE / NO-GO FOR PUBLIC**

## File identity / technical checks
- Source SHA256 (previously verified): `3436c9d7b9fd27caa97c6fc2c95aa2322e5bec1d8a69a8575722d52bd81e5b3d`
- 174,986,220 bytes; 988.458667 seconds = 16:28.459
- H.264 High; 1920×1080; 25 fps; 24,711 frames; yuvj420p full range
- Video bitrate 1,092,780 b/s (~1.09 Mbps)
- Color matrix `bt470bg`; primaries/transfer not reliably signaled as BT.709
- Audio AAC stereo 48 kHz / 317,375 b/s
- Previous measured audio -14.57 integrated LUFS, peak -3.57 dBTP (from earlier master-QC report)

## What ACTUALLY passed in new run
- **Full software decode of BOTH audio and video streams using FFmpeg: PASS** (exit 0; no errors).
- `blackdetect` full video, >=0.4s: **zero detected black frames/events**.
- `silencedetect` audio, >=2s -45dB: only ~16:08.470 → 16:28.459 (20-sec end card); no long gaps in voiced story detected.
- Frame samples at 00:00, 00:05 ... 01:30 and additional 14 story/key-act frames reviewed via contact sheets.
- Above tests prove stream integrity only; do NOT imply cinematic/editorial release PASS or a frame-by-frame human inspection of all frames.

## CONFIRMED FAILS
P0-1 — **Entire picture has burned-in dialogue subtitles** in white/orange. Violates latest owner NO-SUBTITLES canon for ALL long/Short content.
P0-2 — 16:05 bottom headline and subtitle collision; a symptom of P0-1, NOT a separate "reposition captions" request.
P0-3 — End screen ~16:09–16:28 contains incorrect "PREVIOUS STORY" and dead box despite EP01 being first release of the new channel.
P0-4 — Current 1080p video is ~1.09 Mbps, about 1/7 of YouTube's current 8 Mbps SDR 1080p25 reference. Severe source/transcode softness risk. Blindly changing container bitrate cannot restore missing detail.
P1-1 — **Opening visual density:** 00:00–00:10 shows nearly identical drilling platform frame while exposition progresses. A channel with no returning viewers needs stronger first 5–15 sec visual promise; a controlled cold-open picture edit should be tested from APPROVED source assets (not invented new incident footage).
P1-2 — Several early cuts reuse closely similar hero/drill or cross-section frames (not proven fatal but visually low-variety); check 0–90 sec for stagnation in clean edit.
P1-3 — Long film final provenance-to-binary mapping not independently verified. R4.1 generated-asset plan is *not proof* of which exact third-party visuals actually appear in the export.
P1-4 — Current primary title not owner-approved; canonical thumbnail actual pixels/mobile readability not inspected in this run.
P1-5 — **0/4 real Shorts MP4s exist for EP01 relaunch**. Exact SRT IN/OUT drafts are NOT deliverables; S02–S04 start with context-dependent wording. Must edit standalone no-captions Shorts.
P1-6 — Correct spoken pronunciation of Peigneur / Delcambre not yet human-ear confirmed.
P1-7 — Re-export may move chapters; description and chapters must be final-checked against new binary.

## New clean-master build specification (not proof it was executed)
- Locate actual source edit/timeline, original approved per-beat imagery, original VO/audio; use highest-quality picture path.
- Disable/remove ALL dialogue caption layers, renderers, karaoke effects across whole 16m story and tail.
- Keep genuine editorial headlines, maps, dates and diagrams, without dialogue transcription.
- Replace EP01 end screen with channel-appropriate CTA (for EP01 subscribe-only unless user explicitly approves another relevant available video). No "PREVIOUS STORY", no empty placeholder box.
- Improve 0:00–0:15 visual sequence from existing approved story content; no unsupported old-footage simulation; story hook has to be immediate.
- Export clean picture from high-quality sources with proper 1080p25 SDR BT.709, progressive H.264 High, yuv420p, reasonable source-derived quality in YouTube's recommended ~8 Mbps upload range (not a promise that a fixed bitrate ensures quality), AAC-LC stereo/48 kHz, fast-start.
- Recompute SHA256, full decode, black/silence checks, audio loudness/peak, grain/text/dark-scene spot reviews, 0–90 sec visual check, end-screen check, subtitles ABSENT from entire master.
- Derive 4 truly standalone 9:16 Shorts from clean master, exact narrative cuts and native full-frame crops, no subtitles, 2.4 s approved HIA Shorts tail if applicable; deliver 4 MP4s + hashes + QC.
- Only after internal QC: upload Unlisted, wait full HD, inspect actual transcoded 1080p stream and complete Studio metadata. DO NOT PUBLIC until pass.

## Source constraints
The user-uploaded 1.09 Mbps H.264 is a *captioned compressed distribution copy*. The needed source edit / original uncaptioned approved assets are NOT available in the active working directory or Git's Lake Peigneur picture-release assets. Removal by cropping/blur/overlay or fake inpainting is forbidden.

## Verified platform guidance
YouTube upload guidance: https://support.google.com/youtube/answer/1722171?hl=en
YouTube thumbnail/title guidance: https://support.google.com/youtube/answer/12340300?hl=en
YouTube synthetic-content disclosure: https://support.google.com/youtube/answer/14328491?hl=en
YouTube end screens: https://support.google.com/youtube/answer/6388789

## Exact current readiness
Full A/V decode: PASS
Black/silence event checks: PASS with expected 20 s silent tail
No subtitles: FAIL
First-episode end screen: FAIL
Upload-master image quality: HOLD/NEEDS SOURCE REBUILD
Opening first-15-sec visual engagement: NEEDS SOURCE RE-EDIT TEST
Rights/provenance verified for binary: NOT YET
Title/thumbnail owner-lock: OPEN
Four no-caption Shorts: 0/4
Studio Unlisted transcode: NOT PERFORMED
**READY FOR RELEASE: NO**
