# BIG MUSKIE — WORD ALIGNMENT / JOIN QC V1

Canonical voice: Arthur / ElevenLabs. No new generation used for alignment.

## Acoustic alignment
- Chunk 1 direct matches: 743/794 = 93.58%
- Chunk 2: 714/771 = 92.61%
- Chunk 3: 727/786 = 92.49%
- Chunk 4: 645/668 = 96.56%
- Remaining tokens are forced/interpolated between neighboring acoustic anchors; canonical spelling always comes from V3 text.

## Join normalization
- J1 raw speech gap ≈0.13s; add 0.52s → target total ≈0.65s at chapter transition.
- J2 raw speech gap ≈0.02s; add 0.28s → target total ≈0.30s for logical chain.
- J3 raw speech gap ≈0.70s; no added silence.

Final chunk start offsets: 0.000 / 375.000 / 749.440 / 1119.920 s.
Canonical join-normalized runtime: **1426.400 s = 23:46.400**.

This supersedes the earlier 23:45.722 MP3 packet-concat measurement for editorial timing.
