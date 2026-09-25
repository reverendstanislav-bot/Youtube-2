# BIG MUSKIE — CURRENT STATUS / HANDOFF

Updated: 2026-09-24

## Canonical status

Episode: **3 — Big Muskie**  
Machine: **Bucyrus-Erie 4250-W walking dragline**  
Project: **Hidden Industrial America / YouTube-2**  
State: **PICTURE V2 DIRECTORIAL QC COMPLETE — FAIL FOR RC — CANONICAL REMOTION FIX PASS OPEN**  
Publication status: **REVIEW ONLY — NOT RC / NOT PUBLICATION CANDIDATE**

Pre-sync repository HEAD used for this handoff refresh: `9f5989ec3dedaf3cb250416b6f9fba04390b645b`.  
The repository may continue to move because other episodes are being edited in parallel; always re-read `main` before any write and apply changes on top of the current HEAD.

## Current user direction

The user has explicitly moved Episode 3 forward from English V3 review into the production chain:

**TTS → word-level transcript → exact runtime → Stage 7 full visual beat map**

English V3 may proceed through preflight, but **paid generation still requires a separate explicit credit-spend approval after the exact cost is shown**.

Current required order:
1. rebuild/validate spoken-only V3 text;
2. TTS preflight and chunking;
3. show exact Arthur TTS cost and wait for explicit user approval;
4. only after approval, generate Arthur TTS with identical settings across chunks;
5. continuity QC and audio master assembly;
6. exact runtime + word-level alignment/transcript;
7. commit audio/timing manifests and hashes;
8. build the full Stage 7 visual beat map from real VO timestamps;
9. do **not** generate images until Stage 7, the full prompt pack, exact image count, and credit budget are reviewed and explicitly approved.

## Inherited non-negotiable production rules

- GitHub is project memory and source of truth.
- Chicago and TC497 are reference only unless the user explicitly asks to modify them.
- no force-push;
- never overwrite newer `main`; re-read HEAD before every write;
- no video generation;
- **no paid generation of any kind without explicit user approval after exact cost preflight**;
- no image-generation spend before script + beat map + complete prompt pack + exact budget approval;
- source provenance and rights must be recorded;
- verified historical visuals may carry `HISTORICAL SOURCE` only while the authentic historical source is actually on screen;
- generated/reconstructed imagery must never be presented as authentic archive and must use the channel's reconstruction labeling;
- final captions: white base `#FFFFFF`, active spoken word `#F28A3A`, word-level sync, one clean renderer, no black subtitle block;
- review/candidate/final labels follow CHANNEL approval semantics;
- proof → user review → RC → exhaustive QC → native upload master.

## Documentary lock

Working title: **America Built a 27-Million-Pound Machine. Then Scrapped It.**

Documentary angle: **Scale with a reason.**

Central question:

> What problem could make a 27-million-pound machine economically rational — and what changed so completely that the machine was eventually scrapped?

This is not a "look how huge it was" film. The story explains why geology, deep overburden, electric-power demand, mine geometry, coal economics and the available mining technology made Big Muskie a rational answer for a particular industrial system — and why that equation later stopped working.

## Dramatic architecture lock

V1 is preserved as the sourced first-draft baseline and must not be overwritten.

V2 directorial direction was approved by the user and is the dramatic basis for V3:

- **Act I — Mystery:** the surviving bucket is the physical mystery; Big Muskie worked, so why was it stopped and dismantled?
- **Act II — Engineering spectacle:** first explain the mine/power problem, then reveal the machine; stage one full dragline cycle as action; explain hoist/drag/swing only after the audience sees the cycle.
- **Walking mechanism:** begins as engineering wonder, ends as an infrastructure constraint.
- **Human scale:** crews, power, prepared ground, mine flow and maintenance enter before the midpoint.
- **Midpoint reversal:** prove productivity first, then reveal the scoped 1977 field-study month with **35% mechanical availability**; never convert that to lifetime availability.
- **Act III — System collapse:** mining technology, high-sulfur-coal economics and the changing emissions environment alter the equation; no single villain.
- **Climax:** 1999 dismantling is a full industrial/preservation problem, not a footnote.
- **Ending:** return to the same bucket; opening meaning = scale curiosity, ending meaning = evidence of a vanished industrial equation.

## Production research lock

Research blockers: **0**.

### Core identity / chronology
- Bucyrus-Erie **4250-W**.
- Central Ohio Coal Company / Muskingum Mine.
- project began in **1966**.
- production began in **1969**.
- stopped in **January 1991**.
- dismantled in **1999**.

### Scale / dimensions
- machine mass: **more than 27 million lb**; do not force one exact converted tonnage.
- height: production wording **about 222 ft / roughly 22 stories**.
- boom: **310 ft**; Caterpillar's 330-ft statement remains a documented outlier and is not used in narration.
- overall boom-down length: about **487 ft**.
- width: about **151 ft**.
- tub: about **105 ft diameter**.
- bucket capacity: **220 yd³**.
- empty bucket: **roughly 240 tons**.
- material per bite: **up to about 325 tons**; never describe 325 tons as empty-bucket mass.

### Construction / logistics
- components arrived in roughly **340 rail cars + 260 trucks**.
- narration construction wording: **hundreds of thousands of labor-hours** / **more than 200,000 labor-hours**.
- do not invent a reconciliation between the 200k and 300k source figures.

### Electrical / motion systems
- narration power feed: **about 13 kV**.
- technical graphics may use **13.8 kV**.
- documented main-motion banks:
  - 10 × 1,000 hp hoist;
  - 8 × 1,000 hp drag;
  - 10 × 625 hp swing.
- this means **28 documented motors for the three main-motion systems**, not 28 total motors in the entire machine.

### Walking / terrain
- four walking shoes, approximately **20 × 65 ft**.
- grade requirement approximately **under 5%**.
- mobility must be framed as requiring prepared infrastructure, not as unrestricted movement.

### Production / lifetime
- contemporary Bucyrus context: **more than 8,000 yd³ per operating hour**.
- lifetime earth/rock moved: **more than 483 million cubic yards**.
- do **not** use 608 million.
- nearly **18 million tons of coal exposed** in current ODNR wording.

### 1977 USBM/Penn State field-study snapshot
- mean cycle approximately **75.25 sec** at about a 120° swing;
- **35% mechanical availability** only for the actual study month;
- about **1,949,200 yd³/month** in the same actual-data row.
- these values must remain explicitly scoped to the measured study period and must never be promoted to lifetime averages.

### Shutdown
Use a multi-factor explanation:
- changing / more efficient mining technology;
- weakening economics and demand for Ohio high-sulfur coal;
- changed post-1990 emissions environment.

Do **not** say `EPA killed Big Muskie`.  
EPA Title IV Phase I compliance began in **1995**, after Big Muskie stopped in January 1991.

### Preservation / surviving material
- preservation attempts existed;
- AEP 1999 documents reclamation obligations, time/funding issues and long-term liability;
- the bucket is the major public surviving artifact;
- HCEA holds smaller components, so never say the bucket is literally the only surviving piece.

Detailed research controls:
- `RESEARCH/SOURCE_LEDGER.md`
- `RESEARCH/FACT_CHECK_AUDIT_2026-09-22.md`
- `RESEARCH/RESEARCH_GAPS_CLOSED_2026-09-22.md`

## Stage 5 lock

- documentary angle: **Scale with a reason**;
- working title locked as above;
- thumbnail direction: authentic EPA/NARA public-domain Big Muskie hero frame; compact optional text **27 MILLION LB**;
- 9-section retention architecture including cold open;
- claim→source map completed;
- sourced English V1 completed and preserved;
- Russian V2 directorial rewrite completed and approved as direction;
- five Shorts designed inside the long-form structure.

Canonical Stage 5 files:
- `DEVELOPMENT/STAGE_5_LOCK.md`
- `SCRIPT/RETENTION_OUTLINE_V1.md`
- `SCRIPT/CLAIM_SOURCE_MAP_V1.md`
- `SCRIPT/NARRATION_DRAFT_V1.md`
- `SCRIPT/NARRATION_DRAFT_V2_RU_REVIEW.md`
- `SCRIPT/V2_DIRECTORIAL_REWRITE_NOTES.md`
- `SCRIPT/SHORTS_EXTRACTION_MAP_V1.md`

## Stage 6 lock

Completed:
- native English V3 adaptation, not literal translation;
- V2 mystery → spectacle → midpoint reversal → system collapse → dismantling climax → bucket callback retained;
- line-by-line factual verification completed;
- factual blockers: **0**;
- V3-aligned Shorts map completed;
- TTS direction/pronunciation package prepared.

Canonical Stage 6 files:
- `SCRIPT/NARRATION_V3_EN_REVIEW.md`
- `SCRIPT/NARRATION_V3_EN_TTS_CLEAN.txt`
- `SCRIPT/V3_FACT_CHECK.md`
- `SCRIPT/SHORTS_EXTRACTION_MAP_V2.md`
- `SCRIPT/TTS_PACKAGE_V1.md`

## TTS lock / current next stage

Canonical Hidden Industrial America / YouTube-2 voice: **Arthur**.

Verified preset:
- `voice_id = 30fc8796-ceb6-4a66-b3a7-4a145ef7f346`
- `voice_type = preset`
- model: `text2speech_v2`
- variant: `elevenlabs`

Verification:
- Chicago canonical voice master duration is 1290.720 s; four historical Arthur/ElevenLabs jobs total exactly 1290.720 s.
- TC-497 historical narration jobs use the same Arthur preset and ElevenLabs engine.
- Alexey was incorrectly introduced into Big Muskie metadata on 2026-09-23 and is rejected for YouTube-2.

Correct spoken-only V3:
- characters: **18657**
- chunks: **4826 / 4844 / 4827 / 4154**
- all chunks <5000 characters;
- no chapter headings or production notes.

User explicitly approved **56.25 credits** for the four Arthur chunks. The four jobs were generated successfully and no additional paid jobs were submitted.

Raw decoded four-chunk runtime: **23:45.600**. Canonical join-normalized editorial runtime: **23:46.400**.

See: `SCRIPT/TTS_GENERATION_MANIFEST_V1.md`.

### Mandatory spend gate

Preflight first → show exact total → wait for explicit user approval → only then generate.

A general instruction to continue production is not permission to spend credits.

### Rejected unauthorized batch

An incorrect Alexey batch was submitted without explicit spend approval:
- spent: **57.00 credits**;
- 4 jobs completed;
- wrong channel voice;
- chapter headings were also accidentally spoken;
- status: **REJECTED / NON-CANONICAL / DO NOT USE**.

## Shorts lock

V3-aligned candidates:
- SHORT-01 — bucket / surviving artifact.
- SHORT-02 — walking system.
- SHORT-03 — 28 documented hoist/drag/swing motors.
- SHORT-04 — why one environmental law did **not** simply kill Big Muskie.
- SHORT-05 — why the machine was dismantled.

Initial cuts use exact long-form wording. After real VO timing, subordinate clauses may be trimmed for duration, but no new factual claim may be added without source-map review.

## Stage 7 gate after VO

Only after final VO timing exists, build the complete visual beat map against **real audio timestamps**, not approximate script timing.

Each beat must contain:
- Beat ID;
- start/end time;
- exact narration segment;
- narrative function;
- visual objective;
- one main asset class;
- specific asset requirement;
- provenance/source requirement;
- motion/editing instruction;
- GFX requirement;
- authenticity label;
- Shorts relation;
- risk/QC note.

Main asset classes:
- `ARCHIVE_PHOTO`
- `ARCHIVE_FILM`
- `DOCUMENT`
- `MAP`
- `TECH_DRAWING`
- `PHOTO_CURRENT`
- `GFX`
- `CHART`
- `GENERATE`
- `EDITORIAL_ONLY`

After the entire beat map:
1. inventory real archive/source assets;
2. identify visual gaps;
3. mark only genuine gaps as `GENERATE`;
4. write the complete prompt pack;
5. prompt audit;
6. exact image count;
7. exact credit budget;
8. explicit user approval;
9. only then image generation.

**Video generation remains prohibited.**

## Visual / provenance / caption lock

Channel visual palette:
- Charcoal `#171A1C`
- Iron `#30363A`
- Warm Paper `#E6DDC8`
- Ivory `#F3EBDD`
- Faded Rust `#A55235`
- Blueprint Gray-Blue `#5F747D`

Typography:
- IBM Plex Sans Condensed Bold
- IBM Plex Sans
- IBM Plex Mono

Do not use:
- orange collage blocks;
- cheap orange rectangles;
- giant info cards;
- generic presentation UI;
- random zooms;
- shakes;
- slideshow cadence;
- three similar hero shots in a row;
- fake archival AI;
- impossible machinery;
- text over faces/important mechanics;
- black subtitle blocks;
- generic neon/horror look.

Sequence rule: no more than two highly similar main objects consecutively; each next beat must change scale, viewpoint, information, subject, medium or function.

High-value archive rights status already identified:
- EPA DOCUMERICA / NARA 554830 — public domain.
- EPA DOCUMERICA / NARA 555644 — public domain.
- 1999 whole-machine side view — CC BY-SA 3.0.
- preserved bucket photo — CC BY-SA 4.0.
- Milwaukee Public Library Bucyrus scans — research source only until publication permission/copyright clearance.
- Google/search thumbnails are never treated as licensed assets.

Final captions:
- base words **WHITE #FFFFFF**;
- active spoken word **ORANGE #F28A3A**;
- word-level sync;
- one renderer/layer;
- safe margins;
- no `100,100)}`;
- no random blue words;
- no duplicate caption layer;
- no black subtitle rectangle.

## Immediate next action

**CANONICAL REMOTION PICTURE FIX PASS**

Directorial QC result:
- Picture V2: **FAIL FOR RC / FIXABLE**
- new paid image generation required: **0**
- patch-boundary defects: **13**
- close duplicate/repeat pairs requiring editorial treatment: **5**
- critical document-readability block: **D03 + D04**
- short unreadable GFX blocker: **BM-B076**
- dense infographic runs requiring staged Remotion treatment: **B010–B016 / B066–B073 / B081–B089 / B113–B115**

Canonical report:
- `ASSEMBLY_V2/DIRECTORIAL_QC_V2.md`

Next:
1. reproduce the accepted V2 replacement map natively in Remotion;
2. extend each picture through the next beat start so narration pauses never reveal old V1 frames;
3. quantize all boundaries to 25 fps;
4. apply document crops, duplicate fixes, staged GFX treatment and restrained motion from the QC report;
5. render Picture V3 / Remotion proof;
6. run full directorial + technical QC;
7. only after picture approval proceed to provenance/captions/music/SFX and RC.
