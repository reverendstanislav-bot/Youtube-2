# BIG MUSKIE — YOUTUBE REPAIR MASTER 1440P — QC

Date: 2026-10-03

## Status

**REPAIR MASTER PHYSICALLY CREATED / VERIFIED / READY AS CURRENT RECOVERY UPLOAD COPY**

This file is a recovery/upscale master made from the surviving low-bitrate 1080p final copy. It does **not** replace the missing original high-quality Codex-final binary as an archival source.

## Source binary

`BIG MUSKIE - ГОТОВОЕ ВИДЕО.mp4`

- SHA256: `ec6a8d3f4ab4091af4f1267b3dc22bb3d8968eb1b4e1dcef9217f522a52ae8ff`
- size: 215,611,833 bytes
- geometry: 1920×1080
- frame rate: 25 fps
- runtime: 1426.400 s
- video bitrate: ~1.14 Mb/s
- audio: AAC / 48 kHz / mono / ~64.8 kb/s

The source remains **REJECTED as the direct final YouTube upload** because of heavy compression.

## Verified repaired upload binary

`BIG_MUSKIE_YOUTUBE_REPAIR_MASTER_1440P.mp4`

- SHA256: `801367340431b179d102efd3b9c2d847dab904c8b202eb15a74a24a44eca537a`
- size: **615,912,469 bytes**
- geometry: **2560×1440**
- frame rate: **25 fps**
- video frames: **35,660**
- runtime: **1426.400 s / 23:46.400**
- video: H.264 High / CRF 14 / tune grain
- video bitrate: **3,383,467 b/s**
- container bitrate: **3,454,360 b/s**
- audio: original AAC copied unchanged, 48 kHz mono, 64,799 b/s
- MP4 faststart: enabled

## Repair processing

Deterministic FFmpeg repair path:
- light compression-noise cleanup;
- Lanczos upscale from 1920×1080 to 2560×1440;
- mild luma sharpening;
- original AAC audio stream copied without re-encoding.

No image generation.
No video generation.
No Higgsfield credits.
No TTS credits.

## QC

- physical output exists: **PASS**
- ffprobe parse: **PASS**
- 2560×1440: **PASS**
- 25 fps: **PASS**
- 35,660 video frames: **PASS**
- exact 1426.400 s runtime: **PASS**
- audio 48 kHz mono preserved: **PASS**
- full end-to-end decode: **PASS — 0 errors**
- representative frame inspection across early / middle / late film: **PASS for repair-master purpose**

## Important limitation

This repair master cannot recreate fine detail already destroyed by the surviving low-bitrate source. It is the best verified recovery upload binary currently available from the surviving final copy.

The missing original high-quality Codex-final master remains a separate archival gap.

## Storage boundary

The repaired MP4 was created as a ChatGPT conversation artifact on 2026-10-03. The 615.9 MB binary is **not physically mirrored inside GitHub Releases/Actions by this commit**. Git records its exact filename, size, technical properties and SHA256 so a downloaded copy can be verified byte-for-byte before local use.
