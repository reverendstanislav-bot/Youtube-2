from pathlib import Path
import json,collections
ROOT=Path(__file__).resolve().parent
qc=json.loads((ROOT/'QC/PROXY_QC.json').read_text())
native=json.loads((ROOT/'NATIVE_FINAL_READBACK.json').read_text())
visual=json.loads((ROOT/'QC/SAMPLED_VISUAL_REVIEW.json').read_text())
plan=json.loads((ROOT/'SHOT_PLAN_R2.json').read_text())
align=json.loads((ROOT/'NATIVE_HIGHLIGHT_AUDIO_ALIGNMENT.json').read_text())
assert qc['technical_checks_pass'] and visual['all_132_midpoint_samples_reviewed']
chapters=[]
for c in sorted({s['chapter'] for s in plan}):
    shots=[s for s in plan if s['chapter']==c]
    archival=[s for s in shots if s['kind']=='REAL_ARCHIVE_MOTION']
    chapters.append(f"| {c} | {sum(s['duration_frames'] for s in shots)/25:.2f} | {len(archival)} | {sum(s['duration_frames'] for s in archival)/25:.2f} |")
counts=collections.Counter(a['status'] for a in align)
report=f'''# Camp Century — R2 correction and review record

**Complete review export; owner approval pending.** The rejected R1 is retained for audit only.

- Native project: `{native['project']}` / `{native['timeline']}`.
- Full MP4: `{qc['file']}`.
- Duration: {qc['duration_seconds']:.3f} seconds / 18:14.720; {qc['encoded_video_frames']:,} frames, 1920 × 1080 / 25 FPS.
- MP4 SHA-256: `{qc['sha256']}`.
- Native checkpoint: `HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2.drp`, SHA-256 `{native['drp_sha256']}`.
- Native saved readback: {native['video_items']} picture items, {native['audio_items']} locked audio item, {native['subtitle_tracks']} subtitle tracks; rendering inactive at checkpoint.

## Actual correction

All generic R1 text cards and direct source scans were replaced. Nineteen selected source-informed generated documents and illustrated scenes follow the approved reference artwork. They are editorial illustrations and do not purport to be original government records. Actual selected files, prompts, reference chains and SHA-256 values are retained in the selected generation records. Rejected raw variants are not installed.

No generated yellow text highlighting remains in the selected PNG bases. Word-height marker sweeps, the precise 5.70 / 7.92 cost bar and local circular contour lenses are native Fusion layers. Exact matched narration cues: {counts.get('ASR_EXACT_PHRASE',0)}. Optional cues without an exact within-scene phrase were omitted rather than timed speculatively. S065/S089 still have declared legacy within-beat subcue fallbacks.

The approved G10 aircraft composition is restored whole. The tractor and sled remain grounded in one coherent road scene with a small camera approach; there is no independent sideways vehicle slide. Most readable pages hold steady; selective focus and ten-frame scene dissolves replace automatic drift. CPU Fusion is explicitly selected.

## Technical evidence

Full-file decode: {qc['full_decode']}. Black events: {len(qc['black_events'])}. Dialogue subtitle streams: {qc['subtitle_stream_count']}. Technical checks: {qc['technical_checks_pass']}.

Original locked narration SHA-256: `{qc['narration_comparison']['locked_file_sha256']}`. Source unchanged: {qc['locked_wav_unchanged']}. AAC review audio correlation: {qc['narration_comparison']['correlation']:.8f}; measured lag: {qc['narration_comparison']['lag_ms']} ms. This compares the encoded review signal with the locked original; it does not claim bit-identical AAC and PCM.

All 132 actual rendered shot midpoint samples were inspected through seven contact sheets. Representative native proofs and three-point full-render sequences were separately inspected for registration, framing, aircraft identity, tractor grounding and local accents. Detailed scope and limitations are recorded in `QC/SAMPLED_VISUAL_REVIEW.json`.

## Moving archive use

These are timeline seconds, not an assertion of an archive-only film or additional unique sources. The 30 archive placements use existing verified real Camp Century clips. Exact new original source frame mappings are recorded in `ADDITIONAL_ARCHIVE_PLACEMENTS.json`. No new download, generated video, voice generation or paid archive order was needed for this correction.

| Chapter | Picture seconds | Real archive clips | Real archive seconds |
| --- | ---: | ---: | ---: |
{chr(10).join(chapters)}

## Remaining gates

Owner picture approval is PENDING. Full continuous real-time audiovisual screening is NOT COMPLETED. Final colour, music and SFX are NOT STARTED. Visual Coverage PASS and publication approval are NOT CLAIMED. A successful render, full technical decode and sampled visual inspection do not waive those gates.

The installation manifest records the actual files copied to the VIDEO 7 R2 review folder and their verified hashes. DRP retains existing absolute source paths and is not a self-contained archive.
'''
(ROOT/'ROUGH_CUT_QC_AND_DELIVERY_2026-10-27.md').write_text(report,encoding='utf-8')
print('REVIEW_REPORT_WRITTEN',flush=True)
