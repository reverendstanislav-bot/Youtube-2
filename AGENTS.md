# Youtube-2 / Hidden Industrial America — Codex start here

**Scope: Youtube-2 only. Do not mix with Youtube-3. Read current `origin/main` before each task.**

## Mandatory startup (in this order)
1. [ACTIVE ROUTE](CHANNEL/OPERATIONS/ACTIVE_ROUTE.md) — short operational contract, status/stop rules and workflow safety.
2. [OWNER LOCK](CHANNEL/EDITORIAL_OWNER_LOCK_2026-11-02.md) — overriding editorial, production and rights decisions.
3. Selected episode `AGENTS.md` (if present) AND its `PROJECT_STATE.json` or `CURRENT_STATUS_HANDOFF.md`; inspect actual current source HOLDs.
4. Only the stage-specific canon/evidence needed for the user request. Never choose a stale branch, archived R1/R2 report or historical workflow as current authority.

## New/unlocked script work only
Read [universal script canon](CHANNEL/SCRIPTWRITING/HIA_SCRIPTWRITING_CANON.md), [12 mandatory skills](CHANNEL/SCRIPTWRITING/HIA_12_MANDATORY_SCRIPT_SKILLS.md), [script template](CHANNEL/SCRIPTWRITING/HIA_SCRIPT_TEMPLATE.md), [20-item QC](CHANNEL/SCRIPTWRITING/HIA_SCRIPT_QC_CHECKLIST.md), and changelog. Each new script needs 20-point QC plus evidence-backed SK01–SK12 review. A completed form does **not** grant Script Lock or owner approval.

## Current specific owner decisions
- **NO SHORTS** for current/future HIA work until expressly reauthorized. No dialogue subtitles; retain source provenance/rights, brand/safe zones and approved voice. No new TTS, image/video generation, spending, assembly or publication without applicable owner permission. AI video is prohibited.
- Glomar Explorer: current source of truth is `GLOMAR_EXPLORER/PROJECT_STATE.json` and `RECHECK_R3/`. Owner-accepted R1.2 narration/script preserved. R2 editorial readiness REJECTED; archive-led film requires scene-specific NEW moving source coverage and rights checks. Never run R2 legacy finalizer as if current.
- VIDEO010 is **Antarctic Snow Cruiser**, not Church Hill or Glomar. Read `VIDEO_010_ANTARCTIC_SNOW_CRUISER/AGENTS.md`, current handoff and competitor-to-scene comparison before work. Do not renumber episodes.
- Previous released/locked episodes, accepted assets and old revisions remain immutable unless the owner explicitly approves revision.

## Exit gate
Run relevant stage validators and report real `PASS/HOLD/REJECT` with source evidence, specific deliverable and commit SHA. For Glomar: `python CHANNEL/tools/hia_preflight.py --repo . --gate audit`; never claim edit-ready while `python CHANNEL/tools/hia_preflight.py --repo . --gate edit-ready` fails. No fabricated full-AV reviews, rights clearance or owner approvals.

## Dual editing engines (owner configuration 2026-11-05)
Read [DUAL_PIPELINE.md](CHANNEL/OPERATIONS/DUAL_PIPELINE.md) and [SKILL_REGISTRY.json](CHANNEL/OPERATIONS/SKILL_REGISTRY.json) only when task concerns montage, asset transfer, graphics or engine choice. Resolve / Remotion+Hyperframes+FFmpeg are two possible routes, not automatic authorization to render, generate or migrate. Follow the existing episode engine unless owner explicitly selects a route; local Codex/Antigravity skill installations are not verifiable from GitHub. Validate configuration with `python CHANNEL/tools/validate_dual_pipeline.py`.
