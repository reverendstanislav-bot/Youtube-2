from pathlib import Path
import json,shutil,csv,subprocess,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2];R3=REPO/'CAMP_CENTURY/DEVELOPMENT/RESOLVE_R3'
for folder in ['03_UPLOAD','04_THUMBNAIL_CANDIDATES','05_PROJECT_AND_QC','06_AUDIO']:(ROOT/folder).mkdir(exist_ok=True)
def put(folder,name,text):(ROOT/folder/name).write_text(text.rstrip()+'\n',encoding='utf-8')
title="The Army Built a Nuclear-Powered City Under Ice. It Couldn't Keep It Open."
assert len(title)<=100
put('03_UPLOAD','TITLE_EN.txt',title)
put('03_UPLOAD','TITLE_ALTERNATIVES_EN.txt',"Camp Century: Why the Army Couldn't Keep Its Nuclear City Open\nThe Nuclear-Powered City Beneath Greenland's Moving Ice")
chapters=json.loads((R3/'SCRIPT_CHAPTER_BOUNDARIES.json').read_text())
labels=['The City the Army Had to Keep Digging Out','An Entire City Arrived on Sleds','Building a Roof Inside Moving Ice','PM-2A: Nuclear Power Beneath the Snow','Project Iceworm: The Network That Was Never Built','The Maintenance Bill That Never Stopped','Shutdown, Removal and Burial','The Ice Core and the Buried Remains']
lines=[]
for c,label in zip(chapters,labels):
    sec=int(c['audio_start_seconds']);lines.append(f'{sec//60:02}:{sec%60:02} {label}')
chaptertext='\n'.join(lines);put('03_UPLOAD','CHAPTERS_EN.txt',chaptertext)
sources=[('U.S. Army / USACE, Camp Century construction film','https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34'),('U.S. Army Camp Century technical report, 1965','https://icedrill.org/sites/default/files/477706.pdf'),('Bierman et al., Camp Century scientific history and ice cores, 2024','https://tc.copernicus.org/articles/18/4029/2024/'),('Colgan et al., abandoned base and future remobilization scenario, 2016','https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016GL069688'),('Camp Century firn evolution study, 2021','https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.578978/full'),('NASA, New View of the City Under the Ice, 2024','https://science.nasa.gov/earth/earth-observatory/new-view-of-the-city-under-the-ice-153616/')]
description="""Camp Century was a real U.S. Army settlement beneath Greenland's ice, with heated corridors, workshops, living quarters and the PM-2A nuclear power plant. Keeping its tunnels open became a job that never ended.

This documentary follows the supply convoys, underground construction, moving snow, reactor removal and surviving evidence. It separates the camp that was actually built from Project Iceworm's proposed missile network, which was never completed.

From Cold War Army films to the 1966 ice core and NASA's 2024 radar images, Hidden Industrial America follows what the surviving records show—and what they don't.

CHAPTERS
"""+chaptertext+"\n\nSOURCES AND FURTHER READING\n"+'\n'.join(label+'\n'+url for label,url in sources)+"""

VISUAL NOTE
The film combines historical Army footage with generated explanatory illustrations and animated diagrams. Illustrations are not original archival photographs or measured survey drawings. Forecast scenarios are distinguished from observed events.

#CampCentury #Greenland #HiddenIndustrialAmerica
"""
assert len(description)<=5000;put('03_UPLOAD','DESCRIPTION_EN.txt',description)
tags='Camp Century, Project Iceworm, Greenland, Hidden Industrial America, Cold War history, US Army, PM-2A, nuclear power plant, city under the ice, Greenland ice sheet, ice core, NASA radar, military history, engineering documentary, abandoned infrastructure, historical documentary'
assert len(tags)<=500;put('03_UPLOAD','TAGS_EN.txt',tags)
put('03_UPLOAD','RESEARCH_SOURCE_LINKS.txt','\n\n'.join(label+'\n'+url for label,url in sources)+'\n\nResearch links are not a substitute for the per-shot rights register in 05_PROJECT_AND_QC/SOURCE_PROVENANCE.')
put('03_UPLOAD','UPLOAD_INSTRUCTIONS_RU.txt',"""VIDEO007 — CAMP CENTURY — ПАКЕТ R3

1. Основной файл: 01_LONG/HIA_VIDEO007_CAMP_CENTURY_R3_1080P25.mp4 — 18:32.720, 1920×1080, 25 FPS. Копия полного проверенного R3; без нового рендера и без вшитых субтитров.
2. TITLE_EN.txt — выбранное основное название. DESCRIPTION_EN.txt — готовое описание с восемью главами и источниками. TAGS_EN.txt — теги. Дополнительные варианты названия лежат отдельно и не входят в основное поле.
3. Язык видео и субтитров — English. В субтитрах загрузить 02_SUBTITLES/CAMP_CENTURY_EN.srt как файл с таймкодами. VTT — альтернативный формат; загружать оба файла в одну языковую дорожку не нужно. Текст соответствует утверждённому V4.
4. В 04_THUMBNAIL_CANDIDATES — четыре JPG из существующих иллюстраций Camp Century. Это варианты исходной картинки для выбора, не новая утверждённая обложка. Чужие обложки Pluto не использованы.
5. Эндскрин уже находится в видео: 18:14.720–18:32.720. В левую рамку назначить предыдущее видео канала VIDEO006 — Project Pluto, в круг справа — подписку Hidden Industrial America. Совместить интерактивные элементы вручную в Studio. Образец: ENDSCREEN_REFERENCE.jpg; отдельный просмотр: ENDSCREEN_18S_PREVIEW.mp4.
6. Учесть фактическое использование сгенерированных поясняющих иллюстраций при ответе на вопрос Studio об изменённом/синтетическом контенте. Иллюстрации не выдаются за архивные фотографии.
7. Перед публикацией просмотреть фильм со звуком и выборочно сверить субтитры, особенно интервалы, отмеченные в SUBTITLE_QC.json. Полная техническая проверка видео пройдена; полный непрерывный AV-просмотр не подтверждён. Исходная принятая озвучка сохранена. Финальные музыка, SFX и цвет ещё не выполнены; пакет содержит текущий R3.
8. Источники и правовые основания каждого архивного кадра: 05_PROJECT_AND_QC/SOURCE_PROVENANCE. Исследовательские ссылки не заменяют права на конкретные материалы. Публикация и загрузка в YouTube этим пакетом не выполнялись.

Официальные справки форматов и глав, проверены 2026-10-27:
https://support.google.com/youtube/answer/2734698?hl=en
https://support.google.com/youtube/answer/9884579?hl=en

R1 и R2 отвергнуты владельцем. Для текущей загрузки использовать только файл R3 из 01_LONG. DRP — checkpoint с существующими абсолютными путями, не автономный архив всего видеофонда.
""")
assets=[('01_CITY_UNDER_ICE.jpg',REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATED_R1/images/G01_DRAFT_R1.png'),('02_WORKERS_IN_TUNNEL.jpg',REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATED_R1/images/G07_REVISED_R2.png'),('03_AIRCRAFT_AND_BURIED_CAMP.jpg',REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATED_R1/images/G10_REVISED_R2.png'),('04_PEOPLE_AND_REMAINS.jpg',REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_MOTION_READY_R1/keyframes/M08_04.0s.jpg')]
records=[]
for name,src in assets:
    im=Image.open(src).convert('RGB');dest=ROOT/'04_THUMBNAIL_CANDIDATES'/name;im.save(dest,quality=92,optimize=True);assert dest.stat().st_size<2_000_000
    records.append(dict(file=name,source=str(src),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),classification='Existing generated illustration, not archival photo',owner_selection='PENDING'))
put('04_THUMBNAIL_CANDIDATES','README_RU.txt','Четыре JPG-кандидата из уже существующих иллюстраций Camp Century. Новая генерация не запускалась. Это исходные изображения для выбора обложки; финальная обложка владельцем ещё не назначена.')
(ROOT/'04_THUMBNAIL_CANDIDATES/SOURCE_MANIFEST.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
put('05_PROJECT_AND_QC','PACKAGE_STATUS_RU.txt','Текущий пакет: R3. Видео технически проверено; полный непрерывный AV-просмотр и окончательное принятие картинки не подтверждены. Субтитры сохраняют весь текст V4, имеют реальную ASR-привязку и локальную medium.en-проверку пропущенной фразы; оставшиеся интервалы интерполяции указаны в аудите. Финальные музыка, SFX и цвет не выполнены. Упаковка не является публикацией или юридическим заключением.')
meta=dict(title=title,title_characters=len(title),description_characters=len(description),tags_characters=len(tags),chapters=8,video='01_LONG/HIA_VIDEO007_CAMP_CENTURY_R3_1080P25.mp4',subtitles='02_SUBTITLES/CAMP_CENTURY_EN.srt',language='en',revision='R3',endscreen_start_seconds=1094.72,endscreen_end_seconds=1112.72,publication_performed=False)
(ROOT/'03_UPLOAD/UPLOAD_METADATA.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
for extension in ['srt','vtt']:subprocess.run(['ffmpeg','-v','error','-i',str(ROOT/'02_SUBTITLES'/('CAMP_CENTURY_EN.'+extension)),'-f','srt','-'],stdout=subprocess.DEVNULL,check=True)
print(json.dumps(meta),flush=True)
