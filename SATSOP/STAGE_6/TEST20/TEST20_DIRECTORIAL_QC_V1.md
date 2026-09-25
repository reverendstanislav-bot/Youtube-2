# SATSOP — 20-IMAGE PROMPT TEST / DIRECTORIAL QC V1

Updated: 2026-09-25

Status: **FAIL FOR SCALE-UP — REMAINING 48 IMAGES ON HOLD**

## Test boundary

- submitted: **20** GPT Image 2 jobs;
- settings: low / 1k / 16:9 / one output per prompt;
- exact spend: **10.00 credits**;
- completed: **20/20**;
- provider failures: **0**;
- retries: **0**;
- post-test balance: **1,256.67 credits**;
- remaining 48 prompts were not submitted.

The test deliberately sampled the hook, Project 3/5 distinction, site/map scenes, finance, construction, technical explanation, combined-cycle comparison, surplus-power argument, preservation, chronology, redevelopment, and rescue training.

## Technical QC

- all 20 files decode as PNG;
- all 20 are **1344 × 752**;
- all 20 have non-zero file sizes and recorded SHA-256 hashes;
- no failed, canceled, NSFW, or IP-detected jobs;
- no visible generated titles or gibberish text;
- the lower frame is generally usable for captions.

## Directorial verdict

| Prompt | Beat | Verdict | Finding |
|---|---|---|---|
| SAT-GEN001 | SAT-B002 | CONDITIONAL | Convincing low-completion construction ground, but generic and not authenticated as Project 5. |
| SAT-GEN002 | SAT-B003 | CONDITIONAL | Strong unfinished-plant establishing shot, but the geometry is generic and cannot carry a 74-percent Satsop claim without real reference control. |
| SAT-GEN003 | SAT-B004 | FAIL | Does not work as a map base; invents two near-complete reactor structures and makes the site appear much more complete. |
| SAT-GEN006 | SAT-B011 | CONDITIONAL | Plausible early construction, but repeats the same concrete/crane vocabulary and does not express cost escalation. |
| SAT-GEN011 | SAT-B019 | FAIL | The 88-participant institutional claim becomes another construction shot; the core idea is absent. |
| SAT-GEN016 | SAT-B026 | FAIL | Does not separate the two projects financially or spatially in a usable map composition. |
| SAT-GEN018 | SAT-B029 | PASS | Clear period boardroom/capability-share visual metaphor with usable negative space; still requires AI reconstruction labeling. |
| SAT-GEN020 | SAT-B032 | FAIL | Invents twin domed reactor buildings and risks false Satsop architecture; unusable for the two 1,240 MW units. |
| SAT-GEN025 | SAT-B039 | FAIL | Shows active concrete construction instead of suspended preservation and retained equipment. |
| SAT-GEN031 | SAT-B047 | PASS | Strong road-level scale and cooling-tower mass; usable as interpretive reconstruction, subject to identity reference correction. |
| SAT-GEN032 | SAT-B048 | CONDITIONAL | Concrete scale reads, but remaining-cost/capital-risk meaning does not. |
| SAT-GEN039 | SAT-B062 | PASS | The nuclear-versus-modular-gas comparison reads immediately; it must be framed as a conceptual composite, not a real Satsop configuration. |
| SAT-GEN044 | SAT-B070 | FAIL | Returns to generic nuclear construction and does not communicate the lower/base/high cost comparison. |
| SAT-GEN046 | SAT-B074 | FAIL | Does not show surplus generation, regional demand, or the 600 aMW imbalance; the required GFX base is absent. |
| SAT-GEN050 | SAT-B079 | CONDITIONAL | Mostly-built project reads, but lack of regional need does not; too similar to other construction frames. |
| SAT-GEN054 | SAT-B084 | PASS | Preservation/uncertainty atmosphere is legible, though it is not a useful map composition. |
| SAT-GEN057 | SAT-B088 | CONDITIONAL | Two completion states are visible, but the 1982/1983 chronology and bond distinction require a separate exact graphic. |
| SAT-GEN063 | SAT-B096 | FAIL | Redevelopment is shown as renewed nuclear construction with cranes, contradicting the 1995 institutional-reuse beat. |
| SAT-GEN066 | SAT-B103 | PASS | Rescue/confined-space training is immediately legible and visually distinct. |
| SAT-GEN068 | SAT-B107 | CONDITIONAL | Aerial closing image is usable, but it shows ruins rather than clearly demonstrating useful present-day reuse. |

Totals: **5 PASS / 7 CONDITIONAL / 8 FAIL**.

Only **25 percent** of the sample passes without prompt redesign. This is below the threshold for scaling the remaining batch.

## Root causes

1. **References were labels, not inputs.** R01–R07 were assigned in the prompt pack, but no real reference media were attached to the generation calls. The phrase “supplied references” therefore had no operational effect.
2. **The global suffix dominates the scene.** Repeating unfinished concrete, cranes, wet Washington weather, and industrial realism in every prompt collapses different narrative functions into the same visual.
3. **Asset classes are only metadata.** `AI_RECONSTRUCTION_MAP` and `AI_RECONSTRUCTION_GFX` still use photographic scene language, so the model returns ordinary site photographs instead of clean map or diagram bases.
4. **Abstract narration lacks a visual mechanism.** Participation, capability shares, cost ranges, capital at risk, surplus power, and chronology often become generic construction because the prompt does not specify a readable spatial metaphor or a precise compositing plan.
5. **Time periods bleed together.** Cranes and active construction appear in preservation and redevelopment beats.
6. **Satsop identity is unreliable.** Several frames invent generic PWR domes, duplicate structures, water bodies, and site arrangements that cannot be treated as Satsop-specific history.
7. **Shot diversity is superficial.** Camera labels change, but the subject, weather, palette, concrete mass, cranes, and horizon remain nearly constant.

## Required correction before any further spend

- acquire and upload actual R01–R07 reference media, then attach the correct subset to every relevant call;
- split the pack into distinct prompt grammars for reconstruction, institutional metaphor, map base, technical cutaway, quantitative GFX base, and modern reuse;
- remove the full narration sentence when it introduces several competing ideas;
- define one visual proposition per image and state the later overlay separately;
- prohibit cranes and active construction in suspended, terminated, debt, transfer, and present-day reuse scenes unless historically required;
- replace generic PWR architecture with reference-controlled Satsop geometry;
- build a deliberate diversity matrix for scale, location, human presence, interior/exterior, lens, elevation, weather, and color temperature;
- run a second small representative test before authorizing the remaining 48 images.

## Spend gate

The original 68-image authorization request is superseded. The remaining 48 images are **not approved for submission** by this QC result. No automatic retries or replacements are authorized.
