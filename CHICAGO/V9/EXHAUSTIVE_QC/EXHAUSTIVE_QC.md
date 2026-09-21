# Chicago V9 — exhaustive pre-publication QC

## Scope
- Full compressed video decoded end-to-end.
- Every decoded video frame analyzed at 25 fps (**40 ms frame cadence**).
- Video PTS checked frame-by-frame.
- Audio decoded continuously and analyzed in 100 ms blocks plus sample-level peak/discontinuity statistics.
- Script, canonical V2 SRT, word-level transcript, scene map, current V9 shot plan, overlays, fact map and audio timeline cross-checked.

## Technical media
- Decode errors: **0**
- Video frames: **32268** (reported 32268)
- FPS: **25.000000**
- PTS interval errors vs 0.040 s: **0**
- Non-monotonic packet streams: **0**

## Frame-level visual QC
- True black frames: **0**
- True white/blank frames: **0**
- Unexpected hard discontinuities away from planned shot boundaries: **0**
- Single-frame flash candidates: **0**
- One-frame blur-collapse candidates: **4**
- Near-static intervals >=3 s: **0** (still-image documentary material is expected; cross-check separately).

## Audio QC
- Loudness input_i: **-14.04 LUFS**
- True peak: **-4.48 dBTP**
- LRA: **3.00 LU**
- Samples >=0.9999: **[0, 0]**
- Channel RMS imbalance: **0.000 dB**
- >=0.5 s runs below -60 dBFS: **63**

## Script / narration / subtitle integrity
- Script ↔ V2 SRT token sequence ratio: **100.0000%**
- Script ↔ word transcript ratio: **98.9394%**
- Script ↔ scene-map narration ratio: **100.0000%**
- V2 SRT ↔ word transcript ratio: **98.9394%**
- Scene-map gaps: **0**, overlaps: **0**
- Current-shot gaps: **0**, overlaps: **0**
- Current shots with unknown scene IDs: **31**
- Low referenced-scene text-similarity candidates (<0.25): **103** (manual editorial review list, not automatic failure).

## Overlay / subtitle layout
- Running caption cues: **338**
- Editorial cards: **33**
- Provenance labels: **207**
- Editorial-card time overlaps: **0**
- Invalid overlay intervals: **0**
- Caption timing/order issues: **0**
- Approx editorial→caption vertical gap: **132 px** at 960x540.
- Approx end-caption→Subscribe-circle gap: **33 px**.

## Fact / licensing package
- fact_map rows: **23**
- fact status counts: **{"": 23}**
- music timeline rows: **7**
- SFX timeline rows: **3**

## Automatic gate
- **REVIEW_REQUIRED**

### Blocking / review issues
- 4 one-frame blur-collapse candidates require review.
- Current V9 shot plan references unknown scene IDs.
