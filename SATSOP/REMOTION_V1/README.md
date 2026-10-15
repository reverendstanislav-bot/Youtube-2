# SATSOP Remotion — clean no-dialogue-subtitles owner variant

**Current active source:** `src/index.jsx` (subtitle component physically removed; no SRT/VTT imports).

**Authority:** `CHANNEL/NO_SUBTITLES_OWNER_LOCK_2026-10-10.md`.

## Unchanged

- 109 visual beats; **30 FPS** canonical Satsop timeline and original 19:23.920 narration (+20s existing HIA endscreen).
- Existing HIA editorial overlays, provenance, cards, motion transformations and end-screen unchanged.
- Exact local `public/SATSOP_VO_MASTER_V1.wav` required; its locked SHA-256 is `5e9afb2310f812cf39aff3f37a8d4500bbca2988ae57ba1633244ed65d9d070c`.
- Asset sources are the existing locked `public/assets/SAT-B*.png/jpg`; **do not fabricate missing files or substitute artwork**.

## Before any clean MP4 export

From `SATSOP/REMOTION_V1`:

```bash
python3 ../DEVELOPMENT/preflight_satsop_clean.py --project .
npm ci
npx remotion render src/index.jsx SatsopV1 out/SATSOP_D3_CLEAN_NO_SUBTITLES_MASTER_1080P30.mp4 --codec=h264 --crf=15 --pixel-format=yuv420p --concurrency=3
python3 ../DEVELOPMENT/preflight_satsop_clean.py --project . --video out/SATSOP_D3_CLEAN_NO_SUBTITLES_MASTER_1080P30.mp4
```

**Hard blocker verified 2026-10-15:** The repo only stores Remotion JS/timeline and selected end-screen/edit assets. The 109 source stills and canonical 103 MB WAV are locally ignored media. Do not run a GitHub Actions render unless these original bytes have first been recovered and SHA/beat inventory verified. An old `SATSOP_FINAL_UPLOAD_MASTER.mp4` is captioned and **not valid for upload**. Do not crop, blur, black-strip or inpaint subtitles from that MP4.

**Release gate:** Provide new actual MP4 link, SHA, full decode/QC and representative stills. No upload approval or public release yet; owner must review actual clean movie.

Previous rough-cut notes describing white/orange captions are superseded by this file and the owner lock.
