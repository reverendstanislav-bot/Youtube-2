# Chicago files inventory

## Available now — Dropbox

| File | Size | Status |
|---|---:|---|
| HIA_DBX_00.part … HIA_DBX_12.part | 99,614,720 bytes each | available, split legacy source |
| HIA_DBX_13.part | 4,544,607 bytes | available, final split part |
| HIA_CHICAGO_FINAL_UPLOAD.mp4 | 31,053 bytes | invalid/incomplete stub; do not use as master |

Total split-part payload: **1,299,535,967 bytes**.

Per-part Dropbox content hashes are recorded in `SOURCE_FILES/DROPBOX_PARTS_MANIFEST.json`.

## Known historical attachments — currently unavailable

- `Hidden_Industrial_America_Chicago_CODEX_READY_v7(5).rar`
- `Hidden_Industrial_America_Chicago_CODEX_READY_v7(6).rar`
- `Hidden_Industrial_America_Quick_Usage_Guide_RU(1).pdf`

These were direct project-chat uploads. They are not currently present in connected Dropbox/GitHub storage, so their bytes/hashes cannot be truthfully reconstructed from filenames alone.

## Do not lose

When the historical archives are reattached/recovered:
1. hash the originals before changing anything;
2. extract both into separate staging directories;
3. compare duplicate paths by content hash;
4. merge without overwriting non-identical collisions;
5. include the Quick Usage Guide in the intended guide section/item 11;
6. emit a complete file manifest and SHA-256 list;
7. store large final package as a GitHub Release asset, not in normal Git history.
