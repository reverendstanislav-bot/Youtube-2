# LAKE PEIGNEUR — MASTER / PROVENANCE QC GATE

Updated: 2026-10-10  
Status: **BLOCKED AT PHYSICAL MASTER BINARY / PROVENANCE PLAN AUDITED**

## What is verified

Project state:
- episode is owner-confirmed COMPLETE / FINAL in the canonical 5/5 registry;
- final captions exist and run to approximately **16:08.080**;
- canonical VO runtime upstream is **16:08.464**;
- final thumbnail is independently locked.

## Master-binary recovery audit

Checked:
- current Git tree;
- GitHub releases;
- Lake Peigneur Git history;
- current Project/conversation files;
- personal Library search;
- active runtime `/mnt/data`.

Result:
**no final Lake Peigneur long-form MP4 binary was found.**

Git contains no final Lake master filename or SHA256.
Prior handoff explicitly calls this a metadata mirror gap.
No older/non-canonical MP4 will be substituted.

Therefore:
- ffprobe cannot yet be run;
- SHA256 cannot yet be calculated;
- frame-level final-master QC cannot honestly be claimed;
- Shorts cannot be physically rendered from the canonical source yet.

## Provenance audit

Stage 8B temporarily assigned 19 authentic MSHA Appendix EE historical frames as **CONDITIONAL_USE** because item-level photographer/source rights were unresolved.

However, later Stage 8C-R3 changed the production plan to a **144-generated-asset pack**:
- DOCUMENT: 12
- MAP / spatial GFX: 26
- GENERATED GFX: 55
- RECONSTRUCTION: 51
- reuse: 0
- hard QC: 144/144 PASS
- **conditional Appendix EE dependencies in the generated prompt pack: 0**

R4 and R4.1 superseded that pack for text/render controls and did not reintroduce an Appendix EE dependency in the documented plan.

### Provenance conclusion

**The final documented generation plan is clean of the unresolved Appendix EE dependency.**

But the repository does not contain:
- the final 144-output visual manifest;
- a final picture-assembly manifest proving the exported master used only that plan;
- the final MP4 itself.

Therefore the provenance risk is reduced at the planning level but **cannot be marked binary-verified** until the actual master is inspected.

## Required physical master check once the exact file is available

P0 — identity:
- exact filename
- byte size
- SHA256
- runtime
- frame rate
- resolution
- H.264/other codec + bitrate
- audio codec / sample rate / channels
- full decode test

P1 — targeted visual spot QC:
- 00:00–00:41 cold open
- 05:36–06:49 surface collapse
- 09:18–10:11 canal reversal
- 11:02–12:49 cause/forensics
- 13:59–16:08 modern context / ending

At each range verify:
- no unresolved Appendix EE historical still masquerading as cleared archive;
- no AI image presented as authentic historical source;
- no text corruption;
- no black panels;
- captions safe;
- no duplicate subtitle layer.

P2 — audio:
human-ear check:
- Peigneur
- Delcambre

P3 — YouTube:
upload Unlisted only after P0–P2 pass; wait for HD processing and check transcode softness.

## Current gate

Packaging: **PASS**  
Description: **PASS**  
4 Shorts selection/timing: **PASS**  
Provenance plan: **PASS WITH BINARY VERIFICATION REQUIRED**  
Physical master QC: **BLOCKED — MASTER FILE NOT AVAILABLE**

**READY_FOR_UNLISTED = NO**

Only blocker:
**the exact final Lake Peigneur MP4 binary must be supplied/recovered.**
