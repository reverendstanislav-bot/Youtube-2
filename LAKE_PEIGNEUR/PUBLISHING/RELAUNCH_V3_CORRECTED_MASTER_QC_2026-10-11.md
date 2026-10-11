# HIA LAKE PEIGNEUR — V3 CORRECTED REBUILD / INDEPENDENT QC

Verified 2026-10-11
Status: **V3 REAL REVIEW MASTER DELIVERED / TECHNICAL QC PASS / OWNER VISUAL APPROVAL AND YOUTUBE UNLISTED TEST PENDING**

## Delivered actual video bytes

FINAL REVIEW candidate:
`HIA_LAKE_PEIGNEUR_V3_CORRECTED_FIRST_ENDSCREEN_SMOOTH_1080P25.mp4`

Direct URL:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/b135d035-6df6-4338-b5c9-5a3a94fa324e.mp4

Size: **230,665,354 bytes**
SHA256: `fbc8efae5ec482b1fd6719e359cd7d50d21ed3ea9b45e0fe7608c399e700b40d`
1920×1080, H.264 at 25fps, 24,711 video frames, **16:28.440**.
Source: original Codex/Higgsfield PNG images (not earlier compressed/suptitled user MP4).
Render: Remotion 4, CRF15 intermediate chunks, FFmpeg stream-copy concat (no extra video re-encode).
BT.709 matrix/transfer/primaries, TV/limited range.
Audio: original Arthur VO master, 48kHz AAC stereo, approximately 188kbps, original 43ms alignment offset.
Measured video bitrate: ~1.672 Mbps. IMPORTANT: static PNG footage compresses at CRF15; this is not a YouTube transcode PASS and no image detail is invented by claiming 8Mbps. The YouTube Unlisted HD check is still required.

## Actual QC evidence

- ALL NINE component MP4s: correct expected frame count (3000×8 + 711), 1080p25.
- FINAL V3 MP4: **24,711 frames**, full video/audio FFmpeg decode without errors.
- `blackdetect`: **0 black events ≥0.4s**.
- `silencedetect`: **only ~968.471–988.459s**, expected ~19.99s silent end screen.
- Final container: **no subtitle stream**.
- Verified corrected Remotion source has **NO `Caption` component**, no SRT/ASS burn-in and no words highlighted.
- Spot/visual QC from final V3 export at 2, 7, 12, 214, 438, 548, 560, 736, 773, 802, 912, 917, 920, 960, 970 and 980 seconds. Verified target scenes now show original photographic/industrial visuals instead of rejected generated collages.
- No full-frame-by-frame editorial or legal certification is claimed.

### Approved FIRST-EPISODE end screen

Exactly from HIA **Chicago R15** original QC:
GitHub release `chicago-r15-smooth-remotion-review-20260924`, asset `HIA_CHICAGO_R15_SMOOTH_REVIEW_QC.zip`, interior path `qc/stills/012.png`.

Source PNG SHA256:
`b794e5582699e90812b25208ca1c5dd053df465825d1ce6e33a7a0c6ea53b575`.

Verified `qc/END_SCREEN_LAYOUT.json`:
`episode=1; video_slots=0; subscribe_avatar_slots=1; text_labels=0`.

The rejected invented charcoal/gray typography endscreen was completely removed.
Normal other-episode end-screen files were NOT modified.

### Transition and shot-edit repairs

- Reject V1 `scale()` reset on every shot removed.
- Reject wipe/blur/abrupt picture zoom removed.
- Gentle **18-frame dissolves at original absolute beat transitions**.
- NO panning, lateral motion, or per-shot scale animation.
- Native `Chapter` and `Fact` informational editorial overlays retained and are not dialogue captions.
- Opening uses drilling platform then APPROVED underground reconstruction image at ~6s instead of new generated graphic.

### Reject visual repairs / story alignment

Rejected editor-native art:
- original ad-hoc LP-GFX-049_EDITOR_REPAIR legal card removed; documentary source imagery substituted;
- LP-GFX-055 final flat typography card removed; existing LP-REC-045 substituted;
- invented LP-REC-044 mine suspension sign removed; existing LP-REC-042 substituted.

Additional documentary director repair (only original already generated/source-locked images, ZERO paid generation):
- LP-GFX-014 fake clock → LP-REC-020 mine workers
- LP-GFX-024 generic pipe feedback loop → LP-REC-010 salt/water visuals
- LP-GFX-035 weak synthetic map → LP-REC-037 context
- LP-GFX-036 incorrect gated canal graphic → LP-REC-038 physical canal visual
- LP-GFX-045 evidence collage/rig → LP-REC-006 drilling source
- LP-GFX-048 big orange legal-card collage → LP-REC-043 legal/investigation source
- LP-B073 duplicate → LP-REC-040 aftermath landscape
- LP-GFX-054 three-panel bad composite → THREE sequential slots: LP-REC-014 flooded mine → LP-REC-035 eroding shoreline → LP-REC-039 canal

Director-repaired timeline **87 beats / 99 individual picture slots**, maximum identical source reuse **2**.

## Four replacement Shorts — actual VIDEO delivery

https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/2001dfc1-6067-4894-8e90-833242b4712d.zip
ZIP size 36,878,138 bytes, SHA256:
`6c86cc3123e3f26a2536869a60c263675adb3f84c9cf6574392b34cec783abae`

Each is 1080×1920 25fps MP4, **caption-free**, source Arthur VO, 0.4sec fade/dissolves and no zoom, full FFmpeg decode PASS:
- LP-S01 43.440s — SHA `6020400d27d2d3e07f0d65e9169d5634feebf1e2d6cd8c3cb6d60c76649da48d`
- LP-S02 40.640s — SHA `3fdeb7f64e290b01a05810ce0f9ce3920fd786158b7376f35a1c119e807f4987`
- LP-S03 54.000s — SHA `3e9ff822decae0f531967386b67279071cb147d82913ad5427c447464cc65aaa`
- LP-S04 38.760s — SHA `39a060f6a907d594cf3acf623fdf09bd8ff587947219b46e9b44fad83fac1296`

## Source patch and review imagery

Reproducible V3 JSX/timeline patch including actual approved original endscreen:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/1bbbe958-3f59-47b2-8a3b-436292440ff6.zip
Bytes 4,312,821, SHA `58a62008e3e901cdaaeda815793e22578f7ef1d9f21c99b1d7633f548bdb6418`.

Actual master samples / FFprobe / QC ZIP:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/544b06c0-c3c6-4798-8a10-e7de8505b6c4.zip
Bytes 350,227, SHA `895d398ee68d46feb64e04cb96562f7a72e0f59be5eb51ace261e56e6a9aee5d`.

## Still-open real publication gates

1. **Six historical CONDITIONAL reconstruction IDs still physically used:** LP-REC-005, LP-REC-008, LP-REC-010, LP-REC-012, LP-REC-038, LP-REC-041. These are native approved original generated PNGs and NOT automatically rights violations, but previous director comments (offshore visual bias, not salt-specific, generic refinery/reversal visibility) merit owner QC before public. DO NOT call all of them PASS without that look.
2. Fact-level provenance/provider-rights reconciliation (source manifests recovered; not equal to legal signoff).
3. Owner review of V3 actual MP4 + 4 Shorts after prior repeated quality failures.
4. **Title/thumbnail pairing not owner-approved.** No title is locked by this work.
5. Correct Peigneur/Delcambre pronunciation human listening QC.
6. Studio upload **Unlisted**; wait for HD and inspect actual YouTube encoded stream for softness/artifacts before Public.
7. Review native Subscribe control placement over approved circle and chapters/metadata/AI disclosure.

**READY_FOR_EDITORIAL_REVIEW: YES.**
**READY_FOR_UNLISTED_TEST: YES (owner can test playback).**
**READY_FOR_PUBLIC: NO.**
Do NOT use retired V1/V2 masters.

No Higgsfield generation, TTS or video generation jobs; all rendering from existing source via Remotion/FFmpeg, 0 generation credits spent.
