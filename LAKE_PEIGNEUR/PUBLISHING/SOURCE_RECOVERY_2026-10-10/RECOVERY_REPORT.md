# HIA Lake Peigneur full source recovery — 2026-10-10

Verdict: **PARTIAL SOURCE RECOVERY — MISSING FILES**.
The original V13 film's editable source and all actual picture/audio dependencies are recovered. The previously prepared corrected EP01 end-screen binary is unavailable, so the expanded relaunch handoff is not called complete. No missing picture asset in the original final timeline.

## A. EDIT PROJECT
YES — self-contained Remotion project: `01_EDIT_PROJECT/project_files/Youtube-2/LAKE_PEIGNEUR/REMOTION_V1/`.
Original local checkout: `C:/Users/KK/Desktop/Youtube/Youtube-2/LAKE_PEIGNEUR/REMOTION_V1`.
Local commit `e8c06a86da4fc383a20e66f9b27ab086cef48715`; original final-render commit `b6c771f1174825628b0315a90b71e59ae27e0319`.
Remote main evidence snapshot `c50e51d3aef113c362372186e5787e542819b5c4`. Local branch was preserved; no reset/merge/pull was performed.
Exact final timeline: 87 beats, 97 slots/97 asset IDs; all 97 source JPGs and corresponding locked original PNGs are included. Caption component is separable from Chapter/Fact. Keyframes: none active in final V13. Source project and final master are bound by the finalization commit/report and exact master SHA256; sampled source/master contact sheet is included.

## B. VISUAL ASSETS
Required by actual final timeline: **97 IDs / 95 unique images**. Found: **97/97 used +3 unused locked alternatives**. Entire lock: **100 IDs /98 unique PNG hashes**.
Fresh read-only provider verification and recovery: **98/98 distinct completed jobs downloaded**, mapped to **100/100 lock rows**; every original matches locked SHA256, decodes and matches recorded dimensions. Most source images are 1344x752; exact per-file values are in ASSET_MANIFEST.csv. Original JPG proxies are retained separately as actually used, without promoting them to originals.
Missing final timeline sources: **0**. Historical director QC is 85 PASS/15 CONDITIONAL over the full 100-row lock; current technical PASS does not erase those editorial conditions. No new semantic/rights blanket PASS is asserted.
Remote 144 prompt rows are not a final edit manifest. The separate 26 TEST30 PNG originals were recovered and verified again, isolated in TEST_ONLY_NOT_FINAL_26_ORIGINALS.zip. Hash comparison establishes that 13/26 test images are byte-identical to images used under different final-lock IDs; those 13 now have confirmed final use through the hash-alias table. The remaining13 have UNKNOWN final use. No test ID is automatically promoted and no timeline substitution was made.

## C. AUDIO
Original approved MP3 master and all four original provider MP3 chunks recovered; all chunk SHA256 values match the canonical TTS manifest and all files fully decode.
Master: 15,495,879 bytes; MP3 128 kb/s, 44,100Hz, mono; ffprobe 968.427755s.
SHA256 `1ae5c97d85b9cf2c10c438a2834d024776ea851a932a02aab2490860fa4afd13`.
No original uncompressed WAV found. Historical PCM was a decode derivative. Renderer narration begins at frame0; story ends at frame24211 (~968.44s), followed by 20s end-screen hold. Sampled waveform alignment (lag of original relative to final, then corrected correlation): 0s: -0.042688s / 0.997044, 120s: -0.042688s / 0.991694, 400s: -0.042688s / 0.997309, 800s: -0.042688s / 0.996116, 950s: -0.042688s / 0.990409. Encoded-audio delay must be retained/checked in a new edit; see detailed metadata/alignment in 03_AUDIO/audio_timing.

## D. EXISTING MASTERS
One exact V13 master recovered: 174,986,220 bytes, H.264 1920x1080/25fps/24711frames, 988.458667s. Video bitrate approx1.093Mb/s; total bitrate1.416Mb/s. Full decode: exit0, empty error log.
SHA256 `3436c9d7b9fd27caa97c6fc2c95aa2322e5bec1d8a69a8575722d52bd81e5b3d`.
It contains baked captions and the old PREVIOUS STORY end screen, and is explicitly REJECTED FOR RELAUNCH. No higher-bitrate or clean picture master found locally, in Lake Releases, or relevant Actions artifact metadata. Existing Actions Lake artifacts are archival source collections, not final edit masters. A new clean render is possible from supplied sources but was not requested at this stage.

## E. RIGHTS
Actual final references: generated originals with job/hash provenance. Appendix EE photo files used: **0** in recovered final mapping. Historical source/rights/claim audits included. Commercial provider terms and historical CONDITIONAL visual notes still require editorial review; this is source recovery, not a new publication clearance.
No protected font binaries, credentials, cookies or API tokens included. Source text/code scan found no credential-pattern matches. node_modules/cache and unrelated projects excluded.

## F. EXPORT AND DOWNLOAD
Technical release: `hia-lake-peigneur-source-recovery-20261010`, repository `reverendstanislav-bot/Youtube-2`.
Independent ZIP parts, each <=500,000,000 bytes. CRC/member counts and SHA256 in HIA_LAKE_SOURCE_INDEX.json. Download verification is recorded separately after upload; no successful transfer is claimed before verification. Extract all parts together; no binary concatenation required.

## G. MISSING / EMPTY LOCATIONS
See MISSING_ASSETS.csv: original uncompressed VO WAV, higher-bitrate previous master, clean master, corrected EP01 subscribe-only end-screen binary, native layered end-screen artwork.
02_FINAL_VISUALS/DOCUMENT and MAP are empty because the final V13 project uses generated GFX/REC rather than those separate categories. 06_EXISTING_MASTERS/clean_picture_master_if_exists is empty because none was found.
Searches covered the original Youtube-2 checkout/ignored assets, Desktop/Downloads, C:/YOUTUBE, C:/tmp, C:/YouTubeEditorAgent, D:/Downloads, D:/Temp, available drive roots, current Higgsfield sandbox and accessible projects, provider jobs, Git main/history, Releases and Actions artifacts. Protected OS/unrelated application trees were not exhaustively scanned. Corrected EP01 export described in remote handoff is absent from accessible sandbox; do not claim it recovered.
No new generations or TTS, no source overwrites/deletions, no production rebuild, and no heavy-media Git commit.

## Historical 144-row inventory clarification
26/144 prompt identities have verified historical TEST30 originals; 118 have no verified original tied to that historical identity and are individually marked MISSING in PROMPT144_RECOVERY_STATUS.csv and MISSING_ASSETS.csv. This does not mean 118 images are missing from the final film: the actual V13 sources are 97/97 complete. ID-only joins across changed plans would give false results. The ASSET_MANIFEST has 100 final-lock rows plus26 explicitly namespaced historical rows; 13 historical rows are byte-identical aliases of used final assets.
All100 original edit JPG proxies decode; their own hashes/dimensions are in EDIT_PROXY_VERIFICATION.csv. Visually compared four exact final-master frames with the corresponding source assets: scene content matches, with the expected caption overlay in the master. This is a source-identity spot check, not full semantic QC.
Audio comparison shows a stable approximately42.69ms encoding offset across all five sampled windows; after compensating that offset waveform correlations are0.9904–0.9973, confirming the recovered original VO. Do not silently shift source timing when reproducing the old encoded master.
