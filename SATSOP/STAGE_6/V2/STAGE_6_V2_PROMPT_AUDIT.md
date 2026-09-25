# SATSOP — STAGE 6 V2 PROMPT AUDIT

Status: **PASS FOR REFERENCE ACQUISITION AND SECOND TEST — NOT AUTHORIZED FOR FULL GENERATION**

## Completeness

- generation-led beats represented: **68/68**;
- unique prompt IDs: **68**;
- unique beat IDs: **68**;
- unique final prompt strings: **68**;
- prompts materially different from V1: **68/68**;
- locked passing outputs: **5**;
- rewritten pending prompts: **63**;
- missing reference assignments: **0**;
- prompt grammar families: **54**;
- prompt length range: **799–901 characters**;
- maximum remaining full-queue cost: **31.50 credits**;
- generation authorized now: **no**.

## Design corrections

- The narration sentence is no longer pasted into the model prompt.
- Every prompt names one literal visual proposition.
- Era and operating state are explicit.
- Exact words, dates, quantities, arrows and maps are deferred to editorial overlays.
- Map/GFX scenes use purpose-built plates rather than documentary photographs.
- Preservation and modern reuse prohibit construction activity.
- Satsop-specific architecture requires real reference input.
- Five accepted outputs retain job IDs and SHA-256 hashes and cannot be regenerated accidentally.

## Hard gate

`BLOCKED_UNTIL_REAL_MEDIA_IDS_ATTACHED` is an execution rule. R01–R07 text labels are insufficient. Before any second test, the required images must be authenticated, rights-logged, uploaded to Higgsfield and recorded as concrete media IDs in a reference manifest.
