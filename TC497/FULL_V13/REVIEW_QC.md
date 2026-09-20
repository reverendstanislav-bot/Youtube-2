# TC497 FULL_V13 — review QC

Status: **REVIEW READY — USER APPROVAL REQUIRED.**

Current build:
- GitHub Actions run: `35481027927`
- workflow: `Build TC497 FULL V13 Optimized Review`
- artifact: `tc497-full-v13-review-optimized`
- artifact id: `10596370068`
- artifact digest: `sha256:13fba3d04ba03b8d0e423e46749e62611ac2410a2dc19cbf947765b2bb717351`

Review file:
- `TC497_FULL_V13_REVIEW_960x540.mp4`
- SHA-256: `138affeb1c185d61fda188c4f1165009a9c749ed8a09eb1703d8c56f77a17d98`
- duration: 1236.533333 s
- 960x540
- 30 fps
- exactly 37,096 frames

## Cutaway purge

Verified:
- WA-09 is gone from the V14 cold-open decision map;
- WA-09 is gone from the post-cold-open `shots.json`;
- the user-reported ugly wheel/turbine cutaway around 01:01–01:04 is gone;
- 01:01–01:04 now uses existing WB-L04 articulation imagery;
- rejected V6 wheel-cutaway breaker is not re-applied.

No new photoreal wheel/turbine/hub cutaway was generated.

## Orange running subtitles

The film is rebuilt from clean picture sources rather than adding another subtitle layer over V9/V10/V11.

Verified:
- dialogue captions are orange only;
- phrase is muted orange;
- currently spoken word is brighter orange;
- no white/blue dialogue-caption words;
- no CapV10;
- no BorderStyle 3;
- no giant black backing rectangle;
- no duplicated burned subtitle layer.

Manual visual samples checked at:
- 01:03 — cold-open replacement + orange running subtitle;
- 01:32 — ordinary subtitle over difficult background;
- Electric Wheel / patent passages;
- 11:57 transition repair;
- V8 ending.

## Preserved picture corrections

- V6 human-break correction;
- V9 Yuma / ground-vs-air fixes;
- 11:57 bridge correction;
- V8 clean ending / identity.

## Audio

V9 and FULL_V13 AAC are bit-identical:

`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

## Technical QC

- 960x540
- 30 fps
- 37,096 frames
- 20:36.533
- no blackdetect event at the configured threshold
- artifact build completed successfully

FULL_V13 is review-only until explicit user approval.
