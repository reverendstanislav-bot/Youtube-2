# TC497 — CURRENT HANDOFF / FINAL MASTER READY

## PROJECT STATUS

Episode: LeTourneau TC-497 Overland Train  
Project: Hidden Industrial America / YouTube-2

Current state: **FULL_V9 EDIT WAS EXPLICITLY APPROVED BY THE USER. A FRESH 1920×1080 UPLOAD MASTER HAS BEEN BUILT AND PASSED FINAL RELEASE QC.**

Creative edit is locked unless the user explicitly reopens it.

## APPROVED EDIT

Approved review version:
- FULL_V9
- review run: `35427554323`
- artifact: `tc497-full-v9-review-fast`
- artifact id: `10579472633`

User approval instruction:
`V9 → свежий 1920×1080 upload master → финальный QC изображения/аудио/субтитров → YouTube.`

## FINAL 1080 MASTER

Preferred master:
- workflow: `Build TC497 FINAL V9 1080 Surgical Master`
- run: `35429775249`
- artifact: `tc497-final-v9-upload-master-1080-surgical`
- artifact id: `10581035854`
- artifact digest: `sha256:56518a28f53d2a908161a83bc3d26b333035ccbbfab13e118e954b830d9a719b`
- file: `TC497_FINAL_UPLOAD_MASTER_V9_1920x1080.mp4`
- file size: `202105388` bytes
- duration: `1236.533333` sec / 20:36.533
- video: 1920×1080, H.264 High, yuv420p, 30 fps
- exact frame count: `37096`
- audio: AAC-LC 48 kHz stereo

Reference:
- `TC497/FINAL_V9/FINAL_RELEASE_QC.md`
- `TC497/FINAL_V9/render_surgical_chunk.py`
- `.github/workflows/build_tc497_final_v9_1080_surgical.yml`

## FINAL QC RESULT

PASS.

Audio is bit-for-bit inherited from approved FULL_V9:
`7954f3218e07a86ec57aa98e2744eabeab4cc4349e32233768b3df77d5ea2aff`

Measured:
- integrated loudness: -13.5 LUFS
- LRA: 3.7 LU
- true peak: -1.9 dBFS

Picture:
- 1920×1080 assertion passed;
- 30 fps assertion passed;
- 37,096-frame assertion passed;
- full decode passed;
- black-frame scan found no blackdetect events;
- changed scenes and ending were visually compared with FULL_V9 and match the approved review composition.

Subtitles / provenance:
- V6 Electric Wheel replacement captions restored;
- V9 replacement captions restored;
- all six replacement stills explicitly show RECONSTRUCTION provenance;
- V8 ending removes the old centered slogan and CTA captions;
- approved HIDDEN INDUSTRIAL AMERICA / TC-497 / OVERLAND TRAIN end identity is present.

## WHY THE SURGICAL MASTER IS PREFERRED

The final master does not upscale the 960×540 review.

It starts from the prior native-1080 picture master. Unchanged native-1080 sections are stream-copied. Only four windows are re-encoded:
- 208.000–245.700
- 757.933–834.533
- 1019.033–1071.433
- 1181.833–end

This minimizes additional H.264 generation loss while reproducing all approved V6/V8/V9 changes.

## NEXT STEP

Platform publication to YouTube.

There is no direct YouTube upload connector available in the current chat toolset. If continuing inside ChatGPT, use Work mode / Cloud Browser with the final master and upload metadata, or upload the preferred master manually in YouTube Studio.

Do not rebuild or revise the film before upload unless the user explicitly asks to reopen the edit.

## ONE-LINE NEW CHAT COMMAND

Open `TC497/CURRENT_STATUS_HANDOFF.md` in `reverendstanislav-bot/Youtube-2`. FULL_V9 is approved, final 1920×1080 surgical master run `35429775249` passed release QC, and the only remaining step is YouTube publication.
