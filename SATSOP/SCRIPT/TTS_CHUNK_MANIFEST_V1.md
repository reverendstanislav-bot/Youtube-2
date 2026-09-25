# SATSOP — TTS CHUNK MANIFEST V1

Updated: 2026-09-25

## Split rules

- source: `NARRATION_V3_EN_TTS_CLEAN.txt`;
- split only at paragraph boundaries;
- no sentence divided between chunks;
- maximum target: 4,800 characters;
- provider hard limit: 5,000 characters;
- order is immutable;
- concatenate in numeric filename order only.

## Chunks

| Order | File | Characters | Words | SHA-256 | Exact cost |
|---:|---|---:|---:|---|---:|
| 1 | `TTS_CHUNKS_V1/CHUNK_01.txt` | 4,501 | 680 | `1f5f523728ff68ef5c6557f240a267a14a9450bb88f6b93b02fbf9c664774ef1` | 13.65 |
| 2 | `TTS_CHUNKS_V1/CHUNK_02.txt` | 4,726 | 704 | `c8f7589e04c1a59c2cf0f96994aa4f86fb0f5451e993cb2c6e83f0feecb14d6e` | 14.25 |
| 3 | `TTS_CHUNKS_V1/CHUNK_03.txt` | 4,703 | 701 | `b26ec187d4adc3b8b27d0c81a37540db322c0926150c0e9c6607a27970fecd42` | 14.25 |
| 4 | `TTS_CHUNKS_V1/CHUNK_04.txt` | 1,532 | 224 | `dc0b4912729c213af9fb9c12ded950caf53ca3804fa7f39751b1e5b2d4f7dc92` | 4.65 |

## Boundary audit

- Chunk 01 begins: `Two cooling towers rise from the wooded hills...`
- Chunk 01 ends: `...who carries the next billion dollars of risk.`
- Chunk 02 begins: `Nor can the tower show how much remained outside it.`
- Chunk 02 ends: `...Bonneville would owe regardless of production.`
- Chunk 03 begins: `The gas option had risks, including fuel prices...`
- Chunk 03 ends: `...had value outside the original plan.`
- Chunk 04 begins: `Roads. Large buildings. Electrical connections.`
- Chunk 04 ends: `The infrastructure found another job.`

All four chunks end at complete paragraph boundaries. No production cue, heading, timestamp, table row, or markdown marker is present.
