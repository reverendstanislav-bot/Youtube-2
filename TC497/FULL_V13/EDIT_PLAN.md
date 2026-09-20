# TC497 FULL_V13 — full cutaway purge + white-base running subtitles

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
- base dialogue phrase text is white #FFFFFF;
- the currently spoken word is highlighted orange #F28A3A;
- word-level timing drives the running highlight;
- no blue dialogue-caption words;
- no muted-orange #B96F3D base dialogue text.

3. Preserve current edit corrections.
- V6 human/control break;
- V9 Yuma / ground-vs-air fixes;
- 11:57 bridge fix;
- V8 ending identity and clean end plate;
- V9 audio lineage bit-for-bit.

## Review lineage

This correction stays on the canonical FULL_V13 optimized architecture:
- previous reviewed build: GitHub Actions run `35481027927`;
- previous artifact: `tc497-full-v13-review-optimized`;
- previous artifact id: `10596370068`.

The only intended subtitle design change is:
- phrase/base text: white;
- active spoken word: orange #F28A3A.

FULL_V13 remains review-only until explicit user approval.
