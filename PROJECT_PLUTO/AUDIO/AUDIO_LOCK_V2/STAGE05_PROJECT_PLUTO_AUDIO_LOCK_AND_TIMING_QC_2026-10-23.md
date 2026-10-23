# Project Pluto Stage05 — Owner Audio Lock and Timing QC

Date: 2026-10-23  
Status: **OWNER_APPROVED_AUDIO_LOCK**

The owner approved the generated narration master. The locked binary is `PROJECT_PLUTO_ARTHUR_V2_ASSEMBLY_MASTER_48K_MONO_S24.wav`, SHA256 `78213c4b5fa68605ae5d50a102de21d49bd419cf28aad77b8ff777e02bb12b19`, duration `1121.600` seconds (`00:18:41:15` at 25 fps). Stage04 V2 remains the authoritative wording. Faster-Whisper output is used only to locate those words in the approved audio.

## Timing method

- Eight chapter WAVs were transcribed separately with local Faster-Whisper base, CPU int8, beam size 5, word timestamps enabled and VAD disabled.
- Chapter offsets use the actual WAV durations plus the seven locked 600 ms assembly gaps.
- Expected V2 tokens were aligned in order to ASR tokens.
- The 30 evidence-aligned semantic beats were located by exact expected-text token ranges.
- Edit boundaries use midpoints between adjacent spoken ranges and were quantized to a contiguous 25 fps timeline from frame 0 through frame 28040.

| Chapter | Duration sec | Expected tokens | ASR tokens | Sequence ratio | Exact | Substitution | Interpolated |
|---|---:|---:|---:|---:|---:|---:|---:|
| CH01 | 91.550 | 257 | 254 | 0.9511 | 243 | 14 | 0 |
| CH02 | 117.820 | 321 | 321 | 0.9969 | 320 | 1 | 0 |
| CH03 | 133.340 | 354 | 345 | 0.9642 | 337 | 17 | 0 |
| CH04 | 179.130 | 468 | 454 | 0.9544 | 440 | 22 | 6 |
| CH05 | 183.400 | 495 | 484 | 0.9499 | 465 | 30 | 0 |
| CH06 | 132.490 | 366 | 359 | 0.9490 | 344 | 21 | 1 |
| CH07 | 178.650 | 478 | 472 | 0.9811 | 466 | 12 | 0 |
| CH08 | 101.020 | 284 | 283 | 0.9735 | 276 | 8 | 0 |

## Result

- Chapters: 8/8 mapped
- Semantic beats: 30/30 mapped
- Expected tokens: 3023
- Weighted ASR sequence ratio: 0.964414
- Exact token alignments: 2891
- Substitution alignments: 125
- Interpolated expected tokens: 7
- Timeline coverage: frame 0 through 28040, contiguous with no gaps or overlaps
- Youtube-3 audio used: no

ASR differences are not authority to rewrite names, dates, numbers or narration. Any future replacement audio changes the master hash and invalidates this lock and its timing files.
