# VIDEO007 Camp Century: native Resolve visual R1

**OWNER REJECTED — retained only for recovery and audit.** This revision is not an approved delivery. Use `../RESOLVE_R2/README.md` and the R2 timeline for the current correction. The technical checks below do not override the owner's rejection of the picture treatment.

Project: `YT2 Vid7`. Timeline: `HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_25FPS`.

The complete rough cut is 1920 x 1080, 25 fps, 27,368 frames (18:14.720), beginning at 01:00:00:00. It contains 132 picture shots, including 28 unique archive clips and 104 native Fusion compositions. The single original narration WAV is on locked A1 from sample zero; there are no dialogue subtitle tracks. The V4 narration was not rewritten.

## Open or restore

Use the existing timeline in the open project. The restoration checkpoint is `HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_CPU_FIXED.drp`. The older DRPs in this working directory predate the mask correction and are not the current delivery. Source paths are absolute Windows paths: original archive under `C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE`, conformed picture under this folder's `CONFORMED_25FPS`, graphics inside this repository, and the locked audio under `C:\YOUTUBE\Youtube 2\VIDEO 7\AUDIO\VOICEBOX_ARTHUR_V1`. DRP is a project export, not a self-contained media archive.

## Picture treatment

The native comps use local progressive yellow word fills on selected authentic documents, restrained subject approaches, progressive transparent illustration accents, independent aircraft/convoy/module layers and a local sample-inspection lens. No random shake, dialogue captions or generic dossier overlay was added. Some authentic documents and photographs deliberately hold steady. The roof-construction worker illustration has a gentle camera approach; the roof panel itself is not independently animated.

The rough cut mixes 219.08 seconds of selected real moving archive, 355.48 seconds of primary-reference stills/documents, 338.72 seconds of generated explanatory illustrations and 181.44 seconds of factual native text graphics. These are timeline durations, not a claim of additional unique archival footage.

## Provenance and gates

`SHOT_PLAN_R1.csv` gives every shot's beat, timing, source, purpose, rights basis and historical restriction. `CONFORMED_MEDIA_MANIFEST.json` records originals and 25 fps derivatives. `FUSION_IMPORT_MANIFEST.json` describes the native treatment, `COMPOSITION_SOURCE_HASHES.json` fingerprints the comp sources, and `NATIVE_COMP_REPLACEMENT_LOG.json` records actual UseGPU=0 readback. `EDIT_PROVENANCE_AND_HOLDS.json` states exclusions and review limitations.

G17, G18, the disputed C06 rediscovery date card, unavailable D07 GAO page and inaccurate M10_MILLER object are excluded. All 32 audio-beat boundaries use locked narration timing; S065 and S089 use within-beat fallback placement and are not claimed word-exact.

## Render and review

Fusion CPU processing is explicitly selected after repeated CUDA error 700. The first mask-bug previews are rejected and must not be used. `NATIVE_CPU_MASK_PROOFS.json` records four fresh native samples; the document and text graphic were visually inspected after correcting mask connections.

`render_chapters.py` exports eight native Resolve video-only chapters. `mux_proxy.py` joins those encoded picture streams without re-encoding and pairs them with the complete original locked WAV in a single continuous AAC proxy. `qc_proxy.py` decodes the full proxy, checks duration/fps/subtitle absence, scans black frames, compares rendered audio with the locked WAV and makes one sample per shot. Actual results belong in `QC/PROXY_QC.json`; this README does not substitute for that report.

The proxy is a rough picture review, not a final color/music/SFX master or publication approval. Full continuous real-time audiovisual review and owner picture approval remain separate gates. No Visual Coverage PASS is claimed from rendering or contact sheets.
