"""Caption the exact locked V4 using existing real audio ASR, without TTS.
Owner explicitly requested external subtitles; no captions are burned in.
"""
from pathlib import Path
import json,re,difflib,textwrap,hashlib,csv,collections
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
SCRIPT=REPO/'CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_VOICE_TEXT_V4_EN.txt'
ASR=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\AUDIO\VOICEBOX_ARTHUR_V1\ASR_QC\CAMP_CENTURY_MASTER_WORDS_SMALL_EN.json')
beats=json.loads((REPO/'CAMP_CENTURY/DEVELOPMENT/RESOLVE_R3/BEATS_AUDIO_LOCKED.json').read_text())
text=SCRIPT.read_text(encoding='utf-8-sig');words=json.loads(ASR.read_text(encoding='utf-8-sig'))
patch_file=ROOT/'05_PROJECT_AND_QC/MEDIUM_EN_525_545_WORD_TIMING.json'
if patch_file.exists():
    patch=[w for w in json.loads(patch_file.read_text())['words'] if 533.3<=w['start'] and w['end']<=536.70]
    assert ' '.join(w['text'] for w in patch)=="Project Iceworm. The idea was to use"
    words=sorted([w for w in words if not 533.3<=float(w['start'])<536.70]+patch,key=lambda w:float(w['start']))
norm=lambda s:' '.join(s.split())
assert norm('\n\n'.join(b['spoken_text_exact'] for b in beats))==norm(text)
canonical=SCRIPT.read_bytes().replace(b'\r\n',b'\n')
assert hashlib.sha1(b'blob '+str(len(canonical)).encode()+b'\0'+canonical).hexdigest()=='46fafe9914c1a061e9f219c344698f9857019973'
OUT=ROOT/'02_SUBTITLES';QC=ROOT/'05_PROJECT_AND_QC';OUT.mkdir(parents=True,exist_ok=True);QC.mkdir(exist_ok=True)
def units(s):return re.findall(r"[a-z0-9]+(?:'[a-z]+)?",s.lower().replace('’',"'"))
timed=[];oplog=[]
for beat in beats:
    source=beat['spoken_text_exact'].split();begin=float(beat['audio_start_sec']);finish=float(beat['audio_end_sec'])
    heard=[w for w in words if begin-.04<=float(w['start'])<finish+.02]
    a=[(u,i) for i,w in enumerate(source) for u in units(w)]
    b=[(u,float(w['start']),float(w['end'])) for w in heard for u in units(w['text'])]
    matches={};matcher=difflib.SequenceMatcher(None,[x[0] for x in a],[x[0] for x in b],autojunk=False)
    for tag,i0,i1,j0,j1 in matcher.get_opcodes():
        if tag=='equal':
            for i,j in zip(range(i0,i1),range(j0,j1)):matches[i]=(b[j][1],b[j][2],'ASR_MATCH')
        elif tag in ['replace','delete']:
            lo=b[j0][1] if j0<j1 else (b[j0-1][2] if j0 else begin)
            hi=b[j1-1][2] if j0<j1 else (b[j0][1] if j0<len(b) else finish)
            lo=max(begin,lo);hi=min(finish,max(lo+.02,hi));weights=[max(1,len(a[i][0])) for i in range(i0,i1)];total=sum(weights);cursor=lo
            for i,weight in zip(range(i0,i1),weights):
                end=cursor+(hi-lo)*weight/max(1,total);matches[i]=(cursor,end,'ASR_SUBSTITUTION_INTERVAL' if tag=='replace' else 'INTERPOLATED_MISSING_ASR');cursor=end
            oplog.append(dict(beat=beat['beat_id'],operation=tag,script_units=' '.join(x[0] for x in a[i0:i1]),asr_units=' '.join(x[0] for x in b[j0:j1]),start=lo,end=hi))
    for index,word in enumerate(source):
        bounds=[matches[i] for i,(_,owner) in enumerate(a) if owner==index]
        if bounds:
            lo=min(x[0] for x in bounds);hi=max(x[1] for x in bounds);status='ASR_MATCH' if all(x[2]=='ASR_MATCH' for x in bounds) else '+'.join(sorted({x[2] for x in bounds}))
        else:
            lo=timed[-1]['end'] if timed else begin;hi=lo;status='PUNCTUATION'
        timed.append(dict(index=len(timed),word=word,start=lo,end=hi,alignment=status,beat=beat['beat_id']))
assert norm(' '.join(w['word'] for w in timed))==norm(text)
def wrap(s):
    if len(s)<=42:return [s]
    items=s.split();choices=[];bad={'a','an','the','of','to','in','and','or','for','with','its'}
    for i in range(1,len(items)):
        left=' '.join(items[:i]);right=' '.join(items[i:])
        if max(len(left),len(right))<=42:choices.append((abs(len(left)-len(right))+(15 if items[i-1].lower() in bad else 0),[left,right]))
    return min(choices,key=lambda x:x[0])[1] if choices else None
groups=[];group=[]
for w in timed:
    candidate=' '.join(x['word'] for x in group+[w])
    if group and (wrap(candidate) is None or w['end']-group[0]['start']>6 or w['beat']!=group[0]['beat']):groups.append(group);group=[]
    group.append(w);s=' '.join(x['word'] for x in group);duration=w['end']-group[0]['start']
    if (len(s)>=65 or (re.search(r'[.!?][\"\u201d\u2019]?$' ,w['word']) and duration>=1.2) or (w['word'].endswith(',') and len(s)>=45)) and duration>=.9:groups.append(group);group=[]
if group:groups.append(group)
merged=[]
for gi,group in enumerate(groups):
    next_start=groups[gi+1][0]['start'] if gi+1<len(groups) else 1094.72
    if merged and (len(' '.join(w['word'] for w in group))<28 or group[-1]['end']-group[0]['start']<1.3) and group[0]['beat']==merged[-1][0]['beat']:
        combined=merged[-1]+group
        if combined[-1]['end']-combined[0]['start']<=6 and wrap(' '.join(w['word'] for w in combined)) is not None:
            merged[-1]=combined;continue
        for k in range(1,min(7,len(merged[-1]))):
            left=merged[-1][:-k];right=merged[-1][-k:]+group
            right_duration=min(right[-1]['end']+.1,next_start-.05)-(right[0]['start']-.035)
            if right_duration>=.9 and len(' '.join(w['word'] for w in right))/right_duration<=22 and right[-1]['end']-right[0]['start']<=6 and wrap(' '.join(w['word'] for w in left)) is not None and wrap(' '.join(w['word'] for w in right)) is not None:
                merged[-1]=left;group=right;break
    merged.append(group)
groups=merged
cues=[]
for group in groups:
    lines=wrap(' '.join(w['word'] for w in group));assert lines
    cues.append(dict(start=max(0,group[0]['start']-.035),end=min(1094.72,group[-1]['end']+.10),lines=lines,word_indexes=[group[0]['index'],group[-1]['index']+1]))
for i,c in enumerate(cues):
    needed=sum(map(len,c['lines']))/21
    available=(cues[i+1]['start']-.015) if i+1<len(cues) else 1094.72
    c['end']=min(available,max(c['end'],min(c['start']+needed,c['end']+.6)))
    if i+1<len(cues):c['end']=min(c['end'],max(c['start']+.001,cues[i+1]['start']-.015))
    assert c['end']>c['start'] and len(c['lines'])<=2 and max(map(len,c['lines']))<=42
    if i:assert c['start']>=cues[i-1]['end']
def stamp(t,comma=True):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02}'+(',' if comma else '.')+f'{ms:03}'
srt=''.join(str(i+1)+'\n'+stamp(c['start'])+' --> '+stamp(c['end'])+'\n'+'\n'.join(c['lines'])+'\n\n' for i,c in enumerate(cues))
vtt='WEBVTT\n\n'+''.join(stamp(c['start'],False)+' --> '+stamp(c['end'],False)+'\n'+'\n'.join(c['lines'])+'\n\n' for c in cues)
(OUT/'CAMP_CENTURY_EN.srt').write_text(srt,encoding='utf-8');(OUT/'CAMP_CENTURY_EN.vtt').write_text(vtt,encoding='utf-8');(OUT/'CAMP_CENTURY_TRANSCRIPT_EN.txt').write_bytes(SCRIPT.read_bytes())
assert norm(' '.join(' '.join(c['lines']) for c in cues))==norm(text)
spotchecks=[dict(cue=i+1,start=c['start'],end=c['end'],cps=round(sum(map(len,c['lines']))/(c['end']-c['start']),2),text=' '.join(c['lines'])) for i,c in enumerate(cues) if sum(map(len,c['lines']))/(c['end']-c['start'])>23 or c['end']-c['start']<.65]
report=dict(status='FILE_AND_TEXT_QC_PASS_TIMING_SPOTCHECK_PENDING',cues=len(cues),script_words_whitespace=len(text.split()),caption_words_whitespace=sum(len(' '.join(c['lines']).split()) for c in cues),exact_locked_v4_text_preserved=True,script_git_blob='46fafe9914c1a061e9f219c344698f9857019973',max_lines=max(len(c['lines']) for c in cues),max_line_chars=max(len(line) for c in cues for line in c['lines']),monotonic_nonoverlap=True,last_caption_end_seconds=cues[-1]['end'],endscreen_start_seconds=1094.72,endscreen_captions=0,timing_basis='Accepted-master small.en ASR plus a local cached medium.en word-timing repair for Project Iceworm. The idea was to use; aligned within 32 locked beats; remaining ASR substitution spans interpolated, not claimed word-exact',alignment_counts=dict(collections.Counter(w['alignment'] for w in timed)),manual_timing_spotchecks=spotchecks,full_human_subtitle_review='PENDING',authorization='Owner explicitly requested uploadable subtitle file on 2026-10-27; external captions only, supersedes older Stage05 prohibition on SRT/VTT export',video_modified=False,audio_modified=False)
(QC/'SUBTITLE_QC.json').write_text(json.dumps(report,indent=2),encoding='utf-8');(QC/'SUBTITLE_ALIGNMENT_AUDIT.json').write_text(json.dumps(dict(words=timed,non_exact_intervals=oplog),indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)
