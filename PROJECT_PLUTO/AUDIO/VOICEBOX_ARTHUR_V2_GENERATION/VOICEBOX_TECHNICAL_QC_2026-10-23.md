# Project Pluto Stage04 V2 — Voicebox Generation and Technical QC

Date: 2026-10-23  
Repository: `reverendstanislav-bot/Youtube-2`  
Project: `PROJECT_PLUTO`, VIDEO006  
Source commit: `f86c121b824fb665d4a84d28e596a21f11791e1f`

## Result

- Voice profile: `HIA Arthur Multi-Source`
- Voice profile ID: `49119911-6b96-4db0-87fe-8a976ccc6b91`
- Model: Voicebox Qwen3-TTS 1.7B, local CUDA
- Exact current narration input: Stage04 V2 only
- Jobs submitted: 8
- Jobs completed: 8
- Spoken words: 2,955
- Job-body characters: 19,050
- Youtube-3 audio used: no
- External generation cost: USD 0.00
- Generation window: 2026-10-23T17:41:34Z to 2026-10-23T20:36:12Z

The owner's direct instruction to start generation lifted the generation hold for this exact V2 job package. Stage03 V1 was not used.

## Output verification

All eight job WAV files exist and independently passed complete FFmpeg decode with `-v error -xerror`. Each is mono PCM signed 16-bit at 24 kHz. Per-file generation IDs, durations and SHA256 values are recorded in `VOICEBOX_GENERATED_AUDIO_MANIFEST.csv`.

The assembly inserted seven planned 600 ms chapter gaps, for 4.200 seconds total. The eight raw jobs total 1,117.400 seconds. The assembled master is 1,121.600 seconds (`00:18:41.600`).

Master:

- Filename: `PROJECT_PLUTO_ARTHUR_V2_ASSEMBLY_MASTER_48K_MONO_S24.wav`
- Size: 161,510,502 bytes
- Codec: PCM signed 24-bit little-endian
- Sample rate: 48,000 Hz
- Channels: 1
- Duration: 1,121.600 seconds
- SHA256: `78213c4b5fa68605ae5d50a102de21d49bd419cf28aad77b8ff777e02bb12b19`
- Full-stream FFmpeg decode: PASS

## Remaining gate

Technical generation and file integrity pass. Human auditory review is still required for pronunciation, dropped or repeated phrases, artifacts, pacing and acceptable chapter joins. Status is `TECHNICAL_GENERATION_COMPLETE_AUDITORY_QC_PENDING`; this report does not claim an auditory PASS.

## Release package checksums

- `PROJECT_PLUTO_ARTHUR_V2_JOBS_01-08.zip` — 41,234,327 bytes — SHA256 `802c909d1e01235573c8673d15e9673193adfb633ef679311dd44ad47131b889`
- `PROJECT_PLUTO_ARTHUR_V2_ASSEMBLY_MASTER_48K_MONO_S24.wav` — 161,510,502 bytes — SHA256 `78213c4b5fa68605ae5d50a102de21d49bd419cf28aad77b8ff777e02bb12b19`
- `VOICEBOX_EXECUTION_MANIFEST.json` — 9,129 bytes — SHA256 `6102b3fa5610701e3e710d948a166cdf6bdc66b5c2261dd0ef2a7a048e67a772`

The ZIP was expanded after creation and all eight extracted WAV hashes matched their source WAVs.
