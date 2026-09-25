# LAKE PEIGNEUR — TTS GENERATION MANIFEST V1

Updated: 2026-09-25

Status: **ARTHUR TTS GENERATED — TECHNICAL QC PASS**

User approval:
explicit approval of **39.60 credits** for exactly four Arthur / ElevenLabs TTS jobs.

## Canonical voice / engine

- voice: **Arthur**
- voice_id: `30fc8796-ceb6-4a66-b3a7-4a145ef7f346`
- voice_type: `preset`
- model: `text2speech_v2`
- variant: `elevenlabs`

## Spend

Pre-generation balance: **1306.27 credits**  
Approved spend: **39.60 credits**  
Post-generation balance: **1266.67 credits**

Exactly four paid jobs were submitted.
No retry, alternate take, test take, image generation or video generation was submitted.

## Final payload / costs

| Chunk | Characters | Words | Cost |
|---:|---:|---:|---:|
| 01 | 3558 | 549 | 10.80 |
| 02 | 3180 | 519 | 9.60 |
| 03 | 3247 | 512 | 9.75 |
| 04 | 3136 | 465 | 9.45 |
| **Total** | **13121** | **2045** | **39.60** |

The chunk boundaries were adjusted after a tool safety filter rejected the initial larger second payload. No spoken wording was removed or added, and the final four payloads still cover the canonical clean text continuously.

## Jobs

| Chunk | Job ID | Provider duration |
|---:|---|---:|
| 01 | `d574664e-51e2-4849-a69a-c87f1c1e1e3c` | 253.20 s |
| 02 | `ce01243f-382c-4b47-a3e0-28ebed0447fd` | 240.56 s |
| 03 | `b40ac1de-544c-4bb9-ac3a-cd76d2d5ac19` | 238.24 s |
| 04 | `dac52f0e-1019-4687-a33d-fb72b0962650` | 236.32 s |

## Download URLs

Chunk 01:
https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_132708_d574664e-51e2-4849-a69a-c87f1c1e1e3c.mp3

Chunk 02:
https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_132923_ce01243f-382c-4b47-a3e0-28ebed0447fd.mp3

Chunk 03:
https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_132923_b40ac1de-544c-4bb9-ac3a-cd76d2d5ac19.mp3

Chunk 04:
https://d8j0ntlcm91z4.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/hf_20260925_132923_dac52f0e-1019-4687-a33d-fb72b0962650.mp3

Assembled master:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/c6302175-e05a-4602-8763-b1899d64fd61.mp3

TTS package ZIP:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/18415ac8-1d10-40c3-831b-8855c85a9aa0.zip

## Downloaded-file technical QC

ffprobe durations:
- CHUNK_01: **253.231020 s**
- CHUNK_02: **240.587755 s**
- CHUNK_03: **238.288980 s**
- CHUNK_04: **236.355918 s**

Lossless MP3 concat:
- runtime: **968.463673 s = 16:08.464**
- codec: MP3
- sample rate: 44.1 kHz
- mono
- 128 kbps
- SHA256: `1ae5c97d85b9cf2c10c438a2834d024776ea851a932a02aab2490860fa4afd13`

Decoded 48 kHz / 24-bit mono PCM:
- runtime: **968.427771 s**
- SHA256: `c360f4ecd5dd2f72602133ad3225ddc27a9ee62c2ac66bb6e1320a35ea533324`

Chunk SHA256:
- 01: `e68a4314b3533c0e9e944e3b12a6e436bed2f6371e60b234b6330ba919d74786`
- 02: `4e6b1c34d6f6d6ccce9bf01b86f6dbdc5cf102a569f41e02f93afbd2d4977a9b`
- 03: `88fccc465180754578d11c34c848fcba037e4f8eb4c9bb5a329ca7ab90056bc7`
- 04: `d0ed66d897622a6df96a092107d1db5a48a73f11cac8e927e050e2156510443b`

Decode check:
**PASS on all 4 chunks + MP3 master + PCM master.**

Measured full-master loudness:
- integrated: **-14.5 LUFS**
- loudness range: **3.1 LU**
- true peak: **-0.5 dBFS**

No loudness normalization has been rendered into the canonical TTS master.

## Join sanity

Natural silence exists around all three chunk boundaries:
- join 1: ~149 ms low-level silence;
- join 2: ~615 ms + ~85 ms low-level regions;
- join 3: ~112 ms low-level silence.

No extra paid regeneration was required.

## Next

1. pronunciation/content listen QC;
2. word-level alignment/transcript;
3. exact editorial timing lock;
4. Stage 7 visual beat map.

Any paid retry requires a new explicit approval.
