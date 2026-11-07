# ARGON HANDOFF — HIA VIDEO 012 — CINCINNATI SUBWAY

## Current verified state

- Worktree: `C:\Users\KK\Youtube-2-VIDEO012-CINCINNATI`
- Branch: `codex/video012-cincinnati-subway-r1`
- Episode root: `VIDEO_012_CINCINNATI_SUBWAY`
- Editorial stage: `DRAFT_SCRIPT_LOCK_HOLD`
- Current Russian structure draft: `01_DEVELOPMENT/HIA_VIDEO012_CINCINNATI_SUBWAY_RU_R4.md`
- English narration: not approved and not ready for voice generation.
- Narration audio: absent.
- HyperFrames project: not created.
- Remotion project: not created.
- Final video/render: not created.
- Publication: not authorized.

The owner explicitly authorized continuing the visual assembly in HyperFrames and Remotion. This does not authorize voice generation, AI image/video generation, publication, or a claim of final approval.

## Required reading before work

1. Repository `AGENTS.md`.
2. `CHANNEL/EDITORIAL_OWNER_LOCK_2026-11-02.md`.
3. `CHANNEL/OPERATIONS/ACTIVE_ROUTE.md`.
4. `CHANNEL/OPERATIONS/DUAL_PIPELINE.md`.
5. `VIDEO_012_CINCINNATI_SUBWAY/AGENTS.md`.
6. `VIDEO_012_CINCINNATI_SUBWAY/PROJECT_STATE.json`.
7. `VIDEO_012_CINCINNATI_SUBWAY/CURRENT_STATUS_HANDOFF.md`.
8. `VIDEO_012_CINCINNATI_SUBWAY/02_ASSETS/PACKAGE_STATUS.md`.
9. `VIDEO_012_CINCINNATI_SUBWAY/02_ASSETS/RIGHTS_QC.csv`.
10. `VIDEO_012_CINCINNATI_SUBWAY/02_ASSETS/SHOT_BY_SHOT_PLAN.csv`.

Do not treat `PASS_CONFIGURATION_ONLY` as production clearance. Do not silently upgrade `DRAFT_SCRIPT_LOCK_HOLD` to Script Lock.

## Asset package

The verified local media package is in `02_ASSETS`.

- 123 physical files, about 1.63 GiB.
- 66 manifest rows were checked for SHA-256 and file size.
- Originals and edit-ready derivatives are separated.
- Two exact Cincinnati construction photographs and thirteen report/engineering plates are present.
- Rights and source evidence are in `ARCHIVE_MASTER.csv` and `RIGHTS_QC.csv`.
- Technical data are in `VIDEO_TECHNICAL.csv` and `PHOTO_TECHNICAL.csv`.
- `ALL_FILES_SHA256.csv` is the integrity reference.
- `MISSING_ASSETS.md` records known gaps and HOLD items.

Never use a row marked `HOLD`. In particular, do not substitute unrelated GCWW footage for the missing exact tunnel film. Preserve original aspect ratios and do not stretch 4:3 archive.

## Authorized assembly target

Create one shared manifest and two deterministic editors under:

```text
VIDEO_012_CINCINNATI_SUBWAY/03_DUAL_EDIT/
  README.md
  SHARED/SHOT_MANIFEST.json
  SHARED/PIPELINE_STATUS.json
  SHARED/VOICE_SLOT.md
  HYPERFRAMES/
  REMOTION/
```

Technical target:

- 1920x1080
- 25 fps
- provisional picture duration: 900 seconds / 22,500 frames
- no dialogue subtitles
- no generated footage
- no fake archive
- no light leaks, full-frame bloom, shake, random drift, or universal zoom
- hard cuts by default; restrained movement only on a verified detail or document
- music and SFX on separate tracks
- narration track intentionally empty and visibly marked `VOICE HOLD`
- final 20 seconds are an internal canonical-end-screen slot, not a fabricated final end screen

## Shared picture sequence

Use the following sequence as the initial deterministic picture edit. Reprises at the end are deliberate motifs, not filler.

| # | In | Out | Asset / purpose |
|---:|---:|---:|---|
| 1 | 0.00 | 15.00 | P002 tunnel flashlight |
| 2 | 15.00 | 25.00 | P010 Central Parkway wide |
| 3 | 25.00 | 35.00 | P013 Parkway / OTR |
| 4 | 35.00 | 45.00 | E001 panorama |
| 5 | 45.00 | 75.00 | P001 Race Street station |
| 6 | 75.00 | 90.00 | M004 report title |
| 7 | 90.00 | 105.00 | M003 route map |
| 8 | 105.00 | 125.00 | L001 Government Square |
| 9 | 125.00 | 145.00 | L002 Walnut Street |
| 10 | 145.00 | 165.00 | P008 historic canal |
| 11 | 165.00 | 180.00 | M002 canal map |
| 12 | 180.00 | 195.00 | M001 subway map |
| 13 | 195.00 | 215.00 | P027E excavation |
| 14 | 215.00 | 235.00 | P032 Central Parkway construction |
| 15 | 235.00 | 250.00 | M005 canal cross-sections |
| 16 | 250.00 | 265.00 | M010 station plan |
| 17 | 265.00 | 280.00 | M014 typical subway |
| 18 | 280.00 | 295.00 | M015 typical tunnel |
| 19 | 295.00 | 315.00 | M016 cost table |
| 20 | 315.00 | 335.00 | L003 downtown 1939 |
| 21 | 335.00 | 355.00 | M011 passenger car |
| 22 | 355.00 | 375.00 | P003 entrance |
| 23 | 375.00 | 395.00 | P004 graffiti |
| 24 | 395.00 | 415.00 | P005 tunnel door |
| 25 | 415.00 | 435.00 | P006 Race Street entrance |
| 26 | 435.00 | 455.00 | M006 trestle |
| 27 | 455.00 | 475.00 | M007 elevated structure |
| 28 | 475.00 | 495.00 | M008 Walnut tracks |
| 29 | 495.00 | 515.00 | M009 roadbed |
| 30 | 515.00 | 535.00 | M012 baggage / Canal station |
| 31 | 535.00 | 555.00 | M013 freight terminal |
| 32 | 555.00 | 570.04 | E005 fallout dosimeter |
| 33 | 570.04 | 587.08 | E006 civil-defense building |
| 34 | 587.08 | 607.08 | P021 GCWW exterior context |
| 35 | 607.08 | 627.08 | P022 GCWW interior |
| 36 | 627.08 | 641.12 | E007 marked entrance |
| 37 | 641.12 | 656.12 | E008 marked building |
| 38 | 656.12 | 681.12 | P023 GCWW mechanism / construction |
| 39 | 681.12 | 706.12 | P024 pump mechanism |
| 40 | 706.12 | 726.12 | M003 map reprise, intentional new crop |
| 41 | 726.12 | 734.52 | E002 river |
| 42 | 734.52 | 746.52 | E004 misty Roebling |
| 43 | 746.52 | 758.52 | E003 night Roebling |
| 44 | 758.52 | 778.52 | P014 modern parkway |
| 45 | 778.52 | 798.52 | P017 modern parkway |
| 46 | 798.52 | 818.52 | P019 modern context |
| 47 | 818.52 | 840.00 | P010 intro/outro motif |
| 48 | 840.00 | 850.00 | E001 motif reprise |
| 49 | 850.00 | 858.40 | E002 motif reprise |
| 50 | 858.40 | 880.00 | P013 motif reprise |
| 51 | 880.00 | 900.00 | internal canonical-end-screen slot |

Resolve every short ID to the exact manifest path in `ARCHIVE_MASTER.csv`, `EDIT_READY_MASTER.csv`, or `SHOT_BY_SHOT_PLAN.csv`. Fail validation if any path is missing; never replace it with a visually similar random file.

## Editorial title beats

These are section cards, not dialogue subtitles:

- 00:00 — `TWO MILES OF SUBWAY. NO TRAIN EVER RAN.`
- 00:45 — `CINCINNATI SUBWAY`
- 01:45 — `A RAILWAY IN A CANAL`
- 03:15 — `CONCRETE WITHOUT A SYSTEM`
- 05:15 — `WHY IT STOPPED`
- 09:15 — `A SECOND LIFE: WATER`
- 12:14 — `THE QUESTION RETURNS`
- 14:18 — `STRUCTURE IS NOT A SYSTEM`

Keep all text inside title/action safe. Do not add orange word highlighting or burned dialogue captions.

## Provisional audio map

Use only PASS rows from `MUSIC_SFX_MASTER.csv`. Keep levels conservative; no automatic normalization.

- A004: 0.00–145.70
- A002: 145.70–291.40
- A001: 291.40–559.10
- A003: 559.10–733.30
- A004 reprise from a different source offset: 733.30–900.00
- S004 at 00:02
- S001 at 03:15
- S003 at 05:15
- S002 at 09:15
- S004 at 11:46
- S003 at 14:18

The audio mix remains provisional until the exact approved English narration is generated, QC'd, and timed.

## HyperFrames implementation gate

Use `C:\Users\KK\AppData\Roaming\npm\hyperframes.cmd` because PowerShell `.ps1` wrappers are blocked.

1. Build a standalone composition with `data-composition-id="hia-video012-picture"`.
2. Keep all media references under the project `assets/` folder.
3. Register exactly one paused timeline at `window.__timelines["hia-video012-picture"]`.
4. Animate only selected child layers; never put a full-frame transform on every shot.
5. Run, in order: `check --json`, `validate --json`, `inspect --json`, then snapshots at representative frames.
6. Visually inspect snapshots for opening, engineering drawings, GCWW section, modern parkway, and end-screen slot.
7. Do not render the full 15-minute master before these gates pass.

## Remotion implementation gate

1. Use exact Remotion 4.x package versions and 25 fps.
2. Register a 22,500-frame 1920x1080 composition.
3. Read the same `SHOT_MANIFEST.json`; do not maintain an independent timeline by hand.
4. Use `staticFile()` for every local asset.
5. Use frame-derived deterministic transforms only.
6. Render stills at the same representative timestamps as HyperFrames.
7. Compare geometry and title timing across both engines before any draft video render.

## Required status labels

Until the remaining gates are actually passed, report:

```text
ASSET_PACKAGE: PASS_WITH_DECLARED_GAPS
SCRIPT_LOCK: HOLD
VOICE: ABSENT
HYPERFRAMES_ASSEMBLY: NOT_STARTED
REMOTION_ASSEMBLY: NOT_STARTED
FULL_RENDER: NOT_STARTED
FULL_REALTIME_AV_REVIEW: NOT_PERFORMED
PUBLICATION: NOT_AUTHORIZED
```

After work begins, update these labels from concrete evidence only. A successful command is not a creative or audiovisual PASS.

## Integrity check after download

From the episode root in PowerShell:

```powershell
$manifest = Import-Csv '.\02_ASSETS\ALL_FILES_SHA256.csv'
foreach ($row in $manifest) {
  $path = Join-Path '.\02_ASSETS' $row.relative_path
  if (-not (Test-Path -LiteralPath $path)) { throw "Missing: $path" }
  $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($hash -ne $row.sha256.ToLowerInvariant()) { throw "Hash mismatch: $path" }
}
"ASSET HASH PASS: $($manifest.Count) rows"
```

If the downloaded archive and the checked-out branch disagree, keep the archive immutable and reconcile paths through the shared manifest. Do not silently overwrite accepted source assets.
