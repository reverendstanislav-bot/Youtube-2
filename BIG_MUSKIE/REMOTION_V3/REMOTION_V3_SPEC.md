# BIG MUSKIE — CANONICAL REMOTION PICTURE V3 SPEC

Status: **BUILD IN PROGRESS / SOURCE LOCKED**

Purpose: implement the approved Picture V2 direction as a clean native Remotion picture timeline before RC.

## Hard locks

- 1920×1080
- 25 fps
- 35,660 frames
- 23:46.400
- no paid generation
- no shake
- no lateral pan / oscillation
- no aggressive zoom
- no captions/music/SFX in this picture-only pass

## V2 QC fixes implemented

- all 116 beats own picture continuously through the next beat start;
- eliminates the 13 V2 patch-boundary defects by construction;
- exact 25 fps frame quantization;
- accepted replacements: FX001 / FX002 / FX013 / FX016 / FX033 / FX036 / FX045 / FX047 / FX048 / FX049;
- B038/B041 D03 close engineering crops;
- B051/B052 D04 close walking/stepping crops;
- B076 simplified to a three-step failure chain;
- B033–B040 reframe plan breaks machine-shot monotony without new assets;
- B102/B104, B105/B107, B109/B112 use distinct reframes;
- dense GFX runs use restrained focus staging, not camera travel;
- final B116 gets only a ≤1% slow push.

## Transition language

- base language: clean cut;
- default documentary transition: 4-frame total micro dissolve;
- dense information sequences: 6-frame total micro dissolve;
- B033–B040 machine-action run: no dissolve to avoid doubled machinery.

## Media boundary

The Remotion source expects:
- `public/beats/beat_001.png` … `beat_116.png` captured from the approved V2 picture master;
- ten accepted replacement PNGs by FX ID.

The beat captures are 1080p picture-source material only; canonical Arthur audio is muxed unchanged after picture render.
