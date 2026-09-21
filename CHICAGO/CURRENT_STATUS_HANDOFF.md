# CHICAGO — CURRENT STATUS / HANDOFF

## Canonical status

**Episode 1 — Chicago is reopened for repair. It is NOT an approved publication master.**

The latest known user-visible defect:
- subtitles still drift / "уезжают";
- prior attempts did not actually solve the timing problem.

Do not call the old `HIA_CHICAGO_FINAL_UPLOAD.mp4` final merely because of its filename.

## Next editing objective

1. Recover/identify the real full Chicago source build.
2. Validate video/audio integrity.
3. Inspect subtitle timing across the whole episode, especially long-term drift rather than only individual lines.
4. Fix subtitle timing from one clean source of truth.
5. Avoid duplicate burned caption layers.
6. Preserve already-accepted picture and audio unless a concrete defect requires a change.
7. Build a new review.
8. User reviews the corrected review.
9. Only after explicit approval: native upload master + full QC.

## Connected-storage state (2026-09-20)

### Canonical source archive recovered

- source archive recovered: **yes**
- exact original filename: `Hidden_Industrial_America_Chicago_CODEX_READY_v7.rar`
- original size: `4,741,988,746` bytes (`4.416319304 GiB`)
- SHA-256: `2fcfcd4767ce0d6234b72a33bde08ea0b5fe0cdb4eb3d9150515cba56ef705eb`
- release tag: `chicago-source-archive-v1`
- release URL: <https://github.com/reverendstanislav-bot/Youtube-2/releases/tag/chicago-source-archive-v1>
- binary parts: `3`
- verification: **PASS** — local split/reassembly, GitHub API asset sizes and server-side SHA-256 digests, downloaded-part SHA-256 checks, and full download/reassembly SHA-256 all match

This archive is the canonical **source package**. It is not a final YouTube master. The unresolved subtitle-drift status below is unchanged.

Dropbox contains:
- `HIA_DBX_00.part` … `HIA_DBX_13.part`
- total bytes: `1,299,535,967`
- standalone `HIA_CHICAGO_FINAL_UPLOAD.mp4`: `31,053` bytes — invalid/incomplete as a master.

See `SOURCE_FILES/DROPBOX_PARTS_MANIFEST.json` and `tools/reassemble_dropbox_parts.py`.

## Historical project-package state

Previously uploaded in project chats:
- `Hidden_Industrial_America_Chicago_CODEX_READY_v7(5).rar`
- `Hidden_Industrial_America_Chicago_CODEX_READY_v7(6).rar`
- `Hidden_Industrial_America_Quick_Usage_Guide_RU(1).pdf`

The intent was to merge the two CODEX_READY archives without duplicates or loss and include the quick usage guide as item 11 in the combined package.

Those original attachments are not currently accessible from the connected GitHub/Dropbox sources. Do not invent their contents. If they are reattached, ingest them into this directory/release structure and record hashes.

## Channel context

Chicago is Episode 1. TC-497 is Episode 2. Branding must stay universal for **Hidden Industrial America**, not tied to tunnels, Chicago, or a single industrial category.

## Automated source-archive audit

- archive SHA-256 verified: PASS
- RAR integrity test: PASS
- full file inventory: `CHICAGO/AUDIT/SOURCE_INVENTORY.json`
- human-readable audit: `CHICAGO/AUDIT/SOURCE_AUDIT.md`
- text/subtitle/build audit: `CHICAGO/AUDIT/TEXT_SOURCE_AUDIT.md`


## Independent media/subtitle audit result

GitHub Actions audit `Audit Chicago Media and Subtitle Sync` independently re-extracted the actual V1/V2 finals from the canonical RAR and checked them against word-level narration timing.

### Media
- V1 `_FINAL/HIA_CHICAGO_FINAL_UPLOAD.mp4`: 1920x1080, 25 fps, 1290.720 s, full decode **PASS**.
- V2 `_V2/final/HIA_CHICAGO_V2.mp4`: 1920x1080, 25 fps, 1290.720 s, full decode **PASS**.
- V1 and V2 AAC elementary streams are bit-identical:
  `a1e84ecb33a2060075b5681a086bf59b166396e16564b8e705a5b201dc4928ed`.

### Subtitle timing
- `03_TIMELINE/subtitles_en.srt`: **REJECTED / DO NOT USE**.
  Independent whole-film alignment found progressive/variable timing errors: P05/P95 offset about -9.726 / +4.996 s and ~9.6 s modeled drift across runtime.
- `_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt`: independent alignment **PASS**; median start offset 0.000 s.
- `_V2/final/HIA_CHICAGO_V2.srt`: independent alignment **PASS**; median start offset 0.000 s.
- V2 also contains actual mixed-audio spot checks at opening/middle/end that are mostly within about ±0.16 s; one isolated cue near 08:37 was handled separately in the source QC.

### Repair source rule
The legacy timeline SRT is now positively identified as the bad timing source and must never be used in another Chicago render.

The preferred technical candidate for the next review is the V2 picture/audio with captions rebuilt from the V2 final SRT / word-level timing source. This is still **not** a publication-master decision until the resulting visible captions are reviewed by the user.


## Final V2 QC status

V2 has now completed an additional final technical + visible-caption QC.

- `HIA_CHICAGO_V2.mp4`: technical upload candidate **PASS**.
- Full decode: PASS.
- 1920x1080 / 25 fps / 21:30.720.
- SHA-256: `f05d600780111e7ebdc2ac6aac29fcf1cb76704e13b4a14d355cbfc713c896e2`.
- V2 SRT timing: PASS against word-level VO timing.
- The encoded V2 MP4 contains **no burned narration subtitle layer**.
- `HIA_CHICAGO_V2.srt` is a sidecar caption file.
- Eight cue-centered encoded-frame samples found expected V2 subtitle text in 0/8 frames, consistent with the V2 build code, which generates sidecar captions rather than burning them into video.

Therefore:
- for YouTube delivery with optional CC: V2 + V2 SRT is technically ready;
- for a channel standard requiring always-visible/running subtitles: one final subtitle-burn render is still required.

No picture/audio re-edit is currently indicated by QC.

See `CHICAGO/QC/V2_FINAL_QC.md`.


## V2 full sequence/composition audit

The visible-caption review exposed systemic composition/pacing problems. Current visible-caption review is **REJECTED** and must not be promoted to publication master.

Confirmed:
- all six explainer systems conflict with the normal lower caption zone;
- affected explainer runtime: ~174.6 s;
- transfer problem range: 04:01.52–04:33.08;
- basement problem range: 09:06.12–09:46.40;
- V2 is 67% static-shot runtime;
- 72 detected near-static intervals last >=3 s;
- major map-heavy repetitive block: ~05:49–07:17;
- repeated State Street archive bouncing: ~01:10–02:34;
- 23 source returns within six shots;
- coal explainer contains 1.04 s and 1.16 s consecutive cuts around 08:30;
- late-film reconstruction sequence ~19:05–20:18 requires consolidation.

The problem is now classified as **picture sequencing + caption-safe composition**, not subtitle timing.

Audio must remain untouched. V2 remains the base source.

See:
- `CHICAGO/QC/V2_FULL_SEQUENCE_AUDIT.md`
- `CHICAGO/AUDIT/V2_SEQUENCE/`


## V3 sequence-fix review

V3 supersedes the rejected V2 visible-caption review as the current review candidate.

Workflow:
- `Build Chicago V3 Sequence Fix Review`
- run `35544915218`
- conclusion: SUCCESS

Review file:
- `HIA_CHICAGO_V3_SEQUENCE_FIX_REVIEW_960x540.mp4`
- SHA-256 `4a88e004a416775ee98eaa385cf1067d41b55df4d1d2cc5ec4fc1c66cac21f07`
- release tag `chicago-v3-sequence-fix-review-20260920`

Key changes:
- rebuilt from clean V2 work-assets;
- old lower three-card explainers removed;
- compact upper-left process rail used instead;
- provenance labels moved upper-right;
- State Street A/B/A bouncing reduced;
- 05:49–07:17 map progression rebuilt;
- coal 1.04s + 1.16s flash pair merged;
- late reconstruction sequence semantically consolidated;
- one white-base / orange-active running caption layer;
- end-screen captions use top-safe placement;
- original AAC preserved bit-for-bit.

Sequence metrics vs V2:
- shots 217 → 207
- shots <1.5s 4 → 2
- A→B→A returns 5 → 3
- source returns within six shots 23 → 10

Status:
**READY FOR USER REVIEW. NOT FINAL / NOT PUBLICATION MASTER until explicit approval.**

See `CHICAGO/V3/REVIEW_QC/`.


## V4 Remotion review

V4 supersedes V3 as the current Chicago review candidate.

Workflow:
- `Build Chicago V4 Remotion Review`
- run `35550663818`
- conclusion: SUCCESS

Review:
- `HIA_CHICAGO_V4_REMOTION_REVIEW_960x540.mp4`
- SHA-256 `8df567038ece5af9b5650eb88cc32bb7eeff6f3ccd701de98e60e0f55170032a`
- release tag `chicago-v4-remotion-review-20260920`

Key differences from V3:
- legacy PIL/FFmpeg explainer cards removed entirely;
- explainer inserts are now Remotion motion graphics only;
- no opaque cards/panels;
- motion language uses line reveal + spring/fade/slide + phase progress rail;
- one Remotion subtitle layer, white base + orange active word;
- end-screen captions use top-safe placement;
- original V1/V2 AAC preserved bit-for-bit;
- full decode PASS;
- sequence remains the cleaned 207-shot V3/V4 plan.

Status:
**READY FOR USER REVIEW. NOT FINAL / NOT PUBLICATION MASTER until explicit approval.**


## V5 editorial Remotion review

V5 supersedes V4 as the current Chicago review candidate.

Workflow:
- `Build Chicago V5 Editorial Review`
- run `35556163548`
- conclusion: SUCCESS

Review:
- `HIA_CHICAGO_V5_EDITORIAL_REVIEW_960x540.mp4`
- SHA-256 `032155221bcb33035eb72f7e28521a81134accf1049fc7f2797700d2fe4956ca`
- release tag `chicago-v5-editorial-review-20260920`

Visual system:
- large off-white serif headline;
- orange kicker / subline;
- compact step marker;
- animated Remotion reveal / hold / fade;
- no gray process-rail UI;
- no opaque cards;
- all editorial cards stay in upper 75% of frame;
- bottom subtitle-safe zone remains clear;
- one white-base / orange-active running subtitle layer;
- original AAC preserved bit-for-bit.

Technical QC:
- full decode PASS;
- 338 caption cues;
- 98.665% word-level mapping;
- 207-shot cleaned sequence;
- 33 editorial cards.

Status:
**READY FOR USER REVIEW. NOT FINAL / NOT PUBLICATION MASTER until explicit approval.**


## V5 editorial review

V5 supersedes V4 as the current Chicago review candidate.

Workflow:
- `Build Chicago V5 Editorial Review`
- run `35556163548`
- conclusion: SUCCESS

Review:
- `HIA_CHICAGO_V5_EDITORIAL_REVIEW_960x540.mp4`
- SHA-256 `032155221bcb33035eb72f7e28521a81134accf1049fc7f2797700d2fe4956ca`
- release tag `chicago-v5-editorial-review-20260920`

Editorial overlay language:
- large off-white serif headline;
- orange kicker / orange subline;
- compact step marker;
- no gray process rail UI;
- no opaque cards;
- editorial cards restricted to upper 75% of the frame;
- bottom subtitle-safe zone remains clear;
- cards appear briefly at narrative beats instead of persisting across a whole explainer sequence.

Audio:
- original V1/V2 AAC preserved bit-for-bit;
- AAC SHA-256 `a1e84ecb33a2060075b5681a086bf59b166396e16564b8e705a5b201dc4928ed`.

QC:
- full decode PASS;
- 338 subtitle cues;
- word-level caption token match 98.665%;
- 33 editorial cards;
- 207-shot cleaned sequence;
- A→B→A returns: 3;
- source returns within six shots: 10.

Status:
**READY FOR USER REVIEW. NOT FINAL / NOT PUBLICATION MASTER until explicit approval.**


## V7 readability + provenance review

V7 supersedes V6 as the current Chicago review candidate.

Workflow:
- `Build Chicago V7 Readability Provenance Review`
- run `35565115646`
- conclusion: SUCCESS

Review:
- `HIA_CHICAGO_V7_READABILITY_PROVENANCE_REVIEW_960x540.mp4`
- SHA-256 `a29a629f6a4e5c99ab4f1457170ce37d7166706cc8984e1a809fd92b30904445`
- release tag `chicago-v7-readability-provenance-review-20260920`

V7 changes:
- `AI RECONSTRUCTION` removed completely;
- provenance label is `HISTORICAL SOURCE` only;
- no black / gradient overlay backgrounds;
- main title gets thin dark glyph stroke + compact shadow for light-background readability;
- kicker / subline / step use lighter glyph stroke + shadow;
- no panel/background introduced;
- V6 typography scale and upper-frame placement preserved;
- bottom subtitle-safe zone remains clear;
- original AAC preserved bit-for-bit;
- full decode PASS.

Status:
**READY FOR USER REVIEW. NOT FINAL / NOT PUBLICATION MASTER until explicit approval.**
