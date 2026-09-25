# LAKE PEIGNEUR — TTS CHUNK MANIFEST V1

Updated: 2026-09-25
Status: **FINAL PREFLIGHT SPLIT / NOT GENERATED**

Source: `SCRIPT/NARRATION_V2_EN_TTS_CLEAN.txt`

Rules:
- paragraph boundaries only;
- no sentence split;
- provider hard limit <5,000 chars;
- production target <=3,600 chars.

| Chunk | Chars | Words | Exact cost |
|---|---:|---:|---:|
| 01 | 3,558 | 549 | 10.80 |
| 02 | 3,532 | 576 | 10.65 |
| 03 | 3,587 | 556 | 10.80 |
| 04 | 2,444 | 364 | 7.35 |
| **Total** | **13,121** | **2,045** | **39.60** |

Boundary audit:
- 01 begins: `On November 20, 1980, a drilling crew on Lake Peigneur had a problem.`
- 01 ends: `Now water was entering that system.`
- 02 begins: `The mine had only one safe strategy left: move people out before flooding, ground failure or loss of access turned distance into a trap.`
- 02 ends: `Those two systems were now coupled.`
- 03 begins: `The faster the lake fed the failure, the more the failure could change the route available to the lake.`
- 03 ends: `Diamond Crystal originally sued Texaco for two hundred and sixty million dollars.`
- 04 begins: `In 1983, Diamond Crystal accepted a thirty-two-million-dollar settlement from Texaco and Wilson Brothers.`
- 04 ends: `And the systems we cannot see can be the systems that matter most.`

The clean master has 7 extra formatting characters relative to the four independent payloads: 6 characters from three paragraph separators at job boundaries plus one final newline.

Embedded Shorts are not spoken twice in the long-form master.

Any wording change invalidates this count and requires a fresh cost preflight.
