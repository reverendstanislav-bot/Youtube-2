> **OWNER OVERRIDE / P0 HARD FAIL — 2026-10-10:** The entire uploaded Lake master contains burned-in dialogue subtitles, and ALL HIA long-form and Shorts must contain NO SUBTITLES. The 16:05 caption collision is only a symptom. Do NOT reposition captions. Remove the entire dialogue-caption renderer across the whole original edit and re-render cleanly. Refer to `CHANNEL/NO_SUBTITLES_OWNER_LOCK_2026-10-10.md`.

# LAKE PEIGNEUR — RELAUNCH NO-GO / CORRECTIVE QC

Date: 2026-10-10
State: **NOT READY FOR PUBLICATION; NOT READY FOR UNLISTED AS A RELEASE CANDIDATE**
Supersedes the inaccurate status claims "PACKAGING LOCKED", "LOCAL MASTER QC PASS", and "READY FOR UNLISTED" in earlier October 10 handoffs.

## What is actually verified

Uploaded user file:
`LAKE PEIGNEUR - ГОТОВОЕ ВИДЕО.mp4`
- SHA256 `3436c9d7b9fd27caa97c6fc2c95aa2322e5bec1d8a69a8575722d52bd81e5b3d`
- 174,986,220 bytes
- 1920×1080, 25 fps, H.264 video
- 16:28.459
- ~1.093 Mb/s video bitrate
- `bt470bg` matrix, full range, unspecified primaries/transfer
- AAC stereo 48 kHz
- previously checked: packet/container integrity and spot decode (NOT full visual frame-by-frame QC)

## Newly confirmed render defects

**P0-1 — text/caption collision at 00:16:05 [FAIL]**
- The big editorial headline "INFRASTRUCTURE DOES NOT STOP AT THE SURFACE." occupies the same bottom band as the burned-in white/orange captions.
- This is directly visible in an extracted original-frame still `00-16-05.jpg` from the supplied MP4.
- The old PASS claim ("captions remain in safe region") was wrong.
- Required fix: strip the full caption track at the SOURCE EDIT and rebuild the entire subtitle-free master; verify the entire on-screen duration of that title, not a single frame.

**P0-2 — first-episode end screen is built for a prior video [FAIL]**
- ~16:09 to 16:28 end card includes "PREVIOUS STORY" and a large empty dark rectangular placeholder.
- Lake Peigneur is planned as first relaunch episode, so the reference is inappropriate.
- Required fix: create an approved first-video end-screen layout that matches the new channel's actual end-screen objects (subscribe-only or a meaningful supported follow-up; no dead "previous story" module). Remove/replace stale placeholder geometry, not merely rename the label.

**P0-3 — local upload-master fidelity [HOLD]**
- H.264 ~1.09 Mb/s at 1080p is a strong recompression-quality risk and old Chicago launch had visible YouTube softness.
- Color metadata is not standard BT.709 SDR.
- Rebuild a clean upload master from the highest-quality available edit/project/source, not by blindly re-encoding the already-compressed 1.09 Mb/s MP4 at higher bitrate.
- Then repeat full technical and sampled visual QC.

## Packaging defects

**P1-1 — title not owner-approved [OPEN]**
- Previous agent unilaterally marked "An Entire Lake Drained Into a Salt Mine. 52 Miners Were Inside." LOCKED.
- This title was never approved by owner and uses "52 miners", whereas the project's precisely verified formulation is "52 people underground".
- Reopen title selection, check factual wording and owner approval before packaging lock.

**P1-2 — thumbnail not freshly visually approved in relaunch pairing [OPEN]**
- Canonical Git thumbnail: `LAKE_PEIGNEUR/THUMBNAIL/VIDEO005_LAKE_PEIGNEUR_THUMBNAIL_FINAL.png`.
- Its prior owner-lock remains valid as archived artwork; relaunch visual/mobile legibility and title pairing were not physically reviewed here.
- Need inspect exact canonical binary at 100% and mobile scale, not an unrelated locally generated Lake Peigneur thumbnail. User approval of final relaunch pair is required.

**P1-3 — description/source metadata not publication-verified [OPEN]**
- Description/chapter draft exists, not actual YouTube-studio validation.
- Verify citations/credits/disclosure after final cut is repaired because chapter timings may shift.
- Set true end-screen arrangement for Episode 01.

## Shorts defects

**P0-4 — 4/4 physical Shorts MP4s missing [FAIL]**
- Git currently contains 4 selected cut specs and upload text only, not 4 delivered/reviewed 1080×1920 final MP4s.
- Source binary is now actually available. The old shorts-map claim "render blocked only by missing master" is stale.
- New bottlenecks: cut/edit, screen composition, subtitle-free source/crop, export and visual/audio QC.

**P1-4 — weak standalone starts in draft extracts [OPEN]**
- LP-S02 at 05:36 starts "Above them", which requires prior context.
- LP-S03 at 09:18 starts "Now the lake had fallen", which also requires setup.
- LP-S04 at 11:02 begins "By now, the natural question seems obvious".
- Cuts end at word boundaries per SRT but must be editorially re-evaluated for a cold Shorts audience.
- Do not mark exact IN/OUT approved before checking standalone hooks and visual crop.

## Rights/provenance

**P1-5 — final-export provenance not independently verified [OPEN]**
- Later R4 generated-asset plan records zero dependencies on Appendix EE conditional photos.
- This does not prove the actual MP4 matches the plan; no exact picture asset manifest has been crosschecked against the final master.
- Do an asset/scene-level provenance check before Public. Do not label it PASS merely from plan status.

## Remaining external gate

**P2-1 — YouTube transcode [PENDING]**
- Only after new master edit passes P0/P1 should upload Unlisted, wait for HD processing and inspect sharpness/codec/captions/end screen on the real platform.
- Human-ear pronunciation of Lake Peigneur and Delcambre remains pending.

## Accurate readiness

- MASTER FILE EXISTS: **YES**
- TECHNICAL METADATA/SHA: **VERIFIED**
- CORRECTED FULL MASTER: **NO**
- EDITORIAL/VISUAL QC: **FAIL**
- FINAL TITLE/THUMB PAIR OWNER APPROVED: **NO**
- COMPLETE PUBLISHING METADATA QA: **NO**
- 4 SHORTS MP4s: **0 / 4 VERIFIED DELIVERED**
- PROVENANCE BINARY/MANIFEST VERIFIED: **NO**
- UNLISTED RELEASE-CANDIDATE READY: **NO**
- PUBLIC READY: **NO**

No new paid generations. No "LOCKED/PASS/READY" labels until the corresponding deliverable exists and is verified.
