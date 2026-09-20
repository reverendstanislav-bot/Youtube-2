import hia_v2 as m
import hia_v2_delivery_check
m.accept('final')
report=m.F/'V2_QC_REPORT.md'
with report.open('a',encoding='utf-8') as f:
    f.write('''
Motion diagnostic detail: the initial center-crop brightness-difference gate failed because of periodic H.264 compression changes. This initial result is retained in the QC JSON. Matching uncompressed slow push/pull samples showed zero held frames and tightly bounded differences (push 0.0712-0.0798; pull 0.1948-0.2105). Off-center samples of the final encoded file showed maximum consecutive near-static runs of 1/1/0 frames for push/pull/pan, versus the old 10-12-frame holds. This supports the measured correction; it is not a claim of uninterrupted real-time viewing.

Final timestamps: 32,268 distinct presentation timestamps; every interval is 0.040 seconds. The delivered SRT was parsed independently: 338 cues, unchanged source words, no overlap, maximum 42 characters per line, maximum 19.92 characters/second. V1 size and modification timestamps were verified unchanged.

Evidence is retained in ../qc/: final_qc.json, final_offcenter_motion.json, uncompressed_motion_diagnosis.json, final_pts_validation.json, delivered_srt_validation.json, final_review.jpg. Small diagnostic tests reused final-render clips where possible; no additional full proxy or full final render was required.
''')
for name in ['hia_v2.py','hia_v2_delivery_check.py','hia_v2_motion_diagnose.py','hia_v2_raw_motion.py','hia_v2_motion_roi.py','hia_v2_finish.py']:
    m.shutil.copy2(name,m.W/name)
files=[]
for p in [m.F/'HIA_CHICAGO_V2.mp4',m.F/'HIA_CHICAGO_V2.srt',report]:
    with p.open('rb') as f: digest=m.hashlib.file_digest(f,'sha256').hexdigest()
    files.append({'path':str(p),'bytes':p.stat().st_size,'sha256':digest})
m.save(m.F/'DELIVERY_MANIFEST.json',files)
print(m.json.dumps(files,indent=2))
print(m.json.dumps(m.load(m.W/'state.json')))
