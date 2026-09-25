# SATSOP — TTS PACKAGE V1

Status: **PREFLIGHT COMPLETE — AWAITING EXPLICIT CREDIT APPROVAL**

## Canonical voice / engine

- voice: **Arthur**
- voice_id: `30fc8796-ceb6-4a66-b3a7-4a145ef7f346`
- voice_type: `preset`
- model: `text2speech_v2`
- variant: `elevenlabs`

The exact voice/engine pair was accepted by the live provider during all four cost-only requests on 2026-09-25.

## Delivery direction

- composed American documentary narrator;
- restrained confidence, never a trailer voice;
- opening: controlled mystery, not horror;
- financing explanation: clear, conversational, slightly faster;
- `fourteen percent` versus `seventy-four percent`: distinct emphasis;
- take-or-pay passage: serious, not accusatory;
- preservation passage: slower and spatial;
- BPA comparison: build momentum through `three times`, `six hundred average megawatts`, and `two hundred million dollars per year`;
- termination: calm finality;
- reuse ending: reflective, not sentimental;
- final two lines: short pause between them; no added outro.

## Clean input

- file: `NARRATION_V3_EN_TTS_CLEAN.txt`
- UTF-8, LF line endings;
- characters including paragraph separators/final newline: **15,465**;
- whitespace-delimited words: **2,309**;
- SHA-256: `d78025ce140f7ceec5e2a62691d55bd8503b3b70a5380e5075081470d9044272`.

Removed from speech:

- title and status metadata;
- hook alternatives;
- timestamps and section headings;
- production cues;
- retention table;
- markdown syntax.

Normalized for speech:

- `WNP-3` → `Project Three`;
- `WNP-5` → `Project Five`;
- `WNP-2` → `Project Two`;
- `BPA` → `Bonneville`;
- `WPPSS` → `the Supply System`;
- digits that risk mechanical reading were written as spoken English.

## Exact live cost preflight

Provider calls used the exact chunk contents with `get_cost:true`. The provider confirmed **no job submitted** for every call.

| Chunk | Characters | Exact credits |
|---|---:|---:|
| 01 | 4,501 | 13.65 |
| 02 | 4,726 | 14.25 |
| 03 | 4,703 | 14.25 |
| 04 | 1,532 | 4.65 |
| **Total** | **15,462 chunk characters** | **46.80** |

The clean master has three additional newline characters at chunk boundaries; no spoken content is missing.

Balance snapshot after cost-only preflight:

- available: **1,353.07 credits**;
- projected balance after one approved four-job batch: **1,306.27 credits**;
- unlimited audio allowance: unavailable;
- paid jobs submitted: **0**.

## Spend gate

Stage 3 does not authorize generation.

Required approval must explicitly authorize **46.80 credits for four Arthur/ElevenLabs TTS jobs**. A general instruction to continue production is not sufficient.

No retry, test take, alternate voice, or additional job is included in this amount.
