# LAKE PEIGNEUR — WORD ALIGNMENT / TIMING QC V1

Canonical voice: Arthur / ElevenLabs. No paid generation was used for alignment.

## Acoustic alignment

- engine: faster-whisper small.en
- canonical normalized word tokens: **2,039**
- ASR word tokens: **2,039**
- direct acoustic matches: **1,984 / 2,039 = 97.30%**
- forced/interpolated canonical tokens: **55**
- mean direct-match probability: **0.9711**
- median direct-match probability: **0.9971**
- first aligned word: **00:00:00.000**
- last aligned word end: **00:16:08.080**
- lossless MP3 master runtime: **00:16:08.464**

Most non-direct matches are formatting equivalents: spelled-out numbers versus numeric ASR, hyphenation, spelling variants, or punctuation boundaries.

A second tiny.en acoustic spot pass verified the two potentially meaningful mismatches:
- “it had been mined” is present;
- “Water. Trees. Gardens.” is present.

Result: **PASS**.

WORD_TIMING_V1_CHUNK_01.csv through 04.csv are the canonical word-level timing files. No extra join padding has been added.
