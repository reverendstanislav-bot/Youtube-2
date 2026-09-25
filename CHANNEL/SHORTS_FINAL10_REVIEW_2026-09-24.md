# HIA Shorts — Final 10 Review Build

Date: 2026-09-24
State: **RENDER_REVIEW / OWNER VISUAL APPROVAL REQUIRED**

## Owner-approved style reference

CHI-S01 reference:
`CHI_S01_SAFE_V2_PLAQUE_ONLY_FIX.mp4`

Locked behavior:
- full-screen 1080x1920 native vertical;
- bottom darkening preserved;
- white running captions with orange active word;
- captions raised into Shorts-safe area;
- no blurred portrait wrapper;
- no floating 16:9 strip;
- no editor-native explanatory GFX;
- no AI RECONSTRUCTION plaque;
- no DOCUMENT plaque;
- no CONCEPT plaque;
- visible HISTORICAL SOURCE only on verified archive/map frames;
- no pan / slide / zoom motion;
- static reframes + hard cuts;
- no new image/video generation.

## GitHub source recovery

The original complete 10-Short review pack was found in GitHub release:
- tag: `hia-shorts-v10-review-20260923`
- asset: `HIA_SHORTS_V10_REVIEW_10.zip`
- release asset id: `584643599`

This recovered the previously missing:
- `TC497-S01_V10_REVIEW.mp4`
- `TC497-S02_V10_REVIEW.mp4`

The old V10 files were **not** promoted as current finals because their visual system contains now-rejected provenance/GFX behavior. They were used as exact Short-audio/reference sources for the current rebuild.

## Remaining-nine locked-native rebuild

Workflow:
`.github/workflows/build_hia_remaining9_locked_native.yml`

Renderer:
`SHORTS_RENDER/build_locked_native_vertical.py`

Actions run:
`36036563543`

Render head:
`9b6608215aa65277e1750e94671a923bdae41791`

All jobs:
- Chicago: PASS
- TC497: PASS
- package: PASS

Artifacts:
- Chicago S02-S05: `10825003142`
  - digest: `sha256:b20f04eefc5f75b23dcf1850108d0af5dae1405b8dc858e14d05705f58c0877b`
- TC497 S01-S05: `10824083660`
  - digest: `sha256:ff9727e01cbae7b6cf78d1fc6c0cc1e19ba8361e54b2bb81ae98f2cec2272723`
- combined remaining-nine: `10824053593`
  - digest: `sha256:768c9a150c26d96623a33c5997fdefdb4e4db6d8ad6d06dfca8bef23ba1ed39b`

## Hard QC

### Chicago
- CHI-S02 — PASS — 42.00 s
  - SHA256 `2f8263da7bef732fd3b7c13ec8e6fd28e1a52cb757fd2cea79851bf0663d2c2b`
- CHI-S03 — PASS — 26.44 s
  - SHA256 `55c4bfb8caa9f4c18ae7763a488ebe92cd4ba5bfbeb885c3ccd22be4509fb2d0`
- CHI-S04 — PASS — 44.40 s
  - SHA256 `66ba1fa6191874d618b3e5c6e2e619f0081bd1b8fa6223d6246fa181bb9fcbbd`
- CHI-S05 — PASS — 47.12 s
  - SHA256 `cd705c9b17607d36059f36a32fd167d13f5ba17f1e4b1df236fdbd888f580e2c`

### TC497
- TC497-S01 — PASS — 53.88 s
  - SHA256 `e85f5777c3286093ad9bb0e25d17dc2debcb081c4e01979fbc9ae46a0c2664e3`
- TC497-S02 — PASS — 50.80 s
  - SHA256 `d9f82b6ecf377a68466fd226b89fdac6f31157f70a5aa8f9422264318cf2e785`
- TC497-S03 — PASS — 38.02 s
  - SHA256 `8a69f0b32e7ec722540344d078f7c3d1158ce6cb49890c6a868bfd8f5c83bdca`
- TC497-S04 — PASS — 45.58 s
  - SHA256 `fbc5c2efb88d35a12aec633b505b248567f9fde1716e99fa50956cbc6018b018`
- TC497-S05 — PASS — 53.86 s
  - SHA256 `80cf66fdd0fdfb99924553be4b737e06eaf3f3ef82eaa452dba4651d3e4af1da`

Machine checks:
- correct 1080x1920;
- Chicago 25 fps;
- TC497 30 fps;
- AAC 48 kHz stereo;
- clean full decode;
- no forbidden ASS strings:
  - `AI RECONSTRUCTION`
  - `DOCUMENT`
  - `CONCEPT`
  - `100,100)}`
  - `Aircrafts`
- no new generation spend.

## Complete 10-Short review set

The complete review set is:
- CHI-S01 — owner-accepted SAFE V2 plaque-only-fix reference;
- CHI-S02;
- CHI-S03;
- CHI-S04;
- CHI-S05;
- TC497-S01;
- TC497-S02;
- TC497-S03;
- TC497-S04;
- TC497-S05.

This package is **not marked APPROVED or PUBLISHED** until the owner visually approves the 10/10 review set.

## Owner-locked Shorts end screen — 2026-09-24

Latest owner instruction overrides the earlier no-CTA-card note in the old extraction maps.

Locked end-screen behavior for all 10 current Shorts:
- append the approved HIA vertical end screen to the end of every Short;
- exact end-screen duration: **2.4 seconds**;
- hard cut into the end screen; no extra transition effect;
- end-screen audio: silence;
- original Short portion must remain unchanged;
- no re-edit of picture, captions, bottom darkening, timing or narration inside the original Short;
- Chicago Shorts remain 25 fps;
- TC497 Shorts remain 30 fps;
- output remains 1080x1920;
- approved CTA artwork text: **FULL STORY ON YOUTUBE / HIDDEN INDUSTRIAL AMERICA / SUBSCRIBE FOR MORE FORGOTTEN INFRASTRUCTURE**.

This end-screen rule is now the active owner override for the current 10-Short batch.

## End-screen assembly status

The current 10-Short batch has been assembled with the owner-locked HIA end screen appended for 2.4 seconds after each story payoff. The preceding Short content is preserved; only the final tail is added. All 10 assembled MP4s completed full decode QC successfully.

Current delivery package names:
- `HIA_SHORTS_FINAL10_WITH_ENDSCREEN.zip`
- `HIA_YOUTUBE_UPLOAD_FINAL_COMPLETE.zip`

The upload-only package intentionally excludes rejected/old review assets and source/QC clutter. A Chicago-specific final thumbnail remains outside the package until explicitly locked by the owner.
