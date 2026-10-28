"""Install the Pluto-shaped package; preserve existing AUDIO and EDIT folders."""
from pathlib import Path
import json,shutil,hashlib,csv,subprocess
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2];R3=REPO/'CAMP_CENTURY/DEVELOPMENT/RESOLVE_R3'
DEST=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7')
qc=json.loads((R3/'QC/PROXY_QC.json').read_text());assert qc['technical_checks_pass']
sub=json.loads((ROOT/'05_PROJECT_AND_QC/SUBTITLE_QC.json').read_text());assert sub['exact_locked_v4_text_preserved'] and sub['endscreen_captions']==0
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as fp:
        for block in iter(lambda:fp.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()
sources=[]
sources.append((Path(qc['file']),Path('01_LONG/HIA_VIDEO007_CAMP_CENTURY_R3_1080P25.mp4')))
for folder in ['02_SUBTITLES','03_UPLOAD','04_THUMBNAIL_CANDIDATES','05_PROJECT_AND_QC']:
    for f in sorted((ROOT/folder).rglob('*')):
        if f.is_file():sources.append((f,f.relative_to(ROOT)))
for name in ['HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3.drp','SHOT_PLAN_R3.csv','NATIVE_FINAL_READBACK.json','BEATS_AUDIO_LOCKED.json','SCRIPT_CHAPTER_BOUNDARIES.json','RESTORED_REFERENCE_MOTION.json','REFERENCE_SOURCE.json','EDIT_PROVENANCE_AND_HOLDS.json','ENDSCREEN_CLEANUP_READBACK.json','ROUGH_CUT_QC_AND_DELIVERY_2026-10-27.md']:
    sources.append((R3/name,Path('05_PROJECT_AND_QC')/name))
for f in (R3/'QC').glob('*.json'):sources.append((f,Path('05_PROJECT_AND_QC/VIDEO_QC')/f.name))
sources.append((R3/'SOURCE_AND_RIGHTS_REGISTER.csv',Path('05_PROJECT_AND_QC/SOURCE_PROVENANCE/SOURCE_AND_RIGHTS_REGISTER.csv')))
with (R3/'SOURCE_AND_RIGHTS_REGISTER.csv').open(encoding='utf-8-sig') as fp:rows=list(csv.DictReader(fp))
for value in sorted({x.get('rights_receipt','') for x in rows}-{''}):
    f=Path(value);assert f.is_file();sources.append((f,Path('05_PROJECT_AND_QC/SOURCE_PROVENANCE/RIGHTS_RECEIPTS')/f.name))
for name in ['STAGE04_CAMP_CENTURY_FULL_NARRATION_V4_EN.md','STAGE04_CAMP_CENTURY_VOICE_TEXT_V4_EN.txt','STAGE04_CAMP_CENTURY_CLAIM_LEDGER_V1.csv','STAGE04_FINAL_FACT_EDITORIAL_LEGAL_QC_2026-10-24.md','STAGE05_SCRIPT_LOCK_V4_2026-10-25.md']:
    sources.append((REPO/'CAMP_CENTURY/SCRIPT'/name,Path('05_PROJECT_AND_QC/SCRIPT_LOCK')/name))
audio=DEST/'AUDIO/VOICEBOX_ARTHUR_V1'
sources.extend([(audio/'AUDIO_LOCK_2026-10-27.md',Path('06_AUDIO/AUDIO_LOCK_2026-10-27.md')),(audio/'HIA_VIDEO007_CAMP_CENTURY_ARTHUR_MASTER_48K_MONO_S24.wav',Path('06_AUDIO/HIA_VIDEO007_CAMP_CENTURY_ARTHUR_MASTER_48K_MONO_S24.wav'))])
sources.append((R3/'ASSETS/HIA_CLEAN_PREVIOUS_ENDSCREEN_18S.mp4',Path('03_UPLOAD/ENDSCREEN_18S_PREVIEW.mp4')))
records=[]
for src,rel in sources:
    assert src.is_file(),str(src);dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    expected=qc['sha256'] if str(rel).startswith('01_LONG/') else sha(src)
    actual=sha(dst) if dst.is_file() else None
    if actual!=expected:shutil.copy2(src,dst);actual=sha(dst)
    assert actual==expected,(src,dst)
    records.append(dict(path=rel.as_posix(),bytes=dst.stat().st_size,sha256=expected,copy_hash_verified=True))
    if str(rel).startswith('01_LONG/'):print('MAIN_VIDEO_INSTALLED_AND_HASH_VERIFIED',flush=True)
ref=DEST/'03_UPLOAD/ENDSCREEN_REFERENCE.jpg'
subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(DEST/'03_UPLOAD/ENDSCREEN_18S_PREVIEW.mp4'),'-frames:v','1','-q:v','2',str(ref)],check=True)
records.append(dict(path=ref.relative_to(DEST).as_posix(),bytes=ref.stat().st_size,sha256=sha(ref),copy_hash_verified=True))
readme=DEST/'00_НАЧНИ_ЗДЕСЬ.txt'
readme.write_text(f'''VIDEO007 — CAMP CENTURY — ПАКЕТ R3

01_LONG — основное видео 18:32.720, 1920×1080, 25 FPS.
02_SUBTITLES — английские SRT и VTT, точный текст утверждённой озвучки V4. {sub['cues']} реплика, {sub['script_words_whitespace']} слов. Субтитры отдельные, не вшитые.
03_UPLOAD — название, описание с восемью главами, теги, источники, инструкция, образец и видео эндскрина.
04_THUMBNAIL_CANDIDATES — четыре JPG-кандидата из существующих иллюстраций Camp Century; выбор владельца.
05_PROJECT_AND_QC — проект Resolve, таймкоды, сценарий, факты, источник каждого кадра, правовые основания и отчёты проверки.
06_AUDIO — принятый исходный WAV и AUDIO LOCK, без изменений.

НАЧАТЬ С 03_UPLOAD/UPLOAD_INSTRUCTIONS_RU.txt.
Для текущей загрузки брать 01_LONG/HIA_VIDEO007_CAMP_CENTURY_R3_1080P25.mp4.
R1/R2 отвергнуты. AUDIO и EDIT сохранены как рабочие архивы, не перепутать их старые версии с основным файлом.
SHA256SUMS.txt проверяет файлы текущего пакета. PACKAGE_MANIFEST.json — состав и фактические хеши.

Технический QC видео пройден. Финальный непрерывный просмотр фильма и субтитров ещё нужен. Музыка, SFX и финальный цвет не выполнены; здесь сохранён текущий R3. Нового рендера, TTS или генерации изображений для упаковки не было. Загрузка и публикация в YouTube не выполнялись.
''',encoding='utf-8')
records.append(dict(path=readme.name,bytes=readme.stat().st_size,sha256=sha(readme),copy_hash_verified=True))
assert sha(DEST/'01_LONG/HIA_VIDEO007_CAMP_CENTURY_R3_1080P25.mp4')==qc['sha256']
assert sha(DEST/'06_AUDIO/HIA_VIDEO007_CAMP_CENTURY_ARTHUR_MASTER_48K_MONO_S24.wav')=='c6a5df8cff089418f4f2300551fd4ba6cb057dcd3012b84fa8143e02976d0480'
manifest=dict(project='HIA VIDEO007 CAMP CENTURY',revision='R3',date='2026-10-27',destination=str(DEST),video_duration_seconds=1112.72,subtitle_cues=sub['cues'],script_words=2931,chapters=8,files=records,all_copy_hashes_verified=True,video_reencoded=False,audio_lock_unchanged=True,uploaded_to_youtube=False,full_continuous_av_review='PENDING',subtitle_timing_review='PENDING',thumbnail_owner_selection='PENDING',final_color_music_sfx='NOT_STARTED')
(DEST/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(ROOT/'INSTALLED_PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
hashlines=[r['sha256']+'  '+r['path'] for r in records];hashlines.append(sha(DEST/'PACKAGE_MANIFEST.json')+'  PACKAGE_MANIFEST.json')
(DEST/'SHA256SUMS.txt').write_text('\n'.join(hashlines)+'\n',encoding='utf-8')
print(json.dumps(dict(destination=str(DEST),files=len(records),all_copy_hashes_verified=True,subtitles=sub['cues'],chapters=8,video_sha256=qc['sha256'])),flush=True)
