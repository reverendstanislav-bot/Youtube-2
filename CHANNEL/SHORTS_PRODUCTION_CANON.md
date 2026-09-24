# HIA — SHORTS PRODUCTION CANON

Status: **OWNER REVIEW / NATIVE VERTICAL PROOF ACTIVE**

## 0. Rejected HIA approaches

The following HIA Shorts approaches are explicitly rejected and must not be reused:
- blurred full-height same-frame background with a small horizontal 16:9 foreground strip;
- floating/stacked horizontal frame inside portrait;
- Shorts built from editor-native replacement GFX/cards;
- visible `AI RECONSTRUCTION`, `CONCEPT`, or `DOCUMENT` provenance plaques;
- micro-dissolve / transition patches added merely to soften bad portrait composition.

The current proof direction is **native full-screen 9:16 assembly from already-approved long-form assets**, using the exact locked source audio span and word timing.

## 1. Canonical origin

Hidden Industrial America Shorts inherit the **Youtube-1 direct-cut V2 model**.

The previous HIA V10 semantic-rebuild system is **REJECTED / DO NOT USE**:
- no Shorts-only editor-native GFX;
- no rebuilding a Short from individual stills;
- no replacement visual sequence assembled separately from the long-form;
- no second caption layer;
- no Shorts-only titles/metric cards;
- no new factual claims;
- no image/video generation for Shorts unless the owner explicitly reopens the format.

Historical files and artifacts may remain for audit, but they are not production references.

## 2. Source rule

Every Short is a direct continuous cut from the current long-form master for that episode.

For each Short:
- preserve the source picture sequence exactly;
- preserve the source narration/audio exactly;
- preserve the source burned captions exactly;
- preserve source provenance labels and source GFX exactly;
- cut only at locked clean word/sentence boundaries;
- do not rebuild shots from underlying assets.

The locked extraction range is the only editorial change before the portrait wrapper.

## 3. Portrait wrapper — inherited from Youtube-1

For a 1920×1080 HIA source:

1. Split the exact same source frame into background and foreground.
2. Background:
   - scale to fill 1080×1920;
   - center crop;
   - blur;
   - slightly darken/desaturate.
3. Foreground:
   - preserve approximately 93% of original source width;
   - canonical crop: `1786×1080`;
   - canonical x offset: `67 px`;
   - scale to approximately `1080×654`;
   - vertically center at approximately `y=633`.
4. No independent foreground/background timing.
5. No duplicate visible content panels.
6. No scene-aware Shorts-only pans.
7. No artificial zoom drift.
8. No replacement graphics.

This intentionally keeps the entire approved long-form composition readable while filling the 9:16 screen with a subdued copy of the same live frame.

## 3A. Native vertical proof direction — ACTIVE

Until owner approval, this is a proof direction rather than a final channel-wide lock.

Rules:
- exact long-form audio extraction remains the narration source;
- visual sequence may use already-approved assets from the same episode to make the Short understandable on a phone;
- no new image generation;
- no new video generation;
- no invented explanatory GFX;
- no blur-fill portrait wrapper;
- use full-screen 9:16 static reframes;
- rebuild running captions for mobile from the canonical word-level transcript;
- captions: white base, orange active word;
- transitions: hard cuts by default;
- visible provenance: `HISTORICAL SOURCE` only, and only on verified historical/archive/map frames;
- reconstruction imagery is shown without an AI plaque.


## 4. HIA-native technical settings

The Youtube-1 editorial model is inherited, but HIA keeps its native master cadence/audio:
- 1080×1920;
- source episode FPS (Chicago 25 fps; TC-497 30 fps unless the approved publication master changes);
- H.264 High;
- yuv420p;
- AAC;
- preserve HIA 48 kHz stereo unless the source master requires otherwise;
- no frame interpolation.

## 5. Captions

Use **only captions already burned into the long-form master**.

Forbidden:
- new ASS/SRT burn-in;
- orange-word caption regeneration;
- duplicate subtitle layer;
- corrected display text that differs from the actual locked master;
- black caption box not present in the master.

If a source master contains a caption/audio error, fix the long-form master first. Do not silently repair it only inside the Short.

## 5A. Provenance plaque rule — OWNER LOCKED

**Visible provenance plaques are allowed only on genuinely historical/archive frames.**

Hard rules:
- `HISTORICAL SOURCE` plaque: allowed only when the currently visible picture is a verified historical/archive source.
- `AI RECONSTRUCTION`: **NEVER show a visible plaque in Shorts.**
- `CONCEPT`: no visible plaque in Shorts.
- `DOCUMENT`: no visible plaque unless the owner explicitly reopens this rule; default is no plaque.
- generated/reconstructed imagery remains visually unlabeled.
- do not invent substitute badges, corner tags, ribbons, boxes, or explanatory labels.
- historical plaque must disappear immediately when the picture switches away from the historical source.

This owner rule overrides older HIA provenance-display behavior inherited from long-form builds.

## 5B. Transition rule — OWNER LOCKED

Default: preserve clean source cuts.

If a source cut is visibly too harsh in 9:16, the only allowed repair is a **very short full-frame micro-softening** around the cut (about 3–4 frames at source FPS).

Hard rules:
- effect applies to the **entire composed frame**, never foreground/background separately;
- no partial-layer dissolve;
- no duplicated panels;
- no left/right slide, whip, pan or zoom transition;
- no long crossfade;
- no black/white flash;
- no timing change;
- no audio shift;
- no source-frame substitution.

The goal is only to remove the harsh visual hit while keeping the edit structurally identical.

## 6. HIA Shorts end card

Youtube-1 uses an exact owner-provided vertical end-card.

HIA currently has **no owner-locked 9:16 Shorts end-card asset** in the repository.

Therefore:
- do not invent one;
- do not redraw the 16:9 long-form end screen;
- do not adapt/recreate a CTA card;
- review proofs end on the source content.
A final HIA Shorts end-card may be appended only after the owner explicitly approves an exact HIA asset.

## 7. Production order

1. Lock the long-form master.
2. Lock Short source IN/OUT on clean spoken boundaries.
3. Render **one SH01 proof** using the Youtube-1 portrait wrapper.
4. Owner reviews the proof.
5. If the format is accepted, scale the exact same wrapper to all remaining Shorts.
6. Run technical + visual QC.
7. Package individual MP4s + ZIP + QC + SHA256.
8. Add an exact HIA Shorts end-card only after a separate owner lock.

## 8. Current source ranges

### Chicago
- CHI-S01: 11.800 → 46.680 (34.880 s)
- CHI-S02: 153.680 → 195.660 (41.980 s)
- CHI-S03: 47.360 → 73.780 (26.420 s)
- CHI-S04: 911.000 → 955.380 (44.380 s)
- CHI-S05: 988.940 → 1036.060 (47.120 s)

### TC-497
- TC497-S01: 0.000 → 53.880 (53.880 s)
- TC497-S02: 265.000 → 315.800 (50.800 s)
- TC497-S03: 494.740 → 532.760 (38.020 s)
- TC497-S04: 663.080 → 708.660 (45.580 s)
- TC497-S05: 1018.600 → 1072.460 (53.860 s)

These ranges are inherited from the existing extraction maps. Old per-beat Shorts montage/rebuild instructions are superseded by this direct-cut rule.

## 9. QC gate

Technical:
- full decode PASS;
- correct 1080×1920;
- correct source-native FPS;
- H.264 High / yuv420p;
- AAC present;
- no black-frame event introduced;
- no PTS discontinuity;
- no audio stretch or duplicate audio.

Visual:
- foreground is one continuous direct-cut master;
- background is the same synchronized source frame;
- no double-screen layout;
- no empty portrait dead zone;
- no Shorts-only GFX;
- no duplicate captions;
- source captions remain readable;
- no horizontal drift;
- no generated replacement imagery.

Editorial:
- exact source boundaries;
- clean spoken start/end;
- no new narration;
- no new claims;
- no scene reconstruction.

## 10. Change control

Do not redesign this format silently.

Any future alternative requires:
- explicit owner request;
- one proof;
- owner approval;
- only then a channel-wide canon update.
