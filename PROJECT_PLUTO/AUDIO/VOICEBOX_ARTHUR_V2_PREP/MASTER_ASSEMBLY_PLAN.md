# Project Pluto V2 narration master assembly

## Inputs

Eight owner-approved Voicebox WAV files in manifest order. Each must match its
exact job text and receive human auditory QC before assembly. Keep raw Voicebox
outputs unchanged alongside the assembled master.

## Join policy

- Convert each approved job to mono 48 kHz PCM 24-bit for a uniform concat.
- Preserve each job's internal phrasing; do not time-stretch narration.
- Insert 600 ms digital silence only between chapters (7 joins, 4.2 seconds).
- Do not crossfade chapter speech. The chapter break is an intentional editorial
  pause, and an overlap could remove consonants or alter a sentence ending.
- Do not apply final loudness processing until all eight chapters pass listening
  review. Produce a transparent assembly master first.

## Expected output

`PROJECT_PLUTO_ARTHUR_V2_ASSEMBLY_MASTER_48K_MONO_S24.wav`

Estimated duration before generated-speech variation is 19:08.071–21:57.533,
including the seven chapter pauses. Actual WAV duration becomes authoritative.

## Required post-assembly checks

1. FFmpeg full decode with `-v error -xerror`.
2. FFprobe: mono, 48,000 Hz, PCM 24-bit, actual duration recorded.
3. SHA-256 for every raw job and the master.
4. Full human listen for identity, word accuracy, repeated/missing text,
   pronunciation, chapter joins, clipping and background artifacts.
5. Only after auditory approval create a delivery loudness version and generate
   word-level timestamps for the edit.

The merge helper refuses missing files and existing output. It does not perform
speech generation or overwrite raw WAV files.
