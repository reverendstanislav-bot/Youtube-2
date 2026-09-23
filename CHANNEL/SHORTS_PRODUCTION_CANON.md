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
