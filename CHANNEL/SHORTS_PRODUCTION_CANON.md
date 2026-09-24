# HIA — Shorts Production Canon

## Purpose

Shorts are derived from the approved long-form film. They are not separate rewrites unless explicitly approved.

## Source lock

For every Short:
- use the exact long-form narration/audio between the locked IN/OUT timecodes;
- select IN/OUT on word boundaries from the episode word-level transcript;
- preserve factual wording from the long-form;
- do not generate a new voice track unless explicitly requested;
- do not use video generation;
- use existing episode archive / document / reconstruction / GFX assets;
- provenance truth rules remain identical to long-form.

## Editorial target

- aspect ratio: 9:16, 1080×1920;
- target runtime: 25–55 seconds; hard maximum 60 seconds unless explicitly approved;
- first 1–2 seconds must contain an immediate visual/narrative hook already present in the source excerpt;
- one Short = one complete idea with setup, escalation/payoff, and a clean ending;
- avoid cutting mid-sentence merely to hit duration;
- cuts should land on source narration word/phrase boundaries;
- no more than two highly similar views in a row;
- use vertical reframing before inventing replacement imagery;
- archive/document frames remain readable and truthful;
- maps must be reframed around the exact region being discussed;
- captions: one layer, white base with orange active word, large 9:16-safe typography;
- keep critical visual content and captions inside vertical safe zones;
- no baked-in YouTube end-screen placeholders inside Shorts.

## Required episode package

Each episode with Shorts must contain:

- `SHORTS/SHORTS_EXTRACTION_MAP.md` — human-readable locked plan;
- `SHORTS/shorts_extraction_map.json` — machine-readable timecodes and beat map;
- exact long-form IN/OUT;
- exact extracted narration text;
- working title and hook;
- 9:16 montage instructions;
- source/provenance expectations;
- caption treatment;
- status per Short.

## Production state

A Short may be:
- `SOURCE_LOCKED` — exact excerpt/timecodes chosen;
- `VERTICAL_PLAN_LOCKED` — 9:16 beat map completed;
- `RENDER_REVIEW` — vertical review rendered;
- `APPROVED` — user approved;
- `PUBLISHED` — platform publish confirmed.

Never mark a Short APPROVED based only on technical QC.

## Vertical composition hard rules

- Never show the same source frame twice in two simultaneous visible panels.
- One moment in narration = one primary crisp visual plane. Decorative duplicated/blurred copies are not allowed as visible content panels.
- Wide maps/documents may be letterboxed inside the 9:16 frame; reconstruction/archive may receive a controlled crop, but must not be duplicated to fill space.
- Do not stack a "full" view and a second "detail" copy of the same image at the same time.
- Preserve the source long-form provenance label when it is visible; do not add a second provenance label over the same frame.
- Rejected V3/V4/V5 mechanical vertical systems are superseded by the V10 clean-source semantic system.

## Clean-source vertical rebuild rule

The rejected V3/V4/V5 Shorts proved that mechanically cropping the finished 16:9 long-form master is not an acceptable vertical workflow.

- Do not use the finished 16:9 long-form master as the primary Shorts picture source.
- Long-form audio/word timing may be source-locked, but picture must be rebuilt from clean underlying archive / document / reconstruction / GFX assets.
- Every Short gets a semantic visual plan: the picture shown must directly explain the narration at that moment.
- The opening hook must show the actual subject immediately; no abstract wheel/tire/texture crop under a machine-scale title.
- Full-bleed 9:16 is allowed only when the clean asset supports a meaningful portrait crop.
- Wide machines, maps and documents require a curated pan/reframe or a purpose-built editorial composition; never a blind center crop.
- Scale from one proof Short first. Do not batch-render all episode Shorts until the proof visual language passes human visual review.

## Motion discipline

- No aggressive horizontal scan / left-right sweep on still images.
- Default motion for Shorts is static framing + hard cut between semantic beats.
- If motion is used later, it must be a very subtle push/reframe (roughly <=2% scale change over the shot), never a full-frame side-to-side traverse.
- More energy should come from stronger shot selection and narration-driven cuts, not from artificial camera movement.
- Captions must remain inside the 9:16 safe area and may use at most two balanced lines; no single-line overflow beyond the frame.

## Current V10 review lock

The current review package is **V10**.

- 10 Shorts exist: 5 Chicago + 5 TC-497.
- TC497-S01 is the original V10 style-bible proof.
- CHI-S01 and TC497-S02 were used as cross-episode V10 gate proofs.
- The remaining seven were rendered only after those gate proofs passed visual review.
- V10 uses clean underlying assets, semantic visual beats, one visual plane, restrained push-ins only, mobile-safe white/orange captions, and truthful per-asset provenance.
- Release tag: `hia-shorts-v10-review-20260923`.
- Publication state remains `RENDER_REVIEW` until explicit user visual approval.
- Do not run or restore the obsolete pre-V10 final-master workflow; it used rejected master-crop logic.

## Wave 2 hard-QC lock — 2026-09-24

The seven remaining V10 review Shorts completed the hard-QC repair pass.

- final Actions run: `36017934649`;
- final head used for render: `d0223420ad6b8b49039dd6fe8571ea5110ae2eaf`;
- combined review artifact id: `10815054356`;
- detailed report: `CHANNEL/SHORTS_WAVE2_FINAL_QC_2026-09-24.md`;
- machine QC: 7/7 technical PASS, zero decode errors, zero ASS overlaps, no legacy subtitle contamination;
- visual QC: no remaining hard blocker in CHI-S02/S03/S04/S05 or TC497-S03/S04/S05;
- generation spend for the repair pass: zero; only existing assets and editor-native GFX were used.

State remains `RENDER_REVIEW` until explicit user visual approval. Do not silently promote these Shorts to `APPROVED`.

