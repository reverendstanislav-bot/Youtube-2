# GitHub Actions — active set

The current branch intentionally contains only the active production/rebuild workflows:

- `workflows/build_chicago_r14_editorial_recut.yml`
- `workflows/build_tc497_r14_remotion_reedit.yml`
- `workflows/build_hia_shorts_final.yml` — manual-only rebuild of the 10 Shorts master pack

Temporary Shorts review/repackage workflows were removed after the corrected 10-master release was produced.

Do not restore old V1–V13 build/review workflows into the active workflow directory merely for reference. Git history preserves them.

Reason: legacy or temporary workflow files create noisy duplicate runs, stale publication paths, and accidental regressions into superseded editing/provenance logic.
