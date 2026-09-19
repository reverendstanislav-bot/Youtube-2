# TC497 — CURRENT HANDOFF / USER REVIEW NOT COMPLETE

## PROJECT STATUS

Episode: LeTourneau TC-497 Overland Train  
Project: Hidden Industrial America / YouTube-2

Current state: **FULL_V8 IS THE CURRENT REVIEW VERSION. IT HAS BEEN BUILT AND INSPECTED, BUT THE USER HAS NOT APPROVED THE VIDEO YET.**

This distinction is critical.

Do **not** say the film is final.  
Do **not** say any 1080p master is approved.  
Do **not** proceed to publishing metadata as though the edit is locked.

## CURRENT REVIEW VERSION

Review artifact:
- GitHub Actions run: `35426397417`
- artifact: `tc497-full-v8-review`
- artifact id: `10579345943`
- size: ~288.3 MB
- review resolution: 960×540
- duration: 20:36.533
- video: H.264 / 30 fps
- audio: AAC
- integrated loudness: -13.5 LUFS
- LRA: 3.7 LU
- true peak: -1.9 dBFS

Relevant files:
- `TC497/FULL_V8/ENDING_DECISION.md`
- `TC497/FULL_V8/v8_fast_render.py`
- `.github/workflows/build_tc497_full_v8.yml`
- `TC497/FULL_V7/generate_outro_music.py`

Status:
- FULL_V8 review render succeeded;
- ending frames and audio QC were inspected;
- user approval is still pending.

## WHY V8 EXISTS

A 10-viewer editorial audit of FULL_V6 found that the remaining strongest weakness was the ending.

The old ending used a centered channel card:
- `HIDDEN INDUSTRIAL AMERICA`
- `THE MACHINE WORKED. THE WORLD MOVED ON.`

It then continued into a generic spoken/subtitled subscribe CTA.

The combination felt like a temporary YouTube bumper rather than the end of a premium documentary.

The existing V5/V6 music architecture also ended around 19:45, leaving roughly the final 51 seconds without a proper musical resolution.

## WHAT FULL_V8 CHANGED

FULL_V8 keeps the approved-in-principle V6 picture/edit before the ending and changes only the tail:

- keeps the final documentary sentence: `something that no longer needed one.`;
- removes the old centered end slogan;
- removes the generic spoken/subtitled subscribe CTA after ~20:25.45;
- replaces the branded final plate with a clean Yuma/desert image;
- uses restrained left-aligned modern editorial typography:
  - `HIDDEN INDUSTRIAL AMERICA`
  - `TC-497`
  - `OVERLAND TRAIN`
- leaves the right side visually quiet for YouTube end-screen elements;
- adds an original copyright-independent resolving music cue from ~19:45 through the ending;
- no zoom ping-pong;
- no collage blocks;
- no fake archive treatment;
- no third-party commercial music.

The final ~11 seconds are now desert / restrained identity / resolving music rather than a sales CTA.

## 10-VIEWER AUDIT — MAIN FINDINGS

1. Casual YouTube viewer
   - Cold open works.
   - Middle can feel longer than its actual cut rate because similar desert/machine/reconstruction families recur.
   - Old ending was the clearest weak point.

2. Industrial-history viewer
   - Archive documents, patents, Yuma material and survivor imagery are the strongest trust-building visuals.
   - Reconstructions work best when documentary evidence remains dominant.

3. Engineer
   - Electric Wheel is materially clearer after V6.
   - A few long technical holds still feel presentation-like.

4. Documentary/cinema viewer
   - Overall grade is coherent.
   - Generated desert reconstructions share a similar beige/olive family.
   - Old centered end card broke the cinematic resolution.

5. AI-skeptical viewer
   - ARCHIVE / DOCUMENT / RECONSTRUCTION / CONCEPT grammar is essential and generally works.
   - Some polished reconstructions rely heavily on their source labels for trust.

6. Mobile viewer
   - Main subtitles are readable.
   - Some provenance labels are relatively small.
   - Removing the centered CTA reduces text competition at the end.

7. Sound-sensitive viewer
   - VO remains clear.
   - V6 lacked a real musical resolve in the last ~51 seconds.
   - V8 restores a restrained ending cue without materially changing overall loudness.

8. Retention editor
   - Biggest remaining fatigue risk is visual-family repetition rather than insufficient cutting.
   - The strongest possible future micro-fixes would target repeated middle-film visual families, not add more motion for its own sake.

9. Premium-documentary viewer
   - Survivor → empty range is conceptually strong.
   - Asymmetric, restrained branding reads materially better than the old centered slogan.

10. Potential subscriber / returning viewer
   - The film does not need a baked sales message after the emotional resolution.
   - A clean end-screen area is more useful and more premium.

## REMAINING P2 EDITORIAL NOTES

FULL_V8 is not automatically approved simply because the ending is better.

Potential remaining P2 issues for user review:
- visual-family repetition in parts of the middle;
- some provenance labels are small on mobile;
- a few technical/reconstruction holds remain long;
- specific middle areas worth checking if the user still feels drag include Yuma around ~12:38–12:56 and selected early reconstruction / sky holds.

Do not make broad pacing changes without reviewing them against the current film. The V14 cold open remains locked.

## HISTORICAL V5/V6 CORRECTIONS

FULL_V5 review artifact from run `35421885255` was inspected and two build defects were found:
1. two declared Electric Wheel replacement images were silently skipped;
2. ASS captions/source labels were missing over rendered replacement intervals.

FULL_V6 corrected those defects and preserved the V5 AAC stream bit-for-bit.

V8 is downstream from that corrected V6 review base.

## 1080p STATUS

Older 1080p candidates predate the current approved-review state and are historical candidates only.

They must **not** be promoted to final.

After the user explicitly approves the current review edit:
1. build a fresh 1920×1080 master from the approved version;
2. run final technical QC;
3. only then call that fresh build the upload master.

## EXACT NEXT STEP

1. User reviews FULL_V8.
2. Collect any remaining timecoded complaints.
3. If user wants further pacing/visual-family fixes, patch the review version again.
4. Only after explicit user approval, build a fresh 1920×1080 master.
5. Do not call any 1080p build final before that approval.

## ONE-LINE NEW CHAT COMMAND

Open `TC497/CURRENT_STATUS_HANDOFF.md` in `reverendstanislav-bot/Youtube-2` and continue from there. FULL_V8 is the current review build with the redesigned cinematic ending, but it is **NOT user-approved**; do not treat any 1080p build as final until the user explicitly approves the video.
