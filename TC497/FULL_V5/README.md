# TC497 FULL_V5 — Critic Pass + YouTube-Safe Music Mixer

This pass is designed to sit on top of the approved FULL_V4 review cut.

## Why V5 exists
FULL_V4 fixed the major technical failures, but the next critic pass still identifies:
- several chapters with long static holds;
- a few visual-language inconsistencies between archive, reconstruction and modern survivor imagery;
- documentary evidence crops that are still too dense for mobile;
- a few helicopter / concept images that can still be read too literally;
- a soundtrack that is technically clean but still too flat (FULL_V4 LRA ~3.8 LU).

## V5 tool
`v5_fix_and_music.py` does three jobs:
1. audits the V4 shot map for repetition / long holds / category streaks;
2. optionally overlays replacement stills for exact time-ranges listed in a visual patch manifest;
3. adds only music that passes a local YouTube-license manifest gate.

### Allowed music sources
The tool accepts only:
- `original` — music you own / create yourself;
- `youtube_audio_library` — files downloaded from YouTube Studio Audio Library.

Anything else is rejected by default.

For YouTube Audio Library tracks:
- `attribution_required=false` is simplest;
- if attribution is required, the exact credit text must be present in the manifest;
- the tool writes `YOUTUBE_DESCRIPTION_MUSIC_CREDITS.txt`.

## Mix design
- Cold open 00:00–01:22.6 is left untouched.
- Music starts only after 01:22.6.
- Cue levels are deliberately low.
- Music is side-chain ducked under the existing narration/audio.
- Document/evidence sections are automatically reduced.
- The final epilogue is near-silent.
- Final output is normalized near -14 LUFS / <= -2 dBTP.

## Recommended Audio Library search
Use YouTube Studio > Audio Library and filter:
- Attribution not required
- Mood: Dark / Dramatic / Calm
- Genre: Ambient / Cinematic / Electronic
- avoid strong melody, vocals and obvious trailer percussion

Download the chosen tracks yourself from YouTube Studio, then put them beside the manifest.

YouTube Help explicitly states that Audio Library music/sfx are known to YouTube as copyright-safe, and tracks marked Attribution not required do not require a credit in the description.
