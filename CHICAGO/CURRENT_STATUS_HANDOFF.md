# CHICAGO — CURRENT STATUS / HANDOFF

## ACTIVE TARGET — R14 EDITORIAL RECUT

**Do not upload R13.**

Deep QC of the completed R13 review found:
- technical decode PASS;
- provenance classification PASS;
- end screen PASS;
- primary editorial pacing FAIL;
- multiple static beats 8–25 s long;
- map block around 05:49–07:17 too static;
- provenance text too small at 10 px;
- caption token alignment 98.665%, not exact word-level coverage;
- output pixel-format/range not accepted as the final upload target.

R14 corrects those defects using only existing approved assets. No image/video generation or external generation credits are authorized or used.

### R14 hard rules
- Remotion remains the primary picture timeline.
- New internal cuts are placed at narration word boundaries where safe.
- No pre-outro visual beat may exceed 7.05 s.
- Archive/map/document: controlled reframing cuts, no constant Ken Burns.
- Reconstruction: alternate framing; subtle push only selectively.
- HISTORICAL SOURCE = verified archive/map only.
- AI RECONSTRUCTION = generated reconstruction only.
- provenance label must be readable at 1080p.
- captions are generated directly from word-level timing and must have 100% sequence coverage.
- approved AAC SHA256 remains `a1e84ecb33a2060075b5681a086bf59b166396e16564b8e705a5b201dc4928ed`.
- outro from 21:08 is textless: one previous-video rectangle + one avatar circle; no captions/provenance.
- final picture target: 1920×1080, 25 fps, exactly 32,268 frames, limited-range `yuv420p`.

### Active workflow
`.github/workflows/build_chicago_r14_editorial_recut.yml`

R14 remains REVIEW until the rendered file passes visual/editorial QC and explicit user approval.
