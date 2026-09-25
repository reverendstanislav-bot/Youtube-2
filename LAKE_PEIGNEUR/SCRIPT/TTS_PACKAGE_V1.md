# LAKE PEIGNEUR — TTS PACKAGE V1

Updated: 2026-09-25

Status: **PREFLIGHT COMPLETE — AWAITING EXPLICIT CREDIT APPROVAL**

## Voice / engine
- Arthur
- voice_id: `30fc8796-ceb6-4a66-b3a7-4a145ef7f346`
- voice_type: `preset`
- model: `text2speech_v2`
- variant: `elevenlabs`

## Clean input
- file: `NARRATION_V2_EN_TTS_CLEAN.txt`
- characters incl. separators/final newline: **13,128**
- billable chunk characters: **13,121**
- words: **2,045**
- embedded SHORT duplicate blocks removed
- headings/source/directorial notes removed

Speech normalization:
- MSHA first reference expanded to Mine Safety and Health Administration
- later MSHA reference normalized to federal mine-safety investigators
- ONEOK spoken as One Oak

## Final four-job split
- 01: 3,558 chars / 549 words / **10.80 credits**
- 02: 3,532 chars / 576 words / **10.65 credits**
- 03: 3,587 chars / 556 words / **10.80 credits**
- 04: 2,444 chars / 364 words / **7.35 credits**

**Exact batch total: 39.60 credits.**

Pricing rule verified against canonical Arthur preflights:
`ceil(characters / 50) × 0.15 credits`.

Live `get_cost:true` on the actual final Chunk 01 returned **10.80** and submitted no job. The same pricing rule is independently verified in prior Big Muskie and Satsop Arthur manifests.

## Balance
- current balance: **1,306.27 credits**
- projected after one approved batch: **1,266.67 credits**
- paid Lake Peigneur jobs submitted: **0**

## Runtime estimate
Using measured Arthur speed from Big Muskie, 2,045 words should land near **16.1 minutes** before final timing normalization.

## Spend gate
No generation is authorized yet.

Required explicit approval:
**39.60 credits for four Arthur / ElevenLabs TTS jobs.**
