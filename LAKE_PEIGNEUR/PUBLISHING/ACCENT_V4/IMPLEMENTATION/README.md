# Lake Peigneur V4 — Remotion code integration

Code only, not a rendered MP4. Requires the recovered exact V3 Remotion project and all 97 source images.

From repo checkout:

    python3 LAKE_PEIGNEUR/PUBLISHING/ACCENT_V4/IMPLEMENTATION/apply_v4_to_v3.py --project /full/path/to/REMOTION_V1 --dry-run
    python3 LAKE_PEIGNEUR/PUBLISHING/ACCENT_V4/IMPLEMENTATION/apply_v4_to_v3.py --project /full/path/to/REMOTION_V1

Place a copy of `HIA_LAKE_PEIGNEUR_V4_ACCENT_MAP_MACHINE.json` (from the parent ACCENT_V4 folder) into IMPLEMENTATION/ alongside the installer.

Then from REMOTION_V1:

    npx remotion compositions src/index.jsx
    npx remotion render src/index.jsx LakePeigneurV1 review/opening.mp4 --frames=0-1599 --codec=h264 --crf=17
    npx remotion render src/index.jsx LakePeigneurV1 review/collapse.mp4 --frames=8375-11499 --codec=h264 --crf=17
    npx remotion render src/index.jsx LakePeigneurV1 review/canal.mp4 --frames=13500-15374 --codec=h264 --crf=17
    npx remotion render src/index.jsx LakePeigneurV1 review/final.mp4 --frames=22125-24710 --codec=h264 --crf=17

Review accent start/mid/end frames and dissolve boundaries at native 1080p. Only then render final 24,711 frames with original Arthur voice, BT.709, and full decode QC.

Important: PATH is a soft focus fallback, not invented flow arrows. Replace with a traced existing source path only after visual coordinates have been confirmed.

No subtitled track, new art, paid generation, TTS, new endscreen or changes to user-approved V3 masters.
