# GitHub Actions — active set

The current branch intentionally contains only the active render workflows:

- `workflows/build_chicago_r13_remotion_reedit.yml`
- `workflows/build_tc497_r14_remotion_reedit.yml`

Do not restore old V1–V13 build/review workflows into the active workflow directory merely for reference. Git history preserves them.

Reason: legacy workflow files created noisy duplicate runs, stale publication paths, and accidental regressions into superseded editing/provenance logic.
