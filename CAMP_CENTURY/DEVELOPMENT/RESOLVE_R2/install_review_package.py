"""Install only the QC'd complete R2; verify every copied byte by SHA-256."""
from pathlib import Path
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parent
DEST=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\EDIT\R2_2026-10-27')
G=ROOT.parents[1]/'GRAPHICS/STAGE07_CORRECTIONS_R3'
REPO=ROOT.parents[2]
qc=json.loads((ROOT/'QC/PROXY_QC.json').read_text())
assert qc['technical_checks_pass'] and qc['encoded_video_frames']==27368
native=json.loads((ROOT/'NATIVE_FINAL_READBACK.json').read_text())
assert native['project_saved'] and not native['render_active']
review=json.loads((ROOT/'QC/SAMPLED_VISUAL_REVIEW.json').read_text())
assert review['all_132_midpoint_samples_reviewed']
assert review['owner_approval']=='PENDING'
sources=[(Path(qc['file']),Path(qc['file']).name)]
for name in ['HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2.drp','SHOT_PLAN_R2.csv','SOURCE_AND_RIGHTS_REGISTER.csv','BEATS_AUDIO_LOCKED.json','EDIT_PROVENANCE_AND_HOLDS.json','NATIVE_FINAL_READBACK.json','README.md','ROUGH_CUT_QC_AND_DELIVERY_2026-10-27.md','NATIVE_HIGHLIGHT_AUDIO_ALIGNMENT.json','ADDITIONAL_ARCHIVE_PLACEMENTS.json']:
    sources.append((ROOT/name,name))
for pattern in ['QC/*.json','QC/RENDERED_CONTACT_*.jpg','QC/motion/*_RENDERED_SEQUENCE.jpg']:
    for src in sorted(ROOT.glob(pattern)):sources.append((src,src.relative_to(ROOT)))
for rec in json.loads((G/'SELECTED_GENERATION_RECORDS.json').read_text()):
    src=REPO/rec['file'];sources.append((src,Path('SELECTED_CLEAN_ARTWORK')/src.name))
for name in ['SELECTED_GENERATION_RECORDS.json','ASSET_MANIFEST.csv','OWNER_STYLE_LOCK_R3.md','SELECTED_BASES_CONTACT_SHEET.jpg']:
    sources.append((G/name,Path('SELECTED_CLEAN_ARTWORK')/name))
records=[]
for src,rel in sources:
    dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    sha=hashlib.sha256(src.read_bytes()).hexdigest()
    actual=hashlib.sha256(dst.read_bytes()).hexdigest() if dst.is_file() else None
    if actual!=sha:shutil.copy2(src,dst);actual=hashlib.sha256(dst.read_bytes()).hexdigest()
    assert actual==sha,(src,dst)
    records.append(dict(source=str(src),installed=str(dst),bytes=dst.stat().st_size,sha256=sha,copy_hash_verified=True))
(DEST/'READ_FIRST_RU.txt').write_text('''CAMP CENTURY — VIDEO007 — ПОЛНЫЙ ВИЗУАЛЬНЫЙ R2

Смотреть HIA_VIDEO007_CAMP_CENTURY_R2_PROXY_1080P25.mp4
18:14.720, 1920×1080, 25 FPS. Без диалоговых субтитров.
Принятая озвучка сохранена без изменений. В review MP4 звук кодирован AAC.

Resolve: YT2 Vid7 / HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2_25FPS.
DRP — checkpoint проекта с существующими абсолютными путями, а не автономный media archive.
Чистые сгенерированные иллюстрации лежат в SELECTED_CLEAN_ARTWORK.
Жёлтые акценты и лупы находятся отдельно в Fusion, не в PNG.
Таблица источников, кадров и прав: SOURCE_AND_RIGHTS_REGISTER.csv.

R1 отвергнут владельцем. Текущий R2 предназначен для просмотра и оценки картинки.
Технический QC и выборочная визуальная проверка выполнены отдельно.
Полный непрерывный просмотр с аудио и принятие владельцем ещё не выполнены.
Финальные музыка, SFX и цвет пока не выполнены. Это не публикационный master.
''',encoding='utf-8')
manifest=dict(status='FULL_R2_PICTURE_REVIEW_INSTALLED',destination=str(DEST),files=records,technical_checks_pass=True,all_copy_hashes_verified=True,owner_approval='PENDING',full_continuous_av_review='NOT_COMPLETED',publication_approved=False)
(DEST/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(ROOT/'INSTALLED_REVIEW_PACKAGE.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
old=DEST.parent/'R1_2026-10-27'
if old.is_dir():(old/'OWNER_REJECTED_READ_FIRST.txt').write_text('R1 отвергнут владельцем. Не использовать для публикации. Текущая исправленная версия находится в ../R2_2026-10-27. Старые материалы оставлены для восстановления и аудита.\n',encoding='utf-8')
print(json.dumps(dict(destination=str(DEST),files=len(records),all_copy_hashes_verified=True)),flush=True)
