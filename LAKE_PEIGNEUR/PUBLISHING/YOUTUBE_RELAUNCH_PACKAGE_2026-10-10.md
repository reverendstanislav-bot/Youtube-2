# LAKE PEIGNEUR — YOUTUBE RELAUNCH UPLOAD PACKAGE

Updated: 2026-10-10  
Status: **WORKING / TITLE REOPENED / NOT READY FOR UNLISTED QC**

## Launch role

**Episode 01 on the new Hidden Industrial America channel.**

## Title status

**NOT LOCKED.** Previous title `How a Salt Mine Swallowed an Entire Louisiana Lake` is **REJECTED / RETRACTED** after the expanded competitor audit.

See: `RELAUNCH_COMPETITOR_TITLE_AUDIT_V2_2026-10-10.md`

Reserve A:
**The Day a Louisiana Lake Fell Into a Salt Mine**

Reserve B:
**How an Entire Louisiana Lake Vanished Underground**

## Final primary thumbnail

Use:
`LAKE_PEIGNEUR/THUMBNAIL/VIDEO005_LAKE_PEIGNEUR_THUMBNAIL_FINAL.png`

Headline:
**THE LAKE**  
**DISAPPEARED**

Dimensions: **1672×941**

Locked SHA256:
`4c96862126f5821684a0efdfa10e934cdfd6bd8d0e4836873ce50c31f0ab43d2`

Decision:
**KEEP EXISTING THUMBNAIL. NO NEW PAID GENERATION BEFORE LAUNCH.**

## Description

Use:
`LAKE_PEIGNEUR/PUBLISHING/YOUTUBE_DESCRIPTION_RELAUNCH.txt`

## Chapters

00:00 The Two Warnings  
01:04 Two Industries, One Salt Dome  
02:52 The Connection  
03:55 Fifty-Two People Below the Lake  
05:36 Then the Surface Moved  
06:50 Why the Failure Could Grow  
07:59 The Lake Becomes the Engine  
09:06 The Canal Ran Backward  
10:11 The Number That Matters Most  
11:02 What Actually Caused It?  
12:51 Settlements and Aftermath  
13:59 The Geology Was Still Valuable  
14:44 The Map You Couldn't See

## Upload metadata

- Language: **English (United States)**
- Audience: **No, it's not made for kids**
- Category: **Education**
- Playlist: **Hidden Industrial America**
- Captions: `LAKE_PEIGNEUR/PUBLISHING/LAKE_PEIGNEUR_ENGLISH_CC.srt`
- Initial visibility: **Unlisted**
- End screen for first release: **Subscribe only** until Episode 02 is public; then update Episode 01 to point to Episode 02.
- Do not publish until all pre-public gates below are complete.

Suggested tags:
- Lake Peigneur
- Lake Peigneur disaster
- salt mine disaster
- Louisiana history
- industrial disaster
- engineering failure
- Jefferson Island
- Hidden Industrial America

## Cold-open decision

**KEEP CURRENT MASTER.**

The final SRT shows:
- dual warning setup by 00:10.5;
- impossible water-in-salt-mine condition by ~00:20;
- 52-person human stakes by ~00:25;
- major disaster promises by ~00:39;
- everyone-survived reversal at ~00:40;
- deeper story thesis by ~01:03.

No audience-retention data exists for this episode, so a speculative re-edit is not justified.

## Pre-public gates

### P0 — actual master identity
The final Codex master filename and SHA256 are not mirrored in Git.
Before upload:
- identify the exact local final binary;
- run ffprobe;
- calculate SHA256;
- record filename / size / duration / video codec / bitrate / audio codec;
- mirror the metadata into Git.

### P1 — provenance spot audit
Historical Stage 8 records marked selected MSHA Appendix EE photographs conditional because item-level rights were unresolved.
Before Public:
- confirm the final master either replaced these frames, or has documented clearance;
- do not assume inclusion in a federal report automatically made each photograph public domain.

### P2 — human pronunciation
Human-ear spot check:
- Lake Peigneur;
- Delcambre Canal.

Automated QC was pass-with-human-check, not final human approval.

### P3 — YouTube transcode
Upload Unlisted and wait for full HD processing.
Check:
- 1080p playback;
- Stats for Nerds if available;
- dark-detail/grain retention;
- text/map legibility;
- audio;
- captions;
- end-screen geometry.

If YouTube's 1080p transcode is materially soft, then evaluate a 1440p upload-master path. Do not create one blindly.

### P4 — thumbnail phone check
Open the exact locked PNG at small/mobile display size.
Verify:
- "THE LAKE DISAPPEARED" reads instantly;
- drilling platform is still legible as scale;
- lake-to-mine relationship reads without zooming in.

## Go / no-go

**UPLOAD UNLISTED: NO-GO until title/thumbnail pairing is owner-approved and the exact master is located.**  
**PUBLISH PUBLIC: NO-GO until P0–P4 pass.**
