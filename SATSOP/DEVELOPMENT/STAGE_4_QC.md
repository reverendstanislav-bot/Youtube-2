# SATSOP — STAGE 4 VO GENERATION AND QC

Updated: 2026-09-25

## Status

**FOUR TTS JOBS COMPLETE — VO MASTER ASSEMBLED — USER LISTENING GATE ACCEPTED — VO LOCKED**

## Authorized generation

- approved amount: **46.80 credits**;
- submitted jobs: **4**, with no retries or additional takes;
- voice: **Arthur** (`30fc8796-ceb6-4a66-b3a7-4a145ef7f346`, `preset`);
- engine: `text2speech_v2` / `elevenlabs`;
- all four jobs reached `completed`.

Job IDs:

1. `bfd91cfb-5e15-4118-8263-a8f6d80caa56`
2. `2945ee6c-697f-4058-8df0-43e0e23dd50a`
3. `93916884-e126-41bd-8054-f8d88d5e3889`
4. `446a7371-7ccc-4d5e-9341-b4c5c23fcb12`

## Canonical local audio

- master: `AUDIO/SATSOP_VO_MASTER_V1.wav`;
- runtime: **00:19:23.920**;
- format: PCM signed 16-bit little-endian, 44.1 kHz, mono;
- size: **102,657,822 bytes**;
- SHA-256: `5e9afb2310f812cf39aff3f37a8d4500bbca2988ae57ba1633244ed65d9d070c`.

The four provider MP3 files and WAV master are ignored by Git and retained locally. Exact hashes, sizes, durations, provider IDs, and settings are in `AUDIO/TTS_GENERATION_MANIFEST_V1.json`.

## Automated QC

- all four source files decoded without error;
- master decoded without error;
- source format consistent: MP3, 44.1 kHz, mono, approximately 128 kbps;
- master peak: **-0.332 dBFS**;
- master RMS: **-14.753 dBFS**;
- clipped samples: **0**;
- sustained quiet runs at or below -45 dBFS for at least 1.5 seconds: **0**;
- local offline word timing produced in `AUDIO/SATSOP_WORD_ALIGNMENT_V1.json`;
- alignment runtime before MP3 decoder-delay removal: **1,164.094694 seconds**;
- script-to-ASR sequence match ratio: **0.928328**.

Most ASR differences are representational: written number words versus digits and compounds split into separate words.

## Listening gate disposition

Automated ASR rendered `Satsop` inconsistently as `Satsup` or `Satsap`. This may be a tiny-model transcription limitation. The user subsequently directed that the listening check be treated as passed, the VO be locked, and Stage 5 begin.

The existing master is therefore the locked production VO. No regeneration is authorized by the original 46.80-credit approval.

## Balance note

- balance before submission: **1,353.07**;
- balance after completion: **1,266.67**;
- workspace-wide difference: **86.40**.

The balance tool exposes only the current shared workspace total, so the difference cannot be attributed entirely to these four jobs when concurrent workspace activity may exist. The four cost-only preflights totaled 46.80 credits, and exactly four corresponding jobs were submitted.
