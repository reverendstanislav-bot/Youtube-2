# Chicago source files

This folder stores manifests and provenance/state information for source material.

The actual ~1.3 GB split payload currently lives in Dropbox and is intentionally not duplicated into normal Git history.

Use:
```
python CHICAGO/tools/reassemble_dropbox_parts.py \
  --parts-dir /path/to/downloaded/parts \
  --manifest CHICAGO/SOURCE_FILES/DROPBOX_PARTS_MANIFEST.json \
  --output HIA_CHICAGO_RECOVERED_SOURCE.bin
```

The script:
- validates file names;
- validates exact sizes;
- validates Dropbox content hashes;
- concatenates in numeric order;
- calculates final SHA-256;
- runs `ffprobe` when available.

Only rename the recovered output to MP4 after `ffprobe` confirms it is a valid video.
