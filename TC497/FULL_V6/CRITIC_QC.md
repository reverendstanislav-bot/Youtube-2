# TC497 FULL_V6 — CRITIC / QC REVIEW

## Status

**REVIEW PASS — USER APPROVAL STILL REQUIRED.**

FULL_V6 is not a final upload master. No 1080p candidate is promoted by this document.

Current review build:
- GitHub Actions run: `35424958934`
- artifact: `tc497-full-v6-review`
- artifact id: `10578413797`
- resolution: 960×540
- duration: 1236.533333 s (20:36.533)
- video frames: 37,096 @ 30 fps

## Why V6 was necessary

The FULL_V5 technical QC missed two concrete build defects:

1. `visual_patches.v5.json` declared seven replacements, but the V5 workflow downloaded only five. The two Electric Wheel continuity breakers were silently skipped.
2. `v5_fix_and_music.py` supports reburning overlapping ASS events, but the V5 workflow did not pass `--source-ass`. As a result, captions/source labels disappeared on the five replacement intervals that did render.

FULL_V6 fixes both defects while preserving the already-QC'd V5 audio.

## Ten-critic audit

1. **Continuity editor — PASS**
   - Electric Wheel no longer sits on the two previously unbroken ~9.8 s reconstruction holds.
   - New human/control-cab and wheel-drive detail beats create a clean wide/detail/human rhythm without zoom ping-pong.

2. **Historical-transparency critic — PASS WITH CAUTION**
   - Both new Electric Wheel generated stills are explicitly tagged `RECONSTRUCTION`.
   - This prevents them from reading as undisclosed archival photographs.
   - As reconstructions, fine-grained hardware/crew details should not be treated as primary-source evidence.

3. **Caption / subtitle QC — PASS**
   - Original V4 ASS events are clipped and reburned only inside the seven replacement intervals.
   - Captions are visibly present on Electric Wheel, Nuclear, heavy-lift, ground-vs-air, and survivor replacements.

4. **Source-label / graphics grammar — PASS**
   - Checked examples:
     - ~03:36 / ~03:51 — `RECONSTRUCTION`
     - ~11:50 — `CONCEPT` + `1961 CONCEPT — NOT THE TC-497 POWERPLANT`
     - ~12:11 — `CONCEPT` + `PROPOSED — NEVER BUILT`
     - ~18:28 — `RECONSTRUCTION` + `GROUND MACHINE → AIRLIFT`
   - V4 ARCHIVE / DOCUMENT / RECONSTRUCTION / CONCEPT grammar is no longer regressed by V5 replacements.

5. **Factual-implication critic — PASS**
   - Heavy-lift imagery remains cargo/logistics imagery; it does not imply that a helicopter lifted the complete TC-497.
   - Nuclear imagery remains explicitly separated from the actual gas-turbine vehicle.

6. **Audio mixer — PASS / UNCHANGED**
   - V6 remuxes the V5 AAC elementary stream without re-encoding.
   - SHA-256 of extracted AAC:
     - V5: `d171be550180d3f03fc89489c7fd2e3c9ece25f5579cfd023df0b4a7d8103722`
     - V6: `d171be550180d3f03fc89489c7fd2e3c9ece25f5579cfd023df0b4a7d8103722`
   - Therefore V5's already-reviewed music/VO/SFX mix is preserved bit-for-bit.

7. **Technical encoder / timing QC — PASS**
   - V5 and V6 are both 30 fps, 1236.533333 s, 37,096 frames.
   - No timeline shortening or drift was introduced by the chunked render/stream-copy assembly.

8. **Chunk-boundary continuity QC — PASS**
   - Sampled boundaries at 205, 410, 700, 900, and 1125 s.
   - No black frames or obvious discontinuities found.
   - Overview sampling across the full 20:36 timeline did not expose a new assembly artifact.

9. **Visual-style critic — PASS WITH MINOR P2 NOTE**
   - The two new Electric Wheel reconstructions are more photographic than some older reconstruction assets.
   - The explicit `RECONSTRUCTION` label and existing HIA grade keep the difference understandable.
   - This is not a blocker for user review.

10. **YouTube editorial reviewer — READY FOR HUMAN REVIEW**
    - V6 resolves the concrete V5 regressions found during artifact inspection.
    - The 960×540 file is a review encode only; its larger ultrafast/chunked encode is not the final delivery strategy.
    - A 1080p upload master must not be promoted until the user explicitly approves the edit.

## Exact patch intervals verified

- 215.356–221.464 — Electric Wheel human/control break + RECONSTRUCTION
- 230.014–237.342 — Electric Wheel drive-detail break + RECONSTRUCTION
- 709.241–717.165 — Nuclear concept + restored ASS
- 730.373–736.976 — Proposed/unbuilt concept + restored ASS
- 1079.245–1087.457 — Heavy-lift logistics + restored captions
- 1107.164–1115.376 — Ground-vs-air + restored reconstruction/source grammar
- 1209.007–1215.477 — Survivor detail + restored captions

## Remaining status

No P1 technical/editorial blocker was found in the targeted V6 audit.

Remaining decision is human/editorial: **the user must watch and explicitly approve FULL_V6 (or provide new timecoded complaints).**

V14 cold-open grammar was not changed in V6.
