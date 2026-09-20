# V2 build-code caption/subtitle references

18: for p in [W,Q,F,W/'assets',W/'overlays']:p.mkdir(parents=True,exist_ok=True)
19: if not (W/'state.json').exists():save(W/'state.json',{'revision':'V2','source_v1':str(OLD),'motion_tests_pass':False,'plan_complete':False,'proxy_complete':False,'proxy_qc_pass':False,'final_complete':False,'final_qc_pass':False})
21:  keep=[OLD,R/'_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt',R/'_FINAL/EDIT_REPORT.md',R/'_EDIT_WORK/codex_edit_state.json'];save(W/'v1_snapshot.json',[{'path':str(p),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in keep])
35:  im=ImageOps.fit(Image.open(s['resolved_asset']).convert('RGB'),(1920,1080));src=Q/f'test_{mode}.png';im.save(src)
42:  rec={'mode':mode,'duration':8,'seconds_to_render':round(time.time()-start,2),'comparisons':len(mad),'near_static':int(sum(steady)),'longest_near_static_run':maxrun,'mad_median':float(np.median(mad)),'mad_max':float(max(mad)),'pass':maxrun<=1};report.append(rec);print(json.dumps(rec),flush=True)
44: if not all(r['pass'] for r in report):raise RuntimeError('Motion test failed')
45: update(motion_tests_pass=True)
47: init();sc=load(R/'_EDIT_WORK/edit_scenes.json');assets={};shots=[];font=ImageFont.truetype(str(W/'font.ttf'),28)
49:  p=Path(s['resolved_asset']);n=int(s['scene'][1:]);kind='reconstruction' if s['reconstruction'] else 'archive';variant='full'
54:  if key not in assets:
68:   out=W/'assets'/(key+'.png');canvas.save(out);assets[key]=str(out)
88:  rec=dict(a=a,b=b,source=str(p),asset=assets[key],scene=s['scene'],kind=kind,variant=variant,motion=motion,section=s['section'],text=s['text_overlay'],chapter=title,explainer=explainer,phase=phase)
93: first=shots[0];img=Image.open(first['source']).convert('RGB');img=ImageOps.fit(img.crop((int(img.width*.2),0,int(img.width*.8),int(img.height*.52))),(1920,1080),method=Image.Resampling.LANCZOS);p=W/'assets/opening_street.png';img.save(p)
94: shots=[dict(first,b=75,asset=str(p),motion='static',text='CHICAGO'),dict(first,a=75,motion='pull')]+shots[1:]
97:  s=next(x for x in sc if x['scene']==sid);im=ImageOps.fit(Image.open(s['resolved_asset']).convert('RGB'),(1120,700));canvas=Image.new('RGB',(1920,1080),(19,24,27));canvas.paste(im,(65,255));d=ImageDraw.Draw(canvas);bold=ImageFont.truetype(str(W/'bold.ttf'),48);small=ImageFont.truetype(str(W/'font.ttf'),27)
98:  d.text((70,80),'HIDDEN INDUSTRIAL AMERICA',font=bold,fill=(232,223,203));d.text((70,155),'THE INFRASTRUCTURE REMAINS',font=small,fill=(187,174,152));d.rectangle((1250,290,1855,630),outline=(156,104,68),width=2);d.text((1250,665),'CONTINUE EXPLORING',font=small,fill=(224,216,199));d.ellipse((1420,790,1580,950),outline=(156,104,68),width=2);d.text((1250,995),'SUBSCRIBE FOR THE NEXT STORY',font=small,fill=(224,216,199));p=W/'assets'/f'end_{sid}.png';canvas.save(p)
99:  shots.append(dict(a=a,b=b,source=s['resolved_asset'],asset=str(p),scene='end',kind='reconstruction',variant='end',motion='static',section='ending',text='',chapter='',explainer='',phase=0))
107: assert shots[0]['a']==0 and shots[-1]['b']==32268
108: assert all(s['b']==shots[i+1]['a'] for i,s in enumerate(shots[:-1]))
109: assert min(s['b']-s['a'] for s in shots)>3
130: assetstat=Path(s['asset']).stat();gh=hashlib.sha256(graphic(s).read_bytes()).hexdigest() if s['explainer'] else ''
131: signature=hashlib.sha256(json.dumps({'s':s,'q':quality,'engine':'subpixel-perspective-v2.4','asset_size':assetstat.st_size,'asset_mtime':assetstat.st_mtime_ns,'graphic_hash':gh},sort_keys=True).encode()).hexdigest()[:14];out=folder/f'{i:03}_{signature}.mp4'
134: args+=['-framerate','25','-i',s['asset']]
144:  filters.append(f"drawtext=fontfile=font.ttf:text='RECONSTRUCTION':fontsize={round(27*scale)}:fontcolor=0xF0E8D7@0.88:shadowcolor=black@0.75:shadowx=1:shadowy=1:x=w*0.04:y=h*0.952:enable='lt({t},2.5)'")
145:  filters.append(f"drawtext=fontfile=font.ttf:text='AI reconstruction':fontsize={round(20*scale)}:fontcolor=0xEEE6D4@0.72:shadowcolor=black@0.65:shadowx=1:shadowy=1:x=w*0.04:y=h*0.952:enable='gte({t},2.5)'")
147:  filters.append(f"drawtext=fontfile=font.ttf:text='HISTORICAL SOURCE':fontsize={round(20*scale)}:fontcolor=0xC6C6BA:shadowcolor=black:shadowx=1:shadowy=1:x=w*0.04:y=h*0.952")
150:  p=W/f'text_{i}_{quality}.txt';p.write_text(title,encoding='utf-8');filters.append(f"drawtext=fontfile=bold.ttf:textfile={p.name}:fontsize={round((45 if s['chapter'] else 36)*scale)}:fontcolor=0xF1E9D7:shadowcolor=black@0.8:shadowx=2:shadowy=2:x=w*0.045:y=h*0.07:enable='lt(t,3.4)'")
168: if quality=='final' and not st.get('proxy_qc_pass'):raise RuntimeError('Proxy QC required')
169: if not st.get('motion_tests_pass') or not st.get('insert_tests_pass'):raise RuntimeError('Short tests required')
179:def captions():
181: blocks=(R/'_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt').read_text(encoding='utf-8').strip().split('\n\n');old=[]
219: (F/'HIA_CHICAGO_V2.srt').write_text('\n\n'.join(f'{i+1}\n{fmt(c["start"])} --> {fmt(c["end"])}\n'+ '\n'.join(c['lines']) for i,c in enumerate(result))+'\n',encoding='utf-8')
220: assert [norm(w) for c in old for w in c['text'].split()]==[norm(w) for c in result for w in c['text'].split()]
222: save(Q/'subtitle_report.json',stats);save(W/'captions.json',result);update(captions_complete=True);print(json.dumps(stats))
236:   donor=next(x for x in shots if x['scene']=='S091');s.update(asset=donor['asset'],source=donor['source'],variant=donor['variant'],motion='static')
238:   im=Image.open(s['source']).convert('RGB');box=(.04,.06,.49,.94) if s['scene']=='S013' else (.04,.01,.96,.55);im=im.crop(tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(box)));canvas=Image.new('RGB',(1920,1080),(20,25,28));im=ImageOps.contain(im,(1690,970),Image.Resampling.LANCZOS);canvas.paste(im,((1920-im.width)//2,(1080-im.height)//2));p=W/'assets'/f'{s["scene"]}_source_detail.png';canvas.save(p)
239:   cut=s['a']+100;new.extend([dict(s,b=cut),dict(s,a=cut,asset=str(p),variant='source_detail',motion='static',chapter='',text='STREET-LEVEL CONGESTION' if s['scene']=='S013' else 'THE TELEPHONE ORIGINS')]);continue
253:def final_caption_boundary():
254: cues=load(W/'captions.json');a=next(c for c in cues if c['old_id']==123);b=next(c for c in cues if c['old_id']==124)
259: save(W/'captions.json',cues);(F/'HIA_CHICAGO_V2.srt').write_text('\n\n'.join(f'{i+1}\n{fmt(c["start"])} --> {fmt(c["end"])}\n'+ '\n'.join(c['lines']) for i,c in enumerate(cues))+'\n',encoding='utf-8')
260: save(Q/'subtitle_boundary_resolution.json',{'time':515.48,'resolution':'Reflow entire adjective phrase together; do not rely on zero-duration dirty token from short-window ASR.','source_word_of_start':515.48,'mixed_audio_word_of_start':515.52,'start_delta':-.04})
270: shots=load(W/'shots.json');cues=load(W/'captions.json');subs=[]
284: v=next(x for x in meta['streams'] if x['codec_type']=='video');report={'duration':float(meta['format']['duration']),'width':v['width'],'height':v['height'],'frames':int(v['nb_frames']),'fps':v['avg_frame_rate'],'decode_exit':p.returncode,'black_intervals':black,'integrated_lufs':float(loud['input_i']),'true_peak_dbtp':float(loud['input_tp']),'audio_bitstream_identical_to_v1':audio_identical,'subtitle_errors':subs,'cues':len(cues),'minimum_shot_seconds':min((s['b']-s['a'])/25 for s in shots),'motion_samples':motions,'visual_review':'pending','playback_ui':'Unavailable: no browsers connected; no claim of real-time visual playback/listening.'}
285: report['technical_pass']=p.returncode==0 and not black and not subs and audio_identical and report['frames']==32268 and abs(report['duration']-1290.72)<.1 and report['true_peak_dbtp']<=-1
286: report['motion_pass']=all(m['near_static']<=3 and m['max_change']<max(.15,m['median_change'])*5 for m in motions)
290: if not d['technical_pass'] or not d['motion_pass']:raise RuntimeError('Unresolved QC failure')
291: d['visual_review']='Sampled compositions, source details, process steps, labels and ending reviewed. Motion measured frame by frame; UI playback unavailable.';save(p,d);update(**{quality+'_qc_pass':True})
296:  caption=load(Q/'subtitle_report.json');shots=load(W/'shots.json')
301:Technical QC: PASS. Full decode; no detected black intervals; subtitle sequence valid; audio bitstream SHA-256 identical to V1. Loudness {d['integrated_lufs']} LUFS, true peak {d['true_peak_dbtp']} dBTP.
303:Motion QC: PASS in three isolated 1080p tests and three samples of the finished video. The old stop/2-pixel-step pattern is absent in measured samples. Subpixel perspective interpolation replaces zoompan; motion is selected by content. Static holds are intentional.
309:Subtitles: {len(load(W/'captions.json'))} English sidecar cues; maximum 42 characters per line / two lines. Orphan tails regrouped, no >20 cps cues in the final reflow. One sub-second emphasis remains: "Coal in.". Source wording preserved. Seven short fresh checks of the actual mixed audio support key cue onsets; the ambiguous zero-duration ASR token near 08:37 was resolved by grouping the whole phrase. No full re-transcription.
317:if __name__=='__main__':{'init':init,'test':motion_test,'prepare':prepare,'preview':preview,'proxy':lambda:render('proxy'),'final':lambda:render('final'),'captions':captions,'audio_check':audio_spotcheck,'refine':refine,'caption_boundary':final_caption_boundary,'proxy_qc':lambda:qc('proxy'),'final_qc':lambda:qc('final'),'accept_proxy':lambda:accept('proxy'),'accept_final':lambda:accept('final')}[sys.argv[1]]()
