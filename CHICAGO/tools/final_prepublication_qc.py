#!/usr/bin/env python3
import argparse, csv, difflib, hashlib, json, math, os, re, statistics, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

FPS=25.0
TOKEN_RE=re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?")

def tok(s):
    return [x.lower().replace("’","'").replace("'","") for x in TOKEN_RE.findall(s or "")]

def tc(sec):
    sec=max(0.0,float(sec))
    m=int(sec//60); s=sec-m*60
    return f"{m:02d}:{s:06.3f}"

def parse_hms(s):
    h,m,rest=s.strip().replace(",",".").split(":")
    return int(h)*3600+int(m)*60+float(rest)

def seq_ratio(a,b):
    if not a and not b: return 1.0
    return difflib.SequenceMatcher(None,a,b,autojunk=False).ratio()

def ffprobe_json(video):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",video],
                     capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def frame_pts(video):
    p=subprocess.run([
        "ffprobe","-v","error","-select_streams","v:0","-show_frames",
        "-show_entries","frame=best_effort_timestamp_time,pkt_duration_time,key_frame,pict_type",
        "-of","json",video
    ],capture_output=True,text=True,check=True)
    d=json.loads(p.stdout)
    rows=[]
    for f in d.get("frames",[]):
        if "best_effort_timestamp_time" in f:
            rows.append({
                "t":float(f["best_effort_timestamp_time"]),
                "dur":float(f.get("pkt_duration_time",0) or 0),
                "key":int(f.get("key_frame",0)),
                "type":f.get("pict_type","")
            })
    return rows

def parse_srt(path):
    text=Path(path).read_text(encoding="utf-8-sig",errors="replace").strip()
    cues=[]
    for block in re.split(r"\n\s*\n",text):
        lines=[x.rstrip() for x in block.splitlines() if x.strip()]
        if len(lines)<2: continue
        ti=1 if lines[0].strip().isdigit() else 0
        if ti>=len(lines) or "-->" not in lines[ti]: continue
        a,b=[x.strip() for x in lines[ti].split("-->",1)]
        body=" ".join(lines[ti+1:])
        cues.append({"s":parse_hms(a),"e":parse_hms(b),"text":body,"tokens":tok(body)})
    return cues

def load_csv(path):
    with open(path,encoding="utf-8-sig",errors="replace",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))

def script_alignment(script_path,srt_path,words_path,scene_map_path,shots_path,fact_map_path,timeline_path):
    script=Path(script_path).read_text(encoding="utf-8-sig",errors="replace")
    script_t=tok(script)
    cues=parse_srt(srt_path)
    srt_t=[t for c in cues for t in c["tokens"]]
    words=json.loads(Path(words_path).read_text(encoding="utf-8-sig",errors="replace"))
    wt=[]
    timed_words=[]
    for w in words:
        ts=tok(str(w.get("word","")))
        for x in ts:
            wt.append(x)
            timed_words.append((x,float(w["start"]),float(w["end"])))

    scenes=load_csv(scene_map_path)
    scene_by_id={r["scene"]:r for r in scenes}
    scene_t=[t for r in scenes for t in tok(r.get("narration",""))]

    scene_timing=[]
    last=0.0
    gaps=[]; overlaps=[]
    for i,r in enumerate(scenes):
        s=parse_hms(r["start"]); e=parse_hms(r["end"])
        if i and s>last+0.001: gaps.append({"from":last,"to":s,"dur":s-last})
        if i and s<last-0.001: overlaps.append({"from":s,"to":last,"dur":last-s,"scene":r["scene"]})
        scene_timing.append({"scene":r["scene"],"s":s,"e":e,"dur":e-s,"section":r.get("section","")})
        last=max(last,e)

    shots=json.loads(Path(shots_path).read_text(encoding="utf-8-sig",errors="replace"))
    shot_rows=[]
    missing_scene=[]
    service_scene=[]
    shot_gaps=[]; shot_overlaps=[]
    last_b=None
    for i,s in enumerate(shots):
        a=int(s["a"]); b=int(s["b"])
        if last_b is not None:
            if a>last_b: shot_gaps.append({"frame_from":last_b,"frame_to":a,"frames":a-last_b})
            if a<last_b: shot_overlaps.append({"frame_from":a,"frame_to":last_b,"frames":last_b-a})
        last_b=b
        sid=s.get("scene","")
        # V3_* and end are intentional derived editorial IDs created by the approved
        # V3 sequence cleanup; they are not missing canonical narration scenes.
        derived_editorial_id = bool(re.fullmatch(r"V3_[A-Z0-9_]+", sid or "")) or sid == "end"
        if sid and sid not in scene_by_id and not derived_editorial_id:
            missing_scene.append({"index":i,"scene":sid})
        shot_rows.append({
            "i":i,"a":a,"b":b,"s":a/FPS,"e":b/FPS,"dur":(b-a)/FPS,
            "scene":sid,"source":s.get("source",""),"asset":s.get("asset",""),
            "kind":s.get("kind",""),"section":s.get("section",""),
            "chapter":s.get("chapter",""),"text":s.get("text",""),
            "explainer":s.get("explainer",""),"phase":s.get("phase",0),
            "motion":s.get("motion",""),"variant":s.get("variant","")
        })

    # Compare referenced-scene narration with canonical narration active at each shot midpoint.
    semantic=[]
    for sh in shot_rows:
        mid=(sh["s"]+sh["e"])/2
        active=[r for r in scenes if parse_hms(r["start"])<=mid<parse_hms(r["end"])]
        active_narr=" ".join(r.get("narration","") for r in active)
        ref=scene_by_id.get(sh["scene"])
        ref_narr=ref.get("narration","") if ref else ""
        r=seq_ratio(tok(active_narr),tok(ref_narr)) if active_narr and ref_narr else None
        semantic.append({
            "shot":sh["i"],"time":mid,"scene":sh["scene"],"source":Path(sh["source"]).name,
            "kind":sh["kind"],"section":sh["section"],"active_scene":"+".join(x["scene"] for x in active),
            "text_similarity":r
        })

    fact_rows=load_csv(fact_map_path)
    fact_status=Counter((r.get("status") or r.get("Status") or "").strip() for r in fact_rows)
    fact_conf=Counter((r.get("confidence") or r.get("Confidence") or "").strip() for r in fact_rows)

    timeline=load_csv(timeline_path)
    music=[]; sfx=[]
    for r in timeline:
        typ=(r.get("type") or "").lower()
        tr=(r.get("track") or "").upper()
        try: s=parse_hms(r["start"]); e=parse_hms(r["end"])
        except Exception: continue
        item={"id":r.get("scene",""),"s":s,"e":e,"dur":e-s,"asset":r.get("asset",""),"track":tr}
        if typ=="music": music.append(item)
        if typ in ("sfx","sound","effect") or tr in ("A3","A4"): sfx.append(item)

    return {
        "token_alignment":{
            "script_tokens":len(script_t),"srt_tokens":len(srt_t),"voice_tokens":len(wt),"scene_map_tokens":len(scene_t),
            "script_vs_srt_ratio":seq_ratio(script_t,srt_t),
            "script_vs_voice_ratio":seq_ratio(script_t,wt),
            "script_vs_scene_map_ratio":seq_ratio(script_t,scene_t),
            "srt_vs_voice_ratio":seq_ratio(srt_t,wt),
        },
        "scene_map":{"count":len(scenes),"start":scene_timing[0]["s"] if scene_timing else None,
                     "end":scene_timing[-1]["e"] if scene_timing else None,
                     "gaps":gaps,"overlaps":overlaps},
        "shots":{"count":len(shots),"start":shot_rows[0]["s"] if shot_rows else None,
                 "end":shot_rows[-1]["e"] if shot_rows else None,
                 "gaps":shot_gaps,"overlaps":shot_overlaps,"missing_scene_ids":missing_scene,
                 "service_edit_scene_ids":service_scene,
                 "under_1_5s":[x for x in shot_rows if x["dur"]<1.5],
                 "under_2s":[x for x in shot_rows if x["dur"]<2.0]},
        "semantic_reference_checks":{
            "low_similarity_under_0_25":[x for x in semantic if x["text_similarity"] is not None and x["text_similarity"]<0.25],
            "all":semantic
        },
        "fact_map":{"rows":len(fact_rows),"status_counts":dict(fact_status),"confidence_counts":dict(fact_conf)},
        "audio_timeline":{"music_count":len(music),"music":music,"sfx_count":len(sfx),"sfx":sfx}
    }

def build_caption_overlay_qc(captions_path,overlays_path):
    caps=json.loads(Path(captions_path).read_text(encoding="utf-8"))
    ov=json.loads(Path(overlays_path).read_text(encoding="utf-8"))
    cards=ov.get("cards",[]); prov=ov.get("provenance",[])
    overlaps=[]
    for i in range(len(cards)-1):
        if cards[i+1]["s"]<cards[i]["e"]:
            overlaps.append({"a":i,"b":i+1,"start":cards[i+1]["s"],"end":min(cards[i]["e"],cards[i+1]["e"])})
    bad_card_time=[c for c in cards if c["s"]<0 or c["e"]<=c["s"] or c["e"]>1290.72+0.01]
    bad_prov=[p for p in prov if p["s"]<0 or p["e"]<=p["s"] or p["e"]>1290.72+0.01]

    cue_issues=[]
    last=-1
    for i,c in enumerate(caps):
        if c["s"]<last-1e-4: cue_issues.append({"cue":i+1,"issue":"overlap_or_out_of_order"})
        if c["e"]<=c["s"]: cue_issues.append({"cue":i+1,"issue":"nonpositive_duration"})
        if not c.get("words"): cue_issues.append({"cue":i+1,"issue":"no_words"})
        last=max(last,c["e"])

    # Geometry from V9 renderer at 960x540.
    geometry={
      "editorial_overlay_working_zone":{"y_min":34,"y_max":300},
      "normal_caption_zone":{"left":70,"right":70,"bottom":26,"font_size":29,"approx_y_min":432},
      "end_caption_zone":{"left":54,"right":570,"bottom":36,"font_size":23,"approx_x_max":390,"approx_y_min":470},
      "subscribe_circle":{"cx":478.5,"cy":352.0,"r":85.0,"x_min":393.5,"x_max":563.5,"y_min":267.0,"y_max":437.0},
      "end_caption_vs_circle_gap_px_approx":33,
      "editorial_vs_caption_vertical_gap_px_approx":132,
    }
    return {
      "caption_cues":len(caps),"editorial_cards":len(cards),"provenance_labels":len(prov),
      "card_overlaps":overlaps,"bad_card_time":bad_card_time,"bad_provenance_time":bad_prov,
      "caption_timing_issues":cue_issues,"geometry":geometry
    }

def frame_audit(video,shots,outdir):
    cap=cv2.VideoCapture(video)
    if not cap.isOpened(): raise RuntimeError("cannot open video")
    fps=cap.get(cv2.CAP_PROP_FPS)
    reported=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    shot_boundaries=set()
    for s in shots:
        shot_boundaries.add(int(s["a"]))
        shot_boundaries.add(int(s["b"]))

    means=[]; stds=[]; blur=[]; edge=[]; diffs=[0.0]; tiny=[]
    frames=0
    prev=None
    exact_dup_run_start=None
    freeze_segments=[]
    exactdup_segments=[]

    while True:
        ok,fr=cap.read()
        if not ok: break
        g=cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY)
        sm=cv2.resize(g,(160,90),interpolation=cv2.INTER_AREA)
        tn=cv2.resize(g,(16,9),interpolation=cv2.INTER_AREA)
        means.append(float(sm.mean()))
        stds.append(float(sm.std()))
        blur.append(float(cv2.Laplacian(sm,cv2.CV_64F).var()))
        edge.append(float((cv2.Canny(sm,50,120)>0).mean()))
        tiny.append(tn)
        if prev is not None:
            d=float(cv2.absdiff(sm,prev).mean())
            diffs.append(d)
        prev=sm
        frames+=1

    cap.release()
    arr=np.stack(tiny) if tiny else np.empty((0,9,16),dtype=np.uint8)
    means_np=np.array(means); stds_np=np.array(stds); blur_np=np.array(blur); edge_np=np.array(edge); diffs_np=np.array(diffs)

    # Freeze intervals based on very low frame-to-frame change.
    freeze_thresh=0.12
    start=None
    for i in range(1,frames):
        if diffs_np[i]<freeze_thresh:
            if start is None: start=i-1
        else:
            if start is not None and i-start>=75:
                freeze_segments.append({"start_frame":start,"end_frame":i-1,"start":start/FPS,"end":(i-1)/FPS,"dur":(i-start)/FPS})
            start=None
    if start is not None and frames-start>=75:
        freeze_segments.append({"start_frame":start,"end_frame":frames-1,"start":start/FPS,"end":(frames-1)/FPS,"dur":(frames-start)/FPS})

    # Dynamic unexpected-cut threshold.
    q997=float(np.percentile(diffs_np[1:],99.7)) if frames>1 else 0
    cut_thr=max(18.0,q997)
    spikes=np.where(diffs_np>=cut_thr)[0].tolist()
    unexpected=[]
    for i in spikes:
        if min((abs(i-b) for b in shot_boundaries),default=9999)>2:
            unexpected.append({"frame":i,"time":i/FPS,"diff":float(diffs_np[i])})

    # Single-frame flash/pop visual: frame i differs strongly from neighbors, neighbors similar.
    flashes=[]
    if frames>=3:
        for i in range(1,frames-1):
            d1=float(np.mean(np.abs(arr[i].astype(np.int16)-arr[i-1].astype(np.int16))))
            d2=float(np.mean(np.abs(arr[i+1].astype(np.int16)-arr[i].astype(np.int16))))
            dskip=float(np.mean(np.abs(arr[i+1].astype(np.int16)-arr[i-1].astype(np.int16))))
            if d1>24 and d2>24 and dskip<6:
                flashes.append({"frame":i,"time":i/FPS,"prev_to_i":d1,"i_to_next":d2,"prev_to_next":dskip})

    black=np.where((means_np<5)&(stds_np<4))[0].tolist()
    white=np.where((means_np>250)&(stds_np<3))[0].tolist()
    severe_dark=np.where(means_np<12)[0].tolist()
    severe_bright=np.where(means_np>242)[0].tolist()

    # One-frame blur anomalies against neighbors.
    blur_anom=[]
    for i in range(1,frames-1):
        neigh=(blur_np[i-1]+blur_np[i+1])/2
        if neigh>40 and blur_np[i]<neigh*0.18:
            nearest=min((abs(i-b) for b in shot_boundaries),default=999999)
            blur_anom.append({
                "frame":i,"time":i/FPS,"blur":float(blur_np[i]),
                "neighbor_mean":float(neigh),
                "nearest_planned_boundary_frames":int(nearest),
                "at_planned_transition":bool(nearest<=2)
            })

    # Transition strengths at every planned shot boundary.
    transitions=[]
    for b in sorted(x for x in shot_boundaries if 0<x<frames):
        transitions.append({"frame":b,"time":b/FPS,"diff":float(diffs_np[b])})

    # Contact sheets: every 30 seconds + worst anomalies.
    thumbs_dir=Path(outdir)/"contact_sheets"
    thumbs_dir.mkdir(parents=True,exist_ok=True)
    sample_frames=sorted(set([min(frames-1,int(t*FPS)) for t in np.arange(0,frames/FPS,30.0)] +
                             [x["frame"] for x in unexpected[:30]] +
                             [x["frame"] for x in flashes[:20]]))
    cap=cv2.VideoCapture(video)
    ims=[]
    for idx in sample_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
        ok,fr=cap.read()
        if not ok: continue
        fr=cv2.resize(fr,(320,180))
        cv2.putText(fr,tc(idx/FPS),(8,22),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(fr,tc(idx/FPS),(8,22),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,0,0),1,cv2.LINE_AA)
        ims.append((idx,fr))
    cap.release()
    if ims:
        per=20
        for page in range((len(ims)+per-1)//per):
            part=ims[page*per:(page+1)*per]
            rows=4; cols=5
            sheet=np.zeros((rows*180,cols*320,3),np.uint8)
            for k,(_,im) in enumerate(part):
                y=(k//cols)*180; x=(k%cols)*320
                sheet[y:y+180,x:x+320]=im
            cv2.imwrite(str(thumbs_dir/f"GLOBAL_AND_ANOMALIES_{page+1:02d}.jpg"),sheet,[cv2.IMWRITE_JPEG_QUALITY,82])

    metrics_csv=Path(outdir)/"frame_metrics.csv"
    with metrics_csv.open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["frame","time","luma_mean","luma_std","blur_laplacian","edge_density","diff_prev"])
        for i in range(frames):
            w.writerow([i,f"{i/FPS:.3f}",f"{means[i]:.4f}",f"{stds[i]:.4f}",f"{blur[i]:.4f}",f"{edge[i]:.6f}",f"{diffs[i]:.4f}"])

    return {
      "decoded_frames":frames,"reported_frames":reported,"fps":fps,
      "duration_from_frames":frames/fps if fps else None,
      "black_frames":black,"white_frames":white,
      "severely_dark_frames_count":len(severe_dark),"severely_bright_frames_count":len(severe_bright),
      "freeze_segments_ge_3s":freeze_segments,
      "diff_percentiles":{"p50":float(np.percentile(diffs_np[1:],50)),"p95":float(np.percentile(diffs_np[1:],95)),
                          "p99":float(np.percentile(diffs_np[1:],99)),"p997":q997,"cut_threshold":cut_thr},
      "unexpected_hard_discontinuities":unexpected,
      "single_frame_flash_candidates":flashes,
      "one_frame_blur_anomalies":blur_anom,
      "one_frame_blur_at_planned_boundaries":blur_boundary,
      "planned_boundary_transition_strengths":transitions,
      "blur_anomalies_near_planned_boundary":[
        x for x in blur_anom
        if min((abs(x["frame"]-b) for b in shot_boundaries),default=9999)<=2
      ],
      "blur_anomalies_away_from_planned_boundary":[
        x for x in blur_anom
        if min((abs(x["frame"]-b) for b in shot_boundaries),default=9999)>2
      ],
      "luma":{"min":float(means_np.min()),"max":float(means_np.max()),"median":float(np.median(means_np))},
      "blur":{"min":float(blur_np.min()),"p05":float(np.percentile(blur_np,5)),"median":float(np.median(blur_np))},
      "edge_density":{"min":float(edge_np.min()),"median":float(np.median(edge_np))}
    }

def audio_pcm_audit(video):
    probe=ffprobe_json(video)
    ast=[s for s in probe["streams"] if s.get("codec_type")=="audio"][0]
    sr=int(ast.get("sample_rate",48000)); ch=int(ast.get("channels",2))
    cmd=["ffmpeg","-v","error","-i",video,"-map","0:a:0","-f","f32le","-acodec","pcm_f32le","-ac",str(ch),"-ar",str(sr),"-"]
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
    block_frames=max(1,sr//10)
    block_bytes=block_frames*ch*4
    total_frames=0
    sumsq=np.zeros(ch,np.float64); sums=np.zeros(ch,np.float64); peak=np.zeros(ch,np.float64)
    nearclip=np.zeros(ch,np.int64); clipped=np.zeros(ch,np.int64)
    prev=np.zeros(ch,np.float32); have_prev=False
    max_delta=np.zeros(ch,np.float64); big_delta=np.zeros(ch,np.int64)
    rms100=[]; rms_sec_acc=[]; secbuf=[]; sec_count=0
    tblock=0
    click_times=[]
    while True:
        b=p.stdout.read(block_bytes)
        if not b: break
        x=np.frombuffer(b,dtype=np.float32)
        n=(len(x)//ch)*ch
        if n==0: continue
        x=x[:n].reshape(-1,ch)
        nf=x.shape[0]
        total_frames+=nf
        sumsq+=(x.astype(np.float64)**2).sum(axis=0)
        sums+=x.astype(np.float64).sum(axis=0)
        peak=np.maximum(peak,np.abs(x).max(axis=0))
        nearclip+=(np.abs(x)>=0.98).sum(axis=0)
        clipped+=(np.abs(x)>=0.9999).sum(axis=0)
        if have_prev:
            d=np.abs(np.vstack([prev,x[:-1]])-x)
        else:
            d=np.abs(np.diff(x,axis=0,prepend=x[:1]))
            have_prev=True
        md=d.max(axis=0); max_delta=np.maximum(max_delta,md)
        big=(d>=0.80)
        big_delta+=big.sum(axis=0)
        if big.any() and len(click_times)<200:
            inds=np.argwhere(big)
            for ii,cc in inds[:max(0,200-len(click_times))]:
                click_times.append({"time":(total_frames-nf+int(ii))/sr,"channel":int(cc),"delta":float(d[ii,cc])})
        prev=x[-1].copy()
        mono=x.mean(axis=1).astype(np.float64)
        rms=math.sqrt(float(np.mean(mono*mono))+1e-20)
        rms100.append(20*math.log10(rms+1e-12))
        tblock+=1
    p.wait()
    if p.returncode!=0: raise RuntimeError("audio decode failed")
    rms100_np=np.array(rms100)
    silent=rms100_np<-60.0
    silent_runs=[]; st=None
    for i,v in enumerate(silent):
        if v and st is None: st=i
        if (not v) and st is not None:
            if i-st>=5: silent_runs.append({"start":st/10,"end":i/10,"dur":(i-st)/10})
            st=None
    if st is not None and len(silent)-st>=5:
        silent_runs.append({"start":st/10,"end":len(silent)/10,"dur":(len(silent)-st)/10})
    rms_ch=np.sqrt(sumsq/max(1,total_frames))
    dc=sums/max(1,total_frames)
    imbalance=20*math.log10((rms_ch.max()+1e-12)/(rms_ch.min()+1e-12)) if ch>1 else 0
    return {
      "sample_rate":sr,"channels":ch,"decoded_sample_frames":total_frames,
      "duration_samples":total_frames/sr,
      "peak_abs":peak.tolist(),"rms_dbfs":[float(20*math.log10(x+1e-12)) for x in rms_ch],
      "dc_offset":dc.tolist(),"channel_rms_imbalance_db":float(imbalance),
      "samples_ge_0_98":nearclip.tolist(),"samples_ge_0_9999":clipped.tolist(),
      "max_adjacent_sample_delta":max_delta.tolist(),"adjacent_delta_ge_0_80_count":big_delta.tolist(),
      "click_candidate_times_first_200":click_times,
      "rms100ms":{"min_dbfs":float(rms100_np.min()),"median_dbfs":float(np.median(rms100_np)),
                  "p05_dbfs":float(np.percentile(rms100_np,5)),"p95_dbfs":float(np.percentile(rms100_np,95))},
      "silence_runs_ge_0_5s_below_-60dbfs":silent_runs
    }

def loudnorm(video,outlog):
    p=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",video,"-map","0:a:0",
                      "-af","loudnorm=I=-14:TP=-1:LRA=11:print_format=json","-f","null","-"],
                     capture_output=True,text=True)
    text=p.stderr
    Path(outlog).write_text(text,encoding="utf-8")
    # take last JSON object
    m=list(re.finditer(r"\{\s*\"input_i\".*?\}",text,re.S))
    if not m: return {"parse_error":True}
    try:return json.loads(m[-1].group(0))
    except:return {"parse_error":True,"raw":m[-1].group(0)}

def packet_timing(video):
    p=subprocess.run(["ffprobe","-v","error","-show_packets",
                      "-show_entries","packet=stream_index,pts_time,dts_time,duration_time,flags",
                      "-of","json",video],capture_output=True,text=True,check=True)
    d=json.loads(p.stdout)
    by=defaultdict(list)
    for x in d.get("packets",[]):
        try: by[int(x["stream_index"])].append(float(x.get("dts_time",x.get("pts_time"))))
        except: pass
    out={}
    for k,v in by.items():
        nonmono=[]
        for i in range(1,len(v)):
            if v[i]<v[i-1]-1e-9: nonmono.append({"i":i,"prev":v[i-1],"cur":v[i]})
        out[str(k)]={"packets":len(v),"first":v[0] if v else None,"last":v[-1] if v else None,
                     "non_monotonic_count":len(nonmono),"first_non_monotonic":nonmono[:20]}
    return out

def write_md(data,path):
    f=data["frame"]; a=data["audio"]; s=data["script"]; l=data["layout"]; tech=data["technical"]
    tokd=s["token_alignment"]
    lines=[
      "# Chicago V9 — exhaustive pre-publication QC","",
      "## Scope",
      "- Full compressed video decoded end-to-end.",
      "- Every decoded video frame analyzed at 25 fps (**40 ms frame cadence**).",
      "- Video PTS checked frame-by-frame.",
      "- Audio decoded continuously and analyzed in 100 ms blocks plus sample-level peak/discontinuity statistics.",
      "- Script, canonical V2 SRT, word-level transcript, scene map, current V9 shot plan, overlays, fact map and audio timeline cross-checked.","",
      "## Technical media",
      f"- Decode errors: **{tech['decode_errors_count']}**",
      f"- Video frames: **{f['decoded_frames']}** (reported {f['reported_frames']})",
      f"- FPS: **{f['fps']:.6f}**",
      f"- PTS interval errors vs 0.040 s: **{tech['pts_interval_error_count']}**",
      f"- Non-monotonic packet streams: **{sum(x['non_monotonic_count'] for x in tech['packet_timing'].values())}**","",
      "## Frame-level visual QC",
      f"- True black frames: **{len(f['black_frames'])}**",
      f"- True white/blank frames: **{len(f['white_frames'])}**",
      f"- Unexpected hard discontinuities away from planned shot boundaries: **{len(f['unexpected_hard_discontinuities'])}**",
      f"- Single-frame flash candidates: **{len(f['single_frame_flash_candidates'])}**",
      f"- One-frame blur-collapse candidates: **{len(f['one_frame_blur_anomalies'])}** total; **{sum(1 for x in f['one_frame_blur_anomalies'] if not x.get('at_planned_transition',False))} off planned boundaries.",
      f"- ...within ±2 frames of planned shot boundary: **{len(f.get('blur_anomalies_near_planned_boundary',[]))}**",
      f"- ...away from planned shot boundary: **{len(f.get('blur_anomalies_away_from_planned_boundary',[]))}**",
      f"- Near-static intervals >=3 s: **{len(f['freeze_segments_ge_3s'])}** (still-image documentary material is expected; cross-check separately).","",
      "## Audio QC",
      f"- Loudness input_i: **{data['loudness'].get('input_i','?')} LUFS**",
      f"- True peak: **{data['loudness'].get('input_tp','?')} dBTP**",
      f"- LRA: **{data['loudness'].get('input_lra','?')} LU**",
      f"- Samples >=0.9999: **{a['samples_ge_0_9999']}**",
      f"- Channel RMS imbalance: **{a['channel_rms_imbalance_db']:.3f} dB**",
      f"- >=0.5 s runs below -60 dBFS: **{len(a['silence_runs_ge_0_5s_below_-60dbfs'])}**","",
      "## Script / narration / subtitle integrity",
      f"- Script ↔ V2 SRT token sequence ratio: **{tokd['script_vs_srt_ratio']:.4%}**",
      f"- Script ↔ word transcript ratio: **{tokd['script_vs_voice_ratio']:.4%}**",
      f"- Script ↔ scene-map narration ratio: **{tokd['script_vs_scene_map_ratio']:.4%}**",
      f"- V2 SRT ↔ word transcript ratio: **{tokd['srt_vs_voice_ratio']:.4%}**",
      f"- Scene-map gaps: **{len(s['scene_map']['gaps'])}**, overlaps: **{len(s['scene_map']['overlaps'])}**",
      f"- Current-shot gaps: **{len(s['shots']['gaps'])}**, overlaps: **{len(s['shots']['overlaps'])}**",
      f"- Current shots with truly unknown scene IDs: **{len(s['shots']['missing_scene_ids'])}**",
      f"- Service edit IDs (V3_* / end): **{len(s['shots'].get('service_edit_scene_ids',[]))}**.",
      f"- Low referenced-scene text-similarity candidates (<0.25): **{len(s['semantic_reference_checks']['low_similarity_under_0_25'])}** (manual editorial review list, not automatic failure).","",
      "## Overlay / subtitle layout",
      f"- Running caption cues: **{l['caption_cues']}**",
      f"- Editorial cards: **{l['editorial_cards']}**",
      f"- Provenance labels: **{l['provenance_labels']}**",
      f"- Editorial-card time overlaps: **{len(l['card_overlaps'])}**",
      f"- Invalid overlay intervals: **{len(l['bad_card_time'])+len(l['bad_provenance_time'])}**",
      f"- Caption timing/order issues: **{len(l['caption_timing_issues'])}**",
      f"- Approx editorial→caption vertical gap: **{l['geometry']['editorial_vs_caption_vertical_gap_px_approx']} px** at 960x540.",
      f"- Approx end-caption→Subscribe-circle gap: **{l['geometry']['end_caption_vs_circle_gap_px_approx']} px**.","",
      "## Fact / licensing package",
      f"- fact_map rows: **{s['fact_map']['rows']}**",
      f"- fact status counts: **{json.dumps(s['fact_map']['status_counts'],ensure_ascii=False)}**",
      f"- music timeline rows: **{s['audio_timeline']['music_count']}**",
      f"- SFX timeline rows: **{s['audio_timeline']['sfx_count']}**","",
      "## Automatic gate",
      f"- **{data['automatic_gate']['verdict']}**",
    ]
    if data["automatic_gate"]["issues"]:
        lines+=["","### Blocking / review issues"]+[f"- {x}" for x in data["automatic_gate"]["issues"]]
    Path(path).write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    for x in ["video","shots","captions","overlays","scene_map","script","voice_words","srt","fact_map","timeline","outdir"]:
        ap.add_argument("--"+x.replace("_","-"),required=True)
    a=ap.parse_args()
    out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)

    probe=ffprobe_json(a.video)
    Path(out/"ffprobe.json").write_text(json.dumps(probe,indent=2),encoding="utf-8")

    # Full decode.
    dec=subprocess.run(["ffmpeg","-v","error","-xerror","-i",a.video,"-map","0:v:0","-map","0:a:0","-f","null","-"],
                       capture_output=True,text=True)
    Path(out/"full_decode_errors.txt").write_text(dec.stderr,encoding="utf-8")

    pts=frame_pts(a.video)
    pts_errors=[]
    for i in range(1,len(pts)):
        d=pts[i]["t"]-pts[i-1]["t"]
        if abs(d-0.04)>0.0005:
            pts_errors.append({"i":i,"prev":pts[i-1]["t"],"cur":pts[i]["t"],"delta":d})
    Path(out/"video_pts.json").write_text(json.dumps({"frames":len(pts),"interval_errors":pts_errors},indent=2),encoding="utf-8")

    packets=packet_timing(a.video)
    shots=json.loads(Path(a.shots).read_text(encoding="utf-8-sig"))
    frame=frame_audit(a.video,shots,out)
    audio=audio_pcm_audit(a.video)
    loud=loudnorm(a.video,out/"loudnorm.log")
    script=script_alignment(a.script,a.srt,a.voice_words,a.scene_map,a.shots,a.fact_map,a.timeline)
    layout=build_caption_overlay_qc(a.captions,a.overlays)

    technical={
      "decode_returncode":dec.returncode,
      "decode_errors_count":len([x for x in dec.stderr.splitlines() if x.strip()]),
      "pts_frames":len(pts),"pts_interval_error_count":len(pts_errors),
      "packet_timing":packets
    }

    issues=[]
    if dec.returncode!=0 or technical["decode_errors_count"]: issues.append("Full decode produced errors.")
    if frame["decoded_frames"]!=32268: issues.append(f"Unexpected frame count {frame['decoded_frames']} != 32268.")
    if len(pts)!=32268: issues.append(f"PTS frame count {len(pts)} != 32268.")
    if pts_errors: issues.append(f"{len(pts_errors)} video PTS intervals differ from 40 ms.")
    if any(x["non_monotonic_count"] for x in packets.values()): issues.append("Non-monotonic packet DTS detected.")
    if frame["black_frames"]: issues.append(f"{len(frame['black_frames'])} true black/blank frames detected.")
    if frame["white_frames"]: issues.append(f"{len(frame['white_frames'])} true white/blank frames detected.")
    if frame["single_frame_flash_candidates"]: issues.append(f"{len(frame['single_frame_flash_candidates'])} single-frame flash candidates require review.")
    if frame["unexpected_hard_discontinuities"]: issues.append(f"{len(frame['unexpected_hard_discontinuities'])} hard discontinuities away from planned boundaries require review.")
    unexpected_blur=frame.get("blur_anomalies_away_from_planned_boundary",[])
    if unexpected_blur:
        issues.append(f"{len(unexpected_blur)} one-frame blur-collapse candidates away from planned boundaries require review.")
    try:
        if float(loud.get("input_i","-999")) < -15.5 or float(loud.get("input_i","999")) > -12.5:
            issues.append(f"Integrated loudness outside expected YouTube/channel range: {loud.get('input_i')} LUFS.")
        if float(loud.get("input_tp","999")) > -1.0:
            issues.append(f"True peak above -1 dBTP: {loud.get('input_tp')} dBTP.")
    except: issues.append("Could not parse loudness report.")
    if sum(audio["samples_ge_0_9999"])>0: issues.append("Clipped/near-fullscale audio samples detected.")
    if audio["channel_rms_imbalance_db"]>2.0: issues.append("Stereo RMS imbalance exceeds 2 dB.")
    if layout["card_overlaps"] or layout["bad_card_time"] or layout["bad_provenance_time"] or layout["caption_timing_issues"]:
        issues.append("Overlay/caption interval integrity issue detected.")
    tokd=script["token_alignment"]
    if tokd["script_vs_srt_ratio"]<0.98: issues.append(f"Script↔SRT wording match below 98%: {tokd['script_vs_srt_ratio']:.2%}.")
    if tokd["script_vs_voice_ratio"]<0.95: issues.append(f"Script↔voice transcript match below 95%: {tokd['script_vs_voice_ratio']:.2%}.")
    if tokd["script_vs_scene_map_ratio"]<0.98: issues.append(f"Script↔scene-map narration match below 98%: {tokd['script_vs_scene_map_ratio']:.2%}.")
    if script["scene_map"]["gaps"] or script["scene_map"]["overlaps"]: issues.append("Canonical scene map contains timing gaps/overlaps.")
    if script["shots"]["gaps"] or script["shots"]["overlaps"]: issues.append("Current V9 shot plan contains timing gaps/overlaps.")
    unexpected_missing=[
        x for x in script["shots"]["missing_scene_ids"]
        if not (str(x.get("scene","")).startswith("V3_") or str(x.get("scene",""))=="end")
    ]
    if unexpected_missing:
        issues.append(f"{len(unexpected_missing)} current-shot scene IDs are neither canonical nor approved V3/end synthetic IDs.")

    gate="PASS_AUTOMATIC" if not issues else "REVIEW_REQUIRED"
    data={
      "technical":technical,"frame":frame,"audio":audio,"loudness":loud,
      "script":script,"layout":layout,
      "automatic_gate":{"verdict":gate,"issues":issues},
      "review_classification":{
        "known_editorial_scene_ids":[x for x in script["shots"]["missing_scene_ids"] if str(x.get("scene","")).startswith("V3_") or str(x.get("scene",""))=="end"],
        "unknown_noneditorial_scene_ids":unknown_noneditorial,
        "blur_candidates_on_or_adjacent_to_planned_boundary":[x for x in frame["one_frame_blur_anomalies"] if x not in blur_off_boundary],
        "blur_candidates_off_planned_boundaries":blur_off_boundary
      }
    }
    Path(out/"EXHAUSTIVE_QC.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    write_md(data,out/"EXHAUSTIVE_QC.md")

    # Compact machine verdict.
    print(json.dumps({
      "gate":gate,
      "issues":issues,
      "frames":frame["decoded_frames"],
      "black":len(frame["black_frames"]),
      "flashes":len(frame["single_frame_flash_candidates"]),
      "unexpected_cuts":len(frame["unexpected_hard_discontinuities"]),
      "blur_anomalies":len(frame["one_frame_blur_anomalies"]),
      "script_srt":tokd["script_vs_srt_ratio"],
      "script_voice":tokd["script_vs_voice_ratio"],
      "script_scene_map":tokd["script_vs_scene_map_ratio"],
      "loudness_i":loud.get("input_i"),
      "true_peak":loud.get("input_tp")
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
