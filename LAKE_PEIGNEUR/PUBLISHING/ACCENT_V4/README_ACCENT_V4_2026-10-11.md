# HIA Lake Peigneur — V4 Full Editorial Accent Map

> **EDITORIAL MAP ONLY. NOT A VIDEO RENDER OR OWNER APPROVAL.** All details below are keyed to the recovered V3 Remotion timeline. No credits, new images, TTS, or motion renders are authorized by this document.

Base V3 SHA256: `fbc8efae5ec482b1fd6719e359cd7d50d21ed3ea9b45e0fe7608c399e700b40d`.
87 beats, 99 V3 timeline slots, **100 visible source exposures** (runtime B001 uses LP-REC-001 frames 0–149 and LP-REC-018 frames 150–277). 25fps, 1920×1080. Approved end screen remains **frames 24211–24710 completely STATIC**.

**36 editorial accents:** 8 PUSH; 10 SPOT; 5 RING; 6 PATH; 4 DOCUMENT_FOCUS; 3 DATA_FOCUS. **57 HOLD, 7 QC_HOLD** appearances. Machine-readable full ledger is in [CSV](./HIA_LAKE_PEIGNEUR_V4_ACCENT_MAP_FULL.csv) and [JSON](./HIA_LAKE_PEIGNEUR_V4_ACCENT_MAP_MACHINE.json). All 100 visual source exposures (even ones with no effects) are mapped.

## P0 before animation: correct two existing Fact labels

- `facts.json` ~06:20.415–06:24.215 uses `65 ACRES`; confirmed historical final estimate is **~68 ACRES**, subject to cited-source recheck before export.
- `facts.json` ~10:16.270–10:20.070 uses `52 MINERS • 7 DRILLERS`; use source-grounded **52 PEOPLE UNDERGROUND • 7 DRILL WORKERS** (fit visually).
- **No dialogue subtitles at all**. No ASS/SRT overlays, karaoke or orange word tracking. Only approved HIA editorial labels, technical graphics and Chapter/Fact cards.

## Effect parameters — implement exactly

- `PUSH`: scale 1.0→`strength`→1.0 inside accent window, ease in/out 18 frames, ROI static origin from CSV, NO lateral pan. Peak ≤1.017. All transforms fully reset before source slot ends.
- `SPOT`: soft, feathered outside darkening max `strength` opacity, no black rings, no faces obscured.
- `RING`: thin 2px warm paper / faded rust ellipse along already existing source feature, 12-frame fades, no fake location.
- `PATH`: 2px trace **on existing sourced diagram/route only**, do not invent canal gates, arrows, maps or causal path. ROI is an approximate region; inspect true pixel path and reject a trace if source has no line.
- `DOCUMENT_FOCUS` / `DATA_FOCUS`: mild local exposure/color emphasis of existing document/number only; do not add new text, fake facts, or obscure current labels.
- `HOLD` preserves V3 picture; `QC_HOLD` has unresolved earlier image issue, forbidden from receiving accent until visually approved.
- All overlays below `Chapter/Fact` and are temporally disjoint from their windows; preserve V3 **18-frame cross-dissolves**, clean Arthur audio, final HIA source look.
- Frame columns are absolute source positions; **IN inclusive / OUT exclusive** (25fps, HH:MM:SS:FF). Six source IDs carry historical QC HOLD: `LP-REC-005`, `LP-REC-008`, `LP-REC-010`, `LP-REC-012`, `LP-REC-038`, `LP-REC-041`.

## Accents (verified to be inside source slots)

| Accent time IN → OUT | Beat / asset | Effect | Strength | Objective |
|---|---|---|---:|---|
| `00:00:00:15 → 00:00:05:15` | `LP-B001` / `LP-REC-001` | **PUSH** | 1.014 | Буровая; микронаезд на конструкцию, без движения камеры по X/Y |
| `00:00:17:05 → 00:00:22:10` | `LP-B002` / `LP-REC-003` | **SPOT** | 0.13 | Шахта: вода там, где её не должно быть; не перекрывать лица |
| `00:00:27:10 → 00:00:33:23` | `LP-B003` / `LP-GFX-001` | **RING** | 0.6 | Обозначить область подземных работников; без дополнительного текста |
| `00:00:35:13 → 00:00:46:04` | `LP-B004` / `LP-GFX-002` | **PATH** | 0.62 | Мягко выделить существующую геометрию течения на схеме; новых стрелок не добавлять |
| `00:01:17:00 → 00:01:27:22` | `LP-B008` / `LP-GFX-004` | **SPOT** | 0.13 | Соляной купол под поверхностью — показать слой, не легенду |
| `00:01:45:07 → 00:01:50:18` | `LP-B011` / `LP-GFX-006` | **RING** | 0.6 | Существующие поддерживающие целики room-and-pillar |
| `00:02:03:06 → 00:02:11:06` | `LP-B012` / `LP-GFX-008` | **DOCUMENT_FOCUS** | 0.15 | Уровни шахты; не закрывать глубины и подписи |
| `00:02:39:00 → 00:02:44:05` | `LP-B015` / `LP-GFX-010` | **SPOT** | 0.13 | Контакт пресной воды и соли |
| `00:03:14:10 → 00:03:20:08` | `LP-B017` / `LP-REC-013` | **PUSH** | 1.014 | Начало притока воды; без резкого приближения |
| `00:03:35:17 → 00:03:44:09` | `LP-B019` / `LP-REC-020` | **SPOT** | 0.12 | Рабочие в шахте — момент принятия решения |
| `00:04:06:09 → 00:04:12:17` | `LP-B022` / `LP-GFX-017` | **PATH** | 0.58 | Проследить только существующий коридор эвакуации; не рисовать новый выход |
| `00:04:26:04 → 00:04:35:18` | `LP-B024` / `LP-REC-019` | **PUSH** | 1.014 | Эвакуация — очень плавный push-in |
| `00:05:09:06 → 00:05:15:22` | `LP-B027` / `LP-REC-023` | **SPOT** | 0.13 | После факта о 52 выбравшихся; фокус на эвакуации |
| `00:05:45:10 → 00:05:57:21` | `LP-B031` / `LP-REC-028` | **PUSH** | 1.017 | Начало масштабного движения воды у поверхности |
| `00:06:10:04 → 00:06:19:10` | `LP-B033` / `LP-REC-030` | **PUSH** | 1.016 | Обрушение берега; строго центрированный аккуратный zoom |
| `00:06:28:21 → 00:06:39:11` | `LP-B035` / `LP-REC-031` | **SPOT** | 0.13 | Масштаб обрушения по реальной линии берега, без числовой плашки |
| `00:06:55:19 → 00:07:02:20` | `LP-B037` / `LP-GFX-021` | **RING** | 0.6 | Точка контакта воды и соли уже присутствует на источнике |
| `00:07:04:01 → 00:07:15:19` | `LP-B038` / `LP-GFX-022` | **PATH** | 0.64 | Действующий контур растворения — подсветить, а не перерисовать |
| `00:07:30:00 → 00:07:40:11` | `LP-B040` / `LP-GFX-026` | **PATH** | 0.57 | Цикл обратной связи по существующей схеме |
| `00:08:04:08 → 00:08:11:05` | `LP-B043` / `LP-GFX-029` | **SPOT** | 0.13 | Гравитация питает разрушение |
| `00:08:24:07 → 00:08:33:21` | `LP-B045` / `LP-GFX-030` | **RING** | 0.62 | Воронка на поверхности — лишь видимое проявление |
| `00:08:52:04 → 00:09:01:17` | `LP-B048` / `LP-GFX-033` | **PUSH** | 1.014 | Масштаб системы вода—шахта—порода, легенду оставить резкой |
| `00:09:11:11 → 00:09:17:18` | `LP-B050` / `LP-REC-037` | **SPOT** | 0.12 | Канал и берег до изменения направления течения |
| `00:09:33:13 → 00:09:43:01` | `LP-B052` / `LP-REC-036` | **PUSH** | 1.015 | Водопад — не создавать выдуманной измерительной стрелки |
| `00:09:55:00 → 00:10:06:17` | `LP-B054` / `LP-GFX-037` | **PATH** | 0.63 | Подчеркнуть действующий маршрут вода/канал, не добавлять затворы |
| `00:10:36:09 → 00:10:42:21` | `LP-B058` / `LP-GFX-039` | **DATA_FOCUS** | 0.13 | Ноль погибших; не менять 52 people на 52 miners |
| `00:11:19:01 → 00:11:26:09` | `LP-B062` / `LP-GFX-041` | **DOCUMENT_FOCUS** | 0.15 | Спорность координатной версии без представления её доказанным фактом |
| `00:11:52:08 → 00:12:01:10` | `LP-B065` / `LP-GFX-043` | **DOCUMENT_FOCUS** | 0.16 | Гипотеза пересечения кровли; сохранить статус disputed |
| `00:12:40:03 → 00:12:50:11` | `LP-B069` / `LP-GFX-047` | **DATA_FOCUS** | 0.15 | Точная первопричина не установлена однозначно |
| `00:13:32:01 → 00:13:43:13` | `LP-B074` / `LP-GFX-051` | **DATA_FOCUS** | 0.13 | Последствия для сотрудников; существующие проверенные данные |
| `00:14:14:00 → 00:14:24:14` | `LP-B078` / `LP-GFX-053` | **PATH** | 0.55 | Природный газ в соляных кавернах, существующая схема сети |
| `00:14:58:09 → 00:15:10:00` | `LP-B082` / `LP-GFX-042` | **RING** | 0.6 | Две отрасли в одном трёхмерном пространстве |
| `00:15:10:21 → 00:15:14:12` | `LP-B083` / `LP-REC-014` | **SPOT** | 0.11 | Заключение 1: затопление шахты |
| `00:15:19:04 → 00:15:22:13` | `LP-B083` / `LP-REC-039` | **SPOT** | 0.11 | Заключение 3: канал (промежуточный кадр берега без эффекта) |
| `00:15:46:21 → 00:15:56:21` | `LP-B086` / `LP-GFX-046` | **DOCUMENT_FOCUS** | 0.14 | Поверхность и скрытая инфраструктура — визуальный итог |
| `00:16:02:00 → 00:16:07:17` | `LP-B087` / `LP-REC-045` | **PUSH** | 1.012 | Очень мягкий финальный hold; ПОЛНОЕ завершение до approved end screen |

## Implementation & gates

1. Rebuild from the V3 exact Remotion `index.jsx` and `timeline.json`. Apply the 100-slot mapping including virtual opening split, not an old draft 97-slot plan.
2. Separate V4 AccentLayer using normalized ROI (relative 1920×1080); compositing beneath Chapter/Fact; no picture resize reset between shots. ROI is a precise proposal for QC — verify on the full-size approved source frame before final draw.
3. Preview 00:00–01:04, 05:35–07:40, 09:00–10:15 and 14:45–16:28. Inspect accent start/mid/end at native 1080p and boundary ±18 frames.
4. Verify every RING/PATH tracks an actual graphic detail; if not, mark local effect REJECT, revert just that slot to HOLD. No new GFX generations.
5. Confirm fact-label corrections, six historical conditional image cases, no visual/audio jump, no captions, original approved subscribe-only end screen unchanged.
6. **V4 render not yet executed.** Do not mark PUBLIC READY without picture QC, provenance and Unlisted transcoding.
