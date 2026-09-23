# HIA — Provenance and Editing Canon

## Provenance is a hard truth rule

A visual may receive **HISTORICAL SOURCE** only when the actual on-screen visual is a verified historical source asset: archival photograph, historical map, period drawing, period document, patent, report, newspaper, or equivalent primary/secondary historical artifact with recorded provenance.

Generated or reconstructed imagery must never receive **HISTORICAL SOURCE**.

Canonical labels:
- verified archival photograph / historical map: `HISTORICAL SOURCE`
- verified report / patent / period document: `DOCUMENT`
- AI-generated or manually reconstructed historical scene: `AI RECONSTRUCTION`
- hypothetical / unbuilt / explanatory concept: `CONCEPT`
- charts, diagrams, editorial graphics: no historical-source label unless the background source itself is historical and separately identified

The renderer must derive the label from the visual asset class, not from the narration topic, chapter, date being discussed, or neighboring shot.

A build fails QC if:
1. a reconstruction carries `HISTORICAL SOURCE`;
2. a concept carries `HISTORICAL SOURCE`;
3. an archival/document label survives onto the following generated shot;
4. provenance is inferred from chapter context instead of the actual current visual.

## Editing architecture

Remotion is the canonical picture-timeline renderer for review/final builds.

FFmpeg may:
- decode/encode;
- mux approved audio;
- normalize technical formats;
- extract frames/stills;
- perform QC.

FFmpeg/Python must not be used as the primary editorial engine by assigning arbitrary weighted durations to stills and concatenating them as the final documentary edit.

Each documentary shot must exist as an explicit Remotion timeline beat with:
- exact start/end frame;
- visual asset;
- provenance class;
- semantic role;
- motion mode;
- caption-safe state;
- optional editorial overlay;
- section/chapter association.

## Motion / pacing rules

- Default transition is a clean hard cut.
- No constant Ken Burns oscillation.
- No push -> pull -> push rhythm simply because assets are static.
- Archive/documents are normally static or use extremely restrained reframing.
- Reconstruction motion is subtle and only when it adds depth or reveals information.
- Cuts should land on narration phrase/word boundaries where possible.
- No more than two highly similar views in a row.
- Repeated identical source images must not create fake cuts.
- Major section changes may use a restrained transition; ordinary shot changes should not.
- No generic UI/card slideshow treatment over every beat.
- Captions remain one layer: white base, orange current word.
- No caption/provenance/editorial overlays in the YouTube end-screen zone.

This file overrides any earlier episode note that says `HISTORICAL SOURCE only` or that suppresses reconstruction provenance.

## End-screen episode logic

End-screen layout must reflect the actual publication order, not a generic reusable template.

- Episode 1: **zero video recommendation slots**; optionally one subscribe/avatar target only.
- Later episodes: video slots may be used only when there is an actual published video to link.
- Never render a placeholder rectangle for a nonexistent previous/next video.
- End screens remain textless unless the user explicitly approves text.
