# Project structure

Recommended episode layout:

```
EPISODE/
  README.md
  CURRENT_STATUS_HANDOFF.md
  PROJECT_HISTORY.md
  FILES_INVENTORY.md
  SOURCE_FILES/
    manifests / provenance / hashes
  QC/
    picture / subtitle / audio notes
  PUBLISHING/
    YouTube checklist / description / chapters / metadata
  tools/
    rebuild / recovery / validation scripts
```

Large binaries should normally be stored as GitHub Release assets or workflow artifacts, with hashes and stable identifiers written into Git.

## Approval semantics

- `review` — can be watched, not publication-approved.
- `candidate` — possible upload source, still requires review.
- `publication master` — only after explicit user approval + successful QC.
- A filename containing `FINAL` from an older workflow does not override the canonical status file.
