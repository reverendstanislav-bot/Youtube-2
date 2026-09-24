# SUPERSEDED / REJECTED

This document describes the rejected HIA V10 semantic-rebuild Shorts system. It is retained only as historical QC evidence. **DO NOT USE IT AS A PRODUCTION REFERENCE.** Active Shorts canon: `CHANNEL/SHORTS_PRODUCTION_CANON.md` (Youtube-1 direct-cut model).

# V10 WAVE 2 — HARD QC

Date: 2026-09-23
Scope: CHI-S02..S05 + TC497-S03..S05
Status: **HOLD — DO NOT PROMOTE TO FINAL**

## Global technical QC

All 7 files decode successfully and have:
- 1080x1920
- yuv420p
- Chicago 25 fps / TC497 30 fps
- AAC stereo 48 kHz
- no detected black-frame runs

Measured integrated loudness / true peak:
- CHI-S02: -13.9 LUFS / -4.4 dBFS
- CHI-S03: -13.8 LUFS / -4.4 dBFS
- CHI-S04: -13.9 LUFS / -4.4 dBFS
- CHI-S05: -14.0 LUFS / -4.3 dBFS
- TC497-S03: -13.6 LUFS / -3.2 dBFS
- TC497-S04: -14.1 LUFS / -3.3 dBFS
- TC497-S05: -14.1 LUFS / -3.3 dBFS

Review video bitrate is only ~715–917 kbps. Fine for review, **not acceptable as final upload master**.

## BLOCKER 1 — caption event overlap on all 7 Shorts

The ASS generator leaves the last event of many phrase groups alive for +0.08 sec while the next group has already started. This creates real simultaneous subtitle layers for 2–3 frames.

Measured overlaps:
- CHI-S02: 18
- CHI-S03: 8
- CHI-S04: 15
- CHI-S05: 17
- TC497-S03: 13
- TC497-S04: 15
- TC497-S05: 21

Typical overlap: 0.06–0.08 sec.

This was visually confirmed on rendered frames: two separate caption groups can stack into four visible lines at once.

Required fix:
- end each caption event at min(next event start, word/group end)
- never add an unconditional +0.08 sec tail across a following group
- clamp final caption event to exact video duration
- automated QC must fail on any ASS event overlap > 1 frame

## BLOCKER 2 — factual / editorial issues

### CHI-S02 — HOLD
- Period telephone advertisement is tagged **HISTORICAL SOURCE**. Under channel canon a period ad/document should be **DOCUMENT**.
- Opening says the system began as a telephone tunnel but opens on a later rail/test-train image; chronology is visually muddy.
- Exact source assets repeat heavily: telephone ad, construction photo, tunnel photo and test-train photo are recycled.
- Final “TWO-FOOT GAUGE” payoff does not clearly show track gauge detail.
- Cut at 22.40 sec is ~0.34 sec before the nearest word end; weak phrase alignment.

Fix: correct provenance; use telephone/document evidence for opening; diversify two middle beats; end on actual rail/gauge detail.

### CHI-S03 — HOLD
- The hook is strong, but the first section uses visually similar generated city/train composites.
- “Why did Chicago need it?” should show the actual surface freight/congestion problem; current middle visual remains an underground/city composite.
- Repeated visual family makes the short feel like a still-image slideshow despite clean motion discipline.
- Cut at 22.80 sec is ~0.34 sec away from phrase boundary.

Fix: replace 10.8–19.6 sec with stronger street/freight problem evidence and a distinct obsolescence visual.

### CHI-S04 — HOLD
- Captions say **Kinsey Street** while the correct on-screen location metric is **Kinzie Street**. Internal inconsistency is visible.
- The Kinzie location beat shows the historical map but does not clearly pinpoint the breach location in the vertical crop.
- Final payoff repeats the same flood-network visual family instead of escalating to a stronger network-wide consequence.
- Several cut points are 0.20–0.36 sec off phrase ends.

Fix: captions/text to Kinzie; add a clean verified location highlight; give final beat a distinct network-wide flood payoff.

### CHI-S05 — HOLD
- Captions again say **Kinsey Street** instead of **Kinzie Street**.
- The sensitive legal-claims section relies mainly on AI reconstruction. The extraction brief asks for document/location evidence and explicit separation of allegation vs finding.
- Provenance is truthful (AI RECONSTRUCTION), but the evidence strength is too weak for a legal-history correction beat.
- Repeated city/tunnel composites reduce visual authority.
- Cut at 31.50 sec is ~0.42 sec before the nearest word end.

Fix: use actual document/evidence crops for allegation/legal-history beats; keep “alleged / not a final finding” markers; correct Kinzie; diversify the final infrastructure lesson.

### TC497-S03 — HOLD / closest to pass
- Overall hook, scale, roadless-terrain and steering payoff work.
- “Ordinary highway truck” comparison is not visually shown as a truck/highway contrast; the shot remains another TC-497/cargo visual.
- Range section spends too long on a relatively empty terrain shot.
- Cut at 21.00 sec is ~0.44 sec after the nearest phrase end.

Fix: one real explanatory truck/road contrast or clean comparison GFX; tighten range beat; snap cut to narration.

### TC497-S04 — FAIL
- Narration says a **1961 Army research publication** discussed nuclear power, but the video does not show the verified publication at that moment.
- Instead it moves directly through photorealistic nuclear concept imagery.
- CONCEPT labels are present, so provenance is not falsely archival, but the documentary evidence chain is missing.
- The “reactor mounted on the train” style concept imagery visually implies more design certainty than the narration supports.
- Wheel/powertrain visuals repeat too much.

Fix: show the verified 1961 document first; crop/highlight the relevant passage/date; only then move into restrained CONCEPT/GFX; reduce photoreal speculative reactor imagery.

### TC497-S05 — FAIL
- First 10.76 sec narration lists rivers, steep ridges, soft ground and dunes; the visuals do not distinctly show those four terrain problems. Too much TC-497/dune repetition.
- Asset **AR_CH54_1.png** is labeled on-screen **SIKORSKY S-64 SKYCRANE**. The archive asset itself is the CH-54 set, so this historical-source label is not safely matched to the asset.
- Generated heavy-lift imagery resembles a different helicopter family in places and can confuse the S-64/CH-54 discussion.
- Captions contain the grammatical error **“Aircrafts such as…”**. Display text should read **“Aircraft such as…”** even if locked audio cannot be changed.
- Caption overlap count is the worst in the batch: 21.
- Final TC-497 legacy visual is acceptable, but the preceding evidence/payoff is not strong enough.

Fix: four distinct terrain beats; use verified CH-54 images with CH-54 labels; use an actual verified S-64 image only if available; correct display caption “Aircraft”; keep generated aircraft clearly AI RECONSTRUCTION.

## Subtitle / platform-safe QC

Positive:
- white base + orange active word is consistent
- no “100,100)}” corruption
- two-line wrapping generally holds
- caption vertical position is much safer than rejected earlier versions

Still required:
- eliminate all event overlaps
- clamp last event to runtime (TC497 S03/S04/S05 currently extend ~0.06–0.08 sec beyond file end)
- consider moving provenance labels down slightly from the extreme top edge for mobile UI safety

## Final gate

Current batch:
- Technical container/decode/audio: **PASS**
- Caption renderer: **FAIL**
- Provenance/evidence: **FAIL on CHI-S02 and TC497-S04; weak on CHI-S05/TC497-S05**
- Editorial semantic match: **HOLD**
- Upload-master readiness: **FAIL**

No Short from Wave 2 should be promoted to FINAL until the caption-overlap bug is fixed globally and the per-Short blockers above are patched.
