# BIG MUSKIE — TTS CHUNK MANIFEST V1

Status: **PREFLIGHT COMPLETE — AUTHORIZED FOR GENERATION**

Source narration: `SCRIPT/NARRATION_V3_EN_REVIEW.md`  
Source narration blob SHA: `8dd9b3cd12e8e5471d86d591fbbb3be33a138c1a`  
Spoken-only file: `SCRIPT/NARRATION_V3_EN_TTS_CLEAN.txt`

## Engine lock
- voice: **Alexey**
- voice_id: `7c2133e5-68ab-511f-9aed-9a67664382b1`
- voice_type: `preset`
- model: `text2speech_v2`
- variant: `elevenlabs`
- identical default tuning on all chunks
- backend limit: <5000 characters per job

## Spoken-only validation
- characters: **18944**
- whitespace-delimited tokens: **3081**
- headings/status/source comments/SHORT markers/end-screen note removed
- no sentence split between chunks

| Chunk | Characters | Tokens | Cost preflight |
|---|---:|---:|---:|
| 01 | 4797 | 795 | 14.40 |
| 02 | 4839 | 770 | 14.55 |
| 03 | 4816 | 790 | 14.55 |
| 04 | 4486 | 726 | 13.50 |

**Total estimated TTS cost: 57.00 credits.**  
**Credits spent by preflight: 0.00.**

Chunk files:
- `SCRIPT/TTS_CHUNKS_V1/CHUNK_01.txt`
- `SCRIPT/TTS_CHUNKS_V1/CHUNK_02.txt`
- `SCRIPT/TTS_CHUNKS_V1/CHUNK_03.txt`
- `SCRIPT/TTS_CHUNKS_V1/CHUNK_04.txt`

Next: submit these exact four texts with the locked Alexey settings, capture job IDs/results/actual cost, run continuity QC, assemble master, then derive runtime and word-level timing.
