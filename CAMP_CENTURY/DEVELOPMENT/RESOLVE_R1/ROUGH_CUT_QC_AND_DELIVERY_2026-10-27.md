# Camp Century VIDEO007: visual R1 review record

Status: complete native rough picture and full proxy exist. Technical QC PASS. Creative/final-release approval HOLD.

## Actual output

- Native project `YT2 Vid7`, timeline `HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_25FPS`; saved and exported after rendering.
- Timeline: 1920 x 1080, 25 fps, 27,368 frames, 18:14.720. 132 picture shots, 104 native Fusion compositions, one locked audio item, zero subtitle tracks.
- Eight freshly rendered native Resolve chapters completed. The mask-bug previews and incomplete CUDA attempts were rejected, not reused.
- Full proxy: `C:\Users\KK\Movies\HIA_VIDEO007_R1\HIA_VIDEO007_CAMP_CENTURY_R1_PROXY_720P25.mp4`, 631,693,718 bytes. SHA-256 `dda57e7cfa13ad357e24059682e42c2555b74f511ed5032facd4406f26bb7e9c`.
- Current native export: `HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_CPU_FIXED.drp`; SHA-256 and actual saved-state readback in `NATIVE_FINAL_READBACK.json`.

## Checks performed

The full proxy decoded without error. Its duration is exactly 1094.720 seconds and its encoded video count is exactly 27,368 frames at 25 fps, 1280 x 720. It has one video stream, one audio stream and no subtitle stream. The full black scan returned no events at the recorded detection threshold.

Rendered narration versus the locked master: normalized correlation 0.9999984018, measured lag 0 ms, gain difference -0.0032 dB. The original 48 kHz/24-bit mono WAV SHA-256 remains `c6a5df8cff089418f4f2300551fd4ba6cb057dcd3012b84fa8143e02976d0480`. Proxy AAC is an encoded listening copy, not bit-identical PCM.

All seven contact sheets (one actual rendered midpoint from each of 132 shots) were visually inspected. No blank full-frame mask fills were seen. The chart qualifiers are visible. Selected document word fills were also inspected at full proxy size. Seven three-point motion strips were inspected: M01/M03 accents progressively reveal, M06 aircraft travels with its attached explanatory ray, M08 module rises on its hoist line, M09 tractor/sled moves as one connected layer, M11 has a restrained camera approach, and M12 reveals a local sample lens. This proves sampled position/reveal changes, not continuous playback smoothness.

## Remaining holds

- Full continuous real-time audiovisual screening has not been completed. Contact sheets and three-point strips do not prove pacing, absence of stepping, transition quality or every narration-to-picture relationship.
- Creative QC remains HOLD: G01, the R02 camp plan and several evidence stills recur; some document/table shots hold a full page at small reading scale. These are visible review issues, not a claimed final creative PASS.
- Only 219.08 timeline seconds are selected genuine moving archive. Primary references, explanatory illustrations and factual native text cards supply the remainder. No archive-only coverage claim is made.
- All 32 approved audio-beat boundaries are used, but S065 and S089 have within-beat fallback visual cue placements rather than word-exact subcue timing.
- G17/G18, disputed C06, unavailable D07 and inaccurate M10_MILLER are excluded. Source-bank independent real-time screening remains separate.
- Final color, music, SFX, owner picture approval and publication approval are not complete. Do not upload this proxy as the final master.

The correct deliverable at this stage is the full rough cut for review. The native project remains editable; the DRP retains source paths and is not a self-contained media archive.
