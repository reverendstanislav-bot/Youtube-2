# HIA LAKE PEIGNEUR — CLEAN REBUILD DELIVERY & QC

Date: **2026-10-11**
Status: **CLEAN MASTER CREATED / FOUR SHORTS CREATED / TECHNICAL QC PASS / PUBLICATION GATES STILL OPEN**
Supersedes earlier descriptions saying "no clean source, no actual master, Shorts 0/4".

## Deliverables — actual downloaded files

### New LONG master
`HIA_LAKE_PEIGNEUR_RELAUNCH_CLEAN_MASTER_1920x1080_25FPS.mp4`

Download:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/bc6e1078-eec8-440c-b003-2c0531f8bde7.mp4

- **347,569,085 bytes**
- **SHA256: `4ca4c63890df57a7203fe715076a4b15f36a408f383af51dd2e3463dba0c2de1`**
- 1920×1080, 25 fps, 24,711 video frames
- duration **988.440 seconds (16:28.440)**
- H.264, constrained playback frame layout, **original image sources / CRF17** renders concatenated without second video encode
- measured video bitrate ~2,618,463 bps, audio AAC ~188,781 bps
- color range TV/limited, BT.709 matrix/primaries/transfer explicitly present
- original Arthur MP3 narration with 43ms source alignment correction, AAC-LC 48 kHz stereo final
- **full final audio+video FFmpeg decode: PASS**
- full-video black-frame scan: **no black events >=0.4 seconds** at the selected threshold
- audio silence: **968.471–988.459 seconds ONLY**, 19.988 sec expected silent end screen
- CDN HTTP HEAD checked: **200**, content-length exactly 347,569,085 bytes

### FOUR caption-free Shorts

Download:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/6583ee88-3e0d-4fbd-be52-3b6d89905af6.zip

- ZIP: **18,841,995 bytes**
- ZIP SHA256: `8a22f654be3979ffb91abe18ec756f687324a866be53e761ad44f0bbbeb7a854`
- all 4 files: 1080×1920, 25 fps, H.264 + AAC, no subtitle streams or burned dialogue-caption layer; exact original VO edits, no TTS regeneration
- visual content native portrait crops from original recovered reconstruction PNG, with preapproved HIA vertical endscreen 2.4s
- each complete MP4: FFmpeg decode PASS; ZIP CRC PASS

| ID | Name | Duration | SHA256 |
|---|---|---:|---|
| LP-S01 | 52 People Under a Disappearing Lake | 43.44s | `b55a336a76a99d1cb332b371a670e5146aaae268eeb95ca08de4d41a79b3395a` |
| LP-S02 | The Drilling Platform Vanished | 40.64s | `b92bad83bc3ab61bbf0986d8ff8218e2caecceba495e69480572e82283838c93` |
| LP-S03 | The Canal That Flowed Backward | 44.16s | `681830ae119c5569cd5ccd0dd3bcd0ddbfe6210abe9e448ef632c21b7e95c8ab` |
| LP-S04 | The Lake Peigneur Cause Was Never That Simple | 38.00s | `19f183018d9b1d59dfc80d47531eea5cbaca1b57cc0251983cafaa7148132396` |

### Reproducible source patch and QC

Download:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/9c3437d5-22e3-429b-af30-a612de406dac.zip

- 77,467 bytes
- SHA256: `4a2f3d3f92441f8135c44a0c42eacb8c53aab8c6a5f1a5e6b3640bf257703f22`
- includes changed `index.jsx`, changed `timeline.json`, editor-native repaired `LP-GFX-049` visual, shorts creation source, technical/shot manifests, conditional-visual inventory, instructions, QC sample sheet.

## Source rebuild facts

Codex recovered source GitHub release:
https://github.com/reverendstanislav-bot/Youtube-2/releases/tag/hia-lake-peigneur-source-recovery-20261010

Independent archive verification before rebuild: 3/3 parts SHA/CRC PASS, 483 actual files, final timeline 87 beats / 97 picture slots / 97 physical referenced images.

The new master is NOT an upscale, blur/crop concealment, or subtitle inpainting of the rejected 1.09Mbps captioned MP4.

- All final story picture slots use original high-quality PNGs (many 1344×752) from the recovered 100-entry lock.
- Removed `Caption` component from actual Remotion source and never burnt an ASS/SRT overlay in either long or Shorts.
- Kept independent `Chapter` and `Fact` components. These are editorial graphics, not speech subtitles.
- Improved cold-open visual variety by cutting from drill platform to existing underground/geology image around 6s.
- Applied restrained 0.6% center-origin push-in to reconstruction source images; no horizontal pans.
- Kept editorial transitions.
- Correct first-release HIA 20s Subscribe-only end screen; no "PREVIOUS STORY" and no dead recommendation rectangle.
- Fixed two legacy historical CONDITIONAL visuals without paid generation:
  - `LP-GFX-049`: adjacent duplicate settlement card replaced with new source-grounded editor-native `$32M / SETTLEMENT IS NOT A CAUSE FINDING` editorial graphic.
  - `LP-REC-044`: source with invented mine-closure sign removed from V13 time slot and replaced by previously approved `LP-REC-042` image (second reuse).

## Remaining editorial/publication gates (not falsely marked PASS)

- Historical director QC: **14 CONDITIONAL visual IDs actually used before rebuild**. Two have been replaced (see above); **12 unresolved conditional editorial notes remain**, generally conceptual accuracy, labeling, generic location, or reconstruction specificity. All recovered assets have original provider job provenance, but semantic review of these 12 is still required before final publication approval.
- End-to-end natural-language fact and scene synchronization not independently reviewed frame-by-frame for every 24,711 frames. Technical full decode != semantic QC.
- The final title was never approved by owner; **TITLE OPEN**.
- Canonical thumbnail **THE LAKE / DISAPPEARED** earlier checked against exact SHA256 and mobile scale, but final *pairing* depends on title approval.
- VO human-ear review for pronunciation Peigneur / Delcambre still pending.
- YouTube Unlisted high-definition transcode / actual platform playback / 1080p softness test **not performed**. Clean source+CRF17 is higher fidelity than old source, but no promise of YouTube's codec/transcode behavior.
- Publication settings, final metadata, source credits, and altered/synthetic footage disclosure need Studio review.

**Technical delivery: PASS.**  
**READY_FOR_UNLISTED_QC: YES.**  
**READY_FOR_PUBLIC: NO.**

No Higgsfield/ElevenLabs image, video or TTS generation invoked; 0 generation credits spent.
