# TC497 — CURRENT HANDOFF / USER REVIEW NOT COMPLETE

## PROJECT STATUS

Episode: LeTourneau TC-497 Overland Train  
Project: Hidden Industrial America / YouTube-2

Current state: **FULL_V9 IS THE CURRENT REVIEW VERSION. IT HAS PASSED TARGETED TECHNICAL / EDITORIAL QC, BUT THE USER HAS NOT APPROVED THE VIDEO YET.**

Do **not** call the film final.  
Do **not** promote any 1080p candidate.  
Do **not** proceed as though the edit is locked until explicit user approval.

## CURRENT REVIEW VERSION

Review artifact:
- GitHub Actions run: `35427554323`
- artifact: `tc497-full-v9-review-fast`
- artifact id: `10579472633`
- resolution: 960×540
- duration: 20:36.533
- H.264 / 30 fps + AAC

Reference:
- `TC497/FULL_V9/EDIT_PLAN.md`
- `TC497/FULL_V9/v9_patch_manifest.json`
- `TC497/FULL_V9/v9_patch_chunk.py`
- `TC497/FULL_V9/CRITIC_QC.md`
- `.github/workflows/build_tc497_full_v9_fast.yml`

## WHAT V9 CHANGED

FULL_V9 is based on FULL_V8 and makes four surgical middle-film visual replacements only:

- `12:46.838–12:55.922` — WC-Y01 dedicated Yuma proving-ground wide;
- `13:35.287–13:42.857` — WD-T03 terrain-constraint composition;
- `17:00.122–17:08.334` — WC-D03 ground-route-vs-airlift overhead composition;
- `17:34.611–17:42.822` — WC-D05 technology-shift overhead composition.

Purpose:
- reduce repeated machine/desert visual families in Yuma;
- reduce repeated helicopter-family imagery in the ground-vs-air transition;
- improve visual meaning without a broad recut.

All four replacement intervals:
- use existing project-approved generated reconstructions;
- are visibly tagged `RECONSTRUCTION`;
- restore V4 captions/tags over the replacement image;
- crop 12% from the raw asset edges to exclude legacy collage/corner styling.

No zoom ping-pong was added.

## AUDIO

V9 preserves FULL_V8 AAC bit-for-bit.

V8 AAC SHA-256:
`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

V9 AAC SHA-256:
`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

Therefore the V8 cinematic ending music and mix remain unchanged.

## ENDING STATUS

FULL_V8 fixed the old weak ending and V9 preserves it unchanged:

- old centered `THE MACHINE WORKED / THE WORLD MOVED ON` card is gone;
- generic spoken/subtitled subscribe CTA after the final documentary sentence is gone;
- final clean Yuma/desert plate remains;
- restrained left-aligned `HIDDEN INDUSTRIAL AMERICA / TC-497 / OVERLAND TRAIN` identity remains;
- right side remains quiet for YouTube end-screen elements;
- original resolving music remains from ~19:45 to the end.

## COLD OPEN

V14 cold-open grammar remains locked and unchanged.

## V5/V6 HISTORY

FULL_V5 had two implementation defects:
- two declared Electric Wheel replacements were silently skipped;
- captions/source labels disappeared over rendered replacement intervals.

FULL_V6 corrected those issues.

FULL_V8 then redesigned the ending.

FULL_V9 is the current downstream review version.

## 1080p STATUS

All existing 1080p encodes are historical candidates only and predate the current review edit.

They are **not final**.

Only after explicit user approval of the review edit:
1. build a fresh 1920×1080 master from the approved version;
2. run final master QC;
3. then promote that fresh build to upload master.

## EXACT NEXT STEP

1. User reviews FULL_V9.
2. Collect any remaining timecoded complaints.
3. If user approves FULL_V9, build a fresh 1920×1080 candidate from V9 and QC it.
4. If user does not approve, patch the review version again.
5. Never call a 1080p build final before explicit user approval.

## ONE-LINE NEW CHAT COMMAND

Open `TC497/CURRENT_STATUS_HANDOFF.md` in `reverendstanislav-bot/Youtube-2` and continue from there. FULL_V9 is the current review build, but it is **NOT user-approved**; review it first and do not treat any 1080p build as final until the user explicitly approves the video.
