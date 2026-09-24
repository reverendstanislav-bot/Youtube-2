# HIA Shorts — Youtube-1 Model Proof

Date: 2026-09-24
Status: **OWNER REVIEW — DO NOT BATCH SCALE YET**

## Canon

Active Shorts source of truth:
`CHANNEL/SHORTS_PRODUCTION_CANON.md`

Inherited model:
`reverendstanislav-bot/Youtube-1-/01_CHANNEL/SHORTS_PRODUCTION_LOCK.md`

Rejected HIA system:
- V10 semantic rebuild from stills / per-beat asset substitution;
- Shorts-only editor-native GFX;
- second caption layer;
- Shorts-only metric/title cards.

## Proof

Short:
`CHI-S01`

Source master:
`HIA_CHICAGO_R14_EDITORIAL_RECUT_REVIEW_1920x1080.mp4`

Source range:
`11.800 -> 46.680`

Output:
`CHI-S01_YOUTUBE1_MODEL_PROOF.mp4`

Actions run:
`36020895519`

Artifact:
`hia-shorts-youtube1-model-chi-s01-proof`

Artifact id:
`10816074280`

Artifact digest:
`sha256:b4870d524142c96db8bb6838652bac074da5f8c933c94247d346b9efd378b0c2`

Proof MP4 SHA256:
`988e52da898080706e3b87f127663064b3261a2d1bb261e0352fbcbc49c16b2c`

## Portrait treatment

Exactly one continuous long-form picture stream:
- same-frame blurred/darkened portrait background;
- centered protected foreground preserving ~93% of 1920x1080 width;
- foreground crop 1786x1080 at x=67;
- foreground scaled to 1080x654;
- foreground centered at y=633;
- no independent pan, zoom, scene rebuild, replacement image, or added graphic.

## Captions / graphics

- source long-form burned captions only;
- source long-form provenance only;
- source long-form GFX only;
- Shorts-only captions: NONE;
- Shorts-only title/metric card: NONE;
- new generated media: NONE.

## Technical QC

- 1080x1920: PASS
- 25 fps: PASS
- H.264 / yuv420p: PASS
- AAC 48 kHz stereo: PASS
- full decode: PASS
- PTS continuity: PASS
- black events introduced: 0
- duration: 34.880 s

## End card

No HIA-specific owner-locked 9:16 Shorts end-card currently exists in the repository.

Therefore this proof deliberately ends on source content.
No new end-card was invented or adapted.

## Gate

Do not render the remaining nine Shorts until the owner visually approves this proof format.
