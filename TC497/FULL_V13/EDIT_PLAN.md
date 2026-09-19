# TC497 FULL_V13 — cutaway purge + orange running subtitles

## Non-negotiable fixes

1. Remove WA-09 everywhere, including the V14 cold open.
   - confirmed V14 use: 00:01:01.080–00:01:04.620;
   - all post-cold-open WA-09 uses are removed from the V4 shot map as well;
   - build fails if WA-09 remains in either cold-open decisions or shots.json.

2. Rebuild captions from a clean picture track.
   - no old burned captions underneath;
   - no second caption layer;
   - no black backing rectangle;
   - no blue caption words;
   - warm-ivory phrase with the currently spoken word highlighted in orange (#D97932);
   - active word advances at word-level timing.

3. Preserve current edit corrections.
   - V6 picture fixes;
   - V9 Yuma / ground-vs-air fixes;
   - 11:57 bridge fix;
   - V8 ending identity and clean end plate;
   - V9/V12 audio lineage.

FULL_V13 is review-only until explicit user approval.
