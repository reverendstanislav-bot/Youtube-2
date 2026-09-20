# TC497 — FULL_V13 CURRENT REVIEW

## STATUS

Episode: LeTourneau TC-497 Overland Train
Project: Hidden Industrial America / YouTube-2

Current state: **FULL_V13 FINAL 1080 MASTER BUILT AND QC-PASSED after explicit user approval.**

Do not use V10/V11/V12 as publication candidates.
Explicit FULL_V13 approval was received. The fresh native 1920x1080 post-approval build completed successfully and is the publication source of truth.

For a new chat, also read:
- `TC497/FULL_V13/NEW_CHAT_HANDOFF.md`

## CANONICAL CURRENT REVIEW

- GitHub Actions run: `35481027927`
- workflow: `Build TC497 FULL V13 Optimized Review`
- artifact: `tc497-full-v13-review-optimized`
- artifact id: `10596370068`
- artifact digest: `sha256:13fba3d04ba03b8d0e423e46749e62611ac2410a2dc19cbf947765b2bb717351`
- file: `TC497_FULL_V13_REVIEW_960x540.mp4`
- file SHA-256: `138affeb1c185d61fda188c4f1165009a9c749ed8a09eb1703d8c56f77a17d98`
- duration: 20:36.533
- 960x540 / 30 fps / 37,096 frames

GitHub artifact URL:
`https://github.com/reverendstanislav-bot/Youtube-2/actions/runs/35481027927/artifacts/10596370068`

## V13 FIXES

Cutaway purge:
- WA-09 removed from the V14 cold open and post-cold-open shot map;
- the ugly wheel/turbine cutaway at ~01:01–01:04 is gone;
- that cold-open interval now uses WB-L04 articulation imagery;
- rejected V6 wheel-cutaway breaker remains removed;
- no new photoreal wheel/turbine/hub cutaway should be generated.

Subtitle system:
- clean picture rebuild;
- one global running subtitle layer;
- phrase text = muted orange `#B96F3D`;
- current spoken word = brighter orange `#F28A3A`;
- no white/blue dialogue-caption words;
- no duplicate burned layer;
- no CapV10;
- no BorderStyle 3;
- no giant black rectangle.

Preserved:
- V6 human/control break;
- V9 Yuma / ground-vs-air fixes;
- 11:57 bridge repair;
- V8 ending;
- V9 audio.

Audio V9/V13 is bit-identical:
`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

## IMPORTANT SOURCE-OF-TRUTH NOTE

A later experimental white-active subtitle branch temporarily changed the repo script after the successful optimized artifact.

The canonical successful artifact is the optimized orange-only V13 above.

Before this handoff, the source was restored to orange-only logic:
- `TC497/FULL_V13/make_orange_running_ass.py`
- restore commit: `355b975056a54aa7b899abfac87f01ebee97cc47`

The V13 edit plan was normalized to the optimized artifact:
- commit: `002c0299d7ac3f69e458c8a3a2de1c118439f436`

The experimental workflow:
- `.github/workflows/build_tc497_full_v13_whiteactive.yml`

is **not** the source of truth.

## RELEVANT FILES

- `TC497/FULL_V13/NEW_CHAT_HANDOFF.md`
- `TC497/FULL_V13/EDIT_PLAN.md`
- `TC497/FULL_V13/REVIEW_QC.md`
- `TC497/FULL_V13/make_orange_running_ass.py`
- `TC497/FULL_V13/prep_v13_cold.py`
- `TC497/FULL_V13/index_v13.jsx`
- `TC497/FULL_V13/download_assets.py`
- `.github/workflows/build_tc497_full_v13_optimized.yml`

## NEXT STEP

User reviews FULL_V13.

If the user reports a defect:
- patch FULL_V13 review only;
- do not regress to V10/V11/V12;
- do not reintroduce the wheel/turbine cutaway family or mixed white/blue captions.

If the user explicitly approves FULL_V13:
1. build a fresh native 1920x1080 FULL_V13 master;
2. run final picture/audio/subtitle QC;
3. only then promote it to upload master.


## FINALIZATION APPROVAL

User explicitly said `Финалим` on 2026-09-20. Fresh native 1920x1080 build started as GitHub Actions run `35512151140`. Do not treat any earlier test 1080 run as the post-approval final source of truth unless the new run fails and the user explicitly chooses otherwise.


## FINAL PUBLICATION MASTER

- GitHub Actions run: `35512151140`
- conclusion: `success`
- artifact: `tc497-full-v13-final-upload-master-1080`
- artifact id: `10606201351`
- artifact digest: `sha256:67ea7cd5ba4b9add4d3f4916ef9e5381c6b043269766ddb1b0e0b5c7236efc57`
- file: `TC497_FINAL_UPLOAD_MASTER_FULL_V13_1920x1080.mp4`
- file SHA-256: `574b14548f70798a1aae0ef5e86845368de5297ba16a4cdc77c2fd199cea9b9a`
- direct release URL: `https://github.com/reverendstanislav-bot/Youtube-2/releases/download/tc497-full-v13-final-1080-20260920/TC497_FINAL_UPLOAD_MASTER_FULL_V13_1920x1080.mp4`
- release page: `https://github.com/reverendstanislav-bot/Youtube-2/releases/tag/tc497-full-v13-final-1080-20260920`

Final QC:
- native 1920x1080, 30 fps;
- 37,096 frames;
- duration 20:36.533;
- one clean subtitle layer;
- base dialogue white #FFFFFF;
- active spoken word orange #F28A3A;
- no muted-orange base dialogue, no blue dialogue, no CapV10, no BorderStyle 3, no giant black caption rectangle;
- WA-09 absent;
- rejected wheel/turbine/hub cutaway family remains absent;
- 01:01-01:04 uses WB-L04 articulation imagery;
- V6 human/control correction, V9 Yuma/ground-vs-air fixes, 11:57 repair and V8 ending retained;
- V9 audio bit-identical: `7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`;
- integrated loudness -13.5 LUFS;
- true peak -1.9 dBFS;
- blackdetect found no configured-threshold black event.
