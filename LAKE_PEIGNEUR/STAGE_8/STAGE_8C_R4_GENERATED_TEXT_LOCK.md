# LAKE PEIGNEUR — STAGE 8C-R4 GENERATED TEXT LOCK

Updated: 2026-09-27

Status: **R4 PROMPTS REWRITTEN / READY FOR HARD QC / NO GENERATION AUTHORIZED**

Canonical pack:
`STAGE_8C_R4_144_PROMPT_PACK_TEXT_LOCK.csv`

## New production rule

Every generated frame now carries an explicit text mode:

- `RENDER_EXACT_TEXT` — all required visible wording must be generated directly into the image.
- `NO_TEXT` — the image must contain no readable text.

There are no blank text boxes, empty excerpt panels, placeholder legends, lorem ipsum, or assumptions that text will be added later.

## Counts

- DOCUMENT: 12 — all `RENDER_EXACT_TEXT`
- MAP / spatial GFX: 26 — all `RENDER_EXACT_TEXT`
- GENERATED GFX: 55 — all `RENDER_EXACT_TEXT`
- RECONSTRUCTION: 51 — all `NO_TEXT`
- TOTAL: 144

Text-bearing frames: **93**
Textless reconstructions: **51**

## DOCUMENT rule

Generated DOCUMENT frames are editorial evidence cards, not fake source pages.

They must:
- render the exact supplied title/source/factual wording directly in-frame;
- never leave a blank evidence box;
- never imitate a scanned government/legal/report page;
- never generate a fake seal, signature, letterhead, agency logo, quotation or dense body copy;
- use concise, mobile-readable factual typography.

## MAP / GFX rule

All required titles, labels, approximation qualifiers and numbers are generated in-frame.

The model must:
- render exactly the supplied wording;
- add no extra readable text;
- avoid placeholder callouts;
- preserve `≈`, `<`, `↔`, and `≠` where specified;
- preserve conceptual/estimated language where geometry is uncertain.

## RECONSTRUCTION rule

All 51 reconstruction prompts explicitly require:
- no text;
- no captions/titles/signage/watermarks;
- no flags;
- no eagles;
- no gear-symbol branding;
- no logos.

## Test-20 corrections baked into R4

- LP-DOC-006: no MSHA logo/letterhead/report-cover facsimile.
- LP-MAP-001: 52 and 7 must be visually dominant and correctly attached to underground/surface groups.
- LP-MAP-016 / LP-GFX-035: `≈150 FT — REPORTED ESTIMATE` must remain explicitly approximate.
- LP-MAP-023 / LP-GFX-051: hub + eight schematic connections only; no synthetic U.S./regional pipeline-route map.
- LP-REC-001: explicit no-flags rule.
- LP-REC-039: no invented locks, gates, dams or concrete canal-control structures.

## Structural validation

R4 structural pass:
- 144 rows present;
- 144 unique IDs;
- 93 text-bearing rows have `EXACT_TEXT_TO_RENDER`;
- 51 reconstruction rows are `NONE — NO TEXT`;
- no legacy blank/later-editor instructions remain;
- lower 15% subtitle-safe rule present throughout.

This file does **not** authorize any new generation or retry.
