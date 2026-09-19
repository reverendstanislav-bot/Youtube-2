# TC497 — CURRENT HANDOFF / USER REVIEW NOT COMPLETE

## PROJECT STATUS

Episode: LeTourneau TC-497 Overland Train  
Project: Hidden Industrial America / YouTube-2

Current state: **FULL_V6 IS THE CURRENT REVIEW VERSION AND HAS PASSED TARGETED TECHNICAL / EDITORIAL QC, BUT THE USER HAS NOT APPROVED THE VIDEO YET.**

This distinction is critical.

Do **not** say the film is final.  
Do **not** say any 1080p master is approved.  
Do **not** proceed to publishing metadata as though the edit is locked.

## CURRENT REVIEW VERSION

Review artifact:
- GitHub Actions run: `35424958934`
- artifact: `tc497-full-v6-review`
- artifact id: `10578413797`
- size: ~288 MB
- review resolution: 960×540
- duration: 20:36.533
- frames: 37,096 @ 30 fps

Reference:
- `TC497/FULL_V6/CRITIC_QC.md`
- `TC497/FULL_V6/v6_patch_chunk.py`
- `TC497/FULL_V6/v6_patch_manifest.json`
- `.github/workflows/build_tc497_full_v6.yml`

Status:
- targeted V6 critic/QC pass completed;
- user approval still pending.

## WHAT WAS FOUND WHEN FULL_V5 WAS ACTUALLY INSPECTED

FULL_V5 review artifact from run `35421885255` was downloaded and visually inspected.

Two build defects were found that the old V5 QC did not catch:

1. `TC497/FULL_V5/visual_patches.v5.json` declared seven visual replacements, but the V5 workflow downloaded only five. The two Electric Wheel continuity breakers were missing and the V5 script logged warnings and skipped them.
2. `v5_fix_and_music.py` supports reburning ASS overlays, but the V5 workflow did not pass `--source-ass`. Therefore captions/source labels disappeared over the five V5 replacement intervals that did render.

So FULL_V5's green technical status did **not** mean the intended edit was fully applied.

## WHAT FULL_V6 CHANGED

FULL_V6 uses FULL_V5 as the review base and changes only the identified regressions:

- adds the missing Electric Wheel human/control-cab breaker;
- adds the missing Electric Wheel drive-detail breaker;
- explicitly labels both new generated Electric Wheel stills as `RECONSTRUCTION`;
- restores the original V4 ASS captions/source labels across all seven replacement intervals;
- preserves all other V5 edit decisions;
- preserves the V5 AAC audio elementary stream bit-for-bit.

Verified V5/V6 AAC SHA-256:
`d171be550180d3f03fc89489c7fd2e3c9ece25f5579cfd023df0b4a7d8103722`

Verified timing:
- V5: 1236.533333 s / 37,096 frames / 30 fps
- V6: 1236.533333 s / 37,096 frames / 30 fps

V14 remains the locked cold-open grammar and was not changed.

## V6 PATCH INTERVALS

- 215.356–221.464 — Electric Wheel human/control break + RECONSTRUCTION
- 230.014–237.342 — Electric Wheel drive detail + RECONSTRUCTION
- 709.241–717.165 — Nuclear concept + restored ASS
- 730.373–736.976 — proposed/unbuilt concept + restored ASS
- 1079.245–1087.457 — heavy-lift logistics + restored captions
- 1107.164–1115.376 — ground-vs-air + restored RECONSTRUCTION/source grammar
- 1209.007–1215.477 — survivor detail + restored captions

## 1080p STATUS

Older 1080p candidates exist, including:
- run `35421769689` — `tc497-final-upload-master-v51-fast`
- run `35421316892` — `tc497-final-upload-master-1080`

These are **historical candidate masters only** and predate the V6 corrections.

They must **not** be promoted to final.

After the user explicitly approves the current review edit, build a fresh 1920×1080 master that includes the V6 corrections and run final technical QC on that new master.

## EXACT NEXT STEP

1. Present / review FULL_V6 with the user.
2. Collect any remaining timecoded complaints.
3. If the user does not approve, patch the review version again.
4. Only after explicit user approval, build a fresh 1920×1080 master from the approved edit.
5. Do not call any 1080p build final before that approval.

## ONE-LINE NEW CHAT COMMAND

Open `TC497/CURRENT_STATUS_HANDOFF.md` in `reverendstanislav-bot/Youtube-2` and continue from there. FULL_V6 is the current review build and passed targeted QC, but it is **NOT user-approved**; review it first and do not treat any 1080p build as final until the user explicitly approves the video.
