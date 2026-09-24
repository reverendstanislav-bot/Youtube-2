# CHI-S01 — Native Vertical Asset Proof

Date: 2026-09-24
Status: **OWNER REVIEW**

This proof supersedes the rejected HIA blur-wrapper attempts.

## Source
- exact Chicago source-audio range: 11.800 -> 46.680
- duration: 34.880 s
- narration source: canonical Chicago long-form audio
- word timing: canonical `voice_words.json`

## Visual method
- 1080x1920 / 25 fps
- full-screen static portrait reframes
- existing approved Chicago long-form assets only
- no image generation
- no video generation
- no invented Shorts-only GFX
- no blurred background wrapper
- no horizontal floating frame
- hard cuts only
- no pan/slide transition
- no transition dissolve

## Provenance
Visible plaque rule:
- `HISTORICAL SOURCE` only on verified archive/map frames
- no `AI RECONSTRUCTION` plaque
- no `CONCEPT` plaque
- no `DOCUMENT` plaque

Raw archive sources are used for:
- `A03_ChicagoTunnelFieldsTrain.jpg`
- `A04_TunnelCoalDelivery.jpg`
- `A02_IllinoisTunnelMap1910.png`

This removes older embedded editorial labels from the processed map/archive assets.

## Captions
- rebuilt for mobile from canonical word-level timing
- white base text
- orange active spoken word
- no opaque caption card

## Sequence
1. surface Chicago
2. freight-tunnel reconstruction
3. historical train archive
4. historical coal-delivery archive
5. freight-transfer / basement reconstruction
6. basement connection reconstruction
7. 1910 map overview/detail
8. city/tunnel scale payoff
9. freight train payoff

## Technical QC
- 1080x1920: PASS
- 25 fps: PASS
- H.264 / yuv420p: PASS
- AAC 48 kHz stereo: PASS
- duration: 34.880 s
- full decode: PASS
- new generation: NONE
- output SHA256: `0ac501cc91e3cbe5352f1181b592877cbecd7672d266c1699c8e50836cc01736`

## GitHub
- Actions run: `36026353535`
- artifact: `chi-s01-native-vertical-asset-proof`
- artifact id: `10819534212`
- artifact digest: `sha256:fdd9f8cb7351bedeeda0a8245c8bdda7194d643b09395604fdb68d8e7af537fd`

Do not batch-scale to the remaining Shorts until owner visually approves this format.
