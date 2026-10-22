# PROJECT PLUTO / VIDEO006 — public source bank R1 QC

Date: 2026-10-22  
Repository: `reverendstanislav-bot/Youtube-2`  
Scope: `PROJECT_PLUTO`, VIDEO006 only

## Delivery result

- 33 usable silent MP4 clips, 656.375 seconds total (10:56.375), 79,850,173 bytes.
- 29 direct 1963 Project Pluto / SLAM R&D clips, 628.375 seconds.
- 4 clearly separated other-program context clips, 28.000 seconds: one B-52/Hound Dog comparison and three Minuteman comparisons.
- All clips are 5–30 seconds, unique by SHA256, and retain native source dimensions/FPS.
- The bank contains no generated video, no paid material, no dialogue subtitles, no audio tracks and no artificial 1080p upscale.

This is a verified source bank for editorial use. It is not a finished film or a locked timeline.

## Existing material and R5 status

- The expected R5 ZIP was not present locally and is not published as a GitHub Release. Its recorded expected SHA256 remains `897cddf56a8299f7ca995cf5a94cca19d965bcc0cdca764e70ddf81272572b66`.
- An existing local R3 ZIP was found and verified without re-downloading: `HIA_VIDEO006_PLUTO_R3_EDITORIAL_QC_SOURCE_BANK.zip`, 120,954,345 bytes, SHA256 `8ef7c1c582ac8afa38b17bdc42af519e752a7f77dbebb5bc03b8e3bf2982e8ad`.
- Because R5 was unavailable, the original USAF 38912 source was recovered and SHA256-verified, then a new narrow R1 selection was made. These files are not claimed to be byte-identical to R5.

## Download and provenance gate

The authoritative queue and `codex_fetch_public_queue.py` were used. Already verified materials were not downloaded again.

| Asset | Result | Bytes | SHA256 |
|---|---:|---:|---|
| Original USAF 38912 LASV-N1 (1963) | PASS | 100,689,792 | `3d9305615472a3ac7a18c50b1d7a3649d20d34f1e1aab93439f535650191114e` |
| Primary Pluto editor bank | PASS | 58,440,612 | `ec9f4a27008a8a1384c3c96ad836e35e712b0dbffb42aeccc9a81b5b26f4b889` |
| DOC-01 July 1964 report | PASS | 13,180,638 | `a267f6db8128518520d1ff86ad6b026613b3ba1414debac9740ad077539c0921` |

The full F013/F015 sources were not fetched because the precise requested context scenes already existed in the verified 58 MB editor bank. DOC-02 and X-15 were also skipped because the required engineering figures and direct Pluto footage already cover the provisional beats.

## Script, narration and timing gate

- Repository truth remains Stage 02: an eight-chapter working outline, not an owner-locked Stage 03 script.
- The local file `VIDEO006_HARRISON_STAGE10_AUDIO_MASTER_48K_MONO.wav` was found and technically inspected: PCM s16le, mono, 48 kHz, 653.130 seconds, 62,700,558 bytes, SHA256 `a42c0e6245d66f4da25b5528bec04047b9e7f7ebf759e412e6490d627cf8d308`.
- Speech transcription showed that this WAV is about the Dragon Train / Light & Wonder legal dispute, not Project Pluto. It is rejected for VIDEO006.
- No voice timestamps were invented. Every scene and chapter remains `AUDIO_TIMING_HOLD_WRONG_PROJECT_AUDIO` until the locked Pluto script, final narration WAV and transcript are available.

## Editorial and visual review

- Every final clip was reviewed through multi-point visual progression frames; ambiguous, stable and context clips received denser 1 fps sequence review.
- The Minuteman motor clip was tightened from source 275–283 to 276–283 to remove the unrelated opening presenter frame.
- LASV-N1 clips were shortened or shifted where visual review found static openings, repeated material or a black tail.
- All final source ranges are non-overlapping within LASV-N1. No clip is included to pad runtime.
- Other-program footage is labeled `REAL_DIFFERENT_PROGRAM_CONTEXT` in both the manifest and chapter map. It must only appear under an explicit comparison beat and must never be presented as a Tory test.

Visual review is an editorial sampling gate, not a claim that a human watched all 656.375 seconds at normal playback speed.

## Technical QC

- 33/33 `ffprobe` structure checks: PASS.
- 33/33 complete video decodes with `ffmpeg -v error -xerror`: PASS.
- 33/33 black-frame scans after final trims: PASS, no black segment of 0.20 seconds or longer.
- 33/33 audio-stream checks: PASS, no audio streams.
- 33/33 subtitle-stream checks: PASS, no subtitle streams.
- 33/33 duration checks: PASS, each clip is between 5 and 30 seconds.
- 33/33 SHA256 values are unique.
- Direct LASV-N1 clips: H.264, 1280x720, 24 fps.
- Context clips preserve their verified 678x442, 30 fps source format.

## Historical limits and holds

- Confirmed moving footage of the May 1964 Tory II-C operating hot test: **0 seconds**.
- Chapters 1 and 6 must use the authentic Tory II-C still and official report data; no other nuclear program may substitute for the missing test footage.
- A tested Tory reactor/ramjet is not footage of an operational or flown SLAM missile.
- Later HAER/site photographs are retrospective and must be labeled as such.
- All LASV-N1, context, photo and document publication rights remain item-level HOLD pending final rights review. No zero-risk or publication clearance is claimed.
- Final film, final timeline, voice synchronization and publication approval remain HOLD.

## Final gate

`SOURCE_BANK_TECHNICAL_PASS`  
`SOURCE_BANK_PROVISIONAL_EDITORIAL_PASS`  
`AUDIO_TIMING_HOLD_WRONG_PROJECT_AUDIO`  
`STAGE03_SCRIPT_HOLD`  
`TORY_IIC_1964_OPERATING_FILM_HOLD_0_SECONDS`  
`PUBLICATION_RIGHTS_HOLD`  
`FINAL_FILM_HOLD`
