# BIG MUSKIE — STAGE 8 V2

Status: **116-BEAT V2 CLEAN REMAP COMPLETE — PROMPT/COST REBUILD NEXT**

Source basis:
- physical archive: `BIG_MUSKIE_FULL_SOURCE_ARCHIVE_V2_CLEAN.zip`
- archive SHA-256: `7e453f165e72ad608324fd285195211d8b3eb20d45844b15850ab17ad510c979`
- canonical runtime: **23:46.400**

Coverage:
- V2_REAL_DIRECT: **38**
- V2_DOCUMENT_DIRECT: **32**
- V2_REAL_CONTEXT: **7**
- V2_GFX_SUPPORTED: **8**
- SOURCE_CAPTURE_GFX: **18**
- GENERATE_UNIQUE: **9**
- GENERATE_REUSE: **4**

Thus:
- physical V2 closes **85/116** beats without new external capture or AI;
- **18/116** require source capture + GFX, not AI imagery;
- **13/116** require reconstruction coverage;
- those 13 reconstruction beats require **9 unique generated stills**.

Current paid-generation authorization: **0**.

The old Stage 8 V1 prompt pack and cost preflight are superseded and must not be used.


## VISUAL DIVERSITY OVERRIDE

Stage 8 V2 established factual/source coverage, but it did not sufficiently penalize repeated archive use.

The later `VISUAL_DIVERSITY_PASS` is authoritative for production shot count and anti-repeat planning.

Current production baseline:
- 116/116 beats assigned a concrete composition;
- 20 REAL;
- 11 REAL_CONTEXT;
- 8 DOC;
- 55 GFX_GAP;
- 22 GEN_GAP;
- visible R/C/D asset reuse maximum: 2;
- reuse violations: 0.

The former 9-generated-image estimate is superseded.
