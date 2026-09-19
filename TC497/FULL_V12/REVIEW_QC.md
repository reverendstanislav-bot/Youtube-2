# TC497 FULL_V12 — duplicate subtitle layer repair QC

Status: **REVIEW READY — USER APPROVAL REQUIRED.**

Current build:
- GitHub Actions run: `35469141767`
- artifact: `tc497-full-v12-review`
- artifact id: `10591798476`
- artifact digest: `sha256:156a1ccd90f7631261dcd075cac35022b068920e7c4d4b5debd63e4b48bbd8f9`

Review file:
- `TC497_FULL_V12_REVIEW_960x540.mp4`
- SHA-256: `565302f81f3ee403d41098325e36a71ecb6349b29267089c828ea5e7659cfc6c`
- duration: 1236.533333 s
- 960x540
- 30 fps
- exactly 37,096 frames

## Root cause fixed

FULL_V10 added a second burned caption layer on top of the already-baked V9 captions.
The main V10 ASS style used `BorderStyle=3` with `Outline=45`, which produced a large black rectangle.
FULL_V11 inherited that layer.

FULL_V12 is rebuilt from the V9 1080 lineage and does **not** use the full-film V10/V11 caption overlay.

Verified at the user-reported subtitle example around 01:32:
- only the original normal subtitle remains;
- no black rectangle;
- no duplicate subtitle echo.

## Re-applied later picture fixes only

Electric Wheel cleanup:
- 04:21.771–04:29.100 → clean ST-ELECTRIC crop, RECONSTRUCTION;
- 04:55.972–05:00.858 → real LeTourneau Electric Vehicle Wheel patent, DOCUMENT • U.S. PATENT;
- 07:54.502–08:00.163 → real archival TC-497, ARCHIVE • TC-497.

11:57 repair:
- 11:56.900–12:04.500 → WB-N04 controlled bridge;
- no engineers/model flash;
- no abrupt reframing;
- bridge captions use original V4 Cap style only;
- no CapV10 style is present.

## Audio

V9 and V12 AAC are bit-identical:

`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

## Technical QC

- 960x540 / 30 fps
- 37,096 video frames
- duration 20:36.533
- no blackdetect events at the configured threshold
- V8 ending preserved
- V14 cold open preserved

FULL_V12 is not final until explicit user approval.
