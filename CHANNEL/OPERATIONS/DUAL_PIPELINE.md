# Dual editing pipeline — HIA operating contract

**Status: ROUTING CONFIGURATION ONLY.** Owner reports 22 local skills installed in Codex (`.codex/skills`) and Antigravity (`C:\Users\KK\.gemini\config\skills\`). This GitHub session cannot inspect either local path. Only **20 distinct skill names** were explicitly supplied; do not silently invent the two missing names or claim installation, versions, interoperability or activation. See `SKILL_REGISTRY.json`.

## Two engines, one editorial source of truth

- **Resolve route:** DaVinci Resolve/Fusion, using approved archive sources, accepted audio, episode motion/graphic locks. FFmpeg may prepare lossless/mezzanine media, verify timing and produce technical QC.
- **Remotion route:** Remotion + optional Hyperframes pre-renders + FFmpeg, independent of Resolve's render queue. The route may assemble previews/masters **only when episode production/render authorization already exists**. A claimed skill installation is not authorization.
- **Owner chooses** “Собираем в Remotion (без DaVinci)” or “Собираем в DaVinci”; if unspecified, preserve currently accepted episode engine and do not migrate. Neither engine automatically replaces the other.
- **Canonical input regardless of engine:** approved script and narration hashes, scene-to-source map with rights/semantics, approved timing, visual style, render spec and episode status. Reuse source IDs and paragraph IDs; no different story/audio between engines unless explicitly approved.
- A scene can move between engines via **rendered intermediate + edit decision/timing manifest**, not by assuming a Resolve Fusion composition is faithfully converted into React/Hyperframes or vice versa. Compare stills, timing, sound and rendered motion for actual equivalence.
- Parallel independent projects use separate worktrees, output folders, manifests, cache and render resources. Never have both engines write to the same master or accepted asset. Report disk/GPU/RAM constraints; 2+ concurrent films is a target, not a guarantee.
- **Audio:** treat Voicebox output as immutable after owner acceptance. Beat maps/word timing derived from ASR are approximate until reviewed; no auto-stretch/re-generation. FFmpeg ducking/normalization target must be specified by the episode; **-14 LUFS is not a universal mandated YouTube mastering standard**. Check integrated loudness, true peak, intelligibility, playback and music licensing; no forced target changes to accepted audio.

## Skills and permitted uses

Named skills are **optional capabilities**, not blanket visual directives or proof that a command exists. `hyperframes-registry` “450+ blocks” is owner-reported and unverified in this runtime; individual effects must be justified by the scene. The following must NOT be used as universal presets: film grain, CRT, glitch, vignette, 2.5D drift, animated maps, 3D documents, camera flythroughs, generic zoom, shake. HIA's documentary realism, truthful archive-first production and episode-specific locks win.

- `cinematic-documentary-editor`: scene rhythm, meaning, measured QC; preserve natural archive pace.
- `hyperframes` / `hyperframes-*` / `remotion-to-hyperframes`: composition library, component bridge and pre-render where compatible; source/frame comparison required.
- `media-use` / `motion-graphics` / `visual-style` / `remotion-best-practices`: choose real media and restrained motion for a proven narrative need.
- `reverse-any-video`: research reference structure only; no unauthorized downloads, exact clone, copyrighted footage reuse or private retention claims.
- `documentary-dual-pipeline`: engine scheduling, manifests, audio/visual interchange and resource isolation.
- `osint-investigation-board`: only sourced, attributed relationships and actual documented evidence. Do not invent companies, transfers, official filings or secret links.
- `geo-documentary-maps`: real verified coordinates, dates, paths and projection; map tile/AIS/API access, rights, costs and keys must be verified for the exact service; don't assume all imagery is unrestricted/free.
- `voicebox-beat-sync`: timing aids; do not bypass owner voice approval or alter locked narration.
- `website-to-video`: only accessible, permitted captures with exact source URLs/dates; never pass fictional pages or unverified text as real evidence.
- `adspower-browser`: optional browser automation capability, not proof a site or protected material can be accessed or used; respect permissions.

## Fast production decision tree

1. Read `AGENTS.md`, `CHANNEL/OPERATIONS/ACTIVE_ROUTE.md`, episode owner locks/current state. Resolve any source or rights HOLD first.
2. Choose engine **from owner instruction or existing episode lock**; do not choose by whichever skill is installed.
3. Read `SKILL_REGISTRY.json` and verify the **required** skill's local SKILL.md, installed dependencies, executable CLI/API and versions. Missing tools => `ENV_HOLD`; fallback only when already authorized and visually equivalent.
4. Before rendering full film, generate a short **representative proof** covering archival motion, factual graphic, document close-up and audio transition from the actual episode. Review pixels/audio at full speed. Do not make a giant prototype suite.
5. Use single episode scene manifest; maintain parity of frame rate, source in/out, narration IDs, safe zones and source attribution across engines.
6. Run `python CHANNEL/tools/validate_dual_pipeline.py CHANNEL/OPERATIONS/DUAL_PIPELINE_CONFIG.json`. This validates configuration integrity only, not local installations, footage rights or picture quality.
7. Never mark final PASS until complete AV review and source/rights/QC gates, owner approval and authorized delivery.

## Operational exclusions

No Shorts until explicit owner reversal, no dialogue subtitles in HIA, no generated video, no false documents, no invented archive, no repeated decorative motions. No production, download, paid service, new Voicebox job, browser automation, render or publication is started by adding this configuration.
