# Satsop Remotion V1 — Full Directorial Audit V2

Date: 2026-09-26

## Scope

- Reviewed midpoint frames for all 109 visual beats in sequence.
- Checked visual relevance, composition, repetition, subtitle presence, and encoded-master continuity.
- Audited the caption timeline against the 19:23.92 locked voiceover.

## Blocking findings and corrections

### 1. Caption outages after TTS chunk boundaries — FIXED

The Remotion caption builder added each chunk offset to word timestamps that were already absolute. This pushed chunks 2–4 forward a second time and produced three long subtitle outages in the rough cut.

Correction: captions now use the absolute word timestamps directly.

Validation after correction:

- 464 subtitle cues;
- first cue starts at 00:00.000;
- last cue ends at 19:24.031;
- no inter-cue gap greater than 1.5 seconds;
- locked picture duration: 19:23.920.

### 2. SAT-B056 exposed a nearly blank white frame — FIXED

The portrait photograph contains the tower on its left side and a large white sky area in the centre. The default centre crop and pan moved the tower out of frame near 09:52.

Correction: this beat now uses a left-top focal position while preserving the shared restrained motion treatment.

## Visual review

- 109/109 beats have an assigned image.
- Active timeline: 97 generated images and 12 licensed current photographs.
- No hand-built GFX or document-card inserts remain in the active timeline.
- No `AI RECONSTRUCTION` overlay remains.
- The visual grammar is coherent: archival institutional interiors, physical models, infrastructure details, and present-day site views.
- Repeated office/model-table motifs are frequent but track the script's financing and planning argument; no exact adjacent image duplication was observed.
- SAT-B092 uses a public-domain military exercise at the Satsop site. It is visually abrupt, but it is authentic evidence of the site's later reuse and directly supports the redevelopment line. Retained.

## Release gate

The corrected render must pass decode, duration, stream, black-frame, and spot-frame checks before this rough cut can be marked QC PASS. It is not a final YouTube master until music, mix, and final delivery review are complete.
