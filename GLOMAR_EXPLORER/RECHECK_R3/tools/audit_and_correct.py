from pathlib import Path
from collections import defaultdict
from copy import deepcopy
import csv,json,hashlib,re,sys,xml.etree.ElementTree as ET,subprocess
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT.parent;PREP=PROJECT/'EDIT_PREP_R2'
def loadcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def writecsv(p,rows):
 if not rows:return
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
rows=loadcsv(PREP/'EDIT_TIMELINE.csv');reg=json.loads((PREP/'ASSET_REGISTER.json').read_text(encoding='utf-8-sig'))
used=defaultdict(lambda:[0.,0])
for a in rows:used[a['asset_id']][0]+=float(a['duration_seconds']);used[a['asset_id']][1]+=1
sources=[]
for aid,(seconds,count) in used.items():
 obj=reg[aid];path=Path(obj['local_file']) if obj.get('local_file') else None
 exists=bool(path and path.is_file());actual=digest(path) if exists else ''
 expected=obj.get('sha256','');w=h=''
 if exists and path.suffix.lower() in ['.png','.jpg','.jpeg']:
  with Image.open(path) as im:w,h=im.size
 sources.append({'asset_id':aid,'source_kind':obj['kind'],'file':str(path) if path else '', 'exists':exists,'sha256':actual,'recorded_sha256':expected,'hash_check':('PASS' if expected==actual else 'NO_RECORDED_HASH' if not expected else 'FAIL') if exists else 'MISSING_OR_NOT_BUILT','width':w,'height':h,'R2_seconds':round(seconds,3),'R2_rows':count,'rights_status':obj.get('rights_status',''),'source_url':obj.get('source','')})
writecsv(ROOT/'SOURCE_AUDIT.csv',sources)
assert not [a for a in sources if a['hash_check']=='FAIL']

def words(text):return re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",text)
def script_paragraphs(path):
 text=path.read_text(encoding='utf-8-sig');parts=re.split(r'^### (A\d{2}-(?:P\d{2}|CTA\d{2}))\s*$',text,flags=re.M)
 return {parts[i]:' '.join(line for line in parts[i+1].splitlines() if not line.startswith('#')).strip() for i in range(1,len(parts),2)}
en=script_paragraphs(PROJECT/'SCRIPT_R1_2/05_SCRIPT_R1_2_EN.md');ru=script_paragraphs(PROJECT/'SCRIPT_R1_2/05_SCRIPT_R1_2_RU.md')
timing=loadcsv(PREP/'PARAGRAPH_TIMING.csv');assert set(en)==set(ru)=={a['paragraph_id'] for a in timing}
for a,b in zip(timing,timing[1:]):assert abs(float(a['end_seconds'])-float(b['start_seconds']))<1e-7
assert abs(float(timing[-1]['end_seconds'])-816.96)<1e-7
master=Path(r'C:\YOUTUBE\Youtube 2\Glomar Explorer\AUDIO\R1_2_MASTER_ASR\GLOMAR_R1_2_ARTHUR_MASTER_48K_PCM24.wav')
accept=json.loads((PREP/'AUDIO_OWNER_ACCEPTANCE.json').read_text(encoding='utf-8-sig'));assert digest(master)==accept['delivery_master_sha256']
voice={'accepted_master_sha256':digest(master),'accepted_master_seconds':816.96,'paragraph_ids_en_ru_audio_match':True,'paragraph_count':len(en),'word_count_en_whitespace':sum(len(v.split()) for v in en.values()),'word_count_en_regex':sum(len(words(v)) for v in en.values()),'audio_sample_format':'PCM 24-bit / 48kHz / mono, FFprobe rechecked','owner_listening_acceptance_preserved':True,'new_ASR_or_listening_performed':False,'EN_RU_semantic_retranslation_performed':False,'current_scope':'Preserved accepted wording and checked ID/byte/timing integrity; no rewrite or generation'}
(ROOT/'NARRATION_INTEGRITY.json').write_text(json.dumps(voice,ensure_ascii=False,indent=2),encoding='utf-8')

notes={
'SH003':('FIX','S02: внутренняя камера колодца. Это не добыча конкреций и не внешний вид судна; значение должно быть контекстом, не доказательством добычи.'),
'SH007':('FIX','Та же камера S02 возвращается через18с. Неповторяющиеся секунды не делают её новым ракурсом.'),
'SH008':('FIX','Нашивка не показывает Хьюза или архитектуру сокрытия. Заменено на название реального корабля NEW_C07.'),
'SH009':('FIX','Нашивка не раскрывает «built into the ship». Продолжить NEW_C07 с переходом от названия к оборудованию, без отдельной мгновенной карточки.'),
'SH014':('FIX','DOC19 не является точным визуальным местом утверждения о глубине; использовать подтверждённое музейное описание глубины/FRUS, не случайную страницу.'),
'SH016':('FIX','Лишнее повторение вертикального C08. Использовать уже скачанный широкий NEW_C07 как контекст оборудования1976года.'),
'SH019':('FIX','CIA_NODULE_02 и PHNODULE — один и тот же файл; два ID скрывают непрерывный14.54с статичный план. Первую часть заменить видом реальной машины.'),
'SH031':('HOLD','В PHWELL нет достаточного объяснения gimbal/heave compensation. Нужна построенная и технически проверенная анимация; источник сам по себе её не закрывает.'),
'SH038':('FIX','CTA должен идти на живой по содержанию реальной машине, а не повторять портретный снимок. Назначен широкий NEW_C07; аудио принято и не переписано.'),
'SH040a':('HOLD','Съёмка операции1974 под текстом об испытаниях. Допустимо лишь как явно обозначенный вид устройства; это не найденная хроника январских испытаний.'),
'SH061a':('HOLD','Цель снята во время операции, не в испытании. Отдельно обозначить характер иллюстративного использования.'),
'SH084':('HOLD','Схематический рисунок92с на весь фильм не заменяет показ работы труб. Нужен собственный короткий проверенный механизм/подходящая хроника.'),
'SH087':('FIX','S09 не показывает остановки sensors/controls. Сохранить как контекст работы, добавить точную запись DOC40; не заявлять съёмку отказа.'),
'SH091':('HOLD','Снятый под водой объект не демонстрирует снятие труб наверху. Не превращать этот кадр в доказательство работы палубного механизма.'),
'SH099':('HOLD','S21 — вид обрабатываемой секции внутри; это не документированный кадр самого момента поступления в колодец.'),
'SH103':('FIX','На выбранном конце S20 виден сильный tracking tear. В скорректированной карте использованы чистые0–4.5с и S24 3–7.02с; требуется просмотр в движении.'),
'SH104':('HOLD','Запись обработки секции не устанавливает состав добытых секретов; не выделять неидентифицированные предметы как трофеи.'),
'SH106':('REJECT_PLACEMENT','S23 показывает обработку материала на борту, а фраза — неидентифицированные предметы в новом поле обломков. Это неверная предметная привязка; оставлен явный визуальный пробел.'),
'SH107':('REJECT_PLACEMENT','S24 с работой на борту не является съёмкой ноябрьской разведывательной оценки или будущего захода. Оставлен явный визуальный пробел вместо наполнителя.'),
'SH118':('FIX','Пятый возврат к нашивке не развивает ситуацию. Использовать NEW_C07 с реальным названием/корпусом как контекст раскрытого назначения.'),
'SH120':('HOLD','1987год поверх консервации1976года. Сохранить только с честным контекстом поздней судьбы, не как изображение события августа1976.'),
'SH121':('HOLD','Фото1976года не показывает позднюю коммерческую буровую службу. Нужен подтверждённый поздний вид или явный нейтральный контекст.'),
'SH122':('HOLD','Локального кадра SEC нет. Содержание проверено по официальной веб-странице; скачивание оригинала в этой проверке вернуло403. Это не готовый документальный кадр.'),
'SH124':('REJECT_PLACEMENT','Очередная нашивка под итогом о публичности цели — наполнитель. Визуальный пробел оставлен явным.'),
'SH128':('HOLD','Есть схема геометрии и проверенный кандидат PreviousStory, но нет финального изображения/композиции и проверки кликабельных слотов Studio.'),
}
audit=[]
for a in rows:
 status,reason=notes.get(a['shot_id'],('KEEP_SOURCE_HOLD_TREATMENT','Источник можно сохранить; это не итоговый творческий PASS.'))
 issues=[]
 if a['visual_type']=='NATIVE_GRAPHIC':issues.append('Композиция не построена; только задание.')
 if a['overlay_id']:issues.append('Слой '+a['overlay_id']+' не построен и не проверен на реальном кадре.')
 if a['asset_id'] in ['D07_NATIVE_21','PHSHIP','FRUS183']:issues.append('Повторяемый источник: нужен конкретный новый предмет внимания, иначе длительность не оправдана.')
 if a['asset_id'] in ['CIA_EXHIBIT_05','CIA_EXHIBIT_08','PHK129','PHWELL']:issues.append('Низкое исходное разрешение; требуются реальное кадрирование и проверка читаемости, не обещание HD.')
 if a['asset_id'].startswith('SUN_'):issues.append('Разрешение SunShip HOLD; резерв не равен новой хронике.')
 audit.append({'shot_id':a['shot_id'],'paragraph_id':a['paragraph_id'],'start_seconds':a['start_seconds'],'end_seconds':a['end_seconds'],'asset_id':a['asset_id'],'editorial_decision':status,'reason_ru':reason,'other_issues_ru':' '.join(issues),'rights_status':a['rights_or_production_status'],'source_intact':True})
writecsv(ROOT/'SHOT_AUDIT.csv',audit)

corrected=[];word_timing=loadcsv(PREP/'WORD_TIMING.csv')
swap={'SH008':'NEW_C07','SH009':'NEW_C07','SH014':'FRUS183','SH016':'NEW_C07','SH019':'NEW_C07','SH038':'NEW_C07','SH118':'NEW_C07'}
new_directions={
'SH008':'Показать настоящее название HUGHES GLOMAR EXPLORER на борту NEW_C07; это кадр1976года, Хьюз не изображён.',
'SH009':'Продолжить тот же план; связь названия с видимым реальным оборудованием. Не вставлять отдельную карточку на1.76с.',
'SH014':'Опора на действительное описание глубины и задачи в FRUS183; точный короткий кроп/цитату ещё подготовить.',
'SH016':'Широкий NEW_C07: настоящий необычный корпус и оборудование. Исторический контекст1976года, не сцена принятия решения1970.',
'SH019':'Вид реального оборудования NEW_C07 перед конкрецией, чтобы противопоставление было предметным. Не продлевать музейный предмет до14.54с.',
'SH038':'Принятый CTA на широком NEW_C07 с названием машины и людьми; маленький отдельный слой Subscribe при проверенной читаемости.',
'SH118':'Реальный корпус/название NEW_C07 как контекст раскрытого назначения; не очередное возвращение к нашивке.'}
def setsource(a,aid):
 obj=reg[aid];a['asset_id']=aid;a['asset_local']=obj.get('local_file','');a['visual_type']=obj['kind'];a['source_url']=obj.get('source','');a['rights_or_production_status']=obj.get('rights_status','')
 a['document_page_1based']=obj.get('page_1_based','')
 a['source_in_seconds']=a['source_out_seconds']=''
 a['on_screen_context']='Long Beach,1976; system/history context, not a photograph of the1974 mission' if aid=='NEW_C07' else ''
for old in rows:
 a=deepcopy(old);a['audit_R3_decision']=next(x['editorial_decision'] for x in audit if x['shot_id']==a['shot_id']);a['audit_R3_notes']=notes.get(a['shot_id'],('', ''))[1]
 a['story_ready']=False;a['publication_gate']='HOLD_SOURCE_RIGHTS_AND_EDITORIAL_REVIEW'
 if a['shot_id'] in swap:
  setsource(a,swap[a['shot_id']]);a['direction_ru']=new_directions[a['shot_id']]
 if a['shot_id'] in ['SH106','SH107','SH124']:
  a['evidence_only_asset_id']='FRUS191' if a['shot_id']!='SH124' else 'CIA_MUSEUM'
  a['visual_type']='VISUAL_GAP';a['asset_id']='GAP_'+a['shot_id'];a['asset_local']='';a['source_in_seconds']=a['source_out_seconds']='';a['overlay_id']='';a['publication_gate']='UNRESOLVED_VISUAL_GAP';a['direction_ru']='Нужен подходящий архивный кадр или конкретное короткое объяснение; прежнюю подстановку не использовать.'
 else:a['evidence_only_asset_id']=''
 if a['shot_id']=='SH103':
  b=deepcopy(a);a['shot_id']='SH103a';a['end_seconds']=str(float(a['start_seconds'])+4.5);a['duration_seconds']='4.5';a['source_in_seconds']='0';a['source_out_seconds']='4.5'
  b['shot_id']='SH103b';b['start_seconds']=a['end_seconds'];b['duration_seconds']='4.02';setsource(b,'S24');b['source_in_seconds']='3';b['source_out_seconds']='7.02';b['direction_ru']='Чистый по контрольным кадрам вид работы экипажа; состав полученных секретов по нему не устанавливать.';corrected.extend([a,b]);continue
 corrected.append(a)
for a in corrected:
 a['proposed_start_frame_25fps']=round(float(a['start_seconds'])*25);a['proposed_end_frame_exclusive_25fps']=round(float(a['end_seconds'])*25)
 for key in ['original_working_in_seconds','original_working_out_seconds','original_public_in_seconds','original_public_out_seconds']:
  a[key]='' # regenerate the derived provenance from the original bank below
 if a['visual_type']=='VIDEO' and a['asset_id']!='V01':
  bank=next(x for x in loadcsv(PROJECT/'VIDEO_ARCHIVE_R2/FULL_SCENES.csv') if x['file'][:3]==a['asset_id'])
  for prefix,basekey in [('original_working','working_in'),('original_public','source_youtube_in')]:
   if bank.get(basekey):
    a[prefix+'_in_seconds']=round(float(bank[basekey])+float(a['source_in_seconds']),6);a[prefix+'_out_seconds']=round(float(bank[basekey])+float(a['source_out_seconds']),6)
 a['words_in_this_interval']=' '.join(x['word'].strip() for x in word_timing if x['paragraph_id']==a['paragraph_id'] and float(x['start_seconds'])>=float(a['start_seconds']) and float(x['start_seconds'])<float(a['end_seconds']))
 a['word_timing_status']='ASR_APPROXIMATE_NOT_NEW_ALIGNMENT; accepted voice unchanged'
for a,b in zip(corrected,corrected[1:]):assert abs(float(a['end_seconds'])-float(b['start_seconds']))<1e-7
assert float(corrected[-1]['end_seconds'])==836.96
writecsv(ROOT/'CORRECTED_TIMELINE_NOT_EDIT_READY.csv',corrected)
writecsv(ROOT/'CORRECTED_VIDEO_CUTLIST.csv',[{'shot_id':a['shot_id'],'asset_id':a['asset_id'],'timeline_start':a['start_seconds'],'timeline_end':a['end_seconds'],'source_in':a['source_in_seconds'],'source_out':a['source_out_seconds'],'source_file':a['asset_local'],'editorial_status':a['audit_R3_decision'],'rights':a['rights_or_production_status']} for a in corrected if a['visual_type']=='VIDEO'])
writecsv(ROOT/'WORD_CUE_READBACK.csv',[{'shot_id':a['shot_id'],'paragraph_id':a['paragraph_id'],'start_seconds':a['start_seconds'],'end_seconds':a['end_seconds'],'parent_phrase_en':a['phrase_en'],'actual_ASR_words':a['words_in_this_interval'],'precision':a['word_timing_status']} for a in corrected])

bytype=defaultdict(float)
for a in rows:bytype[a['visual_type']]+=float(a['duration_seconds'])
repeats=sorted([{'asset_id':k,'seconds':round(v[0],3),'rows':v[1],'source_file':reg[k].get('local_file','')} for k,v in used.items()],key=lambda x:-x['seconds'])
writecsv(ROOT/'REPEATED_SOURCE_USE.csv',repeats)
video_groups=[]
for a in rows:
 if a['visual_type']!='VIDEO':continue
 if video_groups and video_groups[-1]['asset_id']==a['asset_id'] and video_groups[-1]['end']==float(a['start_seconds']) and abs(video_groups[-1]['source_end']-float(a['source_in_seconds']))<1e-6:
  video_groups[-1]['end']=float(a['end_seconds']);video_groups[-1]['source_end']=float(a['source_out_seconds']);video_groups[-1]['rows'].append(a['shot_id'])
 else:video_groups.append({'asset_id':a['asset_id'],'start':float(a['start_seconds']),'end':float(a['end_seconds']),'source_end':float(a['source_out_seconds']),'rows':[a['shot_id']]})
overlay=sum(float(a['duration_seconds']) for a in rows if a['overlay_id'] and a['visual_type'] in ['PHOTO','DOCUMENT','ARCHIVAL_DRAWING'])
counts={'R2_video_seconds':bytype['VIDEO'],'R2_video_percent_narration':round(100*bytype['VIDEO']/816.96,3),'R2_video_rows':sum(a['visual_type']=='VIDEO' for a in rows),'R2_continuous_video_insertions':len(video_groups),'R2_video_clip_files':len({a['asset_id'] for a in rows if a['visual_type']=='VIDEO'}),'R2_actual_underlying_historical_video_sources':3,'new_motion_video_sources_added_last_turn':0,'R2_doc_and_drawing_seconds':round(bytype['DOCUMENT']+bytype['ARCHIVAL_DRAWING'],3),'R2_doc_and_drawing_percent':round(100*(bytype['DOCUMENT']+bytype['ARCHIVAL_DRAWING'])/816.96,3),'R2_fullframe_graphics_seconds':bytype['NATIVE_GRAPHIC'],'R2_overlay_assigned_over_primary_sources_seconds':round(overlay,3),'R2_fullframe_or_overlay_assigned_seconds':round(overlay+bytype['NATIVE_GRAPHIC'],3),'overlay_caveat':'A planned overlay interval is not proof of fullframe graphics or of a built/readable effect; actual screen occupancy has not been rendered.','R2_museum_nodule_and_patch_photo_seconds':round(sum(float(a['duration_seconds']) for a in rows if a['asset_id'] in ['PHNODULE','CIA_NODULE_02','NEW_C10']),3),'R2_source_repeat_max':repeats[0],'corrected_video_seconds':round(sum(float(a['duration_seconds']) for a in corrected if a['visual_type']=='VIDEO'),3),'corrected_unfilled_visual_seconds':round(sum(float(a['duration_seconds']) for a in corrected if a['visual_type']=='VISUAL_GAP'),3),'R2_91_59_percent_caveat':'Bookkeeping sum includes original documents, repeated drawings, modern museum photography and conditional sources. It is not archive-motion coverage, final visual quality, or rights clearance.','generation_count':'NOT_ESTABLISHED; zero submissions is confirmed, zero necessary images was not proved'}
(ROOT/'ACCOUNTING_READBACK.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2),encoding='utf-8')

# Check documented page assignments against primary OCR words and record precise source positions.
xml=ET.parse(ROOT/'EVIDENCE/D07_OCR_COORDINATES.xml').getroot();pages=xml.findall('.//OBJECT')
anchors=[('DOC30',30,'cables'),('DOC30',30,'winches'),('DOC30',30,'divers'),('DOC30',30,'puddle'),('DOC35',35,'12,000'),('DOC38',38,'crates'),('DOC39',39,'helicopter'),('DOC40',40,'shutdowns')]
found=[]
for aid,page,token in anchors:
 obj=pages[page-1];ws=obj.findall('.//WORD');matches=[w for w in ws if token.lower() in ''.join(w.itertext()).lower()]
 assert matches,(aid,page,token)
 for w in matches:
  found.append({'asset_id':aid,'pdf_page_1based':page,'anchor':token,'ocr_word':''.join(w.itertext()),'coords_as_recorded':w.get('coords'),'ocr_page_width':obj.get('width'),'ocr_page_height':obj.get('height'),'coordinate_status':'PRIMARY_OCR_COORDS_RECORDED; map normalization to native scan before crop render'})
writecsv(ROOT/'DOCUMENT_ANCHOR_CHECK.csv',found)
readiness={'base_commit_reviewed':'1699c4bcf4ecb7ec0c87edef12c120deb7c3eabf','scope':'All132R2rows,47usedassetIDs,27video placements with81exact source samples, accepted narration byte/timing integrity, CTA/sound/end-screen status','technical_integrity':'PASS_WITH_SEC_CAPTURE_MISSING_AND_UNBUILT_ART','editorial_readiness':'REJECT_R2_AS_READY_FOR_ASSEMBLY','asset_rejection_scope':'No source asset deleted or globally rejected; specific placements corrected/held','rights':'HOLD_PRESERVED_NO_NEW_LICENSE','full_realtime_AV_review':'NOT_PERFORMED_NO_FILM_EXISTS','accepted_narration':'PRESERVED_AND_HASH_MATCHED','new_generation_jobs_submitted':0,'budget_spent':0,'new_moving_sources_acquired':0,'current_corrected_map':'RECHECK_R3/CORRECTED_TIMELINE_NOT_EDIT_READY.csv','remaining_main_issue':'Need scene-specific moving archive and constructed mechanism sequences; no more arbitrary document/patch filler or source relabelling'}
(ROOT/'AUDIT_RESULT.json').write_text(json.dumps(readiness,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'scope':readiness['scope'],'verdict':readiness['editorial_readiness'],'accounting':counts,'narration':voice},ensure_ascii=False,indent=2))
