# VIDEO 009 — Stage 09–10 Codex Execution Contract
Date: 2026-10-28
STATUS: READY FOR LOCAL EXECUTION — NOT GENERATED / NOT AUDIO-QC PASS
Source of truth: current origin/main.
Source script: VIDEO_009_PROJECT_NIKE/08_VOICE_SCRIPT_CLEAN_EN_V3.txt
Locked script: VIDEO_009_PROJECT_NIKE/07_SCRIPT_LOCK_EN_V3.md
RU review: VIDEO_009_PROJECT_NIKE/07_SCRIPT_RU_REVIEW_V3.md
Read applicable HIA CHANNEL voice and delivery canon before selecting a TTS model/voice. DO NOT use WHAT IT COST Harrison voice by default.
Constraints: paid generation requires explicit owner approval; never submit paid Higgsfield jobs by default. No generated video.

## Codex instructions
1. git fetch origin main && git checkout main && git pull --ff-only; record SHA. Confirm source script equals locked English spoken paragraphs (46 blocks); no headings or nonspoken editor instructions in clean script.
2. Identify the exact existing approved HIA narrator voice from canonical channel config, prior episode master, voice sample or voice profile. Do not guess or introduce another voice. If none can be proven, return VOICE HOLD with the evidence investigated. No commercial generation or paid credits without explicit owner approval.
3. If the approved HIA voice is locally reproducible without paid spend, produce WAV for the 46 paragraphs or chapter-sized clips (avoid mid-sentence joins), 48kHz 24-bit PCM, mono or stereo according to HIA delivery spec; preserve pronunciation and consistent loudness, head/tail padding. No rewritten source text.
4. Build a concatenated master WAV, retaining join QC (clicks, pauses, relative levels, plosives, speaking pace, breathing, artifacts). Verify via ffprobe (duration, sample rate, bit depth, peaks and channel layout). Record SHA256 for master and each clip. Do not claim listening QC without actually listening to complete audio.
5. Run ASR against the rendered master (Whisper or other available installed ASR); compare against clean EN V3. Check all 46 paragraphs for omissions, duplicate sentences, mispronunciations (Nike Ajax, Nike Hercules, SF-88, Fort Meade, Integrated Fire Control, ARADCOM), unwanted markup or hallucinations. Document word-level differences and fixes.
6. Correct any errors, rerender affected blocks, regenerate master, repeat ASR and audio listening. Output SRT/VTT as optional deliverables with natural-size subtitles; separate tracks never inherit in-video branded caption styling.
7. Store large WAV/ASR artifacts via approved artifact delivery path (Release or Actions artifact, not raw Git tree). Record accessible URLs and SHA256. Git may contain only stage reports, manifests and small scripts. Do not invent file links/hashes.
8. Update Stage 09 report and Stage 10 QC ledger. PASS only after actual files exist, verified ffprobe and full listen; otherwise explicit HOLD cause. Log branch head and commit.

## Acceptance
- Approved narrator matches HIA canon; no unapproved costs.
- Exactly 46 complete spoken blocks, same order, no omissions.
- Measured duration (not script outline time).
- Measured LUFS and true peak according to HIA master canon (do not invent targets).
- All join transitions and entire audio heard in full.
- ASR accuracy QC with a log of fixes.
- Actual downloadable audio or artifact location plus SHA.
- Owner can review before visual lock; footage rights a separate hold.

## Current evidence
RU V3 present and aligned by ID to 46 EN V3 blocks.
The ChatGPT execution environment has ffmpeg but NO installed Qwen TTS/Voicebox or Whisper/faster-whisper runtime. No approved HIA voice has yet been verified from the linked repo in this session. No WAV has been produced. Stage 09–10 HOLD.
