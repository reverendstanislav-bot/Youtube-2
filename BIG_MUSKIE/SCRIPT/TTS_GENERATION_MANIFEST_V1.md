# BIG MUSKIE — TTS GENERATION MANIFEST V1

Status: **ARTHUR TTS GENERATED — TECHNICAL QC PASS — WORD-LEVEL ALIGNMENT NEXT**

Generation date: 2026-09-23  
User approval: explicit approval for **56.25 credits** in the immediately preceding user instruction before generation.

## Canonical voice / engine

- voice: **Arthur**
- voice_id: `30fc8796-ceb6-4a66-b3a7-4a145ef7f346`
- voice_type: `preset`
- model: `text2speech_v2`
- variant/engine: `elevenlabs`

## Cost lock

Free preflight immediately before submission:
- chunk 01: 14.55 credits
- chunk 02: 14.55 credits
- chunk 03: 14.55 credits
- chunk 04: 12.60 credits
- approved batch total: **56.25 credits**

Exactly four jobs were submitted. No retry or additional paid generation was submitted.

## Jobs

| Chunk | Job ID | Duration (provider) | Download URL |
|---|---|---:|---|
| 01 | `f3af59ce-8b81-4d6f-9980-103cfc133bcb` | 374.48 s | https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260923_121755_f3af59ce-8b81-4d6f-9980-103cfc133bcb.mp3 |
| 02 | `a41a21f8-5b87-48c8-a6cd-a7723fd58ef4` | 374.16 s | https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260923_121754_a41a21f8-5b87-48c8-a6cd-a7723fd58ef4.mp3 |
| 03 | `5966eff5-f4f7-4795-bc95-40e84350d080` | 370.48 s | https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260923_121754_5966eff5-f4f7-4795-bc95-40e84350d080.mp3 |
| 04 | `fd0210e2-baad-4e8d-881c-9fb81383adf9` | 306.48 s | https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260923_121755_fd0210e2-baad-4e8d-881c-9fb81383adf9.mp3 |

All four jobs completed successfully. Provider metadata confirms Arthur + ElevenLabs for every job.

## Downloaded-file SHA-256 / ffprobe duration

| Chunk | SHA-256 | ffprobe duration |
|---|---|---:|
| 01 | `15819c59785c7e5271850f5fdd0066267f29cc9f39e2b53958f09c224acce789` | 374.517551 s |
| 02 | `94f4b4530f28d75f6f1dda7e71d9d0eecc4afd127900ecae6b3fe5e9c98b9ced` | 374.204082 s |
| 03 | `8dd816028ab89f7b8534a7029791d4cac579d8eaeccfa32157d3021202975ec3` | 370.520816 s |
| 04 | `a60786d521ac3fbc1c066ee98a27064d093555e8fd291c0c4b431aef8cee4ca7` | 306.520816 s |

## Assembled VO master QC

Lossless MP3 concat SHA-256:
`a2de325f51864dcae16eca15a7482fc779647878320d4defe8221e35ecf02f88`

Decoded PCM 48 kHz / 24-bit mono master SHA-256:
`722d0e4f9e353e665534ee22e758d1e9bd7eadb5817412681e26d0ca8e2e1db4`

Runtime:
- provider four-chunk decoded sum: **1425.600 s = 23:45.600**
- earlier MP3 packet-concat measurement: 1425.722458 s — superseded for editorial timing
- canonical join-normalized editorial timeline: **1426.400 s = 23:46.400**
- final chunk starts: **0.000 / 375.000 / 749.440 / 1119.920 s**

Decode check: **PASS**

Measured source VO loudness:
- integrated: **-14.47 LUFS**
- true peak: **-0.42 dBTP**
- LRA: **3.40 LU**

No loudness normalization has been rendered into the canonical VO at this stage; these are analysis measurements only.

## Rejected audio lineage

The earlier Alexey batch remains:
**REJECTED / NON-CANONICAL / DO NOT USE**.

Do not reuse its job IDs, URLs, timings or audio in Big Muskie.

## Post-generation timing status

Word-level alignment, pronunciation/join QC and Stage 7 are complete.

Canonical editorial timing is **23:46.400** after deterministic silence normalization at chunk joins. See `BIG_MUSKIE/STAGE_7/`.

Next: asset inventory / gap analysis / prompt package. No additional paid generation is authorized by this manifest.
