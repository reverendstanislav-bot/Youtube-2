# SATSOP — STAGE 3 LOCK

Updated: 2026-09-25

## Status

**STAGE 3 COMPLETE — NARRATION PREFLIGHT READY — PAID TTS NOT AUTHORIZED**

## Completed

- final English cadence polish;
- spoken-only narration extraction;
- TTS-specific name and number normalization;
- pronunciation and delivery package;
- four-chunk split below the ElevenLabs 5,000-character limit;
- hashes and boundary audit for every chunk;
- live provider cost preflight with `get_cost:true`;
- current workspace balance check;
- semantic audit against the fact-checked V2 review script.

## Canonical Stage 3 files

- `SCRIPT/NARRATION_V2_EN_REVIEW.md` — editorial script with cues;
- `SCRIPT/NARRATION_V3_EN_TTS_CLEAN.txt` — spoken-only input;
- `SCRIPT/TTS_CHUNKS_V1/CHUNK_01.txt` through `CHUNK_04.txt`;
- `SCRIPT/TTS_CHUNK_MANIFEST_V1.md`;
- `SCRIPT/PRONUNCIATION_PACKAGE_V1.md`;
- `SCRIPT/TTS_PACKAGE_V1.md`;
- `SCRIPT/V3_TTS_TEXT_AUDIT.md`.

## Cost lock

- engine: `text2speech_v2`;
- variant: `elevenlabs`;
- voice: Arthur;
- exact provider preflight: **46.80 credits**;
- current authorization: **0.00 credits**;
- jobs submitted in Stage 3: **0**.

## Next stage — Stage 4

Stage 4 begins only after explicit approval of the exact **46.80-credit** spend:

1. submit exactly four Arthur/ElevenLabs jobs with unchanged settings;
2. wait for all jobs and record IDs/provider metadata;
3. download and verify every audio file;
4. assemble a single canonical VO master;
5. run decode, duration, join, continuity, and pronunciation QC;
6. produce word-level alignment and exact runtime.
