# Satsop Motion Review V3 — Extensive QC

Date: 2026-09-27

File: `out/SATSOP_MOTION_REVIEW_V3_HIA_END.mp4`

Overall status: **FAIL — NOT READY FOR PICTURE LOCK OR DELIVERY**

The picture content and corrected HIA end-screen layout pass. The candidate fails on burned-caption accuracy and one non-CFR timestamp at the transition into the end screen.

## Container and decode

- MP4 probe score: 100
- Size: 926,935,818 bytes
- SHA-256: `5e142ec16cd8d5590ba4caf8960a498d9915012117279fb15cdc6f36dcb497c6`
- Duration: 1,183.989333 seconds
- Video: H.264 High, 1920x1080, progressive, 8-bit 4:2:0, 35,518 frames
- Audio: AAC LC, 48 kHz stereo
- Full decode: **PASS**
- Video/audio end-time difference: 0.000010 seconds — **PASS**

## Picture integrity

- V2 content frames compared with the first 34,918 decoded V3 frames: **34,918 / 34,918 identical; 0 pixel-hash differences**
- Timeline beats: 109
- Missing assets: 0
- Undersized or unreadable assets: 0
- Exact duplicate asset groups: 0
- Beat range errors: 0
- Beat frame gaps: 0
- Black intervals of 0.20 seconds or longer: 0
- Global visual contact-sheet review: **PASS**
- HIA end-screen layout: **PASS** — one previous-story rectangle, one subscribe circle, no overlap

## Freeze analysis

Fourteen freeze starts were detected with a two-second threshold. Twelve occur inside deliberately static `hold` or the initial hold portion of `hold_then_push` beats. Two occur during the intentionally static HIA end screen. No unexplained encode stall was found.

Status: **PASS / intentional motion design**

## Audio

- Music: none
- Integrated loudness: -14.7 LUFS
- Loudness range: 3.0 LU
- True peak: -3.3 dBFS
- Clipping: none
- Four program pauses longer than one second: 06:20.372, 07:30.415, 10:44.808, 11:29.860; each is 1.01–1.14 seconds
- End-screen silence: 20.048 seconds

Status: **PASS**

## Frame cadence and outro seam

- Expected frame duration: 0.033333 seconds
- Normal packets: 35,517
- Anomalous packets: 1
- Anomaly at the V2-to-outro seam: a packet duration and PTS step of 0.089323 seconds
- Result: the last program frame is held approximately 0.055990 seconds longer than the 30 fps cadence before the HIA end screen begins

Status: **FAIL**

The final assembly must be rebuilt with continuous 30 fps timestamps. Every video frame must have a 0.033333-second duration.

## Burned-caption structure

- Caption cues: 464
- Word-timing errors: 0
- Cue overlaps: 0
- Gaps longer than 1.5 seconds: 0
- Maximum caption gap: 1.18 seconds
- Zero-duration cues: 1

At 04:14.400, `1983,` has identical start and end times. In the encoded file it appears as an approximately 80–100 ms flash between otherwise blank caption intervals.

Status: **FAIL**

## Burned-caption accuracy

The 2,304 burned-caption tokens were compared with the canonical TTS text. There are 59 non-equal alignment blocks. Many are harmless number-style changes, but the following require correction:

- 00:41.700 — `Satsup` → `Satsop`
- 01:07.640 — `Satsup` → `Satsop`
- 02:02.480 — `rewined 16 years` → `rewind sixteen years`
- 03:33.340 — `It's meaning` → `Its meaning`
- 04:14.400 — zero-duration `1983,` cue
- 04:23.970 — `Satsap` → `Satsop`
- 05:10.500 — `For investor-owned utilities` → `Four investor-owned utilities`
- 05:44.011 — `Satsap` → `Satsop`
- 06:16.051 — `Satsap` → `Satsop`
- 08:44.071 — `supply systems executive board` → `Supply System's executive board`
- 11:23.071 — `combined cycle plants costs` → `combined-cycle plant's costs`
- 12:14.228 — `.55 billion` → `$1.55 billion`
- 14:18.788 — `sighting permits` → `siting permits`
- 15:48.468 — `Bonnes defaulted` → `bonds defaulted`
- 17:05.928 — `Graze Harbour` → `Grays Harbor` (two occurrences across the wrapped cue)
- 19:01.331 — `Satsap` → `Satsop`

Status: **FAIL**

## Narration/script language issue

At approximately 04:19, the locked narration says: `That is the famous the Supply System financial collapse.` This is present in the canonical TTS script and is not only a caption error. The correct English construction needs a script decision and a replacement VO phrase.

The alignment transcript also repeatedly recognizes the spoken name as `Satsup` or `Satsap` and recognizes `Grays Harbor` as `Graze Harbour`. This strongly suggests pronunciation problems in the locked VO. These names require an aural human check before the narration can remain locked.

Status: **FAIL / VO REVIEW REQUIRED**

## Required repair order

1. Correct the canonical English sentence and record a replacement VO phrase around 04:19.
2. Aurally verify every spoken `Satsop` and `Grays Harbor`; replace mispronounced takes where necessary.
3. Rebuild captions from the corrected canonical text while retaining the verified word timings.
4. Give `1983,` a real display interval and remove the flash.
5. Rebuild the HIA seam with continuous 30 fps timestamps.
6. Rerun full decode, packet cadence, subtitle comparison, black/freeze, loudness, silence and visual contact-sheet QC.

The candidate must not be renamed or copied as a final upload master until all FAIL items are closed.
