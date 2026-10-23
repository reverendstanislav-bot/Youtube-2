# PROJECT PLUTO — Stage 04 V2 Voicebox preparation

Status: **READY FOR OWNER SCRIPT LOCK / GENERATION NOT STARTED**

This package accepts Stage 04 V2 as the sole current production-preparation
script. Stage 03 V1 is preserved as history and must not be used for voice.
Source Bank R1 remains rejected and is unrelated to this audio package.

## Verified input

- Authoritative script: `../../SCRIPT/STAGE04_PROJECT_PLUTO_FULL_NARRATION_V2_EN.md`
- Exact voice text: `../../SCRIPT/STAGE04_PROJECT_PLUTO_VOICE_TEXT_V2_EN.txt`
- 8 chapters
- 2,955 spoken words by whitespace-token count
- 19,064 characters in the canonical voice file after newline normalization
- 19,050 billable characters across the eight job bodies; the 14-character
  difference is seven double-newline chapter separators replaced by controlled
  pauses during assembly
- 54 claim-ledger rows
- 30 evidence-aligned narration beats
- Exact reconstruction from the eight job texts: PASS; no sentence loss

## Job design

There are **8 jobs, one complete chapter per job**. Chapter boundaries are the
only split points. This avoids cutting a sentence or paragraph and allows one
chapter to be regenerated without changing the rest of the narration.

Voicebox profile: `HIA Arthur Multi-Source`, local profile ID
`49119911-6b96-4db0-87fe-8a976ccc6b91`. Its four references come only from
verified Youtube-2 Big Muskie and Lake Peigneur narration. No Youtube-3 audio
is used.

Planned local engine: Qwen3-TTS 1.7B, sequential generation, fixed seed
20261022, internal sentence chunks capped at 800 characters with 50 ms joins.
The request templates are recorded in `VOICEBOX_REQUESTS_HOLD.json`, with
`submit:false`.

## Cost and duration

- Local Voicebox external API/credit cost: **USD 0.00**.
- Paid-provider cost: not asserted because no paid provider or rate is
  authorized. Exact formula: `19,050 / 1,000 × provider rate per 1,000 chars`.
- Expected narration: 19:03.871 at 155 wpm, 20:22.759 at 145 wpm, or 21:53.333
  at 135 wpm, before seven planned 600 ms chapter pauses.

## After owner approval

1. Reconfirm that the five Stage 04 inputs match `PREGENERATION_QC.json`.
2. Submit the eight jobs sequentially; never retry a completed exact-text job.
3. Save returned generation IDs and WAV SHA-256 values in `JOB_MANIFEST.csv`.
4. Listen to every job for voice identity, pronunciations, missing/repeated
   phrases, joins, clipping and artifacts.
5. Place approved files under `GENERATED_WAV/` with the expected names.
6. Run `merge_voicebox_jobs.ps1` to create the 48 kHz mono PCM master.
7. Decode-check and listen to the full master before any timeline sync.

Owner Script Lock and explicit voice-generation authorization are still
required. Nothing in this package submits a TTS request.
