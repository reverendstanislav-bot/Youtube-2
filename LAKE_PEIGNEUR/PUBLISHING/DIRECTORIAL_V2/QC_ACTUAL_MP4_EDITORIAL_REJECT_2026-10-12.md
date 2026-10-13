# Lake Peigneur Director V2 — independent ACTUAL-MP4 editorial QC — 2026-10-12

**Final verdict: EDITORIAL REJECT / PUBLICATION HOLD.** Do not designate Director V2 a final upload master. This is a QC of the existing finished file; it does not claim to be a full human frame-by-frame or listening audit.

## Verifiable exact master
- Release: https://github.com/reverendstanislav-bot/Youtube-2/releases/tag/hia-lake-peigneur-directorial-v2-master-20261012
- MP4: `HIA_LAKE_PEIGNEUR_DIRECTORIAL_V2_MASTER_1080P25.mp4`, **261150294 bytes**, SHA256 `045c4097c0bd3433b94ede5f0cfa85987df0f9605803c848eacaa1a95301da0a`.
- Original full render workflow run `38269998769`: **FAILURE** in QC because `qc_directorial_master.py` was absent from the workflow's checked-out commit, not because the render failed.
- Independent verification workflow `38276113252`: **SUCCESS**, actual V2 master downloaded and verified; `HIA_LAKE_V2_ACTUAL_QC_EVIDENCE.zip` includes actual MP4 contact sheets, with 13 × before/inside/end = 39 frames.
- Technically verified: full decode of 24711 frames at 1920×1080, 25 fps, duration 988.44 sec, >=400ms black events none, Arthur original AAC packet stream identical. These facts are NOT a creative/editorial certification.
- The current V2 file has no subtitle stream; the compositor also suppresses `<Caption`. White/orange word-following HIA caption canon is not fulfilled by this file.

## Actual rendered scene findings (based on 39 source frames; timings in master)
| Time | Severity | Actual visual problem | Corrective editorial decision |
| --- | --- | --- | --- |
| 00:02 | HOLD | 'THE LAKE BEGINS TO FAIL' appears as a tiny top-right overlay; weak mobile-readability and a second layer over the original shot. | Use one strong scene-driven opening, larger legible hierarchy; avoid redundant triple-line overlay. |
| 00:24 | REJECT | '52 PEOPLE BELOW' sits over a detailed multi-level mine diagram already showing its own large 52; the competing labels obscure the same evidence. | Keep the canonical source diagram and prioritize a single readable 52 / evacuation cue without duplicate lettering. |
| 03:25 | HOLD | 'THE CONNECTION' caption floats above generic flooding/mine reconstruction; no specific bore-to-mine linkage is demonstrated visually. | Use verified existing connection explanation and source-appropriate provenance, not simply a claim placed on reconstruction. |
| 05:21 | HOLD | Overlay says '52 MINERS' whereas source/script lock refers to 52 people underground; label risks overclaiming each person's role. | Use '52 PEOPLE UNDERGROUND', as established in source-safe wording. |
| 06:10 | REJECT | 'THE SHORE GIVES WAY' plays over an excavator/industrial waterfront with large distant industrial towers; does not reliably establish rural Lake Peigneur 1980 shoreline. | Replace mismatched industrial-context visual with appropriate existing lake/shore-collapse source, label reconstruction accurately. |
| 07:30 | HOLD | 'A SELF-WIDENING PATH' overlays a very busy synthetic cross-section; no stepwise guided explanation, headline repeats what narration does. | Expose the mechanics source stages one at a time without a generic headline obscuring the picture. |
| 09:14 | REJECT | 'THE FLOW REVERSED' is overlaid in low contrast on a very bright archival map and reveals reversal while Arthur is still establishing the normal flow. Map alone contains no verified animated direction evidence. | Delay claim to its spoken factual onset, improve contrast and identify actual source; do not add imaginary flow arrows. |
| 09:36 | **CRITICAL REJECT** | 'ROUGHLY 150 FEET / A temporary waterfall' appears over a two-panel **navigation-lock / shipping canal** graphic (NORMAL FLOW / REVERSED FLOW), not the described ~150-ft waterfall. Misleading illustration; source context does not show the claimed event. | Replace graphic with historically defensible river/lake level graphic or grounded evidence; no fictional navigation locks. |
| 10:40 | HOLD | 'ALL 52 ESCAPED' appears while picture still shows workers within flooded mine, instead of visual confirmation of evacuation; label itself reflects narration but action cue does not. | Align escape payoff with source of people exiting/surviving, not recurring flooded tunnel. |
| 11:10 | REJECT | 'CAUSE DISPUTED' overlays split industrial refinery images, implying a scene or facility reference not authenticated for the documented initiating mechanism. | Use factual evidence/mine-drill disputed pathways and attribution, not generic refineries. |
| 12:34 | PROVENANCE HOLD | 'CONNECTED — NOT EXPLAINED' overlays a stylized 'FEDERAL EVIDENCE CARD' bearing apparent report branding and page references. Contact sheet alone cannot authenticate such source-looking lettering. | Verify actual source references or clearly mark original editorial graphic; no fabricated document attribution. |
| 14:22 | **CRITICAL REJECT** | '8 MAJOR PIPELINES' appears over an illustrated hub with **six drawn radial connections**, contradicting the number asserted on the same shot. | Correct actual schematic geometry/data or remove the misleading literal six-arm diagram; cross-check original source. |
| 15:36 | HOLD | 'WHAT WE CANNOT SEE' is a small additional overlay at upper right of a pre-existing industrial scene, more slogan repetition than a stronger final idea. | Keep strong actual closing visuals and textless locked end screen; avoid a competing late overlaid slogan. |

## Fundamental regression vs D1
V2's workflow starts from the 141-slot HOLD12 canon and applies `DIRECTORIAL_V2/apply_directorial_v2.py`. It **does not apply** the existing `DIRECTORIAL_D1/apply_directorial_reedit.py`. Consequently it omits D1's five context-source repairs, 16 guided technical-diagram attention cues and eleven motivated hard cuts. V2 should not be called 'D1 plus improvements' or a superior successor.

## QC gate
- Technical video/audio: **PASS** (independent verifier; 39/39 selected samples extracted).
- 13 editorial callout scenes visually reviewed from actual MP4: **FAIL**, with explicit source-context, number/graphic and legibility errors.
- Seven motion windows: defined in Remotion; **not independently motion-QCed** by 39 static cue captures.
- Full 87-beat narration-to-picture listening/editorial check: **OPEN**, not falsely marked PASS.
- Closed captions: **MISSING FROM MP4** (separate publication subtitle preparation unverified).
- Latest D2 correction attempts: workflow runs `38277583175`, `38277884432`, `38278366114` all failed; no accepted D2 master was established from those runs.

**Disposition:** Keep D1 frozen as last technically finished coherent director baseline. Repair factual shot selection first, using the Git-backed `DIRECTORIAL_D2_REPAIR_PLAN.json` where provenance allows, then create a new complete master and conduct real picture/story QC. Do not publish V2 and do not infer PASS from file existence or ffmpeg decode.
