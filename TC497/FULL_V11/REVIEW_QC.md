# TC497 FULL_V11 — targeted review QC

Status: **REVIEW READY — USER APPROVAL REQUIRED.**

Current build:
- GitHub Actions run: `35460168540`
- artifact: `tc497-full-v11-review`
- artifact id: `10589563318`
- artifact digest: `sha256:3d99b07887f3a49692eb890146f83ff60fde33f1f8e0084aeb98d751dbd87bdd`

Review file:
- `TC497_FULL_V11_REVIEW_960x540.mp4`
- duration: 1236.533333 s
- 960x540
- 30 fps
- exactly 37,096 video frames

## Electric Wheel cleanup

Confirmed against V4 `shots.json`: WA-09 had three uses.

All three are removed in FULL_V11:

1. `04:21.771–04:29.100`
   - replaced by a clean crop of existing `ST-ELECTRIC`;
   - shows distributed electrical drive logic instead of a fake wheel cutaway;
   - no orange collage corners;
   - label: `RECONSTRUCTION`.

2. `04:55.972–05:00.858`
   - replaced by the real LeTourneau `Electric Vehicle Wheel` patent figure;
   - U.S. Patent 2,726,726;
   - label: `DOCUMENT • U.S. PATENT`.

3. `07:54.502–08:00.163`
   - replaced by real archival TC-497 proving-ground imagery;
   - avoids an unnecessary third return to the wheel-motor visual;
   - label: `ARCHIVE • TC-497`.

No new AI wheel image is used.

## Preserved

Verified sampling confirms:
- FULL_V10 semantic subtitle highlights remain;
- FULL_V10 11:57 transition repair remains;
- V14 cold open remains;
- V8 ending remains;
- V9 middle-film corrections remain.

## Audio

FULL_V10 and FULL_V11 AAC are bit-identical:

`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

## Technical QC

- 960x540 / 30 fps
- 37,096 video frames
- duration 20:36.533
- no blackdetect events at the configured threshold
- V10 audio copied bit-for-bit

FULL_V11 is not final until explicit user approval.
