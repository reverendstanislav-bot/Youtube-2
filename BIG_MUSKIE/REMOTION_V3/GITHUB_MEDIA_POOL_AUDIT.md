# BIG MUSKIE — GITHUB-ONLY MEDIA POOL AUDIT

Date: 2026-09-25

Status: **GITHUB ARTIFACT INVENTORY VERIFIED — FINAL PICTURE BINARY GAP IDENTIFIED**

Audit workflow:
- `Audit Big Muskie production media artifacts`
- run: `36174431632`
- conclusion: **PASS**
- audit artifact: `BIG_MUSKIE_GITHUB_MEDIA_POOL_AUDIT`

## What is physically present in GitHub Actions artifacts

### BIG_MUSKIE_LOCKED_MEDIA_PAYLOAD
- `BIG_MUSKIE_ARTHUR_CANONICAL_23m46p400.wav` — 205,401,702 bytes
- `BIG_MUSKIE_FULL_SOURCE_ARCHIVE_V2_CLEAN.zip` — 57,557,895 bytes
- Arthur MP3 chunks 01–04
- source/audio SHA files

### BIG_MUSKIE_SOURCE_ARCHIVE_V2_CLEAN
- clean source archive ZIP
- source SHA file

### BIG_MUSKIE_ARTHUR_CHUNKS
- chunk01.mp3
- chunk02.mp3
- chunk03.mp3
- chunk04.mp3
- chunk hashes

### BIG_MUSKIE_RECON_BASE7
- GEN01.png
- GEN02.png
- GEN03.png
- GEN04.png
- GEN11.png
- GEN15.png
- GEN17.png
- SHA256SUMS.txt

### BIG_MUSKIE_ASSEMBLY_SUPPORT
- FINAL_116_BEAT_ASSET_LOCK_V1.csv
- D03 page 1 / page 2
- D04 page 1 / page 2
- hashes

## What is NOT physically present in GitHub

The audit proves GitHub does **not** currently contain the complete final pixel media required to reproduce Picture V2 exactly:

- the final 55/55 physical GFX PNG package;
- the 15 final replacement reconstruction PNGs beyond base7;
- the 10 final cinematic V2 replacement PNG binaries;
- `BIG_MUSKIE_FULL_PICTURE_ASSEMBLY_V1_1080P.mp4`;
- `BIG_MUSKIE_FULL_PICTURE_ASSEMBLY_V2_1080P.mp4`.

The repository contains their mapping/QC/locks/hashes, but not all final binary pixels.

## Important boundary

Do **not** silently substitute:
- rejected GEN01–GEN22 originals for the final reconstruction replacements;
- V1 GFX for the accepted V2 cinematic replacements;
- regenerated images.

That would violate the locked production state.

## GitHub-only V3 runner

The durable runner remains the required path.

It must consume a GitHub-hosted exact final picture input/media pack, then:
1. restore the locked media pool;
2. build the 116-beat frame-quantized Remotion V3;
3. eliminate V2 boundary flashes by construction;
4. mux canonical Arthur;
5. perform frame/runtime/decode/audio QC;
6. upload the finished V3 MP4 as a GitHub Actions artifact.

Dropbox is not part of this pipeline.
No paid/new generation is authorized.
