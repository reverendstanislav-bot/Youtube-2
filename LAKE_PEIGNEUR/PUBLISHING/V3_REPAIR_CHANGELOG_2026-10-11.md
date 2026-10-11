# LAKE PEIGNEUR — DIRECTORIAL REPAIR V3

Date: 2026-10-11
Status: **RENDER AND TECHNICAL QC COMPLETE / V3 MASTER DELIVERED; OWNER REVIEW PENDING**.
Latest owner instruction: all long-form and Shorts without subtitles; only approved end screens; no invented editorial slides / abrupt zoom or horizontal movement.

## Exact approved end screen identified
Chicago R15 authoritative end-screen layout from `chicago-r15-smooth-remotion-review-20260924` GitHub Release:
- Asset inside `HIA_CHICAGO_R15_SMOOTH_REVIEW_QC.zip`: `qc/stills/012.png`
- Full 1920×1080 PNG
- SHA256 `b794e5582699e90812b25208ca1c5dd053df465825d1ce6e33a7a0c6ea53b575`.
- Associated `qc/END_SCREEN_LAYOUT.json` explicitly: `episode=1`, `video_slots=0`, `subscribe_avatar_slots=1`, `text_labels=0`.
- The rejected custom charcoal `CleanEndScreen` JSX function was entirely removed.
- This screen is for the FIRST video. The normal subsequent-video end-screen source is separate and is **not** changed here.

## Motion and subtitle cleanup
- Rejected V1 CSS per-slot scale reset: **removed**.
- Original wipes/fast clip-path/blur transitions: **removed**.
- Implemented 18-frame cross-dissolves, stable geometry: NO zoom, slide, pan or image scale reset.
- Burned dialogue subtitles / `Caption` renderer: **absent**.
- Editorial Chapter and Fact labels retained. They are not spoken subtitles.

## Rejected graphic / asset removal
The following were replaced in original recovered timeline with already approved original photographic reconstruction assets:
- LP-GFX-014 → LP-REC-020 (workers underground, no generic timer)
- LP-GFX-024 → LP-REC-010 (water/salt-wall visual, no generic industrial tank-loop)
- LP-GFX-035 → LP-REC-037 (actual physical setting, not synthetic inaccurate canal map)
- LP-GFX-036 → LP-REC-038 (no fictitious lock-gate graphic)
- LP-GFX-045 → LP-REC-006 (drilling operation, not mixed evidence-collage)
- LP-GFX-048 → LP-REC-043 (investigative/legal discussion, no big orange collage)
- At beat LP-B073, prior custom LP-GFX-049_EDITOR_REPAIR removed in V2; LP-REC-043 replaced with LP-REC-040 to keep source reuse max two and improve scene variety.
- LP-GFX-054 → THREE separate shots: LP-REC-014 (mine), LP-REC-035 (shore), LP-REC-039 (canal), each ~4s, instead of three-panel AI collage.
- Previously removed LP-GFX-055 (generic final title-card illustration), replaced with approved LP-REC-045 for the story conclusion.
- Previous artificial LP-REC-044 `OPERATIONS SUSPENDED` sign is still excluded, replaced with approved LP-REC-042.

Only approved preexisting original images used. **ZERO new paid generation**.
Current physical timeline has **87 beats / 99 individual picture slots**; max reuse per image **2**.

## Source patch delivered
Actual modified JSX + timeline + approved original first-video end card and V2 Shorts renderer:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/1bbbe958-3f59-47b2-8a3b-436292440ff6.zip
Archive SHA256:
`58a62008e3e901cdaaeda815793e22578f7ef1d9f21c99b1d7633f548bdb6418`.

## Four improved Shorts
Physically exported 4 portrait 1080×1920 videos with 0.4-sec dissolves, no zoom or subtitles. Audio edits are source-locked and the reversal/cause Shorts are in source order.
Download:
https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/2001dfc1-6067-4894-8e90-833242b4712d.zip
ZIP SHA256:
`6c86cc3123e3f26a2536869a60c263675adb3f84c9cf6574392b34cec783abae`.

## Release blockers
The latest V3 long master must still finish rendering, undergo the full FFmpeg decode, black/silence checks, visual QC at all repaired timestamps, and owner review. YouTube Unlisted transcode and title+thumbnail approval are also still pending.

Never promote this entry to PUBLIC READY until those checks pass.
## V3 final render delivered

Actual MP4: https://d2ol7oe51mr4n9.cloudfront.net/user_3J3zfwu7kpgllQvPySWoLtXHwdR/b135d035-6df6-4338-b5c9-5a3a94fa324e.mp4

SHA `fbc8efae5ec482b1fd6719e359cd7d50d21ed3ea9b45e0fe7608c399e700b40d`.

Full QC report: `RELAUNCH_V3_CORRECTED_MASTER_QC_2026-10-11.md`.

V3 source patch and four Shorts are uploaded and verified. Owner editorial approval and actual YouTube Unlisted transcode are open.
