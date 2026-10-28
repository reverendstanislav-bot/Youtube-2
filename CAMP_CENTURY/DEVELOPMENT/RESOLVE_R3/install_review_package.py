"""Install the complete QC'd R3 and hash-check all copied files."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parent;DEST=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\EDIT\R3_2026-10-27')
qc=json.loads((ROOT/'QC/PROXY_QC.json').read_text());native=json.loads((ROOT/'NATIVE_FINAL_READBACK.json').read_text());visual=json.loads((ROOT/'QC/SAMPLED_VISUAL_REVIEW.json').read_text())
assert qc['technical_checks_pass'] and qc['encoded_video_frames']==27818 and native['project_saved'] and not native['render_active'] and visual['all_124_midpoint_samples_reviewed']
report=f'''# Camp Century R3 — complete picture review

The owner rejected R2. The explicit existing reference `CAMP_CENTURY_8_MOTION_TESTS_64S.mp4` is now restored through its original M01–M08 clips in the native Resolve timeline, with ten contextual placements. No new generation was performed.

Full MP4: `{qc['file']}`. Duration 18:32.720, 27,818 frames, 1920 × 1080 / 25 FPS. SHA-256 `{qc['sha256']}`. Native project `YT2 Vid7`, timeline `HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3_25FPS`; 124 picture items, one unchanged locked narration WAV and no subtitle track.

The first 62.24 seconds are reassembled to narration, the aircraft moves at its original source cadence, generic camera pushes are removed, and an 18-second previous-channel-video endscreen follows the complete narration. The old endscreen's baked Pluto-body crossfade is excluded. Adjacent repeated illustrated subcues are combined; some other still illustrations continue to recur for context and reading.

Full-file decode: {qc['full_decode']}; black events: {len(qc['black_events'])}. Original narration SHA-256 `{qc['narration_comparison']['locked_file_sha256']}`; unchanged: {qc['locked_wav_unchanged']}. Review AAC correlation {qc['narration_comparison']['correlation']:.8f}, lag {qc['narration_comparison']['lag_ms']} ms. Original narration length remains 1094.720 seconds; the appended 18 seconds are silent. AAC is not bit-identical PCM.

Seven contact sheets covering all 124 shot midpoint samples, ten actual-render four-point motion sequences, and native opening/aircraft/clean-end proofs were inspected. This does not establish full continuous real-time audiovisual screening or owner approval. Final colour, music and SFX remain not started. Publication approval is not claimed.

The existing rendered motion clips are native Resolve video media; their internal individual strokes were not claimed to be new Fusion nodes. Editable source plates/alpha objects and original animation source remain in the reference package. Document markers and retained inspection lenses remain native Fusion. DRP retains existing absolute paths, not a self-contained archive.

Use `SCRIPT_CHAPTER_BOUNDARIES.json` or `BEATS_AUDIO_LOCKED.json` for narration chapter timing; native export part boundaries are administrative splits and may cross a continuous illustrated view. All file copies in this package are hash-verified in PACKAGE_MANIFEST.json.
'''
(ROOT/'ROUGH_CUT_QC_AND_DELIVERY_2026-10-27.md').write_text(report,encoding='utf-8')
sources=[(Path(qc['file']),Path(qc['file']).name)]
for name in ['HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3.drp','README.md','ROUGH_CUT_QC_AND_DELIVERY_2026-10-27.md','SHOT_PLAN_R3.csv','SOURCE_AND_RIGHTS_REGISTER.csv','BEATS_AUDIO_LOCKED.json','SCRIPT_CHAPTER_BOUNDARIES.json','RESTORED_REFERENCE_MOTION.json','REFERENCE_SOURCE.json','NATIVE_FINAL_READBACK.json','EDIT_PROVENANCE_AND_HOLDS.json','ENDSCREEN_CLEANUP_READBACK.json']:
    sources.append((ROOT/name,Path(name)))
for pattern in ['QC/*.json','QC/RENDERED_CONTACT_*.jpg','QC/*_RENDERED_SEQUENCE.jpg','QC/motion/*_RENDERED_SEQUENCE.jpg']:
    for src in sorted(ROOT.glob(pattern)):sources.append((src,src.relative_to(ROOT)))
g=ROOT.parents[1]/'GRAPHICS/STAGE07_MOTION_READY_R1'
for i in range(1,9):
    src=g/'preview'/f'M{i:02}_MOTION_DEMO.mp4';sources.append((src,Path('RESTORED_MOTION_REFERENCE')/src.name))
for src in Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R3\PROOFS').glob('*.mp4'):sources.append((src,Path('SHORT_REVIEW_PROOFS')/src.name))
records=[]
for src,rel in sources:
    dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True);sha=hashlib.sha256(src.read_bytes()).hexdigest()
    actual=hashlib.sha256(dst.read_bytes()).hexdigest() if dst.is_file() else None
    if actual!=sha:shutil.copy2(src,dst);actual=hashlib.sha256(dst.read_bytes()).hexdigest()
    assert actual==sha
    records.append(dict(source=str(src),installed=str(dst),bytes=dst.stat().st_size,sha256=sha,copy_hash_verified=True))
(DEST/'READ_FIRST_RU.txt').write_text('''CAMP CENTURY — VIDEO007 — R3

Смотреть HIA_VIDEO007_CAMP_CENTURY_R3_PROXY_1080P25.mp4 — полный фильм 18:32.720, 1080p25.
Оригинальная принятая озвучка: 18:14.720, без изменений. Затем 18 секунд эндскрина.
Resolve: YT2 Vid7 / HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3_25FPS.
В RESTORED_MOTION_REFERENCE — именно исходные восемь анимационных сцен из указанного владельцем теста.
В SHORT_REVIEW_PROOFS — новое начало, пролёт самолёта и чистый эндскрин из Resolve.
Новой генерации не было. На повторных иллюстрациях отключены общие произвольные приближения.
DRP содержит существующие абсолютные пути: это checkpoint, не автономный архив всех исходников.

Техническая проверка и просмотр контрольных кадров выполнены. Полный непрерывный AV-просмотр и принятие владельцем ещё не выполнены. Финальные цвет, музыка и SFX не выполнены.
R1 и R2 отвергнуты; не использовать их для публикации.
''',encoding='utf-8')
manifest=dict(status='FULL_R3_PICTURE_REVIEW_INSTALLED',destination=str(DEST),files=records,all_copy_hashes_verified=True,technical_checks_pass=True,owner_approval='PENDING',full_continuous_av_review='NOT_COMPLETED',publication_approved=False)
(DEST/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(ROOT/'INSTALLED_REVIEW_PACKAGE.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
old=DEST.parent/'R2_2026-10-27'
if old.is_dir():(old/'OWNER_REJECTED_READ_FIRST.txt').write_text('R2 отвергнут владельцем. Текущая версия: ../R3_2026-10-27. Не использовать R2 для публикации.\n',encoding='utf-8')
print(json.dumps(dict(destination=str(DEST),files=len(records),all_copy_hashes_verified=True)),flush=True)
