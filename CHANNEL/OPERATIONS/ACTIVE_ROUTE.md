# Codex execution route — Youtube-2 / Hidden Industrial America
Updated 2026-11-05. This is the SHORT entry point, not a replacement for source-specific locks.

## 1. Read ONLY the currently relevant authority
1. Fetch `origin/main` HEAD and read root `AGENTS.md`; do not trust stale worktrees.
2. Read `CHANNEL/EDITORIAL_OWNER_LOCK_2026-11-02.md`, then the chosen episode `AGENTS.md` (when present), then its current `PROJECT_STATE.json` or `CURRENT_STATUS_HANDOFF.md`.
3. Read ONLY the documents relevant to the requested stage. For NEW/UNLOCKED writing read `CHANNEL/SCRIPTWRITING/HIA_SCRIPTWRITING_CANON.md` and `HIA_12_MANDATORY_SCRIPT_SKILLS.md` plus the script template/QC. For visuals read current episode source/rights/scene-gaps and working timeline. Do not ingest all 95 historical GitHub workflows or every previous R-version.
4. Current Glomar authority: `GLOMAR_EXPLORER/RECHECK_R3/README_RU.md`, `AUDIT_RESULT.json`, `SCENE_GAPS.csv`, `PROJECT_STATE.json`. R1/R2 are historical and must NEVER override R3; the R2 finalizer is not an approved current process.

## 2. Execution contract — mandatory
- State exact requested deliverable, current SHA, stage, locked assets, existing materials to reuse and the 1–3 real blockers before doing work. Don't restart completed research.
- Make smallest necessary change to the current active artifacts. Never overwrite approved voice, story, assets or prior versions. Source-first: moving historical archive before still photos, verified documents or narrowly justified graphics; never pretend a document replaces missing filmed action.
- Every footage placement needs a source ID, real original source/time, scene-specific semantic fit, quality and rights decision. Technical decode/hash PASS is **not** editorial/rights PASS.
- Never fabricate QA, full real-time playback, thumbnail performance, owner acceptance, cleared rights or finished graphics. No fixed number of shots/prompts, fake archive, generative video, random stock substitutes, gratuitous zooms or artificial duration padding.
- Current owner locks: NO SHORTS until explicitly reauthorized; no dialogue subtitles; preserve provenance, visual safe zones, established narrator/profile, source HOLDs and owner approval. No spending, generation, new TTS or publishing without stage-specific permission. Do not mix with Youtube-3.
- When a block is real, report `HOLD` and the exact evidence or missing asset; do not solve a blank cell by repeating a document. Production readiness is never inferred from completion of tables.

## 3. Finish with verifiable evidence
- Run applicable stage checks: `python CHANNEL/tools/hia_preflight.py --repo . --episode GLOMAR_EXPLORER --gate audit` for Glomar; `--gate edit-ready` only when claiming editor-ready. Audit HOLD is an honest outcome; edit-ready FAIL must stop handoff.
- Run existing 20-item script QC validator and manual 12-skill evidence review for any new script; script validator checks structure, not meaning.
- Report files changed, SHA/commit, validation results, what is LOCKED, what remains HOLD, and ONE next action. No `PASS` by self-declaration.
- Existing accepted projects and historical files must remain byte-identical unless the owner explicitly requests their revision.

## Workflow safety
Do not choose a workflow from `.github/workflows/` by name similarity. Those are episode/version-specific historical automation. Read its exact source and the episode's CURRENT status before invoking any workflow. Read `CHANNEL/OPERATIONS/ACTIVE_ROUTE.md` for stage routing and stop conditions.
