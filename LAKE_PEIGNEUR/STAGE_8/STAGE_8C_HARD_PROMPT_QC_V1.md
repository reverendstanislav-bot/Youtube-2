# LAKE PEIGNEUR — STAGE 8C HARD PROMPT QC V1

Updated: 2026-09-27

Status: **QC COMPLETE / PAID GENERATION NOT AUTHORIZED**

Scope: all 100 rows in `STAGE_8C_GENERATED_ASSET_PROMPT_PACK.csv`.

## Executive verdict

The 100-row pack is **not approved for a 100-job / 50-credit Higgsfield run**.

The controlling Stage 8C density lock separates:
- **55 EDITOR GFX / diagrams / typography**
- **45 unique reconstruction images**

Therefore the 55 `LP-GFX-*` rows are treated as **editor-native build specifications, not paid image-generation jobs**. This restores the correct prospective paid-image ceiling to:

**45 reconstruction jobs × 0.5 credit = 22.5 credits maximum before any retries.**

No generation is authorized by this QC.

## Global checks

All 100 prompts mechanically include:
- 16:9 / 1920×1080;
- HIA palette;
- lower 15% caption-safe instruction;
- no black caption box;
- no fake archival damage/date stamp/newspaper;
- text restriction;
- no duplicate asset IDs.

Prompt-template warning:
- all 55 GFX prompts share one identical global template;
- all 45 reconstruction prompts share one identical global template.

This is acceptable only if the scene-specific objective is strong enough. It is **not** sufficient justification to turn the 55 editor-native GFX into paid image jobs.

## Results

### GFX / editor-native
- 49 PASS as editor-native build specs.
- 6 require content/source wording fixes before build.
- **0 / 55 authorized as paid Higgsfield jobs.**

### Reconstruction / actual paid-image candidates
- 25 PASS generation candidates.
- 2 PASS with explicit reference-only source guard.
- 14 rights HOLD because an Appendix EE frame is still conditional.
- 4 require prompt/content/source rewrite (some also have Appendix EE holds).

Paid generation gate remains **CLOSED** until the HOLD/REWRITE reconstruction rows are repaired or their conditional references are removed/cleared.

## Critical cross-pack findings

1. **Stage 8C budget contradiction:** the later prompt-pack note incorrectly converts 55 editor-native GFX into generated images. The earlier density lock is internally consistent and should control: only 45 unique reconstructions are paid images.
2. **Appendix EE:** 15 reconstruction prompts reference individual EE frames. Stage 8 rights audit says these remain CONDITIONAL_USE until item-level provenance is verified. They must not be silently attached as generation references or copied compositionally.
3. **Reference-only sources:** UPI / 64 Parishes / corporate imagery may supply facts, not visual-reference pixels.
4. **Causation/geometry:** exact underground breach geometry remains blocked. Any cutaway must show uncertainty rather than a definitive contact point.
5. **Caption safety:** all 100 prompts explicitly preserve the lower 15%; PASS at prompt level.
6. **HIA style:** palette and anti-PowerPoint/anti-fake-archive constraints are present throughout; PASS at prompt level.

## 100-row QC matrix

| Asset | Type | Beat(s) | QC | Finding |
|---|---|---|---|---|
| LP-GFX-001 | GENERATED_GFX | LP-B003 | **FIX EDITOR SPEC** | SOURCE FIX — number 7 is not supported by LP-S02; add the locked rig-crew source (LP-S11/factual source only) or remove 7 from the generated/base spec. |
| LP-GFX-002 | GENERATED_GFX | LP-B004 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-003 | GENERATED_GFX | LP-B006 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-004 | GENERATED_GFX | LP-B008 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-005 | GENERATED_GFX | LP-B009 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-006 | GENERATED_GFX | LP-B011 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-007 | GENERATED_GFX | LP-B011 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-008 | GENERATED_GFX | LP-B012 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-009 | GENERATED_GFX | LP-B013 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-010 | GENERATED_GFX | LP-B015 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-011 | GENERATED_GFX | LP-B015 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-012 | GENERATED_GFX | LP-B016 | **FIX EDITOR SPEC** | PRECISION FIX — render the drill depth as ≈1,228 ft / roughly 1,228 ft; do not present 1,228 as an exact surveyed depth. |
| LP-GFX-013 | GENERATED_GFX | LP-B017 | **FIX EDITOR SPEC** | UNCERTAINTY FIX — explicitly depict a non-exact conceptual water path / uncertainty zone; no single verified ingress route. |
| LP-GFX-014 | GENERATED_GFX | LP-B019 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-015 | GENERATED_GFX | LP-B020 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-016 | GENERATED_GFX | LP-B021 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-017 | GENERATED_GFX | LP-B022 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-018 | GENERATED_GFX | LP-B025 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-019 | GENERATED_GFX | LP-B027 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-020 | GENERATED_GFX | LP-B034 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-021 | GENERATED_GFX | LP-B037 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-022 | GENERATED_GFX | LP-B038 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-023 | GENERATED_GFX | LP-B038 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-024 | GENERATED_GFX | LP-B039 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-025 | GENERATED_GFX | LP-B039 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-026 | GENERATED_GFX | LP-B040 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-027 | GENERATED_GFX | LP-B041 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-028 | GENERATED_GFX | LP-B042 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-029 | GENERATED_GFX | LP-B043 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-030 | GENERATED_GFX | LP-B045 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-031 | GENERATED_GFX | LP-B046 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-032 | GENERATED_GFX | LP-B047 | **FIX EDITOR SPEC** | WORDING FIX — replace quantitative-sounding 'flow rate versus pathway enlargement' with qualitative 'increasing flow ↔ pathway enlargement' unless a measured rate is sourced. |
| LP-GFX-033 | GENERATED_GFX | LP-B048 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-034 | GENERATED_GFX | LP-B049 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-035 | GENERATED_GFX | LP-B050 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-036 | GENERATED_GFX | LP-B051 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-037 | GENERATED_GFX | LP-B054 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-038 | GENERATED_GFX | LP-B057 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-039 | GENERATED_GFX | LP-B058 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-040 | GENERATED_GFX | LP-B060 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-041 | GENERATED_GFX | LP-B062 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-042 | GENERATED_GFX | LP-B064 | **FIX EDITOR SPEC** | LABEL FIX — an isolated '1300 ft' risks repeating the viral lake-depth misconception; editor label must explicitly read '1,300-ft mine level' / 'estimated drill-hole location near mine level'. |
| LP-GFX-043 | GENERATED_GFX | LP-B065 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-044 | GENERATED_GFX | LP-B066 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-045 | GENERATED_GFX | LP-B067 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-046 | GENERATED_GFX | LP-B068 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-047 | GENERATED_GFX | LP-B069 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-048 | GENERATED_GFX | LP-B070 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-049 | GENERATED_GFX | LP-B071 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-050 | GENERATED_GFX | LP-B072 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-051 | GENERATED_GFX | LP-B074 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-052 | GENERATED_GFX | LP-B078 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-053 | GENERATED_GFX | LP-B078 | **FIX EDITOR SPEC** | CURRENT-CONTEXT FIX — '8 pipelines' must be presented as a current/source-dated ONEOK fact, not a timeless historical property. |
| LP-GFX-054 | GENERATED_GFX | LP-B083 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-GFX-055 | GENERATED_GFX | LP-B087 | **PASS — EDITOR NATIVE** | Narration/source/HIA/subtitle-safe checks pass. Do not spend Higgsfield credits on this asset. |
| LP-REC-001 | RECONSTRUCTION | LP-B001-B002 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-002 | RECONSTRUCTION | LP-B002 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-003 | RECONSTRUCTION | LP-B002 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-004 | RECONSTRUCTION | LP-B003 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-005 | RECONSTRUCTION | LP-B004 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-006 | RECONSTRUCTION | LP-B007 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-007 | RECONSTRUCTION | LP-B010 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-008 | RECONSTRUCTION | LP-B014 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-009 | RECONSTRUCTION | LP-B014-B015 | **REWRITE REQUIRED** | CONTENT FIX — the cutaway must NOT show the drill intersecting a mine room. Show vertical drill and horizontal mine as separate systems with an explicitly uncertain/non-contact relationship. |
| LP-REC-010 | RECONSTRUCTION | LP-B015 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-011 | RECONSTRUCTION | LP-B016 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-012 | RECONSTRUCTION | LP-B016 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-013 | RECONSTRUCTION | LP-B017 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-014 | RECONSTRUCTION | LP-B018 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-015 | RECONSTRUCTION | LP-B020 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-016 | RECONSTRUCTION | LP-B021-B022 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-017 | RECONSTRUCTION | LP-B023 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-018 | RECONSTRUCTION | LP-B023 | **REWRITE REQUIRED** | CONTENT FIX — 'marked exit route' invents signage/wayfinding detail. Change to workers moving toward known egress without fabricated signs. |
| LP-REC-019 | RECONSTRUCTION | LP-B024 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-020 | RECONSTRUCTION | LP-B024 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-021 | RECONSTRUCTION | LP-B025 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-022 | RECONSTRUCTION | LP-B026 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-023 | RECONSTRUCTION | LP-B027 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-024 | RECONSTRUCTION | LP-B028 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-025 | RECONSTRUCTION | LP-B029 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-026 | RECONSTRUCTION | LP-B030 | **PASS WITH SOURCE GUARD** | Narration/HIA/subtitle-safe pass. LP-S11 is factual reference only: no UPI image/screenshot may be attached or visually copied. |
| LP-REC-027 | RECONSTRUCTION | LP-B030 | **PASS WITH SOURCE GUARD** | Narration/HIA/subtitle-safe pass. LP-S11 is factual reference only: no UPI image/screenshot may be attached or visually copied. |
| LP-REC-028 | RECONSTRUCTION | LP-B031 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-029 | RECONSTRUCTION | LP-B032 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-030 | RECONSTRUCTION | LP-B033 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-031 | RECONSTRUCTION | LP-B035 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-032 | RECONSTRUCTION | LP-B036 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-033 | RECONSTRUCTION | LP-B037-B038 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-034 | RECONSTRUCTION | LP-B043 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-035 | RECONSTRUCTION | LP-B044 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-036 | RECONSTRUCTION | LP-B047 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-037 | RECONSTRUCTION | LP-B052 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-038 | RECONSTRUCTION | LP-B053 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-039 | RECONSTRUCTION | LP-B056 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-040 | RECONSTRUCTION | LP-B059 | **REWRITE REQUIRED** | SOURCE FIX — seven rig workers are not grounded by LP-S02. Use the locked contemporary/source record for the seven-man drilling crew; do not use copyrighted imagery as a visual reference. |
| LP-REC-041 | RECONSTRUCTION | LP-B060 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-042 | RECONSTRUCTION | LP-B063 | **REWRITE + RIGHTS HOLD** | CONTENT + RIGHTS FIX — do not assert a visibly flooded shaft/entrance unless directly sourced; depict inaccessible post-event mine access/evidence loss generically. EE-136 remains conditional. Appendix EE source is conditional; do not attach/use as visual reference until item-level provenance clears. |
| LP-REC-043 | RECONSTRUCTION | LP-B064-B068 | **PASS — GENERATION CANDIDATE** | Narration/source/HIA/subtitle-safe checks pass. |
| LP-REC-044 | RECONSTRUCTION | LP-B073-B076 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |
| LP-REC-045 | RECONSTRUCTION | LP-B081-B087 | **RIGHTS HOLD** | Prompt/scene is narration-aligned, but Appendix EE source is CONDITIONAL_USE. Until item-level provenance clears, generate only from cleared textual/federal facts and do not attach/copy the EE image. |

## Next gate

Before any paid run:
1. rewrite the 6 flagged editor-native GFX specs;
2. rewrite the 3 non-EE reconstruction issues;
3. resolve/remove conditional EE visual-reference usage across 15 reconstruction prompts (including REC-042);
4. re-QC only the changed rows;
5. then present the exact paid preflight for the remaining **45 reconstruction jobs maximum**.

No paid retries and no video generation.
