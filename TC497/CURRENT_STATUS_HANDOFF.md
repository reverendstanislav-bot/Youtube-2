# TC497 — FULL_V12 CURRENT REVIEW

## STATUS

Episode: LeTourneau TC-497 Overland Train
Project: Hidden Industrial America / YouTube-2

Current state: **FULL_V12 is the active review version. It fixes the V10/V11 duplicate subtitle/backplate defect and has passed targeted technical/visual QC, but the user has not approved it yet.**

Do not use FULL_V10 or FULL_V11 as publication candidates.
Do not promote a new 1080p final until explicit FULL_V12 approval.

## CURRENT REVIEW

- run: `35469141767`
- artifact: `tc497-full-v12-review`
- artifact id: `10591798476`
- digest: `sha256:156a1ccd90f7631261dcd075cac35022b068920e7c4d4b5debd63e4b48bbd8f9`
- file: `TC497_FULL_V12_REVIEW_960x540.mp4`
- file SHA-256: `565302f81f3ee403d41098325e36a71ecb6349b29267089c828ea5e7659cfc6c`
- duration: 20:36.533
- 960x540 / 30 fps / 37,096 frames

## IMPORTANT FIX

The large black subtitle rectangle in FULL_V10/FULL_V11 was caused by a second full-film ASS caption layer:
- `BorderStyle=3`
- `Outline=45`
- rendered on top of already-baked V9 captions.

FULL_V12 removes that architecture entirely.

FULL_V12 is rebuilt from the V9 picture/audio lineage:
- original normal V9 subtitles remain;
- no CapV10 full-film layer;
- no giant black backplate;
- no duplicate caption echo.

Only replacement picture windows receive original V4 Cap subtitles because those replacement images cover the baked captions underneath.

## RETAINED LATER FIXES

Electric Wheel:
- 04:21.771–04:29.100 → clean ST-ELECTRIC;
- 04:55.972–05:00.858 → real LeTourneau patent;
- 07:54.502–08:00.163 → real TC-497 archive.

11:57:
- WB-N04 controlled bridge;
- engineers/model flash removed;
- abrupt reframing removed.

Audio remains bit-identical to V9:
`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

## NEXT STEP

User reviews FULL_V12.
If approved, build a fresh native 1920x1080 master from the V12 edit.
If not approved, patch FULL_V12 review again.
