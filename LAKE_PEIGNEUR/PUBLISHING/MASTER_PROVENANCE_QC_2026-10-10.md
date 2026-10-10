# LAKE PEIGNEUR — FINAL MASTER / PROVENANCE QC

Updated: 2026-10-10  
Status: **LOCAL MASTER QC PASS / READY FOR UNLISTED YOUTUBE TEST**

## Exact supplied final master

Original supplied filename:
`LAKE PEIGNEUR - ГОТОВОЕ ВИДЕО.mp4`

SHA256:
`3436c9d7b9fd27caa97c6fc2c95aa2322e5bec1d8a69a8575722d52bd81e5b3d`

File size:
**174,986,220 bytes**

Container:
**MP4 / isom**

Runtime:
**00:16:28.459**

### Video

- codec: H.264 / AVC
- profile: High
- resolution: 1920×1080
- progressive
- frame rate: 25/1
- frames: 24,711
- pixel format: yuvj420p
- video bitrate: ~1.093 Mb/s
- 2 B-frames
- level 4.0

### Audio

- codec: AAC-LC
- 48 kHz
- stereo
- bitrate: ~317 kb/s
- integrated loudness: **-14.57 LUFS**
- true peak: **-3.57 dBTP**
- LRA: **3.10 LU**

## Integrity / decode checks

- whole-file packet/container integrity: **PASS / 0 errors**
- targeted video+audio decode at critical regions: **PASS / 0 errors**
  - opening
  - surface-collapse act
  - canal-reversal act
  - cause/forensics act
  - ending
  - end-screen tail

A full frame-by-frame software decode exceeded the current runtime limit, so it is **not** falsely claimed here. Packet integrity plus targeted decode checks passed.

## Narration / end-screen timing

Detected final long silence:
**00:16:08.470 → 00:16:28.459**
duration: **19.989 sec**

This aligns with the final subtitle track:
last caption ends at **00:16:08.080**.

End screen is therefore approximately 20 seconds and silent.

Transition inspection:
- final story graphic persists through ~16:08.2;
- transition/crossfade begins around ~16:08.5;
- end screen is clean by ~16:09.5;
- no caption remains on the clean end-screen state.

## Visual spot QC

Reviewed representative frames at:
00:00:02, 00:00:12, 00:00:25, 00:00:40, 00:01:04, 00:03:55, 00:05:36, 00:06:10, 00:09:18, 00:10:00, 00:11:02, 00:12:30, 00:13:59, 00:14:44, 00:16:05, 00:16:15, 00:16:27.

Observed:
- 16:9 framing correct;
- captions are white with orange active-word highlight;
- captions remain in the expected lower safe region;
- no opaque black caption slab;
- no duplicate subtitle layer in sampled frames;
- maps / diagrams / generated visuals are legible;
- end screen is present and clean after the short transition.

No sampled visual showed an unresolved Appendix EE historical still being presented as a cleared historical source.

## Provenance

Earlier Stage 8B had conditional Appendix EE imagery.
The later canonical Stage 8C-R3 generation plan explicitly records:
**conditional Appendix EE dependencies in generated prompt pack: 0**.

R4 / R4.1 continued the generated-asset plan.

The supplied final master was visually spot-checked at the major story acts above. No sampled frame contradicted the later zero-conditional-dependency plan.

Status:
**PROVENANCE QC PASS FOR UNLISTED TEST.**

## Quality warning — important

The supplied 1080p master averages only **~1.09 Mb/s video bitrate**.

YouTube's current recommended upload bitrate for 1080p SDR at 24/25/30 fps is **8 Mb/s**.

This does **not** automatically mean the file is unusable: the episode is dominated by still/editorial imagery and sampled frames remain visually clean. But the low source bitrate creates a real risk of extra softness after YouTube performs another encode.

Also, the file reports:
- color matrix: `bt470bg`
- color range: full / `pc`
- transfer: unknown
- primaries: unknown

YouTube recommends BT.709 metadata for SDR uploads.

Therefore:
- do **not** publish Public immediately;
- upload this exact master **Unlisted first**;
- wait for full 1080p processing;
- compare the YouTube stream against the local file, especially fine text, diagrams, water, grain and dark mine scenes;
- inspect Stats for Nerds / codec;
- if the Unlisted transcode is visibly soft, build/test a dedicated higher-resolution upload master before Public.

No claim is made that re-encoding this already-compressed file can restore source detail.

## Pronunciation gate

Existing automated pronunciation QC passed with human-ear spot-check required for:
- Lake Peigneur
- Delcambre

That human-ear check should be done during the Unlisted review.

## Final gate

**READY_FOR_UNLISTED = YES**

**READY_FOR_PUBLIC = NO**

Public blockers:
1. YouTube 1080p transcode quality check.
2. Human-ear check: Peigneur / Delcambre.
3. If the YouTube transcode shows the same "mushy" behavior seen on the old channel, do not publish until the upload-master path is corrected.
