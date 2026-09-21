#!/usr/bin/env python3
import json,re,cv2,argparse
import numpy as np
from collections import Counter
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("--root",required=True)
a=ap.parse_args()
root=Path(a.root)

data=json.loads((root/"EXHAUSTIVE_QC.json").read_text())
shots=json.loads((root/"qc/V9_SHOTS.json").read_text())
video=str(root/"HIA_CHICAGO_V9_FIRST_EPISODE_END_SCREEN_REVIEW_960x540.mp4")

boundaries=sorted(set([int(s["a"]) for s in shots]+[int(s["b"]) for s in shots]))
def nearest_boundary(fr):
    b=min(boundaries,key=lambda x:abs(x-fr))
    return b,fr-b

blur=data["frame"]["one_frame_blur_anomalies"]
blur_rows=[]
cap=cv2.VideoCapture(video)
panels=[]
for n,x in enumerate(blur,1):
    fr=int(x["frame"])
    b,delta=nearest_boundary(fr)
    si=next((i for i,s in enumerate(shots) if int(s["a"])<=fr<int(s["b"])),None)
    shot=shots[si] if si is not None else {}
    row={**x,"nearest_boundary_frame":b,"boundary_delta_frames":delta,
         "active_shot_index":si,"scene":shot.get("scene",""),
         "source":Path(shot.get("source","")).name,
         "kind":shot.get("kind",""),"motion":shot.get("motion",""),
         "variant":shot.get("variant","")}
    blur_rows.append(row)
    trip=[]
    for ofs in (-1,0,1):
        idx=max(0,fr+ofs)
        cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
        ok,img=cap.read()
        if not ok: continue
        img=cv2.resize(img,(480,270))
        label=f"{(idx/25):.3f}s frame {idx} ({ofs:+d})"
        cv2.rectangle(img,(0,0),(480,34),(0,0,0),-1)
        cv2.putText(img,label,(8,23),cv2.FONT_HERSHEY_SIMPLEX,.53,(255,255,255),1,cv2.LINE_AA)
        trip.append(img)
    if len(trip)==3:
        panel=np.hstack(trip)
        cv2.putText(panel,f"Candidate {n}: {row['scene']} {row['source']} boundary_delta={delta}f",
                    (8,265),cv2.FONT_HERSHEY_SIMPLEX,.52,(0,255,255),1,cv2.LINE_AA)
        panels.append(panel)
cap.release()
if panels:
    sheet=np.vstack(panels)
    cv2.imwrite(str(root/"BLUR_CANDIDATES_TRIPTYCH.jpg"),sheet,[cv2.IMWRITE_JPEG_QUALITY,90])

missing=data["script"]["shots"]["missing_scene_ids"]
by_scene=Counter(x["scene"] for x in missing)
missing_rows=[]
for x in missing:
    i=x["index"]; s=shots[i]
    missing_rows.append({
      "shot":i,"start":int(s["a"])/25,"end":int(s["b"])/25,"scene":x["scene"],
      "source":Path(s.get("source","")).name,"kind":s.get("kind",""),
      "section":s.get("section",""),"chapter":s.get("chapter",""),
      "text":s.get("text",""),"explainer":s.get("explainer",""),
      "phase":s.get("phase",0),"motion":s.get("motion",""),"variant":s.get("variant","")
    })

low=data["script"]["semantic_reference_checks"]["low_similarity_under_0_25"]
low_by_scene=Counter(x["scene"] for x in low)
low_by_kind=Counter(x["kind"] for x in low)

audio=data["audio"]
sil=audio["silence_runs_ge_0_5s_below_-60dbfs"]
max_sil=max(sil,key=lambda x:x["dur"]) if sil else None

freeze_text=(root/"INDEPENDENT_FFMPEG_DIAGNOSTICS.md").read_text()
freezes=[]; pending=[]
for line in freeze_text.splitlines():
    m=re.search(r"freeze_start:\s*([0-9.]+)",line)
    if m: pending.append(float(m.group(1)))
    m=re.search(r"freeze_end:\s*([0-9.]+)",line)
    if m and pending:
        st=pending.pop(0); en=float(m.group(1)); freezes.append((st,en,en-st))
freeze_class=[]
for st,en,dur in freezes:
    mid=(st+en)/2; fr=int(mid*25)
    si=next((i for i,s in enumerate(shots) if int(s["a"])<=fr<int(s["b"])),None)
    s=shots[si] if si is not None else {}
    freeze_class.append({
      "start":st,"end":en,"dur":dur,"shot":si,"scene":s.get("scene",""),
      "source":Path(s.get("source","")).name,"kind":s.get("kind",""),
      "motion":s.get("motion",""),"variant":s.get("variant","")
    })

report={
  "blur_candidates":blur_rows,
  "unknown_scene_ids":{"count":len(missing_rows),"unique":dict(by_scene),"shots":missing_rows},
  "low_semantic_similarity":{"count":len(low),"by_scene":dict(low_by_scene),
                             "by_kind":dict(low_by_kind),"first_120":low[:120]},
  "audio":{"silence_runs_count":len(sil),"longest_silence":max_sil,
           "click_candidate_count":len(audio.get("click_candidate_times_first_200",[])),
           "max_adjacent_sample_delta":audio["max_adjacent_sample_delta"],
           "samples_ge_0_9999":audio["samples_ge_0_9999"],
           "channel_rms_imbalance_db":audio["channel_rms_imbalance_db"]},
  "freeze_events":freeze_class
}
(root/"TRIAGE.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))

lines=["# Chicago V9 exhaustive QC — candidate triage","",
       "## Blur-collapse candidates"]
for x in blur_rows:
    lines.append(f"- {x['time']:.3f}s / frame {x['frame']} — boundary delta {x['boundary_delta_frames']}f — "
                 f"shot {x['active_shot_index']} / {x['scene']} / {x['source']} / "
                 f"{x['kind']} / {x['motion']} / {x['variant']}")
lines+=["","## Unknown scene IDs",f"- Total: **{len(missing_rows)}**",
        f"- Unique IDs: {dict(by_scene)}",""]
for x in missing_rows:
    lines.append(f"- {x['start']:.2f}–{x['end']:.2f}s | shot {x['shot']} | {x['scene']} | "
                 f"{x['source']} | {x['kind']} | section={x['section']} | text={x['text']}")
lines+=["","## Semantic-reference low-similarity candidates",
        f"- Count: **{len(low)}**",f"- By kind: {dict(low_by_kind)}",
        f"- By referenced scene: {dict(low_by_scene)}","",
        "These are editorial-review candidates only; current sequence intentionally reuses/reorders evidence in places.",
        "","## Audio residual checks",
        f"- >0.5s sub--60dB block runs: **{len(sil)}**",
        f"- Longest: **{max_sil}**",
        f"- Click-candidate list size: **{len(audio.get('click_candidate_times_first_200',[]))}**",
        f"- Max adjacent sample delta: **{audio['max_adjacent_sample_delta']}**",
        f"- Samples >=0.9999: **{audio['samples_ge_0_9999']}**",
        f"- Stereo RMS imbalance: **{audio['channel_rms_imbalance_db']:.6f} dB**",
        "","## FFmpeg >=3s freeze events"]
for x in freeze_class:
    lines.append(f"- {x['start']:.2f}–{x['end']:.2f}s ({x['dur']:.2f}s) | "
                 f"shot {x['shot']} | {x['scene']} | {x['source']} | "
                 f"{x['kind']} | {x['motion']} / {x['variant']}")
(root/"TRIAGE.md").write_text("\n".join(lines)+"\n")
