# Lake Peigneur — R4.1 Higgsfield TEST30 Visual QC

- Model: gpt_image_2_5
- Aspect: 16:9
- Submitted/completed: 30/30
- Preflight rate: 0.25 credit/image
- Calculated spend: 7.5 credits
- Retries: 0
- PASS: 26
- REJECT: 4
- HOLD: 0

## Rejects
- **LP-DOC-002** — Required labels duplicated in a second lower strip; redundant text/clutter.
- **LP-DOC-011** — Adds readable Diamond Crystal brand/logo text outside exact-text lock.
- **LP-MAP-023** — Text says 8 connections but only 6 connection nodes/lines are drawn.
- **LP-GFX-013** — Adds readable CH4 text not in exact-text lock.

## Systemic findings
The R4.1 fixes corrected the major previous TEST20 defects: fake MSHA-page styling, 52/7 hierarchy, ~150-ft uncertainty, flags, canal-control inventions, and scene/text mismatch errors.

Remaining failure modes are narrow:
1. duplicate required text;
2. extra readable text/logo/formula outside EXACT_TEXT_TO_RENDER;
3. diagram topology contradicting its own stated fact.

No rejected frame is authorized for retry by this QC file.

## Matrix
| Asset | QC | Reason |
|---|---|---|
| LP-DOC-001 | **PASS** | Exact text clean; HIA evidence card works. |
| LP-DOC-002 | **REJECT** | Required labels duplicated in a second lower strip; redundant text/clutter. |
| LP-DOC-005 | **PASS** | 52 evacuated / <1 hour / no fatalities read clearly. |
| LP-DOC-006 | **PASS** | Fake MSHA-report defect fixed; no agency facsimile. |
| LP-DOC-007 | **PASS** | Popular claim vs federal finding reads clearly. |
| LP-DOC-009 | **PASS** | Geology evidence frame is clear and on-style. |
| LP-DOC-011 | **REJECT** | Adds readable Diamond Crystal brand/logo text outside exact-text lock. |
| LP-DOC-012 | **PASS** | Settlement / layoffs / mine-not-restored hierarchy works. |
| LP-MAP-001 | **PASS** | 52 underground / 7 on platform fixed and dominant. |
| LP-MAP-004 | **PASS** | Clean regional orientation. |
| LP-MAP-007 | **PASS** | ≈1,228 ft vs 1,300-ft mine level reads correctly. |
| LP-MAP-008 | **PASS** | Hydraulic connection + unknown initiating geometry preserved. |
| LP-MAP-016 | **PASS** | ≈150 FT + REPORTED ESTIMATE fixed. |
| LP-MAP-017 | **PASS** | Myth vs evidence separation works. |
| LP-MAP-023 | **REJECT** | Text says 8 connections but only 6 connection nodes/lines are drawn. |
| LP-MAP-025 | **PASS** | Surface / hidden-infrastructure thesis works. |
| LP-GFX-001 | **PASS** | 7 / 52 hierarchy strong. |
| LP-GFX-008 | **PASS** | Scene/text repair works: small opening can enlarge. |
| LP-GFX-013 | **REJECT** | Adds readable CH4 text not in exact-text lock. |
| LP-GFX-035 | **PASS** | ≈150 FT / reported estimate reads correctly. |
| LP-GFX-036 | **PASS** | Salt mining vs gas storage continuity works. |
| LP-GFX-042 | **PASS** | Settlement ≠ scientific finding works. |
| LP-GFX-051 | **PASS** | Eight abstract connections visible; no fake route geography. |
| LP-GFX-055 | **PASS** | Final thesis frame is strong/readable. |
| LP-REC-001 | **PASS** | Flag defect fixed; clean pre-event platform shot. |
| LP-REC-009 | **PASS** | Drill and mine remain separate; no implied confirmed intersection. |
| LP-REC-027 | **PASS** | Evacuation reads urgent but not sensational. |
| LP-REC-039 | **PASS** | Canal defect fixed; no invented locks/gates/dams. |
| LP-REC-045 | **PASS** | Forensic reconstruction stays estimated and non-fake-document. |
| LP-REC-051 | **PASS** | Strong closing HIA cutaway. |
