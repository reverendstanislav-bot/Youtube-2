# CHICAGO — CURRENT STATUS / HANDOFF

## Canonical status

**Episode 1 — Chicago is reopened for repair. It is NOT an approved publication master.**

The latest known user-visible defect:
- subtitles still drift / "уезжают";
- prior attempts did not actually solve the timing problem.

Do not call the old `HIA_CHICAGO_FINAL_UPLOAD.mp4` final merely because of its filename.

## Next editing objective

1. Recover/identify the real full Chicago source build.
2. Validate video/audio integrity.
3. Inspect subtitle timing across the whole episode, especially long-term drift rather than only individual lines.
4. Fix subtitle timing from one clean source of truth.
5. Avoid duplicate burned caption layers.
6. Preserve already-accepted picture and audio unless a concrete defect requires a change.
7. Build a new review.
8. User reviews the corrected review.
9. Only after explicit approval: native upload master + full QC.

## Connected-storage state (2026-09-20)

Dropbox contains:
- `HIA_DBX_00.part` … `HIA_DBX_13.part`
- total bytes: `1,299,535,967`
- standalone `HIA_CHICAGO_FINAL_UPLOAD.mp4`: `31,053` bytes — invalid/incomplete as a master.

See `SOURCE_FILES/DROPBOX_PARTS_MANIFEST.json` and `tools/reassemble_dropbox_parts.py`.

## Historical project-package state

Previously uploaded in project chats:
- `Hidden_Industrial_America_Chicago_CODEX_READY_v7(5).rar`
- `Hidden_Industrial_America_Chicago_CODEX_READY_v7(6).rar`
- `Hidden_Industrial_America_Quick_Usage_Guide_RU(1).pdf`

The intent was to merge the two CODEX_READY archives without duplicates or loss and include the quick usage guide as item 11 in the combined package.

Those original attachments are not currently accessible from the connected GitHub/Dropbox sources. Do not invent their contents. If they are reattached, ingest them into this directory/release structure and record hashes.

## Channel context

Chicago is Episode 1. TC-497 is Episode 2. Branding must stay universal for **Hidden Industrial America**, not tied to tunnels, Chicago, or a single industrial category.
