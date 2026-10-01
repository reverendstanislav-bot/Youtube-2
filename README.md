# Youtube-2

Production repository for **Hidden Industrial America**.

## Canonical release status

**Episodes 001–005: 5 / 5 COMPLETE — OWNER/CODEX FINAL — READY FOR PUBLICATION.**

Current release registry:
`CHANNEL/FINAL_RELEASE_REGISTRY_001_005_2026-10-01.md`

For current state, use the registry plus each episode's `CURRENT_STATUS_HANDOFF.md`. Older review/QC documents are historical audit records and do not override the current release lock.

## Episodes

1. `CHICAGO/` — Chicago Freight Tunnel — **COMPLETE / READY**
2. `TC497/` — LeTourneau TC-497 Overland Train — **COMPLETE / READY**
3. `BIG_MUSKIE/` — Big Muskie / Bucyrus-Erie 4250-W — **COMPLETE / READY**
4. `SATSOP/` — Satsop Nuclear Plant / WNP-3 and WNP-5 — **COMPLETE / READY**
5. `LAKE_PEIGNEUR/` — Lake Peigneur / Jefferson Island Mine Inundation — **COMPLETE / READY**

## Release-metadata mirror rule

Do not invent missing hashes.

The edit state is final for all five episodes. A missing final-binary filename/hash in Git means only that the Codex-final media metadata has not yet been mirrored into this repository; it does **not** reopen production.

Current metadata gaps are listed in:
`CHANNEL/FINAL_RELEASE_REGISTRY_001_005_2026-10-01.md`

## Channel

Channel-level rules, branding, provenance conventions, thumbnail locks, Shorts canon and release registry live under `CHANNEL/`.

## Source-of-truth rule

Current release status is determined by:
1. `CHANNEL/FINAL_RELEASE_REGISTRY_001_005_2026-10-01.md`;
2. each episode's `CURRENT_STATUS_HANDOFF.md`;
3. locked delivery / publishing manifests.

Historical QC files remain preserved for audit history only.

Large media belongs in GitHub Releases/Actions rather than the Git tree. The Git tree keeps production code, recovery dependencies, manifests, source/QC records, locks and canonical status.
