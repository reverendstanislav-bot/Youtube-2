"""Owner-requested archive-first revision. Preserve narration and all R1 files."""
from pathlib import Path
from copy import deepcopy
from collections import defaultdict
import csv, json, hashlib, html, re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parents[1]
PROJECT=OUT.parent
OLD=PROJECT/'EDIT_PREP_R1'
EXP=PROJECT/'ARCHIVE_EXPANSION_R5'
DELIVERY=Path(r'C:\YOUTUBE\Youtube 2\Glomar Explorer')
OUT.mkdir(exist_ok=True)
def readcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def writecsv(p,rows,fields=None):
    if not rows:return
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

rows=readcsv(OLD/'EDIT_TIMELINE.csv')
reg=json.loads((OLD/'ASSET_REGISTER.json').read_text(encoding='utf-8-sig'))
for a in readcsv(PROJECT/'ARCHIVE_R1/ASSET_REGISTER.csv'):
    if a['local_file'] and a['asset_id'] not in reg:
        p=DELIVERY/'ARCHIVE_R1'/a['local_file']
        reg[a['asset_id']]={'asset_id':a['asset_id'],'kind':'PHOTO','local_file':str(p),'source':a['source_page'],'rights_status':a['rights_status'],'notes_ru':a['editorial_note_ru'],'sha256':a['sha256'],'exists':p.exists(),'width':a['width'],'height':a['height']}
for a in json.loads((EXP/'ACQUISITION_RESULTS.json').read_text(encoding='utf-8')):
    if a.get('status')!='DOWNLOADED_ITEM_EVIDENCE_SAVED' or a['asset_id']=='C12':continue
    p=EXP/a['local_file'];aid='NEW_'+a['asset_id'];license=a.get('license','')
    reg[aid]={'asset_id':aid,'kind':'PHOTO','local_file':str(DELIVERY/'ARCHIVE_EXPANSION_R5'/a['local_file']),'staging_file':str(p),'source':a['source_page'],'rights_status':('CC_BY_SA_ATTRIBUTION_AND_ADAPTATION_TERMS' if license.startswith('CC BY-SA') else 'COMMONS_PD_CIA_ITEM_EVIDENCE_SAVED'),'notes_ru':html.unescape(re.sub('<[^>]*>','',a.get('description_html',''))),'sha256':sha(p),'exists':p.exists(),'width':a['width'],'height':a['height'],'historical_date':a.get('date_html'),'license':license,'license_url':a.get('license_url'),'author':html.unescape(re.sub('<[^>]*>','',a.get('artist_html','')))}
for n in [19,20,21,28,30,33,35,38,39,40]:
    p=EXP/'ORIGINALS'/f'D07_P{n:02d}_NATIVE.png'
    if not p.exists():continue
    aid=f'D07_NATIVE_{n}'
    reg[aid]={'asset_id':aid,'kind':('ARCHIVAL_DRAWING' if n==21 else 'DOCUMENT'),'local_file':str(DELIVERY/'ARCHIVE_EXPANSION_R5/ORIGINALS'/p.name),'staging_file':str(p),'source':'https://archive.org/details/cia-readingroom-document-0005301269','rights_status':'OFFICIAL_HISTORY_COMPONENT_REVIEW_PENDING','notes_ru':('Подлинный рисунок из отчёта CIA; один источник с DOC21, не новая независимая фотография. Повернуть на 90 градусов в редакторе; без дорисовки.' if n==21 else 'Точное извлечение исходного скана страницы; не фотография события и не новый независимый источник.'),'sha256':sha(p),'exists':True,'page_1_based':n}
    if n!=21 and f'DOC{n}' in reg:
        original=reg[f'DOC{n}'];original['source_pdf']=original['local_file'];original['source_pdf_sha256']=original['sha256']
        original['local_file']=reg[aid]['local_file'];original['staging_file']=str(p);original['sha256']=sha(p)

# Exact phrase timings stay unchanged unless a single old shot is intentionally split.
# 637.04-637.22 was an unnecessary 0.18s flash; absorb it into the burial shot.
for a in rows:
    if a['shot_id']=='SH100':a['end_seconds']='637.22';a['duration_seconds']='7.18'
rows=[a for a in rows if a['shot_id']!='SH101']
changes=[]
def assign(a,asset,direction,overlay='',meaning='EXACT_SOURCE_OR_HISTORICAL_CONTEXT',context=''):
    old=a['asset_id'];obj=reg[asset]
    a['asset_id']=asset;a['visual_type']=obj['kind'];a['asset_local']=obj.get('local_file','')
    a['source_url']=obj.get('source','');a['document_page_1based']=str(obj.get('page_1_based',''))
    a['rights_or_production_status']=obj.get('rights_status','')
    for k in ['source_in_seconds','source_out_seconds','original_working_in_seconds','original_working_out_seconds','original_public_in_seconds','original_public_out_seconds']:a[k]=''
    a['direction_ru']=direction;a['overlay_id']=overlay;a['archive_semantics']=meaning;a['on_screen_context']=context
    a['motion']='STATIC; only a named detail may receive one motivated reveal; no whole-frame drift, shake or blanket zoom'
    a['transition']='CLEAN_CUT_OR_CONTINUATION; no automatic transition preset'
    a['publication_gate']='HOLD_FINAL_ASSET_AND_FULL_AV_REVIEW'
    if old!=asset:changes.append({'shot_id':a['shot_id'],'paragraph_id':a['paragraph_id'],'previous_asset':old,'new_asset':asset,'reason_ru':direction})
    return a

# A real drawing is a primary archival source, never a generated reconstruction.
# Native animation is reserved for movements a still cannot explain.
replacements={
'SH001':('PHSHIP','Настоящий корабль задаёт объект; подлинная запись об облётах появляется коротким читаемым кропом, без выдуманного вертолёта.','DOC38_EXCERPT'),
'SH002':('DOC38','Точная запись о ящиках и блокировании посадочной площадки. Не генерировать посадку или контейнеры.','LOCAL_TEXT_REVEAL'),
'SH004':('D07_NATIVE_21','Исходная схема судна, повернутая в редакторе; глубина вынесена отдельным объясняющим слоем.','DEPTH_RELATION'),
'SH005':('D07_NATIVE_21','Продолжить исходную схему; сопоставить поверхность и глубокую цель одним коротким элементом.','DEPTH_RELATION'),
'SH006':('PHSHIP','Реальный корпус и линия обзора: только нужный участок борта и скрытый путь.','O08_SIGHTLINE'),
'SH008':('NEW_C10','Подлинная нашивка предприятия прикрытия; музейная фотография предмета. Без ложной сцены работы Хьюза.',''),
'SH009':('NEW_C10','Продолжение того же плана с нашивкой; не делать отдельную 1.76-секундную карточку.',''),
'SH012':('FRUS183','Настоящий документ о найденном объекте: раскрыть только относящийся к фразе абзац.','LOCAL_TEXT_REVEAL'),
'SH014':('DOC19','Ограничение глубины показать коротким точным фрагментом документа и реальной геометрией судна, без длинной схемы.',''),
'SH016':('NEW_C08','Исторический снимок Glomar: силуэт и высота вышки. Это 1976 год, а не момент проектирования.',''),
'SH017':('NEW_C08','Продолжить тот же снимок, локально назвать вышку. Не зумить весь кадр.','O01_DERRICK'),
'SH018':('D07_NATIVE_21','Подлинный схематический рисунок: выделить центр корпуса, без генерируемого cutaway.','O01_WELL'),
'SH019':('CIA_NODULE_02','Настоящий музейный предмет — конкреция. Не выдавать музейную съёмку за добычу 1974.',''),
'SH021':('NEW_C10','Подлинная нашивка Hughes/Summa и точный фрагмент DOC19 о прикрытии отдельным слоем.','DOC19_EXCERPT'),
'SH022':('PHSHIP','Реальное судно целиком; считывается промышленный масштаб и необычная компоновка.',''),
'SH023':('D07_NATIVE_21','Подлинный рисунок судна: по очереди назвать три уже видимых узла, без новой фоновой плашки.','O01_THREE_NODES'),
'SH024':('PHWELL','Настоящий центральный колодец; вопрос видимости груза связывается с физическим местом.',''),
'SH030':('D07_NATIVE_21','Исходный рисунок и отдельная короткая стрелка движения корпуса; не раскачивать сам кадр.','O01_HEAVE'),
'SH031':('PHWELL','Настоящий колодец и ограниченная поясняющая анимация компенсации. Не заявлять, что виден конкретный компенсатор.','O01_COMPENSATION'),
'SH032':('SUN_PLATFORM','Подлинная фотография монтажа из Sun Ship. До разрешения не входит в публикационный пакет; резерв DOC19.',''),
'SH034':('D07_NATIVE_21','Показать, где установлен тяжёлый узел, на подлинном рисунке после реального монтажного фото.','O01_ASSEMBLY'),
'SH036':('DOC20','Подлинная запись о снятии секции вышки. Фотографическую сцену крана и моста не выдумывать.','LOCAL_TEXT_REVEAL'),
'SH038':('NEW_C08','Короткий принятый устный CTA поверх исторического снимка; маленький знак подписки отдельным слоем.','SUBSCRIBE'),
'SH039':('NEW_C08','Продолжить план после CTA, не создавать мгновенную вторую карточку.',''),
'SH041':('DOC30','Оригинальная запись испытаний; показать событие, затем его материальную причину.','LOCAL_TEXT_REVEAL'),
'SH042':('D07_NATIVE_21','Подлинная схема как перечень проверяемых узлов, три локальных последовательных акцента.','O01_TEST_ITEMS'),
'SH043':('DOC28','Подлинный план сезона и испытаний. Даты объясняют давление срока.','LOCAL_TEXT_REVEAL'),
'SH044':('DOC28','Продолжение того же источника: выделить сезонное ограничение, не выдумывать погодную диаграмму.','LOCAL_TEXT_REVEAL'),
'SH045':('DOC28','Удержать реальный источник на причинно-следственном выводе. Никакой новой карточки с пересказом.',''),
'SH047':('DOC30','Подлинная запись повреждения привода, локальное выделение точных слов.','LOCAL_TEXT_REVEAL'),
'SH049':('DOC30','Подлинный текст об использовании тросов и лебёдок; генерацию IG04 исключить.','LOCAL_TEXT_REVEAL'),
'SH050':('DOC30','Продолжить запись об остановке испытаний и возвращении. Не использовать поздний порт как январь 1974.','LOCAL_TEXT_REVEAL'),
'SH052':('DOC30','Ремонт и ограничение докования — действительный текст источника, не выдуманное фото ремонта.','LOCAL_TEXT_REVEAL'),
'SH053':('DOC30','Свидетельство о водолазной проверке/ремонте; IG05 убрать. Точный кроп сверить с OCR до монтажа.','LOCAL_TEXT_REVEAL'),
'SH055':('DOC33','Реальный отчёт о февральских ремонтах.','LOCAL_TEXT_REVEAL'),
'SH056':('DOC33','Продолжить источник об удовлетворительной работе трубной системы, без 2.98-секундной генерации.','LOCAL_TEXT_REVEAL'),
'SH057':('DOC33','Реальная последовательность неисправностей в одном отчёте; никакой условной погодной плашки.','LOCAL_TEXT_REVEAL'),
'SH058':('DOC35','Конкретная запись об отказе от полного испытания.','LOCAL_TEXT_REVEAL'),
'SH059':('DOC35','Удержать настоящий документ на принятом риске; не переобъяснять всё ещё одной длинной схемой.','LOCAL_TEXT_REVEAL'),
'SH060':('DOC35','Сохранить оговорку: решение по испытанию не доказывает причину последующего разрушения.',''),
'SH062':('CIA_EXHIBIT_05','Опубликованный рисунок захвата, а не фантазийная конструкция или доказательство точной формы обломка.','O04_STRUCTURE'),
'SH063':('CIA_EXHIBIT_05','Исходный рисунок захвата вводит предмет передачи. Генерация скрытого цеха IG06 не нужна.',''),
'SH064':('D07_NATIVE_21','Реальная компоновка объясняет необходимость скрыть входящее оборудование.','O01_WELL'),
'SH065':('CIA_EXHIBIT_08','Опубликованная CIA схема передачи; контур реального рисунка, не новая физическая сцена.',''),
'SH066':('CIA_EXHIBIT_08','Подлинная опубликованная схема HMB-1. Позднюю M05 с Sea Shadow не подставлять в 1974.',''),
'SH067':('CIA_EXHIBIT_08','На исходном рисунке обозначить крышу отдельным акцентом; из-за малого разрешения не растягивать весь исходник.','O03_ROOF'),
'SH071':('PHWELL','Настоящая фотография центрального колодца объясняет скрытый вход; это не съёмка тайной передачи.',''),
'SH072':('D07_NATIVE_21','Вернуть подлинный рисунок и коротко указать вход снизу, не повторяя всю анимацию.','O03_ENTRY'),
'SH073':('NEW_C08','Реальный исторический корабль; точная дата снимка указана один раз для серии.',''),
'SH074':('CIA_EXHIBIT_08','Исходная опубликованная схема с последовательным маршрутом отдельным слоем; не ещё один полный анимационный ролик.','O03_ROUTE'),
'SH075':('PHSHIP','Реальный корабль и сохранённая пауза взгляда на заметный силуэт.',''),
'SH076':('PHSHIP','Продолжение предыдущего плана. Не добавлять новую 1.98-секундную графическую карточку.',''),
'SH078':('PHSHIP','Настоящее судно; календарная отметка 4 July 1974 отдельным слоем. Точный маршрут не выдумывать.','DATE_JUL4'),
'SH080':('DOC39','Подлинная запись о Chazhma и фотографических облётах. Нет проверенной съёмки этого вертолёта.','LOCAL_TEXT_REVEAL'),
'SH081':('DOC38','Первичная запись о ящиках перед появлением корабля. IG01 не производить.','LOCAL_TEXT_REVEAL'),
'SH082':('PHSHIP','Реальное судно и один слой линии взгляда сверху; не физическая реконструкция облёта.','O08_SIGHTLINE'),
'SH083':('D07_NATIVE_21','Подлинный рисунок: локально показать путь трубной колонны, не обычный трос.','O04_PIPE'),
'SH084':('D07_NATIVE_21','Отдельная схема добавления секций привязана к подлинной компоновке. Нет архивного видео работы трубной системы.','O04_PIPE'),
'SH086':('PHSHIP','Корабль над условной целью: минимальный знак удержания положения. Не поддельная телеметрия.','O04_STATION'),
'SH092':('D07_NATIVE_21','Короткая поясняющая последовательность удаления секций у реальной вышки. Не выдавать за видеосъёмку.','O04_PIPE'),
'SH093':('PHWELL','Настоящий колодец: физическая цель подъёма, затем стыковка в записи операции.','O01_WELL'),
'SH102':('CIA_MUSEUM','1992 год относится к передаче записи, а не к дате похорон. Настоящая официальная запись CIA.','DATE_1992'),
'SH108':('PHSHIP','Реальное судно после показанного частичного результата.',''),
'SH109':('FRUS191','Настоящая оценка возможности второго захода.','LOCAL_TEXT_REVEAL'),
'SH110':('FRUS183','Подлинная официальная хронология, точная дата решения отдельным слоем.','DATE_FEB6'),
'SH112':('FRUS183','Удержать источник: одобрение и публикация оказались рядом во времени.','DATE_FEB7'),
'SH113':('CIA_MUSEUM','Официальный рассказ CIA об ограблении. Фальшивой газеты и инсценировки кражи нет.','LOCAL_TEXT_REVEAL'),
'SH115':('FRUS183','Настоящие документы об обращениях Colby и огласке.','LOCAL_TEXT_REVEAL'),
'SH116':('FRUS183','Точные даты телевизионного сообщения и газетной публикации поверх подлинного источника. Не создавать газетный макет.','DATES_MAR18_MAR19'),
'SH117':('NEW_C08','Реальное изображение Glomar; связь с лодкой уже опубликована.',''),
'SH118':('NEW_C10','Подлинная вещь прикрытия: теперь принадлежность больше не сохраняет тайну.',''),
'SH121':('NEW_C08','Реальная историческая фотография судна. Не выдавать резервный флот за коммерческое бурение.',''),
'SH123':('D07_NATIVE_21','Исходная схема завершает объяснение скрытого пути; только 3 коротких последовательных акцента, затем реальная запись стыковки.','O01_FINAL_ROUTE'),
'SH124':('NEW_C10','Настоящая нашивка прикрытия после потери секретности.',''),
'SH126':('PHSHIP','Реальное судно удерживается на фразе о несостоявшемся втором рейсе.',''),
'SH127':('PHSHIP','Продолжить тот же план до окончания эмоциональной развязки; CTA её не перебивает.',''),
}
for a in rows:
    a['overlay_id']='';a['archive_semantics']='EXACT_SOURCE_OR_HISTORICAL_CONTEXT';a['on_screen_context']=''
    a['source_visual_qc']='EXISTING_SOURCE_SAMPLED_ONLY'
    if a['shot_id'] in replacements:assign(a,*replacements[a['shot_id']])
    if a['asset_id']=='PHBARGE':assign(a,'CIA_EXHIBIT_08','Исходная схема вместо поздней фотографии баржи.','O03_ROUTE')
    if a['asset_id']=='NEW_C08':a['on_screen_context']='Long Beach, 13 June 1976; identify once per continuous sequence; not the 1974 mission'
    if a['asset_id']=='NEW_C10':a['on_screen_context']='CIA Museum artifact photo, 2022; not contemporary shipboard footage'

bank={a['file'][:3]:a for a in readcsv(PROJECT/'VIDEO_ARCHIVE_R2/FULL_SCENES.csv')}
used=[]
def video(a,sid,start,duration=None):
    duration=float(a['end_seconds'])-float(a['start_seconds']) if duration is None else duration
    b=bank[sid];assert start+duration<=float(b['seconds'])+.001,(a['shot_id'],sid,start,duration,b['seconds'])
    assign(a,sid,'Подлинная запись операции 1974; показать наблюдаемое действие без домысла о невидимых деталях. Поздний монтаж и авторство остаются HOLD.','','ACTUAL_1974_OPERATION_NOT_JANUARY_TRIALS','1974 recovery recording; identify when used to explain the system outside the operation act')
    a['source_in_seconds']=round(start,6);a['source_out_seconds']=round(start+duration,6)
    a['original_working_in_seconds']=round(float(b['working_in'])+start,6);a['original_working_out_seconds']=round(float(b['working_in'])+start+duration,6)
    a['original_public_in_seconds']=round(float(b['source_youtube_in'])+start,6) if b.get('source_youtube_in') else ''
    a['original_public_out_seconds']=round(float(b['source_youtube_in'])+start+duration,6) if b.get('source_youtube_in') else ''
    a['source_visual_qc']='CONTACT_SHEET_AND_REPRESENTATIVE_FRAME_REVIEW; FULL_SELECTED_PLAYBACK_PENDING'
    used.append({'shot_id':a['shot_id'],'asset_id':sid,'source_in_seconds':a['source_in_seconds'],'source_out_seconds':a['source_out_seconds'],'seconds':round(duration,6),'working_in':a['original_working_in_seconds'],'working_out':a['original_working_out_seconds'],'rights':'V03_AUTHORSHIP_AND_EDIT_COMPONENT_HOLD' if sid not in ['S25','S26'] else 'V04_KXTV_AUTHORITY_HOLD'})

video_map={
'SH003':('S02',0),'SH007':('S02',3.22),'SH028':('S02',6.9),
'SH079':('S06',0),'SH085':('S09',0),'SH087':('S09',3.8),'SH088':('S09',13.56),
'SH089':('S08',0),'SH090':('S14',0),'SH091':('S15',0),'SH094':('S09',20.18),'SH095':('S09',28.46),
'SH096':('S15',9.23),'SH098':('S16',0),'SH099':('S21',0),'SH103':('S20',0),'SH104':('S21',2.84),
'SH106':('S23',0),'SH107':('S24',0)
}
new=[]
for a in rows:
    if a['shot_id'] in video_map:video(a,*video_map[a['shot_id']])
    if a['shot_id']=='SH100':
        assign(a,'V01','Подлинная церемония 1974. Без музыки и эффектов; не использовать её как кадры подъёма.','','BURIAL_1974','Burial at sea, 4 September 1974')
        a['source_in_seconds']=60.;a['source_out_seconds']=67.18
        used.append({'shot_id':a['shot_id'],'asset_id':'V01','source_in_seconds':60.,'source_out_seconds':67.18,'seconds':7.18,'working_in':60.,'working_out':67.18,'rights':'EXISTING_PD_CIA_EVIDENCE'})
    if a['shot_id']=='SH120':
        # Existing short reserve-fleet clip fits the actual post-mission fate, never construction.
        video(a,'S26',0)
        a['archive_semantics']='RESERVE_FLEET_1987_NOT_1976_EVENT';a['on_screen_context']='Suisun Bay, 1987'
    if a['shot_id']=='SH029':
        first=deepcopy(a);first['shot_id']='SH029a';first['end_seconds']=str(float(first['start_seconds'])+6);first['duration_seconds']='6'
        second=deepcopy(a);second['shot_id']='SH029b';second['start_seconds']=first['end_seconds'];second['duration_seconds']=str(round(float(second['end_seconds'])-float(second['start_seconds']),6))
        video(first,'S02',11.08);video(second,'S03',0);new.extend([first,second]);continue
    if a['shot_id']=='SH015':
        first=deepcopy(a);first['shot_id']='SH015a';first['end_seconds']=str(float(a['start_seconds'])+8.8);first['duration_seconds']='8.8'
        second=deepcopy(a);second['shot_id']='SH015b';second['start_seconds']=first['end_seconds'];second['duration_seconds']=str(round(float(second['end_seconds'])-float(second['start_seconds']),6))
        video(first,'S04',0);assign(second,'CIA_EXHIBIT_05','Подлинный опубликованный рисунок захвата сопоставляется с реально снятым механизмом.','O04_CAPTURE');new.extend([first,second]);continue
    if a['shot_id']=='SH040':
        first=deepcopy(a);first['shot_id']='SH040a';first['end_seconds']=str(float(a['start_seconds'])+7);first['duration_seconds']='7'
        second=deepcopy(a);second['shot_id']='SH040b';second['start_seconds']=first['end_seconds'];second['duration_seconds']='4.5'
        video(first,'S01',0);assign(second,'G02','Короткое объяснение ворот. Это схема принципа, не архивная съёмка январской аварии.');new.extend([first,second]);continue
    if a['shot_id']=='SH061':
        first=deepcopy(a);first['shot_id']='SH061a';first['end_seconds']=str(float(a['start_seconds'])+5);first['duration_seconds']='5'
        second=deepcopy(a);second['shot_id']='SH061b';second['start_seconds']=first['end_seconds'];second['duration_seconds']='3.76'
        video(first,'S09',32.66);assign(second,'DOC35','Подлинный отчёт об испытаниях. Съёмка целевого объекта относится к операции, не к испытаниям.');new.extend([first,second]);continue
    if a['shot_id']=='SH123':
        first=deepcopy(a);first['shot_id']='SH123a';first['end_seconds']=str(float(a['end_seconds'])-5.8);first['duration_seconds']=str(round(float(first['end_seconds'])-float(first['start_seconds']),6))
        second=deepcopy(a);second['shot_id']='SH123b';second['start_seconds']=first['end_seconds'];second['duration_seconds']='5.8'
        video(second,'S18',0);second['direction_ru']='Настоящая запись стыковки завершает объяснение входа снизу. Не утверждать видимость всего найденного содержимого.';new.extend([first,second]);continue
    new.append(a)
rows=new

# Some original R1 video assignments had no carefully authored source choice after revision.
# No stock/generation is made necessary just to increase runtime.
for a in rows:
    a['duration_seconds']=round(float(a['end_seconds'])-float(a['start_seconds']),6)
    a['proposed_start_frame_25fps']=round(float(a['start_seconds'])*25)
    a['proposed_end_frame_exclusive_25fps']=round(float(a['end_seconds'])*25)
    if a['visual_type']=='GENERATED_STILL':raise AssertionError('Unresolved mandatory generation '+a['shot_id'])
    if a['asset_id'].startswith('CIA_EXHIBIT_') and a['asset_id'] in ['CIA_EXHIBIT_05','CIA_EXHIBIT_08','CIA_EXHIBIT_11']:
        a['visual_type']='ARCHIVAL_DRAWING'
    if a['asset_id'] in ['SUN_PLATFORM','SUN_LAUNCH','SUN_DEPART']:
        a['publication_gate']='PERMISSION_HOLD_DO_NOT_RENDER_SOURCE';a['fallback_asset_id']='DOC19' if a['asset_id']!='SUN_LAUNCH' else 'DOC20'
    if a['asset_id']=='SEC2015':a['publication_gate']='SOURCE_CAPTURE_MISSING_USE_EXACT_FILING_ONLY'
    if a['asset_id'].startswith('DOC'):
        a['asset_local']=reg[a['asset_id']]['local_file']

# Fail visibly on gaps, duplicate temporal windows or out-of-bounds source trims.
for i,a in enumerate(rows):
    if i:assert abs(float(rows[i-1]['end_seconds'])-float(a['start_seconds']))<.00001
    assert a['duration_seconds']>0
for i,a in enumerate(used):
    for b in used[i+1:]:
        if a['asset_id']==b['asset_id']:
            assert min(a['source_out_seconds'],b['source_out_seconds'])-max(a['source_in_seconds'],b['source_in_seconds'])<.00001,(a,b)
bykind=defaultdict(float)
for a in rows:bykind[a['visual_type']]+=a['duration_seconds']
narration=816.96
archive_kinds=['VIDEO','PHOTO','PHOTO_DOCUMENT','DOCUMENT','ARCHIVAL_DRAWING']
archive_seconds=sum(bykind[k] for k in archive_kinds)
holds_seconds=sum(a['duration_seconds'] for a in rows if a['visual_type']=='VIDEO' and 'HOLD' in a['rights_or_production_status'])
summary={'base_commit':'49fb7e6f6630fb6a5ea4f9838283c9cdd0116c0a','owner_instruction_date':'2026-11-05','status':'ARCHIVE_FIRST_PLAN_REVISED_NOT_FINAL_FILM','shot_rows':len(rows),'narration_seconds':narration,'end_screen_seconds':20,'total_seconds':836.96,'primary_visual_seconds':dict(bykind),'planned_moving_archive_seconds':round(bykind['VIDEO'],3),'archival_primary_visual_seconds':round(archive_seconds,3),'archival_primary_visual_percent':round(100*archive_seconds/narration,2),'mandatory_generated_stills':0,'generated_video':0,'stock_selected':0,'motion_source_windows_unique':True,'overlays_are_counted_separately_from_primary_sources':True,'rights_holds_preserved':True,'moving_archive_rights_hold_seconds':round(holds_seconds,3),'full_av_review':False,'new_cleared_construction_or_trials_footage_found':False,'not_a_claim_of_video_dominance':True,'narration_unchanged':True,'fps':'25 proposed only; no timeline or frame rate lock created'}
writecsv(OUT/'EDIT_TIMELINE.csv',rows)
writecsv(OUT/'MOVING_ARCHIVE_CUTLIST.csv',used)
writecsv(OUT/'R1_TO_R2_ASSET_CHANGES.csv',changes)
(OUT/'ASSET_REGISTER.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'PLAN_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['PARAGRAPH_TIMING.csv','WORD_TIMING.csv','PHRASE_ALIGNMENT.csv','CTA_AND_ENDSCREEN_TIMING.csv','AUDIO_OWNER_ACCEPTANCE.json','SCRIPT_R1_2_EN.md','SCRIPT_R1_2_RU.md','MUSIC_CUE_MAP.csv','SFX_CUE_MAP.csv','SOUND_SOURCES_AND_LIMITS.md','ENDSCREEN_SPEC_RU.md','ENDSCREEN_LAYOUT_REVIEW_ONLY.svg']:
    if name=='ENDSCREEN_SPEC_RU.md' and (OUT/name).exists():continue
    shutil.copy2(OLD/name,OUT/name)
writecsv(OUT/'GENERATION_QUEUE.csv',[{'old_job_id':f'IG{i:02d}','status':'DEFERRED_NOT_REQUIRED_NOT_SUBMITTED','reason':'Use assigned original archival source in EDIT_TIMELINE.csv; reassess only if a specific visual gap survives source and edit review'} for i in range(1,8)])
writecsv(OUT/'OVERLAY_CUE_MAP.csv',[{'shot_id':a['shot_id'],'paragraph_id':a['paragraph_id'],'start_seconds':a['start_seconds'],'end_seconds':a['end_seconds'],'primary_source':a['asset_id'],'overlay_id':a['overlay_id'],'direction_ru':a['direction_ru'],'safe_zone':'bottom20 percent empty; verify readable source and actual output','status':'BRIEF_ONLY_NOT_RENDERED'} for a in rows if a['overlay_id']])
writecsv(OUT/'PARAGRAPH_TO_SHOTS.csv',[{'paragraph_id':pid,'start_seconds':min(float(a['start_seconds']) for a in rows if a['paragraph_id']==pid),'end_seconds':max(float(a['end_seconds']) for a in rows if a['paragraph_id']==pid),'shots':';'.join(a['shot_id'] for a in rows if a['paragraph_id']==pid),'primary_assets':';'.join(dict.fromkeys(a['asset_id'] for a in rows if a['paragraph_id']==pid))} for pid in dict.fromkeys(a['paragraph_id'] for a in rows)])
validation={'continuity':'PASS','unique_source_intervals':'PASS','same_accepted_narration':'PASS_UNCHANGED_TIMINGS_AND_FILES','generated_assets_submitted':0,'stock_substitutions':0,'removed_flash_seconds':.18,'timeline_created':False,'rights':'HOLD_UNCHANGED_UNTIL_EVIDENCE','picture_qc':'SAMPLED_SOURCE_ONLY_FULL_SEQUENCE_PENDING','end_screen_target':'HOLD_VERIFIED_PUBLISHED_PREVIOUS_STORY_NOT_SELECTED'}
(OUT/'VALIDATION.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
