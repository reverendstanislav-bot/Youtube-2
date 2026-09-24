# CHICAGO — CURRENT STATUS / HANDOFF

## ACTIVE TARGET — R15 SMOOTH REMOTION REVIEW

**Do not upload R14.**

R15 supersedes R14 as the current Chicago review target because the owner rejected the R14 transition feel as too abrupt.

### What R15 changes
- Remotion remains the primary picture compositor.
- Same approved R14 source assets and phrase-driven timing are retained.
- Adjacent R14 segments using the same source asset are merged into continuous visual groups.
- 89 same-asset hard boundaries were removed.
- Different source assets use centered 6-frame / 240 ms full-frame dissolves.
- No horizontal translation.
- No vertical translation.
- No shake.
- No whip/slide transitions.
- No rapid zoom-in/zoom-out bouncing.
- Only extremely restrained scale interpolation/breathing is allowed.
- Exact word-level captions and provenance logic are retained.
- Approved Chicago AAC remains bit-identical.
- Episode-1 textless subscribe/avatar end screen remains.

### R15 QC
- GitHub Actions run: `36046301264`
- render: PASS
- technical QC: PASS
- R14 shots: 294
- R15 continuous visual groups: 205
- same-asset boundaries removed: 89
- full-frame dissolve boundaries: 204
- residual scene jumps above threshold 0.65: 0
- black events: 0
- video SHA256: `712a043166052a7077203501117c75fce5b0047fcd6794f7b22ff64513291128`
- approved AAC SHA256: `a1e84ecb33a2060075b5681a086bf59b166396e16564b8e705a5b201dc4928ed`

### Release
Tag: `chicago-r15-smooth-remotion-review-20260924`

File:
`HIA_CHICAGO_R15_SMOOTH_REMOTION_REVIEW_1920x1080.mp4`

Status remains **REVIEW ONLY — USER VISUAL APPROVAL REQUIRED** until the owner watches and approves the R15 film.
