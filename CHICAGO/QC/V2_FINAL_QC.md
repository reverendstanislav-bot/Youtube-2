# Chicago V2 — FINAL QC

## Verdict

**TECHNICAL UPLOAD CANDIDATE: PASS**

**CHANNEL-STYLE / VISIBLE-CAPTIONS FINAL: NOT YET APPROVED**

The encoded V2 MP4 is technically healthy and YouTube-compatible, but the final QC confirmed that it does **not** contain a burned/visible subtitle layer. The delivered English captions are a separate sidecar SRT.

## Media

- File: `HIA_CHICAGO_V2.mp4`
- SHA-256: `f05d600780111e7ebdc2ac6aac29fcf1cb76704e13b4a14d355cbfc713c896e2`
- Size: 575,515,224 bytes
- Duration: 1290.720 s / 21:30.720
- Resolution: 1920x1080
- Frame rate: 25 fps
- Frames: 32,268
- Video: H.264 High, yuv420p, BT.709, progressive
- Audio: AAC LC stereo, 48 kHz
- Full decode: PASS
- Black interval QC: PASS from prior V2 QC
- Audio loudness: -14.05 LUFS integrated
- True peak: -4.48 dBTP
- V1/V2 audio elementary stream: bit-identical

## Subtitle timing

### Rejected timing source

`03_TIMELINE/subtitles_en.srt`

Independent full-film alignment found major variable/progressive timing error and this file must never be used again.

### Valid timing source

`_V2/final/HIA_CHICAGO_V2.srt`

- 338 cues
- independent word-level timing alignment: PASS
- median start offset: 0.000 s
- whole-film modeled timing change: ~0.005 s
- no overlap
- max two lines / 42 chars
- max ~19.92 cps

## Visible-caption audit

Eight encoded V2 frames were sampled at the midpoint of active V2 SRT cues across the full runtime.

Expected V2 cue text detected in encoded picture: **0 / 8**.

Build-code inspection confirms V2 creates and validates `HIA_CHICAGO_V2.srt` as a **sidecar subtitle file**. The V2 render path contains no subtitle-burn filter for that SRT.

Therefore:

- there is no burned subtitle drift in V2;
- there is also no persistent visible narration subtitle layer in V2;
- labels such as `AI reconstruction`, `HISTORICAL SOURCE`, chapter titles, and other editorial graphics are encoded in picture and are unrelated to the narration SRT.

## Publication interpretation

If the intended YouTube delivery is **video + optional YouTube CC**, V2 is technically ready:
- upload `HIA_CHICAGO_V2.mp4`;
- upload `HIA_CHICAGO_V2.srt` as English captions.

If the channel standard requires **always-visible burned/running captions**, V2 needs one final caption render before it can be called the publication master.

No picture/audio re-edit is required by this QC.

## Evidence

- `CHICAGO/AUDIT/MEDIA_SYNC/PLAN_AUDIT.md`
- `CHICAGO/AUDIT/MEDIA_SYNC/SUBTITLE_ALIGNMENT.md`
- `CHICAGO/AUDIT/V2_FINAL_QC/VISIBLE_CAPTION_QC.md`
- `CHICAGO/AUDIT/V2_FINAL_QC/BUILD_CAPTION_REFERENCES.md`
- `CHICAGO/AUDIT/V2_FINAL_QC/FFPROBE.json`
- `CHICAGO/AUDIT/V2_FINAL_QC/V2_SHA256.txt`
