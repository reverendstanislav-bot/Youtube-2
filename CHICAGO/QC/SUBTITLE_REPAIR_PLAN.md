# Chicago subtitle repair plan

## Blocking defect

The old Chicago upload candidate still has subtitles that drift / move out of sync. This is the last explicitly reported user defect and must be treated as unresolved.

## Repair principles

- Work from the cleanest recoverable picture/audio source.
- Do not stack a new burned subtitle layer over an old burned layer.
- Identify whether drift is:
  - constant offset;
  - progressive timebase drift;
  - frame-rate mismatch;
  - transcript/VO alignment error;
  - concat/edit boundary error.
- Measure timing at the beginning, middle, and end before choosing a fix.
- If progressive drift exists, do not fix it with a single global offset.
- Preserve accepted picture/audio unless the timing source itself requires remux/re-encode.

## Minimum QC gates

Before calling a new review ready:
1. inspect opening captions;
2. inspect at least three middle checkpoints;
3. inspect the final 20% of the film;
4. compare spoken word vs caption onset/exit;
5. verify no duplicate caption layer;
6. verify no text crosses safe margins;
7. verify final duration/audio sync;
8. export objective media metadata and screenshots.

## Approval

A corrected Chicago review still requires explicit user approval before any file is called publication/upload master.
