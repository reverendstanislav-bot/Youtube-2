"""Copy the actual verified rough cut to the user's VIDEO 7 folder."""
from pathlib import Path
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parent
DEST=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\EDIT\R1_2026-10-27')
qc=json.loads((ROOT/'QC/PROXY_QC.json').read_text(encoding='utf-8'))
assert qc['technical_checks_pass'], 'Do not install a technical failure as ready'
native=json.loads((ROOT/'NATIVE_FINAL_READBACK.json').read_text(encoding='utf-8'))
assert native['project_saved'] and not native['render_active']
DEST.mkdir(parents=True,exist_ok=True)
sources=[Path(qc['file']),ROOT/'HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_CPU_FIXED.drp',ROOT/'SHOT_PLAN_R1.csv',ROOT/'BEATS_AUDIO_LOCKED.json',ROOT/'EDIT_PROVENANCE_AND_HOLDS.json',ROOT/'NATIVE_FINAL_READBACK.json',ROOT/'README.md',ROOT/'QC/PROXY_QC.json',ROOT/'ROUGH_CUT_QC_AND_DELIVERY_2026-10-27.md']
sources.extend(sorted((ROOT/'QC').glob('RENDERED_CONTACT_*.jpg')))
records=[]
for src in sources:
    dst=DEST/src.name;sha=hashlib.sha256(src.read_bytes()).hexdigest()
    actual=hashlib.sha256(dst.read_bytes()).hexdigest() if dst.is_file() else None
    if actual!=sha:shutil.copy2(src,dst);actual=hashlib.sha256(dst.read_bytes()).hexdigest()
    assert actual==sha
    records.append(dict(source=str(src),installed=str(dst),bytes=dst.stat().st_size,sha256=sha,copy_hash_verified=True))
(DEST/'READ_FIRST_RU.txt').write_text('''CAMP CENTURY — VIDEO007 — ВИЗУАЛЬНЫЙ ЧЕРНОВОЙ МОНТАЖ R1

Смотреть: HIA_VIDEO007_CAMP_CENTURY_R1_PROXY_720P25.mp4
Полный фильм: 18:14.720, 25 FPS. Это proxy 1280x720; монтажный таймлайн — 1920x1080.
В Resolve: проект YT2 Vid7, таймлайн HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_25FPS.
DRP — резервная копия проекта с исходными абсолютными путями; исходники остаются в репозитории и локальном архиве. Это не автономный media archive.
Оригинальная принятая озвучка не изменена. Диалоговых субтитров нет.

Готовы монтаж и черновая анимация. Финальные музыка, SFX и цвет не выполнены.
Техническая проверка — PROXY_QC.json. Привязки и источники — SHOT_PLAN_R1.csv.
Полный непрерывный просмотр с аудио и утверждение картинки владельцем ещё нужны; техническая проверка не заменяет их.
''',encoding='utf-8')
manifest=dict(status='ROUGH_PICTURE_REVIEW_PACKAGE_INSTALLED',destination=str(DEST),files=records,technical_checks_pass=True,full_continuous_av_review='PENDING',owner_approval='PENDING',publication_approved=False)
(DEST/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(ROOT/'INSTALLED_REVIEW_PACKAGE.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'destination':str(DEST),'files':len(records),'all_copy_hashes_verified':True}),flush=True)
