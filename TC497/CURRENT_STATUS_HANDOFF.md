# TC497 — FULL_V13 CURRENT REVIEW

## STATUS

Episode: LeTourneau TC-497 Overland Train
Project: Hidden Industrial America / YouTube-2

Current state: **USER APPROVED FULL_V13 FOR FINALIZATION on 2026-09-20. Fresh native 1920x1080 final build is in progress in GitHub Actions run 35512151140.**

Do not use V10/V11/V12 as publication candidates.
Explicit FULL_V13 approval has now been received. Promote only the fresh native 1920x1080 build from run 35512151140 after its final QC succeeds.

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
