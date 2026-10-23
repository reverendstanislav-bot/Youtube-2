# VIDEO 006 — PROJECT HISTORY

## 2026-10-21
- Began VIDEO 006 under the existing HIA GitHub repo after owner instruction.
- Selected working Project Pluto topic from prior project discussion; no final title/thumbnail was approved.
- Verified primary and institutional sources (AEC 1964 via NASA; LLNL; OSTI; Library of Congress).
- Logged critical distinctions: ground-tested ramjet versus unflown missile; power versus thrust; cancellation evidence versus interpretation.
- Prepared Stage 01 research, fact/source/visual ledgers; Stage 02 editorial draft.
- No media downloaded, no assets generated, no credits spent.

## 2026-10-22 — Stage 03 Narration Script V1 physically completed
- Created entire 8-chapter American English 2,887-word Project Pluto narration draft. Files at `SCRIPT/STAGE03_PROJECT_PLUTO_FULL_NARRATION_V1_EN.md` and `SCRIPT/STAGE03_PROJECT_PLUTO_VOICE_TEXT_V1_EN.txt`; 33 ordered semantic beats in `SCRIPT/STAGE03_PROJECT_PLUTO_SEMANTIC_BEATS_V1.csv`.
- Evidence and initial script fact QC documented in `SCRIPT/STAGE03_SCRIPT_EDITORIAL_AND_FACT_QC_V1.md`. AEC 1964 report paragraph cross-checked against original PDF; no flights/total cost/missile completion invented.
- **Stage 03 V1 draft done; Stage 04 independent fact/legal and owner Script Lock HOLD; no TTS or precise audio/video sync yet.**

## 2026-10-22 — Stage 04 independent fact/QC revision V2
- Reviewed 54 substantial narrative claims with original AEC 1964 printed p63, period UCRL project reports, LLNL history, LOC HAER Area26 site report, contemporary 1964 Congress/NASA budget chronology and independent accounts. See `SCRIPT/STAGE04_CLAIM_BY_CLAIM_EVIDENCE_LEDGER_V1.csv` and `SCRIPT/STAGE04_FINAL_FACT_EDITORIAL_LEGAL_QC_2026-10-22.md`.
- Corrected generalized Tory II-A 1-minute-air constraint to contemporary several-minute limit; preserved separately 45sec May14 1961 first test. Retained official May20 for full Tory II-C test in light of May22 Air Force magazine conflicting period press. Made June11 funding clash and lack of weapons requirement explicit in Chapter7; clarified reactor 500MW as approximate heat, not thrust; added real remote-controlled reactor-test railroad.
- Authoritative narratable V2 `SCRIPT/STAGE04_PROJECT_PLUTO_FULL_NARRATION_V2_EN.md`, voice text `SCRIPT/STAGE04_PROJECT_PLUTO_VOICE_TEXT_V2_EN.txt` (2955 words, 19.1–21.9min), 30 beats `SCRIPT/STAGE04_PROJECT_PLUTO_EVIDENCE_ALIGNED_BEATS_V2.csv`. Stage04 script FACT PASS with qualifications, **producer Script Lock and permission to run TTS still OPEN**. R1 footage REJECT preserved.
## 2026-10-23 ? Stage 04 V2 voice-production preparation
- Accepted Stage04 V2 as the only current input for production preparation; Stage03 V1 explicitly superseded for voice use.
- Verified exact reconstruction of the clean voice text from 8 chapter bodies: 2,955 words, 19,064 normalized characters, 54 claim rows and 30 evidence-aligned beats.
- Prepared 8 chapter-boundary Voicebox jobs totaling 19,050 job-body characters, with SHA256 manifests, held request templates and a 48 kHz mono PCM WAV assembly plan in `AUDIO/VOICEBOX_ARTHUR_V2_PREP/`.
- Local Voicebox external credit estimate is USD 0.00. **Owner Script Lock remains open; no voice generation submitted and no credits spent.** No Youtube-3 audio used; R1 source bank remains rejected.

## 2026-10-23 — Stage 05 V2 Voicebox generation completed
- Owner directly instructed generation of the prepared Stage04 V2 jobs, lifting the generation hold for this exact package.
- Voicebox profile `HIA Arthur Multi-Source` generated 8/8 chapter WAVs from the 2,955-word V2 narration; Youtube-3 audio was not used and external cost was USD 0.00.
- All chapter WAVs passed complete FFmpeg decode and SHA256 verification. The 48kHz mono PCM 24-bit assembly master is 00:18:41.600, 161,510,502 bytes, SHA256 `78213c4b5fa68605ae5d50a102de21d49bd419cf28aad77b8ff777e02bb12b19`.
- Technical records are in `AUDIO/VOICEBOX_ARTHUR_V2_GENERATION/`. **Human auditory QC remains HOLD before audio lock and exact picture sync.**
- Master, eight-job ZIP and QC records were published and server-digest verified at https://github.com/reverendstanislav-bot/Youtube-2/releases/tag/project-pluto-video006-stage05-voicebox-v2-20261023 .

## 2026-10-23 — Owner audio approval and Stage 05 timing lock
- Owner explicitly approved the complete 18:41.600 narration master, establishing AUDIO LOCK on SHA256 `78213c4b5fa68605ae5d50a102de21d49bd419cf28aad77b8ff777e02bb12b19`.
- Faster-Whisper base aligned the eight original chapter WAVs to the authoritative Stage04 V2 text: 3,023 normalized expected tokens, weighted sequence ratio 0.964414. ASR is timing evidence only and does not alter script wording.
- All 30 evidence-aligned beats received spoken-word bounds plus contiguous 25fps editorial boundaries. Frames 0–28,039 are covered with frame 28,040 exclusive and no gaps or overlaps.
- Lock manifest, raw ASR evidence, per-word alignment, chapter timing, 30-beat timeline and QC are in `AUDIO/AUDIO_LOCK_V2/`.
- Next gate: source-to-beat visual assignment and a representative DaVinci sequence. Producer-rejected Source Bank R1 remains rejected.
