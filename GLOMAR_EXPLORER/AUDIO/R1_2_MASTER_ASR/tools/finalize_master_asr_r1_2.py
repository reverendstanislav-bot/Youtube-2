from pathlib import Path
import json,csv,sys,hashlib,shutil,re
sys.path.insert(0,str(Path(__file__).parent))
from asr_normalize_r1_2 import norm,ops
SRC=Path(r'C:\YOUTUBE\Youtube 2\Glomar Explorer\AUDIO\R1_2_VOICEBOX_QUEUE');OUT=SRC.parent/'R1_2_MASTER_ASR'
q=json.loads((SRC/'QUEUE.json').read_text(encoding='utf-8'));assert len(list((OUT/'ASR_BASE_EN').glob('*.json')))==50
flags=[d['paragraph_id'] for d in json.loads((OUT/'ASR_DIFF_BASE.json').read_text(encoding='utf-8')) if d['differences']]
assert all((OUT/'ASR_MEDIUM_EN'/(pid+'.json')).exists() for pid in flags),'Medium verification not yet complete'
rows=[];diffs=[];words=[];transcripts=[]
timing={r['paragraph_id']:r for r in csv.DictReader((OUT/'PARAGRAPH_TIMING.csv').read_text(encoding='utf-8').splitlines())}
for j in q['jobs']:
 pid=j['id'];f=OUT/('ASR_MEDIUM_EN' if pid in flags else 'ASR_BASE_EN')/(pid+'.json');d=json.loads(f.read_text(encoding='utf-8'));a=norm(d['expected']);b=norm(d['recognized']);changes=ops(a,b)
 rows.append({'paragraph_id':pid,'model':d['model'],'start_seconds':timing[pid]['start_seconds'],'duration_seconds':timing[pid]['duration_seconds'],'expected_words_normalized':len(a),'recognized_words_normalized':len(b),'diff_groups':len(changes),'status':'ASR_TEXT_MATCH_NORMALIZED' if not changes else 'HOLD_TARGETED_LISTENING','expected_en':d['expected'],'recognized_en':d['recognized']});diffs.append({'paragraph_id':pid,'differences':changes,'model':d['model']});transcripts.append(f'### {pid}\n{d["recognized"]}\n')
 offset=float(timing[pid]['start_seconds'])
 for seg in d['segments']:
  for w in seg['words']:words.append({'paragraph_id':pid,'word':w['word'],'start_seconds':offset+w['start'],'end_seconds':offset+w['end'],'asr_probability':w['probability'],'model':d['model']})
def writecsv(name,rows):
 with(OUT/name).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
writecsv('ASR_COMPARISON_FINAL.csv',rows);writecsv('WORD_TIMING_FINAL.csv',words)
(OUT/'ASR_DIFF_FINAL.json').write_text(json.dumps(diffs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(OUT/'ASR_TRANSCRIPT_FINAL_EN.md').write_text('# Actual ASR transcript — internal QC only, not subtitle delivery\n\n'+'\n'.join(transcripts),encoding='utf-8')
remaining=[d for d in diffs if d['differences']];passed=50-len(remaining)
summary={'status':'ASR_TEXT_PASS_LISTENING_PENDING' if not remaining else 'ASR_COMPLETE_TARGETED_REVIEW_HOLD','paragraphs_checked':50,'base_asr_passes':50,'medium_rechecks':len(flags),'normalized_matches':passed,'unresolved_paragraphs':remaining,'text_prompt_used':False,'models':'cached faster-whisper-base.en and medium.en; CPU int8; English; independent text recognition without source prompt','normalization':'Case/punctuation, numeric notation and hull ID spacing, common contractions, center/centre, under cover/undercover, Transocean spacing, gimbaled/gimballed. Raw transcripts retained. No phonetic name aliases or dropped words are excused.','scope':'Recognized word sequence only; not proof of correct pronunciation, prosody or absence of clicks.','source_pcm_matches_master':True,'full_listening':'NOT_PERFORMED','regeneration':False}
(OUT/'ASR_QC_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qc=json.loads((OUT/'MASTER_TECHNICAL_QC.json').read_text(encoding='utf-8'));qc['asr']=summary['status'];qc['status']='TECHNICAL_AND_ASR_PASS_LISTENING_PENDING' if not remaining else 'MASTER_TECHNICAL_PASS_ASR_REVIEW_HOLD';qc['integrated_loudness_lufs']=-20.4;qc['true_peak_dbfs']=-2.8;(OUT/'MASTER_TECHNICAL_QC.json').write_text(json.dumps(qc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cta=timing['A03-CTA01'];first=sum(float(timing[j['id']]['duration_seconds']) for j in q['jobs'] if j['id'].startswith('A01'))
report=f'''# Glomar R1.2 — мастер и ASR

## Выполнено
Собраны все50 WAV из завершённой очереди, строго по исходному порядку, включая A03-CTA01. Проверены SHA256, соответствие текстов источнику и полное FFmpeg-декодирование50/50. Нативный мастер — точная последовательная PCM-склейка24kHz/16-bit mono. Монтажная копия —48kHz/24-bit PCM mono. Исходные WAV не изменены. Нет добавленных пауз, обрезки, crossfade, gain, нормализации или time stretch.48kHz не выдаётся за новое исходное разрешение.

## Измеренные параметры
- Длительность:816.960с =13:36.960. Это фактическая озвучка, не прежний прогноз16–18мин; скорость не замедлялась ради длительности.
-2184 слова сценария; около160.4слова/мин с учётом всех исходных пауз. Этот показатель относится только к текущему дублю.
- Первый акт:{first:.3f}с. CTA начинается на{float(cta['start_seconds']):.3f}с и длится{float(cta['duration_seconds']):.3f}с. Точные позиции остальных абзацев —PARAGRAPH_TIMING.csv.
- Integrated loudness −20.4LUFS; true peak −2.8dBFS; нативный sample peak{qc['peak_dbfs']}dBFS. Параметры измерены, но не подгонялись под громкость финального фильма.
-49стыков сохранены; диагностические измерения в JOIN_DIAGNOSTICS.csv не заменяют слуховую проверку.

## ASR
Распознаны50/50 абзацев cached base.en;20различающихся перепроверены cached medium.en cVAD. Скрипт в prompt не подавался. После описанной нормализации совпало{passed}/50. Неразрешённых абзацев:{len(remaining)}. ASR_DIFF_FINAL.json содержит оставшиеся различия; если список пуст, словеских расхождений в выбранном распознавании не найдено. Base-проход и его ошибки сохранены, не подменены исправленным вручную текстом. Выбранный финальный транскрипт — фактический вывод моделей.

ASR выполнен по всем исходным сегментам, PCM которых побитно составляет мастер; абсолютные word timings перенесены по точным sample offsets. Это покрытие всего мастера через50сегментов, не заявление о втором непрерывном распознавании всего файла.

## Ограничения
Полное прослушивание/произношение, художественная подача, дыхание, clicks и acceptance владельца не проверены. ASRсовпадение не означает слушательскийPASS. Никакой перегенерации, монтажа, изображений, субтитров для публикации или платных операций. Исторические/архивные HOLD сохранены.

Текущий статус:{qc['status']}.
'''
(OUT/'README_RU.md').write_text(report,encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256.csv']
writecsv('SHA256.csv',[{'file':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)])
print(json.dumps({'matches':passed,'unresolved':remaining,'status':qc['status'],'first_act_seconds':first,'cta_seconds':cta['start_seconds']},ensure_ascii=False))
