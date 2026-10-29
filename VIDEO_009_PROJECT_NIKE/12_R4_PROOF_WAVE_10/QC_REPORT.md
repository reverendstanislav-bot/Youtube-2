# VIDEO 009 R4 ImageGen Proof Wave 10 - QC

Date: 2026-10-28

Provider: built-in ImageGen

Cost: $0 external API spend; 0 Higgsfield credits

Scope: ten still images only; no video generation; no Script Lock changes

## Result

**PASS: 10 / 10 selected deliverables.**

All selected assets are independent 16:9 stills in the approved Camp Century charcoal/ink/transparent-watercolor family. Baked editorial highlights, arrows, labels, typography and motion accents are absent. Those remain reserved for native Resolve/Fusion layers.

## Asset QC

| ID | Revision | QC | Historical/style check | Subtitle-safe check |
|---|---:|---|---|---|
| I01 | R1 | PASS | Underground elevator and horizontal missile read clearly; coherent period machinery | Lower band remains non-critical |
| I02 | R1 | PASS | Cutaway storage magazine remains physically legible and source-informed | Lower band remains non-critical |
| I03 | R1 | PASS | Dispersed urban-defense site reads at a glance; no invented signage | Lower band remains non-critical |
| I05 | R3 | PASS | Ajax is a slender coaxial single-booster profile; Hercules reads as a larger clustered-booster profile | Broad blank lower field |
| I09 | R2 | PASS | Period analog radar room and conventional dish/mesh antennas; Arctic contamination removed | Lower foreground is non-critical |
| I10 | R1 | PASS | Early above-ground deployment/construction context is coherent | Lower foreground is non-critical |
| I12 | R2 | PASS | Dry-site Nike storage elevator; hatch, cradle and clustered rear booster geometry are credible | Lower concrete foreground is non-critical |
| I13 | R2 | PASS | Period acquisition/tracking radar forms and physically separated launch area are readable | Lower landscape is non-critical |
| I18 | R2 | PASS | Unmarked preserved Hercules hero image; no generated lettering remains | Lower apron is non-critical |
| D01 | R1 | PASS | Clean notebook/editorial plate with no baked annotations | Large blank field remains safe |

## Rejected attempts retained for audit

- `I05_R1_GEOMETRY`: incorrect multi-body missile comparison.
- `I05_R2_GEOMETRY`: Ajax booster/body alignment remained incorrect.
- `I09_R1_ARCTIC`: copied polar environment from style reference.
- `I12_R1_ARCTIC`: copied snow/ice into a temperate Nike site.
- `I13_R1_RADAR`: implausible giant rectangular radar array.
- `I18_R1_TEXT`: generated lettering on the missile body.

Rejected attempts are stored under `REJECTED/` and are not approved for edit use.

## Technical verification

- Ten selected originals preserved under `ORIGINALS/`.
- Ten delivery copies normalized with Lanczos scaling to 1920x1080 RGB24 PNG under `DELIVERY_1920x1080/`.
- Dimensions verified with FFprobe.
- SHA256 recorded in `SHA256_MANIFEST.csv`.
- Contact-sheet order, left-to-right: first row `I01 I02 I03 I05 I09`; second row `I10 I12 I13 I18 D01`.

## Gate

Proof wave is technically and creatively ready for owner review. Remaining 61 R4 jobs were not generated in this run.
