# HIA Chicago V2 — QC report

Delivery: 00:21:30.720; 1920×1080; 25 fps; 32,268 frames; H.264 yuv420p / AAC 48 kHz.

Technical QC: PASS. Full decode; no detected black intervals; subtitle sequence valid; audio bitstream SHA-256 identical to V1. Loudness -14.05 LUFS, true peak -4.48 dBTP.

Motion QC: PASS in three isolated 1080p tests and three samples of the finished video. The old stop/2-pixel-step pattern is absent in measured samples. Subpixel perspective interpolation replaces zoompan; motion is selected by content. Static holds are intentional.

Editorial changes: 217 shots; same-source holds merged; deliberate source-detail views replace small arbitrary crop jumps; the 00:41.320 three-frame flash removed. Larger archival framing; source-map overview plus real enlarged detail; six explanatory sequences (gauge, transfer, basement connection, coal/ash, water, surviving equipment). Repeated full-screen title cards replaced with short titles over relevant material. End screen retains a story image.

Labels: no persistent black RECONSTRUCTION box. Clear sequence-entry label followed by small unboxed attribution. Archive labels are fixed after image transformation.

Subtitles: 338 English sidecar cues; maximum 42 characters per line / two lines. Orphan tails regrouped, no >20 cps cues in the final reflow. One sub-second emphasis remains: "Coal in.". Source wording preserved. Seven short fresh checks of the actual mixed audio support key cue onsets; the ambiguous zero-duration ASR token near 08:37 was resolved by grouping the whole phrase. No full re-transcription.

Visual review: sampled finished frames and short insert renders inspected. Limit: browser/player control was unavailable, so no claim of a continuous 1× watch or subjective listening of the entire film. Frame-by-frame measurements support the motion result; aesthetic quality remains a viewer judgment.

Cost control: no paid generation, no network, no new voice, no audio re-encode. Three motion tests (24 s), short insert tests, one complete 720p proxy and one final video render. V1 files and state remain unchanged.

Motion diagnostic detail: the initial center-crop brightness-difference gate failed because of periodic H.264 compression changes. This initial result is retained in the QC JSON. Matching uncompressed slow push/pull samples showed zero held frames and tightly bounded differences (push 0.0712-0.0798; pull 0.1948-0.2105). Off-center samples of the final encoded file showed maximum consecutive near-static runs of 1/1/0 frames for push/pull/pan, versus the old 10-12-frame holds. This supports the measured correction; it is not a claim of uninterrupted real-time viewing.

Final timestamps: 32,268 distinct presentation timestamps; every interval is 0.040 seconds. The delivered SRT was parsed independently: 338 cues, unchanged source words, no overlap, maximum 42 characters per line, maximum 19.92 characters/second. V1 size and modification timestamps were verified unchanged.

Evidence is retained in ../qc/: final_qc.json, final_offcenter_motion.json, uncompressed_motion_diagnosis.json, final_pts_validation.json, delivered_srt_validation.json, final_review.jpg. Small diagnostic tests reused final-render clips where possible; no additional full proxy or full final render was required.
