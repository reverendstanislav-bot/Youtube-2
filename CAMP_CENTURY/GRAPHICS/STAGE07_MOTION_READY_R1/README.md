# Camp Century — eight motion-ready anchor illustrations

The owner accepted the visual style of the 24 previous illustrations. This package selects eight explanatory anchors and adapts that style for independent motion. Approval of this new animation treatment remains pending.

## Open

`preview/CAMP_CENTURY_8_MOTION_TESTS_64S.mp4` contains eight separate 8-second silent treatment tests. These are examples, not a newly assembled film or production narration sync. `keyframes/` contains four sampled states for each test. `assets/` contains full clean plates and two genuine-alpha objects. `overlays/` contains transparent accent end states, not the animated versions. `render_motion.py` is the editable deterministic animation source, and regenerates actual individual MP4s and the combined test. Nothing was installed into Resolve.

The native backgrounds are 1672 x 941; previews use 1672 x 940 to satisfy 4:2:0 encoding, dropping the last bottom row without stretching/upscaling. The default preview rate is 25 fps, explicitly independent of any unverified production timeline rate. Re-render with `--fps <actual project fps>` after verifying the edit. No production frame rate is assumed.

## Selected treatments

| Test | Original | Purpose and actual motion |
| --- | --- | --- |
| M01 | G01 | Foreground prefab room gains a local warm accent, then a separate leader identifies the arch; one shallow 2.8% push targets the room. |
| M02 | G02 | CUT / COVER / BURY accents are written on sequentially; keep the original construction drawing visible. |
| M03 | G06 | Initial/reduced states receive separate readable accents and a local translucent roof-intrusion stroke; no morph, invented measurement or simulated deformation rate. |
| M04 | G05 | Cold-water shaft trace followed by a warm waste-cavity contact trace; systems stay disconnected. |
| M05 | G08 | Highlight travels down the borehole in two segments around the visible depth-break symbol, then accents basal sediment. |
| M06 | G10 | Independent alpha aircraft traverses the sky; a moving conceptual sensor wedge reaches the shallow remnants, which are then locally emphasized. This is not radar data. |
| M07 | G07 | Local tool/snow accents and sequential maintenance words; no fake character animation. |
| M08 | G21 | Generic container rises on its own alpha layer while structures stay still; a small local accent then identifies the remnants. Removal and later remains are a conceptual comparison, not a recorded historical instant. |

## Production boundaries

`MOTION_PLAN.json` carries exact locked V4 word cues and word indexes, with AUDIO_TIMING_HOLD. Eight seconds is a test duration only: remap attack, reading hold and exit to the approved voiceover before editing. Do not place all eight consecutively in the film. M03 and M07 belong to the same chapter and need intervening genuine footage. Original generated pictures are illustrative concepts, not archival photographs, measured drawings or historical documents. Do not imply precise time/depth/rate from qualitative motion.

Only seven new ImageGen outputs were requested: five cleaned plates and two isolated objects. Three accepted backgrounds were reused. No generated video, TTS, paid archive purchase, script rewrite or Resolve timeline mutation was performed. Monetary ImageGen cost is not exposed; the platform's generation allowance was used.

## Reproduce

Install Pillow in the chosen Python environment and have ffmpeg/ffprobe on PATH. Run `python render_motion.py --stills` for sampled states, or `python render_motion.py --fps 25` for all clips. Select a subset with `--only M01,M06`. Curve timing is independent of the chosen frame rate and is defined in seconds. Shapes are composited at 2x then sampled down for antialiasing; background transforms use fractional coordinates. No random camera movement, shake, looped pulse, full-screen flash, fake documents, giant labels or template UI is used.

The preview renderer is an offline motion-design test, not a claim that Fusion has been implemented or reviewed. Use the assets, exact cue list and the motion source to rebuild in Fusion for the documentary edit. Original R1 source files remain preserved.
