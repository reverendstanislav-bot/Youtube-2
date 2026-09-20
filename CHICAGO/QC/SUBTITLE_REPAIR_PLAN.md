# Chicago subtitle repair plan

## Root cause confirmed

The canonical source archive has now been independently audited.

**Bad timing source — never use again:**
- `03_TIMELINE/subtitles_en.srt`
- 293 cues
- independent whole-film word alignment shows large variable/progressive errors;
- modeled runtime drift ~9.6 s;
- P05/P95 start-offset range approximately -9.726 s to +4.996 s.

**Good timing sources:**
- `_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt` — 320 cues; independent timing alignment PASS.
- `_V2/final/HIA_CHICAGO_V2.srt` — 338 cues; independent timing alignment PASS.
- `_QC/voice_words.json` — word-level narration timing authority used for independent verification.

## Media facts

- V1 final: 1920x1080, 25 fps, 1290.720 s; full decode PASS.
- V2 final: 1920x1080, 25 fps, 1290.720 s; full decode PASS.
- V1/V2 AAC is bit-identical, SHA-256:
  `a1e84ecb33a2060075b5681a086bf59b166396e16564b8e705a5b201dc4928ed`.

## Next repair

1. Use V2 as the preferred technical picture candidate because it is the later revision and preserves V1 audio bit-for-bit.
2. Do **not** use `03_TIMELINE/subtitles_en.srt`.
3. Build the visible subtitle layer from `_V2/final/HIA_CHICAGO_V2.srt` / word-level timing.
4. Do not stack captions on top of an existing visible/burned layer. Confirm the picture base is clean before burn-in.
5. Preserve V2 picture and the exact existing AAC unless a concrete picture defect is found.
6. Render a review build first.
7. Inspect visible caption onset at opening, quarter, middle, three-quarter and ending, plus several transitions around 08:37.
8. User approval is mandatory before a new upload master is promoted.

## Evidence

- `CHICAGO/AUDIT/MEDIA_SYNC/PLAN_AUDIT.md`
- `CHICAGO/AUDIT/MEDIA_SYNC/SUBTITLE_ALIGNMENT.md`
- `CHICAGO/AUDIT/MEDIA_SYNC/SUBTITLE_ALIGNMENT.json`
- `CHICAGO/AUDIT/MEDIA_SYNC/DECODE_STATUS.txt`
- `CHICAGO/AUDIT/MEDIA_SYNC/AUDIO_SHA256.txt`
- `CHICAGO/AUDIT/SELECTED_SOURCE/`
