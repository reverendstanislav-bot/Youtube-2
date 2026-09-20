# TC497 — NEW CHAT HANDOFF — FULL_V13

## READ THIS FIRST

Repository: `reverendstanislav-bot/Youtube-2`

Current active edit: **FULL_V13 review**.

The user has **NOT approved FULL_V13 yet**.
Do not build or promote a new 1920x1080 final until the user explicitly approves FULL_V13.

## CANONICAL CURRENT REVIEW

Use this build as the source of truth:

- GitHub Actions run: `35481027927`
- workflow: `Build TC497 FULL V13 Optimized Review`
- artifact: `tc497-full-v13-review-optimized`
- artifact id: `10596370068`
- artifact digest: `sha256:13fba3d04ba03b8d0e423e46749e62611ac2410a2dc19cbf947765b2bb717351`
- review file: `TC497_FULL_V13_REVIEW_960x540.mp4`
- file SHA-256: `138affeb1c185d61fda188c4f1165009a9c749ed8a09eb1703d8c56f77a17d98`
- duration: `1236.533333` s = 20:36.533
- 960x540
- 30 fps
- exactly 37,096 video frames
- H.264 + AAC

Direct GitHub artifact page:
`https://github.com/reverendstanislav-bot/Youtube-2/actions/runs/35481027927/artifacts/10596370068`

## WHAT FULL_V13 FIXED

### 1. Wheel / turbine cutaway purge

The user repeatedly rejected the photorealistic wheel/turbine/hub cutaway family.

FULL_V13 removes WA-09 from:
- the V14 cold open;
- the post-cold-open V4 shot map.

The user-reported ugly cutaway around `01:01–01:04` is gone.

Cold-open replacement:
- `61.08–64.62` now uses existing `WB-L04` articulation imagery.

Also:
- the rejected V6 wheel-cutaway breaker at `230.014–237.342` is not re-applied;
- do not generate another photorealistic wheel/turbine/hub cutaway;
- prefer archive, patent, schematic, articulation, real TC-497, or restrained project reconstruction.

### 2. Subtitle system

The user explicitly requested **running orange subtitles**, not mixed white/blue captions.

Canonical FULL_V13 subtitle behavior:
- entire phrase: muted orange `#B96F3D`;
- currently spoken word: brighter orange `#F28A3A`;
- word-level running highlight;
- no white dialogue words;
- no blue dialogue words;
- no black subtitle rectangle;
- no duplicate burned subtitle layer;
- no `CapV10`;
- no `BorderStyle=3`.

The successful optimized artifact contains the orange-only implementation.

Important: a later experimental "white-active" code change briefly diverged from the successful artifact.
Before this handoff, `TC497/FULL_V13/make_orange_running_ass.py` was restored to the optimized orange-only logic.
Do not use the white-active experiment as the canonical design.

### 3. Preserved corrections

FULL_V13 retains:
- V6 human/control visual breaker;
- V9 Yuma / ground-vs-air visual corrections;
- the 11:57 bridge repair;
- the V8 ending / clean end plate / identity;
- V9 audio.

Audio is bit-identical to V9:
`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

## IMPORTANT HISTORY / DO NOT REGRESS

### V10 / V11 subtitle defect
V10 added a second ASS subtitle layer over already burned V9 captions.
The style used `BorderStyle=3` with a huge outline, producing a large black rectangle.
V11 inherited it.

Do not reuse that architecture.

### V12
V12 removed the duplicate black-rectangle subtitle defect but returned to the older mixed subtitle look.
The user rejected that because subtitles were still white/blue instead of the requested orange-running system.

### FULL_V13
FULL_V13 rebuilds from clean picture sources and adds one global subtitle layer.

## RELEVANT REPO FILES

Start with:
- `TC497/CURRENT_STATUS_HANDOFF.md`
- `TC497/FULL_V13/NEW_CHAT_HANDOFF.md`
- `TC497/FULL_V13/EDIT_PLAN.md`
- `TC497/FULL_V13/REVIEW_QC.md`
- `TC497/FULL_V13/make_orange_running_ass.py`
- `TC497/FULL_V13/prep_v13_cold.py`
- `TC497/FULL_V13/index_v13.jsx`
- `TC497/FULL_V13/download_assets.py`
- `.github/workflows/build_tc497_full_v13_optimized.yml`

The experimental `.github/workflows/build_tc497_full_v13_whiteactive.yml` is **not** the source of truth.

## CURRENT GIT LOCKS

Orange-only subtitle source restored:
- commit `355b975056a54aa7b899abfac87f01ebee97cc47`

V13 edit plan normalized to optimized artifact:
- commit `002c0299d7ac3f69e458c8a3a2de1c118439f436`

## EXACT NEXT ACTION IN A NEW CHAT

1. Open `TC497/CURRENT_STATUS_HANDOFF.md` and this file.
2. Treat run `35481027927` / artifact `10596370068` as the current review.
3. If the user wants to inspect/download it, provide the GitHub artifact link.
4. If the user reports a defect, patch FULL_V13 only; do not fall back to V10/V11/V12.
5. If the user explicitly approves FULL_V13, then build a fresh native 1920x1080 FULL_V13 master and run final QC.
6. Never call a 1080p build final before explicit user approval.

## ONE-LINE COMMAND FOR THE NEXT CHAT

Open `TC497/FULL_V13/NEW_CHAT_HANDOFF.md` and `TC497/CURRENT_STATUS_HANDOFF.md` in `reverendstanislav-bot/Youtube-2`. Continue from the canonical optimized FULL_V13 review (run 35481027927, artifact 10596370068). FULL_V13 is not user-approved yet. Do not use V10/V11/V12 or the white-active subtitle experiment.
