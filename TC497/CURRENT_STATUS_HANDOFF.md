# TC497 — FINAL V9 UPLOAD MASTER READY

## STATUS

Episode: LeTourneau TC-497 Overland Train
Project: Hidden Industrial America / YouTube-2

The user explicitly approved the V9 edit and authorized the finalization chain.

Current status: **FINAL V9 1920x1080 UPLOAD MASTER PASSED FINAL QC.**

## FINAL MASTER

GitHub Actions:
- run: `35431145052`
- workflow: `Build TC497 FINAL V9 1080 Surgical Master`
- artifact: `tc497-final-v9-upload-master-1080-surgical`
- artifact id: `10580753397`
- artifact digest: `sha256:a343124d6db20b9e7bf7a3f1963c9d1d387313b8b3c4f691ee7ae9e12bae61b3`

Master:
- `TC497_FINAL_UPLOAD_MASTER_V9_1920x1080.mp4`
- SHA-256: `e63ac00674e715db62b1fbd879cf83dceb1d30007b7ed9c79431d86081916655`
- size: 202,105,468 bytes
- duration: 1236.533333 s (20:36.533)
- 1920x1080
- 30 fps CFR
- H.264 High
- yuv420p
- exactly 37,096 video frames
- AAC-LC audio

## AUDIO QC

V9 review AAC and final-master AAC are bit-identical:

`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

Measured final audio:
- Integrated loudness: -13.5 LUFS
- Loudness range: 3.7 LU
- True peak: -1.9 dBFS

## PICTURE / SUBTITLE QC

Final QC passed:
- no blackdetect events >= configured threshold;
- 1920x1080 assertion passed;
- 30/1 frame-rate assertion passed;
- 37,096-frame assertion passed;
- sampled subtitle and provenance-label frames were visually checked at multiple points including:
  - cold/opening sections;
  - Electric Wheel corrections;
  - nuclear concept;
  - Yuma V9 replacements;
  - ground-vs-air V9 replacements;
  - historical-account section;
  - survivor/final documentary sentence;
  - V8 cinematic end identity.

No subtitle cutoff, missing replacement-label, black frame, or obvious chunk-boundary discontinuity was found.

## EDIT LINEAGE

V14 cold open remains locked.
FULL_V6 corrected V5 implementation defects.
FULL_V8 redesigned the ending and added the resolving original music cue.
FULL_V9 applied four surgical middle-film visual-family replacements.
The final master was rebuilt from native 1080 picture sources rather than upscaling the 960x540 review.

Only these windows were re-rendered in the surgical 1080 pipeline:
- 208.000–245.700
- 757.933–834.533
- 1019.033–1071.433
- 1181.833–end

Unchanged native-1080 picture sections were stream-copied.

## PUBLICATION STATUS

The video file is **upload-ready for YouTube**.

No direct YouTube publishing connector is currently available in this chat, so publication itself is the remaining external step.

