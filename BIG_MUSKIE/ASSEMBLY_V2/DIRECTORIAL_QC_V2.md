# BIG MUSKIE — PICTURE V2 DIRECTORIAL QC

Date: 2026-09-24

Status: **FAIL FOR RC — CANONICAL REMOTION FIX PASS REQUIRED**

Reviewed master:
- `BIG_MUSKIE_FULL_PICTURE_ASSEMBLY_V2_1080P.mp4`
- verified local SHA-256: `cf022849456c43cbc10ff38659d3e5b7033d8bac386597c47db41b11a0130f7c`
- 1920×1080 / 25 fps / 35,660 frames / 23:46.400
- Arthur VO only; no captions/music/SFX

## Executive verdict

The story structure and most locked imagery are strong enough to continue. **No new paid generation is required.**

Picture V2 is **not RC-ready** because the review-patch implementation itself introduces old-frame flashes/reversions, several document beats are unreadable at full-page scale, multiple near-duplicate images recur too close together, and several long sections still read as static infographic slides rather than a continuous film.

Canonical Remotion should be used to rebuild the accepted V2 asset map cleanly, not to redesign the whole film.

## BLOCKER A — V2 patch boundary defects

The exact-window patch returns to the old V1 frame during narration gaps after replaced beats. At four entries, a single V1 frame also appears before the new replacement because the patch begins between 25 fps frame boundaries.

Detected boundary defects:

| Asset / beat | Defect |
|---|---|
| FX001 / BM-B001 | old V1 frame returns from ~00:11.000 to next beat at ~00:11.600 |
| FX002 / BM-B006 | one-frame old-V1 flash around 00:59.040–00:59.080; old V1 returns ~01:08.960–01:09.840 |
| FX013 / BM-B021 | old V1 returns ~04:35.880–04:37.000 |
| FX016 / BM-B035 | old V1 returns ~07:25.040–07:25.840 |
| FX033 / BM-B074 | one-frame old-V1 flash ~15:20.000–15:20.040; old V1 returns ~15:30.080–15:30.720 |
| FX036 / BM-B079 | one-frame old-V1 flash ~16:13.120–16:13.160 |
| FX045 / BM-B094 | old V1 returns ~19:25.400–19:26.600 |
| FX047 / BM-B096 | old V1 returns ~19:49.520–19:50.560 |
| FX048 / BM-B099 | old V1 returns ~20:24.960–20:25.280 |
| FX049 / BM-B100 | one-frame old-V1 flash ~20:25.280–20:25.320; old V1 returns ~20:34.240–20:35.160 |

Total: **13 visible boundary events: 9 old-frame reversion windows + 4 one-frame entry flashes.**

### Required Remotion fix

Do not patch only narration start→end. Each accepted replacement must own the picture from its beat start **through the next beat start**, including the inter-beat narration pause. All boundaries must be quantized to exact 25 fps frames before render.

## BLOCKER B — document readability

### BM-B038 / 00:07:50.400–00:08:01.480
D03 patent page is shown almost as a full white page on black. The mechanism being discussed is too small to read.

**Fix:** use a close crop of the relevant hoist figure/linework, with a restrained Remotion reveal/highlight. Do not enlarge the entire page.

### BM-B041 / 00:08:28.220–00:08:39.960
The same D03 full-page presentation repeats only three beats later.

**Fix:** use a second distinct crop from D03 focused on motor/mechanical relationships. Never show the same full page twice.

### BM-B051 + BM-B052 / 00:10:29.020–00:10:54.900
D04 is effectively one static full-page patent image for **25.88 seconds** across two narration beats.

**Fix:** split into two source-grounded crops:
- B051: walking-shoe/mechanism detail;
- B052: ground/route/grade constraint detail.
Use slow crop/highlight only; no aggressive pan.

## BLOCKER C — unreadable short-duration GFX

### BM-B076 / 00:15:41.980–00:15:44.920
`THE FAILURE PATH` is a multi-column information graphic shown for only **2.94 seconds**. It cannot be read in the available screen time.

**Fix:** reduce to one instantly legible chain:
`component fault → machine unavailable → stripping system affected`.
No four-column paragraph card.

## BLOCKER D — near-duplicate/repeated frames too close together

Confirmed strong visual duplicates/near-duplicates:

| Beats | Problem | Required fix |
|---|---|---|
| BM-B038 / BM-B041 | identical D03 full-page treatment | distinct source crops |
| BM-B083 / BM-B085 | same EPA Title IV white card | B083 = source/context crop; B085 = date comparison / 1995 highlight |
| BM-B102 / BM-B104 | same current bucket image separated by one beat | reframe one to detail/scale crop |
| BM-B105 / BM-B107 | same chain detail separated by one beat | B105 bucket/other-survivors setup; B107 cable/chain macro |
| BM-B109 / BM-B112 | same reclaimed-landscape image only two beats apart | use different crop/scale or alternate existing context source |

These do not require new generation.

## MAJOR — generated machine-shot monotony

### BM-B033–BM-B040 / ~00:06:51.640–00:08:28.220
The film enters a long run dominated by visually similar Big Muskie hero views. The images are individually usable, but the sequence becomes machine → machine → machine with only the patent page as a break.

Canonical treatment:
- B033: bucket/load hero;
- B034: machine-to-bucket scale relationship;
- B035: operating-cycle GFX;
- B036: drag/bucket contact detail;
- B037: loaded bucket detail;
- B038: hoist patent crop;
- B039: upper house / swing structure;
- B040: dump/return geometry.

Use existing frames and reframing; **do not generate new images**.

## MAJOR — infographic-slide runs

### BM-B010–BM-B012 / 00:01:46.460–00:02:25.500
Three geological cards in succession feel like separate slides.

**Remotion direction:** make them one evolving cross-section sequence: overburden concept → 97 ft average → 182 ft deep case. One visual system, staged information, no hard reset each beat.

### BM-B013–BM-B016 / 00:02:26.040–00:03:22.180
Nearly a minute of dense explanatory cards before archive relief.

**Remotion direction:** retain the assets but reveal only the line/number currently being narrated. Avoid showing every label from frame one.

### BM-B066–BM-B073 / 00:13:35.440–00:15:19.000
The 1977-study section is factually strong but visually becomes a long statistics deck.

Preferred progression:
1. actual study/source;
2. 75.25 sec cycle;
3. cycle visualization;
4. exact data-row crop;
5. 35% measured-month availability;
6. clarify “one month, not lifetime”;
7. 1,949,200 yd³;
8. paradox synthesis.

Keep the same evidence, but use staged highlights and continuity rather than eight unrelated static cards.

### BM-B081–BM-B089 / 00:16:32.020–00:18:24.560
This is the largest “presentation deck” section in V2. It contains multiple full-screen info cards and two near-identical EPA cards.

**Fix:** keep the factual chain but vary the medium:
- mining-pathway diagram;
- factors/equation;
- real EPA source treatment;
- myth/reality contrast;
- 1991 vs 1995 timeline;
- changing-equation synthesis;
- return to machine image before the preservation act.

## MAJOR — generic white-card treatment

BM-B083/B085 EPA cards and several nearby explanatory cards visually break HIA’s dark industrial language.

Canonical Remotion should present exact source-derived text inside the HIA document treatment:
- charcoal/iron surround;
- warm-paper source crop;
- one highlighted sentence/date at a time;
- no giant generic white presentation rectangles.

No factual rewrite is needed.

## MAJOR — current-source framing

Several authentic/context photographs are preserved in narrow aspect ratios over a large blurred extension. This protects source integrity, but some backgrounds are bright and soft enough to feel cheap beside the HIA GFX.

Use one consistent source treatment in Remotion:
- source image fully visible;
- darker/desaturated restrained extension or charcoal matte;
- no destructive crop;
- source/provenance label stays attached only while that source is on screen.

Do not reframe important evidence out of the image.

## MAJOR — final act repetition

### BM-B106
`WHAT SURVIVED` reads like an intermediate explanatory placeholder compared with adjacent strong frames.

**Fix:** simplify the card or use existing surviving-parts imagery as the visual center. No new generation required.

### BM-B113–BM-B115
Three concept-heavy GFX beats run consecutively immediately before the final bucket.

The concepts are good; the issue is static density.

**Fix:** use restrained staged reveals:
- B113: question / scale;
- B114: machine → bucket transformation;
- B115: “particular system / particular time” synthesis.
Do not animate every element.

### BM-B116
The final bucket is thematically correct but remains a static 12.34-second hold.

**Fix:** very soft ≤1% push or light/parallax-free scale only, then reserve final seconds for the established HIA YouTube end-screen treatment if required. No shake, no lateral motion.

## CAPTION-SAFE WATCH

FX013 and FX016 were explicitly user-accepted despite lower-frame callouts.

Do **not** regenerate them.

During final caption integration, test these beats separately. If the normal caption baseline collides with their lower callouts, solve at the edit/caption-layout level rather than changing the approved GFX.

## PROVENANCE / AUTHENTICITY FOR RC

V2 intentionally has no final provenance labels yet.

Before RC:
- verified archive only → `HISTORICAL SOURCE`;
- generated/reconstructed machine scenes → channel reconstruction label;
- explanatory generated GFX → `HIA EXPLANATORY GFX` / no historical-source implication;
- labels must begin/end with the source itself, never carry across a cut.

BM-B097 dismantling imagery is especially important: it must not read as authentic filmed demolition if it is reconstruction.

## TRANSITION / MOTION DIRECTION FOR CANONICAL REMOTION

Current V2 is a hard-cut/static review assembly. That is acceptable for review, not for RC.

Canonical Remotion rules:
- eliminate all V2 patch flashes by rebuilding the timeline natively;
- no shake;
- no left/right oscillation;
- no aggressive zoom;
- no random Ken Burns;
- do not use heavy dissolves that visibly double machinery;
- use clean cuts as the base language;
- use very short restrained transition treatment only when it improves continuity;
- use internal staged reveal for GFX/documents;
- use ≤1–1.5% slow push on a limited number of hero stills, not on every shot.

## AUDIO PREFLIGHT

Arthur VO is technically intact.

Measured on V2 voice-only master:
- integrated loudness: **-14.48 LUFS**
- true peak: **-0.43 dBTP**
- LRA: **3.4 LU**
- no >2 s narration silence was previously detected; current 1 s pauses match the editorial beat structure.

For the final music/SFX mix, create headroom before adding stems. Do not stack music/SFX onto the current near-full-scale voice and then limit aggressively.

## WHAT SHOULD NOT BE REDESIGNED

Keep the accepted direction of:
- BM-B001 opening hero;
- BM-B020 “Four Inputs, One Giant Solution”;
- BM-B021 operating-cycle replacement;
- BM-B048 power/footprint;
- BM-B061 single-point vulnerability;
- BM-B066/B067 1977-study setup;
- BM-B073 capability/productivity synthesis;
- BM-B074 capability concentration;
- BM-B078/B079 changing-equation turn;
- BM-B093–BM-B096 preservation sequence;
- BM-B098–BM-B100 bucket/disappearance callback;
- BM-B111–BM-B116 thematic ending.

These need editorial integration/motion, not conceptual replacement.

## RC GATE

Picture V2: **DIRECTORIAL FAIL / FIXABLE**

Required before RC:
1. rebuild the accepted V2 map natively in Remotion;
2. remove all 13 patch-boundary defects;
3. fix D03/D04 document crops;
4. simplify B076;
5. eliminate the five close duplicate pairs;
6. apply staged treatment to the four dense infographic runs;
7. add provenance/authenticity labels;
8. caption-collision test FX013/FX016;
9. final picture QC after Remotion render.

**New paid image generation required: 0.**
