# BIG MUSKIE — GENERATED REPLACEMENT QC V1

Date: 2026-09-25

Status: **2 PASS / 1 HOLD / 7 REJECT**

Scope: ten separately generated 16:9 replacement candidates for the non-final editor-native / blurry-document insert cleanup.

## QC results

| # | Beat / candidate | Result | Reason |
|---|---|---|---|
| 1 | BM-B076 — THE FAILURE PATH | REJECT | Central dragline is visibly crawler-mounted. Big Muskie / HIA machine language for this beat must not imply crawler propulsion. |
| 2 | BM-B083 — EPA TITLE IV — OFFICIAL SOURCE | REJECT | Generated fake official-looking EPA document/seal treatment creates false documentary provenance. Must use real EPA source material or a clearly explanatory non-document visual. |
| 3 | BM-B085 — PHASE I COMPLIANCE — 1995 | REJECT | Severe factual/render failure: timeline numerals read 1001 / 1005, and generated paper incorrectly mixes Title IV with the Surface Mining Control and Reclamation Act. |
| 4 | BM-B106 — WHAT SURVIVED | PASS WITH LABEL | Strong HIA composition; cable / chain / bucket-tooth callouts are legible and match locked narration. Must be labelled as HIA EXPLANATORY GFX, never as historical/source photography. |
| 5 | BM-B114 — A MACHINE DISAPPEARS, cinematic version | HOLD | Strong direction, but the generated machine/bucket geometry is generic enough that it should not be treated as literal Big Muskie evidence. Prefer candidate #10 for final integration. |
| 6 | BM-B038 — HOIST MECHANISM | REJECT | Clean visually but not source-grounded D03. It invents a generic crane/hoist technical drawing and therefore cannot replace documentary engineering evidence. |
| 7 | BM-B041 — MAIN-MOTION ENGINEERING | REJECT | Invented mechanical architecture; right-side assembly reads unlike the locked Bucyrus/dragline engineering lineage. Not source-grounded D03. |
| 8 | BM-B051 — WALKING SHOE MECHANISM | REJECT | Generated geometry uses a central hydraulic support concept and does not accurately represent the locked four-shoe / walking-dragline engineering lineage. |
| 9 | BM-B052 — STEPPING PROPULSION | REJECT | Visually strong but invented stepping geometry; cannot be presented as source-grounded D04 engineering evidence. |
| 10 | BM-B114 ALT — A MACHINE DISAPPEARS | PASS WITH LABEL | Best final B114 direction of the batch. Blueprint-memory + surviving-bucket metaphor fits HIA and avoids literal demolition. Must be labelled HIA EXPLANATORY GFX. |

## Document-source root cause confirmed

The blur in the old D03/D04 document beats is not a Remotion scaling bug alone.

GitHub artifact inspection confirmed:
- assembly-support `D03_page1.png`, `D03_page2.png`, `D04_page1.png`, `D04_page2.png` are only **82×120 px**;
- files named `D03_US3531088A_Hoist_Mechanism.pdf` and `D04_US3375892A_Stepping_Propulsion.pdf` inside the clean source archive are actually saved **HTML Google Patents pages**, not PDF binaries;
- each HTML file contains the canonical real PDF link:
  - `https://patents.google.com/patent/US3531088A/en.pdf`
  - `https://patents.google.com/patent/US3375892A/en.pdf`

Therefore the canonical fix for B038/B041/B051/B052 is:
- redownload the actual patent PDFs;
- render the relevant figures at high resolution;
- use real source linework as the visible base;
- optionally add restrained HIA framing/highlights;
- do not AI-invent the engineering drawing itself.

## Locked next state

Accepted now:
- BM-B106 candidate #4
- BM-B114 candidate #10

Hold:
- BM-B114 candidate #5

Must be rebuilt:
- BM-B076
- BM-B083
- BM-B085
- BM-B038
- BM-B041
- BM-B051
- BM-B052

No rejected candidate may enter canonical Picture V3.
