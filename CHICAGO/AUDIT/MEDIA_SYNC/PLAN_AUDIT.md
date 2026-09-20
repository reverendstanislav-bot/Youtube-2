# Chicago — plan audit after source recovery

## 1. Source recovery / archive integrity

- Canonical RAR: **PASS** (verified before this run; RAR5 integrity test also PASS).

## 2. Media integrity

- V1 final: 1920x1080, fps 25/1, duration 1290.720s, h264 + aac.
- V2 final: 1920x1080, fps 25/1, duration 1290.720s, h264 + aac.
- Full decode: see DECODE_STATUS.txt.

## 3. Independent subtitle ↔ VO timing

- **subtitles_en.srt** — FAIL: progressive drift ~9.60s across runtime; variable offset spread 14.72s; median -0.360s; P05/P95 -9.726/4.996s; runtime change 9.597s.
- **HIA_CHICAGO_FINAL_UPLOAD.srt** — PASS; median 0.000s; P05/P95 0.000/0.000s; runtime change 0.006s.
- **HIA_CHICAGO_V2.srt** — PASS; median 0.000s; P05/P95 0.000/0.000s; runtime change 0.005s.

## 4. V1/V2 audio identity

a1e84ecb33a2060075b5681a086bf59b166396e16564b8e705a5b201dc4928ed  /tmp/v1_audio.aac
a1e84ecb33a2060075b5681a086bf59b166396e16564b8e705a5b201dc4928ed  /tmp/v2_audio.aac
V1_V2_AUDIO_BIT_IDENTICAL=YES

## 5. Repair rule

Do not trust old PASS labels by themselves. The independent word-timing audit is the authority for subtitle timing. Preserve picture/audio only after identifying which visual version the user wants as the base; rebuild captions from the best-aligned timing source and verify opening/middle/end against VO before promotion.
