# LAKE PEIGNEUR — HIGGSFIELD TEST 20 / VISUAL QC V1

Updated: 2026-09-27

Status: **TEST BATCH COMPLETE / NO RETRIES AUTHORIZED**

Canonical prompt source:
`STAGE_8C_R3_144_PROMPT_PACK.csv`

## Paid preflight / execution

- Model requested: `gpt_image_2_5`
- Aspect: 16:9
- Jobs: **20**
- Higgsfield exact estimate at submission: **0.25 credit/image**
- Batch calculated cost: **5.0 credits**
- Jobs completed: **20/20**
- Submission failures: **0**
- Retries: **0**

The 20-frame test was deliberately balanced:
- 5 DOCUMENT
- 5 MAP / spatial GFX
- 5 GENERATED GFX
- 5 RECONSTRUCTION

## QC verdict

- **PASS: 12/20**
- **REJECT: 8/20**
- **HOLD: 0**

No rejected image is authorized for retry by this QC file.

## Per-frame QC

| Asset | Job ID | QC | Reason |
|---|---|---|---|
| LP-DOC-001 | `2d989a71-f173-41b5-990f-b32e07c3e7e7` | **PASS** | HIA evidence-card treatment works; blank evidence zone preserved; editorial framing is clearly not a fake source page. |
| LP-DOC-004 | `ec1948c7-8811-438e-b687-ae228148a6b8` | **PASS** | Federal-evidence layout works; source anchor visible; no fabricated quotation/body paragraph dominates the frame. |
| LP-DOC-006 | `953cd855-be9b-4e40-b792-402dc1e9085e` | **REJECT** | Looks too much like a fabricated official MSHA report/page with agency-style document facsimile. Must be an HIA editorial source card, not a fake report. |
| LP-DOC-009 | `b5906db0-3cf5-4e6b-902e-dc3ab8f2103c` | **PASS** | Strong geology evidence visualization; readable hierarchy; distinct from fake scanned-document styling; subtitle-safe. |
| LP-DOC-012 | `bb6c0c6e-4d61-4354-ad30-d97fa825aed1` | **PASS** | $12.8M and ~250 employees are clear and separated; strong HIA economic-consequence frame. |
| LP-MAP-001 | `93cbffb4-2ac0-4b7f-8ff9-ee88c901a50e` | **REJECT** | Misses required 52-underground / 7-surface count anchors and substitutes generic explanatory text/icons; narration match too weak. |
| LP-MAP-006 | `003fd741-3caf-46c6-9179-42d33e29d3d2` | **PASS** | Good conceptual vertical relationship; drill and mine are visually separate; no confirmed intersection; uncertainty preserved. |
| LP-MAP-010 | `0083792c-b39a-477b-8bf5-2ec5c41c0ea6` | **PASS** | Multi-level mine occupancy concept reads clearly and remains conceptual rather than a literal surveyed mine plan. |
| LP-MAP-016 | `344937b2-3789-4faf-94a4-4ecd4da6999e` | **REJECT** | Renders 150 ft too much like an exact elevation value. Must explicitly say ≈150 ft / roughly 150 ft / reported estimate. |
| LP-MAP-023 | `5e864bdd-29f6-4120-897e-1d3d4aaced7a` | **REJECT** | Invents specific-looking pipeline routes/locations and labels. Current JISH graphic must be generic or source-traced, not a synthetic exact network map. |
| LP-GFX-001 | `c8135137-5c54-49c3-8973-f474e674c206` | **PASS** | 52 underground / 7 surface hierarchy is immediate, visually strong and on-script. |
| LP-GFX-010 | `33e0a262-b690-44dd-ae5b-53352dbf0bc0` | **PASS** | ≈1,228 ft and 1,300-ft mine level are both clear; does not imply a 1,300-ft-deep lake; strong technical frame. |
| LP-GFX-022 | `cbd8907a-7fd7-4aa6-864e-6090994cfb5b` | **PASS** | Qualitative feedback-loop visual is clear and does not introduce unsupported numeric hydraulics. |
| LP-GFX-035 | `6ae9a0de-c452-44cc-b275-7bf31db559ce` | **REJECT** | Shows ~150 ft as a quasi-exact vertical dimension and does not clearly communicate 'reported estimate'; needs explicit uncertainty treatment. |
| LP-GFX-051 | `370b6b7b-c712-4961-adc8-0eedba73167c` | **REJECT** | Synthetic U.S.-wide pipeline-route map looks factual but routes are not source-traced. Replace with generic 8-connection hub graphic, no literal national routes. |
| LP-REC-001 | `e9f574d0-a8c0-4620-ad9a-dcabfa154690` | **REJECT** | Visible U.S. flag violates HIA visual lock. Reconstruction base must explicitly prohibit flags/eagles/gears; otherwise composition is usable. |
| LP-REC-009 | `862db854-5244-468b-a75e-518f04734288` | **PASS** | Vertical drill and horizontal mine remain visually separate; no confirmed intersection; strong conceptual reconstruction. |
| LP-REC-027 | `609c53b3-9c77-4c60-9856-dada3e060eb7` | **PASS** | Crew evacuation reads clearly without panic spectacle; period industrial look is acceptable; subtitle-safe. |
| LP-REC-039 | `1ce8f10f-5921-4870-b5f4-0d2db537c323` | **REJECT** | Adds specific concrete/industrial canal structures that are not source-locked and can imply a lock/gate system. Use natural/simple canal banks and reversed current only. |
| LP-REC-051 | `07c42c0d-310a-46ff-9f9e-874829f5b4ae` | **PASS** | Strong final HIA cutaway: calm surface above hidden industrial layers; distinct closing composition and no exact breach claim. |

## Systemic findings

1. **HIA palette / overall art direction works.** The batch reads as the same channel family across evidence cards, diagrams and reconstructions.
2. **Generated DOCUMENT frames need a stricter anti-facsimile rule.** Do not allow model-generated official report pages, seals/logos, agency letterheads, or fake body text. Use HIA editorial evidence cards with source labels and blank excerpt zones.
3. **Current pipeline visuals need a strict no-fake-route rule.** The fact is '8 major pipelines'; generated exact-looking U.S./regional route geometry is prohibited unless traced from a cleared factual map.
4. **Approximate quantities must visually stay approximate.** The ~150-ft waterfall/elevation claim must render as '≈150 ft reported' / 'roughly 150 ft', never as a precise measured dimension.
5. **RECONSTRUCTION global base needs HIA iconography exclusions restored:** no U.S. flag, eagle, gear-symbol branding.
6. **Canal reconstructions must avoid invented civil works.** No lock/gate/concrete-control structure unless source-locked.
7. Subtitle-safe lower zone worked across the test set.

## Required prompt-pack repairs before larger generation

Global:
- add `no flags, no eagles, no gear-symbol iconography` to all RECONSTRUCTION prompts;
- add `no official-agency facsimile / no agency logo / no report-page imitation` to all DOCUMENT prompts;
- add `no synthetic exact pipeline routes or named connection geography unless source-traced` to JISH pipeline prompts;
- force approximate labels for the ~150-ft claim;
- add `no invented canal locks/gates/control structures` to canal-reversal reconstructions.

Targeted rewrites:
`LP-DOC-006, LP-MAP-001, LP-MAP-016, LP-MAP-023, LP-GFX-035, LP-GFX-051, LP-REC-001, LP-REC-039`.

Do not generate the next paid batch until these prompt repairs are applied and re-QC'd.
