# TC497 FULL_V13 — full cutaway purge + orange-only running subtitles

## Non-negotiable fixes

1. Remove WA-09 everywhere, including the cold open.
- confirmed cold-open use: 00:01:01.080–00:01:04.620;
- replacement: WB-L04 articulation imagery;
- all post-cold-open WA-09 uses are removed from the V4 shot map;
- the rejected V6 electric-wheel cutaway breaker at 230.014–237.342 is not used;
- do not generate another photoreal wheel/turbine/hub cutaway.

2. Rebuild captions from a clean picture track.
- no old burned captions underneath;
- no second caption layer;
- no black backing rectangle;
- all dialogue subtitle words are orange;
- phrase text uses muted orange #B96F3D;
- the currently spoken word uses brighter orange #F28A3A;
- word-level timing drives the running highlight;
- no white or blue dialogue-caption words.

3. Preserve current edit corrections.
- V6 human/control break;
- V9 Yuma / ground-vs-air fixes;
- 11:57 bridge fix;
- V8 ending identity and clean end plate;
- V9 audio lineage bit-for-bit.

## Current source of truth

Use the successful optimized V13 review build:
- GitHub Actions run: `35481027927`
- workflow: `Build TC497 FULL V13 Optimized Review`
- artifact: `tc497-full-v13-review-optimized`
- artifact id: `10596370068`

FULL_V13 is review-only until explicit user approval.
