# Chicago source text/build/subtitle audit

- Extracted text/project files: **189**
- Files with relevant keyword matches: **66**

## Relevant files and excerpts

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/00_START_HERE/FINAL_AUDIT.txt\`
Keywords: subtitle, ass
- L10: Subtitle rows: 293
- L12: Archive unique assets: 13
- L13: Music assets: 7
- L14: SFX assets: 3
- L15: Structure validator: PASS
- L16: Ready validator: expected FAIL until DOWNLOAD and GENERATE assets are populated.
- L19: Fact text overlays moved to V4 so V5 subtitle rows never conflict with another simultaneous V5 element.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/00_START_HERE/master_assets.csv\`
Keywords: ass
- L1: asset_id;mode;kind;destination;download_url;source_page;license;prompt_id;status
- L2: A01;DOWNLOAD;archive;10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelIntersectionCloser.jpg;https://commons.wikimedia.org/wiki/File:IllinoisTunnelIntersectionCloser.jpg;Public domain in the United States;;MISSING_UNTIL_DOWNLOADED
- L3: A02;DOWNLOAD;archive;10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelMap1910.png;https://commons.wikimedia.org/wiki/File:IllinoisTunnelMap1910.png;Public domain in the United States;;MISSING_UNTIL_DOWNLOADED
- L4: A14;DOWNLOAD;archive;10_ASSETS_WORK/archive/A14_LOC_State_Street_1905.jpg;https://cdn.loc.gov/service/pnp/det/4a10000/4a12000/4a12800/4a12894r.jpg;https://www.loc.gov/item/2016805496/;Library of Congress: No known restrictions on publication;;MISSING_UNTIL_DOWNLOADED
- L5: A13;DOWNLOAD;archive;10_ASSETS_WORK/archive/A13_LOC_State_Street_1903.jpg;https://cdn.loc.gov/service/pnp/stereo/1s10000/1s12000/1s12700/1s12706v.jpg;https://www.loc.gov/item/2014650313/;Library of Congress: No known restrictions on publication;;MISSING_UNTIL_DOWNLOADED
- L6: A15;DOWNLOAD;archive;10_ASSETS_WORK/archive/A15_LOC_Wabash_Avenue_c1900.jpg;https://cdn.loc.gov/service/pnp/det/4a00000/4a08000/4a08100/4a08136v.jpg;https://www.loc.gov/item/2016799520/;Library of Congress: No known restrictions on publication;;MISSING_UNTIL_DOWNLOADED
- L7: A08;DOWNLOAD;archive;10_ASSETS_WORK/archive/A08_IllinoisTelephoneAndTelegraphAd.png;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTelephoneAndTelegraphAd.png;https://commons.wikimedia.org/wiki/File:IllinoisTelephoneAndTelegraphAd.png;Public domain in the United States;;MISSING_UNTIL_DOWNLOADED
- L8: A05;DOWNLOAD;archive;10_ASSETS_WORK/archive/A05_IllinoisTunnelConstruction.jpg;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelConstruction.jpg;https://commons.wikimedia.org/wiki/File:IllinoisTunnelConstruction.jpg;"Public domain; Commons Public Domain Mark / life+70 note";;MISSING_UNTIL_DOWNLOADED

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/00_START_HERE/master_assets.json\`
Keywords: ass
- L3: "asset_id": "A01",
- L6: "destination": "10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg",
- L14: "asset_id": "A02",
- L17: "destination": "10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png",
- L25: "asset_id": "A14",
- L28: "destination": "10_ASSETS_WORK/archive/A14_LOC_State_Street_1905.jpg",
- L36: "asset_id": "A13",
- L39: "destination": "10_ASSETS_WORK/archive/A13_LOC_State_Street_1903.jpg",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/03_TIMELINE/subtitles_en.srt\`
Keywords: ass, burn
- L95: And once that coal was burned, the ash had to be removed.
- L115: That made the space beneath the streets valuable for a reason that had nothing to do with passengers.
- L183: A project associated with underground communications infrastructure had evolved into an urban freight
- L199: The tunnel railroad used tiny cars running through confined underground passages.
- L299: The easiest way to underestimate Chicago’s freight tunnels is to picture one long underground passage.
- L435: Then, after the coal was burned, the waste had to leave.
- L463: The system was not trying to be a glamorous replacement for passenger rail.
- L651: Chicago’s passenger subway arrived while the freight tunnels were still operating.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_FINAL/EDIT_REPORT.md\`
Keywords: subtitle, srt, ass, narration, timing
- L6: Subtitle status: PASS; English sidecar SRT, 320 cues, maximum two lines; retimed to unchanged narration and checked at five points.
- L7: Brand assets used: 03 Documentary Title Card; 06 End Screen (last 18 seconds).
- L8: Critical corrections made: repaired original 3–4-second variable subtitle drift; aligned scene timing; remapped generated-media paths; replaced 17 misleading technical/map or baked-editorial-text images using existing library sources; labeled reconstructions.
- L9: QC result: PASS. Full decode successful, no detected black intervals, no missing timeline media, audio within target; sampled visuals and end screen verified.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt\`
Keywords: ass, burn
- L117: And once that coal was burned,
- L146: had nothing to do with passengers.
- L226: A project associated with underground
- L246: confined underground passages.
- L390: long underground passage.
- L562: burned, the waste had to leave.
- L602: glamorous replacement for passenger rail.
- L830: Chicago’s passenger subway arrived while

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_QC/final_ffprobe.json\`
Keywords: caption, final_upload
- L53: "captions": 0,
- L106: "captions": 0,
- L120: "filename": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_FINAL\\HIA_CHICAGO_FINAL_UPLOAD.mp4",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_QC/final_qc.json\`
Keywords: subtitle, ass
- L12: "subtitle_cues": 320,
- L13: "subtitle_errors": [],
- L14: "visual_review": "PASS: opening, quarter, half, three-quarter, ending and five chapter cards inspected.",
- L15: "automated_pass": true

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/final/DELIVERY_MANIFEST.json\`
Keywords: srt
- L8: "path": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_V2\\final\\HIA_CHICAGO_V2.srt",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/final/HIA_CHICAGO_V2.srt\`
Keywords: ass, burn
- L132: And once that coal was burned,
- L162: had nothing to do with passengers.
- L250: A project associated with underground
- L270: confined underground passages.
- L421: long underground passage.
- L601: Then, after the coal was burned,
- L645: glamorous replacement for passenger rail.
- L893: Chicago’s passenger subway arrived while

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/final/V2_QC_REPORT.md\`
Keywords: subtitle, srt, ass, transcript, resolve
- L5: Technical QC: PASS. Full decode; no detected black intervals; subtitle sequence valid; audio bitstream SHA-256 identical to V1. Loudness -14.05 LUFS, true peak -4.48 dBTP.
- L7: Motion QC: PASS in three isolated 1080p tests and three samples of the finished video. The old stop/2-pixel-step pattern is absent in measured samples. Subpixel perspective interpolation replaces zoompan; motion is selected by content. Static holds are intentional.
- L13: Subtitles: 338 English sidecar cues; maximum 42 characters per line / two lines. Orphan tails regrouped, no >20 cps cues in the final reflow. One sub-second emphasis remains: "Coal in.". Source wording preserved. Seven short fresh checks of the actual mixed audio support key cue onsets; the ambiguous zero-duration ASR token near 08:37 was resolved by grouping the whole phrase. No full re-transcription.
- L21: Final timestamps: 32,268 distinct presentation timestamps; every interval is 0.040 seconds. The delivered SRT was parsed independently: 338 cues, unchanged source words, no overlap, maximum 42 characters per line, maximum 19.92 characters/second. V1 size and modification timestamps were verified unchanged.
- L23: Evidence is retained in ../qc/: final_qc.json, final_offcenter_motion.json, uncompressed_motion_diagnosis.json, final_pts_validation.json, delivered_srt_validation.json, final_review.jpg. Small diagnostic tests reused final-render clips where possible; no additional full proxy or full final render was required.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/qc/final_metadata.json\`
Keywords: caption
- L53: "captions": 0,
- L106: "captions": 0,

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/qc/final_qc.json\`
Keywords: subtitle, ass
- L12: "subtitle_errors": [],
- L43: "technical_pass": true,
- L44: "motion_pass": true,
- L45: "initial_brightness_metric_pass": false,

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/qc/subtitle_audio_verification.json\`
Keywords: srt
- L7: "srt_start": 5.08,
- L18: "srt_start": 305.02,
- L24: "srt_start": 307.98,
- L30: "srt_start": 311.56,
- L41: "srt_start": 517.24,
- L47: "srt_start": 520.0,
- L53: "srt_start": 523.7,
- L64: "srt_start": 636.56,

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/captions.json\`
Keywords: ass, burn
- L269: "text": "And once that coal was burned, the ash had to be removed.",
- L272: "And once that coal was burned,",
- L329: "text": "had nothing to do with passengers. If some of the city\u2019s repetitive",
- L332: "had nothing to do with passengers.",
- L507: "text": "A project associated with underground communications infrastructure had evolved",
- L510: "A project associated with underground",
- L546: "text": "tiny cars running through confined underground passages.",
- L550: "confined underground passages."

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/00_START_HERE/project_config.json\`
Keywords: ass, master
- L4: "audio_master": "01_AUDIO/voice.wav",
- L13: "generated_assets": 175,
- L14: "archive_assets_unique": 13,
- L15: "music_assets": 7,
- L16: "sfx_assets": 3

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/00_START_HERE/PROJECT_MEMORY.md\`
Keywords: ass, master
- L12: Every scene asset is either DOWNLOAD or GENERATE. DOWNLOAD files go to `10_ASSETS_WORK/archive`, `music`, or `sfx`; generated frames go to `10_ASSETS_WORK/generated` using `05_PROMPTS/visual_prompts.pdf`. Do not begin final automated edit until `python 09_TOOLS/validate_project.py --ready` returns PASS.
- L18: Long-form is primary. Shorts/Reels are extracted only after the long-form master is complete.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/00_START_HERE/README_CODEX.md\`
Keywords: ass
- L9: 3. Download archive assets:
- L17: 8. Verify all required edit assets:
- L19: 9. Only after READY PASS, feed `03_TIMELINE/timeline.csv` to the editing agent.
- L24: - exact header: scene;start;end;track;type;asset;text;z;source_in;source_out;preset;params;transition_in;transition_out;mode;notes

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/00_START_HERE/SHA256.csv\`
Keywords: subtitle, srt, ass, master, voiceover
- L5: 00_START_HERE/master_assets.csv;c23cb212fd7b263b9ef1d9f0921e4fb8cdac12f000f9fb3adba33915bf424935;25227
- L6: 00_START_HERE/master_assets.json;b0a1b5d70e6b5fd7339b5f68aa5eb2a4e356dd6991b524accd1b844beb2e77e8;60389
- L11: 02_SCRIPT/voiceover_en.txt;f6da0d2056a226468e190c10c7a3b0eb6a2bb738658685412b4fba7af87a55ab;18095
- L14: 03_TIMELINE/subtitles_en.srt;6880c067763db4f674ca2646e9ebf2057a0d64e88b748ed467520678c6ce685a;28007

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/00_START_HERE/work_queue.csv\`
Keywords: ass
- L1: asset_id;action;kind;destination;source_or_prompt;status;notes
- L2: A01;DOWNLOAD;archive;10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelIntersectionCloser.jpg;TODO;Run downloader
- L3: A02;DOWNLOAD;archive;10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelMap1910.png;TODO;Run downloader
- L4: A14;DOWNLOAD;archive;10_ASSETS_WORK/archive/A14_LOC_State_Street_1905.jpg;https://cdn.loc.gov/service/pnp/det/4a10000/4a12000/4a12800/4a12894r.jpg;TODO;Run downloader
- L5: A13;DOWNLOAD;archive;10_ASSETS_WORK/archive/A13_LOC_State_Street_1903.jpg;https://cdn.loc.gov/service/pnp/stereo/1s10000/1s12000/1s12700/1s12706v.jpg;TODO;Run downloader
- L6: A15;DOWNLOAD;archive;10_ASSETS_WORK/archive/A15_LOC_Wabash_Avenue_c1900.jpg;https://cdn.loc.gov/service/pnp/det/4a00000/4a08000/4a08100/4a08136v.jpg;TODO;Run downloader
- L7: A08;DOWNLOAD;archive;10_ASSETS_WORK/archive/A08_IllinoisTelephoneAndTelegraphAd.png;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTelephoneAndTelegraphAd.png;TODO;Run downloader
- L8: A05;DOWNLOAD;archive;10_ASSETS_WORK/archive/A05_IllinoisTunnelConstruction.jpg;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelConstruction.jpg;TODO;Run downloader

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/02_SCRIPT/voiceover_en.txt\`
Keywords: ass, burn
- L31: Stores needed merchandise. Buildings needed supplies. Boiler rooms needed coal. And once that coal was burned, the ash had to be removed.
- L41: That made the space beneath the streets valuable for a reason that had nothing to do with passengers. If some of the city’s repetitive freight movements could be pushed underground, the same downtown could keep functioning without asking every wagon and delivery to fight for the same curb.
- L65: A project associated with underground communications infrastructure had evolved into an urban freight system.
- L69: Chicago’s mainline railroads used normal freight cars. The tunnel railroad used tiny cars running through confined underground passages.
- L107: The easiest way to underestimate Chicago’s freight tunnels is to picture one long underground passage.
- L155: Then, after the coal was burned, the waste had to leave.
- L169: The system was not trying to be a glamorous replacement for passenger rail.
- L247: Chicago’s passenger subway arrived while the freight tunnels were still operating.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/03_TIMELINE/README_TIMELINE.txt\`
Keywords: subtitle, srt
- L8: Subtitles are also represented as individual timeline rows and additionally provided as subtitles_en.srt.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/03_TIMELINE/scene_map.csv\`
Keywords: ass, narration, burn
- L1: scene;start;end;section;mode;source_id;asset;narration;visual;text_overlay
- L2: S001;00:00:00.000;00:00:11.520;ANOTHER CHICAGO BELOW CHICAGO;GENERATE;P001;10_ASSETS_WORK/generated/S001_P001.png;Walk through downtown Chicago today, and almost nothing at street level tells you that another transportation network once existed roughly forty feet below the traffic.;"Modern downtown Chicago street-level establishing shot, recognizable Loop architecture and everyday traffic; visual should imply hidden depth below without showing the tunnel yet; leave composition ready for a later 
- L3: S002;00:00:11.520;00:00:13.080;ANOTHER CHICAGO BELOW CHICAGO;GENERATE;P002;10_ASSETS_WORK/generated/S002_P002.png;Not a subway.;Cutaway - generated reconstruction/diagram matched to narration.;
- L4: S003;00:00:13.080;00:00:16.590;ANOTHER CHICAGO BELOW CHICAGO;DOWNLOAD;A01;10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg;A freight railroad.;Use selected free/public-domain source with slow crop, pan, parallax, or map animation as appropriate.;
- L5: S004;00:00:16.590;00:00:29.860;ANOTHER CHICAGO BELOW CHICAGO;GENERATE;P003;10_ASSETS_WORK/generated/S004_P003.png;Small electric locomotives hauled coal, merchandise, supplies, and ash through narrow tunnels beneath the Loop. The tracks connected with railroad freight houses. In some buildings, they reached directly into basement-level facilities.;Cutaway - generated reconstruction/diagram matched to narration.;
- L6: S005;00:00:29.860;00:00:34.280;ANOTHER CHICAGO BELOW CHICAGO;DOWNLOAD;A02;10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png;And this was not one tunnel linking two points.;Use selected free/public-domain source with slow crop, pan, parallax, or map animation as appropriate.;
- L7: S006;00:00:34.280;00:00:39.810;ANOTHER CHICAGO BELOW CHICAGO;GENERATE;P004;10_ASSETS_WORK/generated/S006_P004.png;At its height, the network stretched roughly sixty miles beneath downtown Chicago.;"Modern or timeless Chicago downtown skyline / simplified city-scale establishing frame that can transition into an underground network overlay; emphasize the scale of the city, not tourism postcard aesthetics.";~60 MILES
- L8: S007;00:00:39.810;00:00:50.010;ANOTHER CHICAGO BELOW CHICAGO;GENERATE;P005;10_ASSETS_WORK/generated/S007_P005.png;For decades, freight moved through an underground grid while the city continued above it. Then, in July 1959, the trains stopped.;Empty Tunnel - generated reconstruction/diagram matched to narration.;JULY 1959

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/03_TIMELINE/timeline.csv\`
Keywords: subtitle, ass, narration, burn
- L1: scene;start;end;track;type;asset;text;z;source_in;source_out;preset;params;transition_in;transition_out;mode;notes
- L2: S001;00:00:00.000;00:00:11.520;V1;image;10_ASSETS_WORK/generated/S001_P001.png;;0;;;slow_push_in+cool_grade;scale_from=1.00|scale_to=1.08|contrast=1.05|saturation=0.88;crossfade;crossfade;EXACT;"Сгенерировать вручную по P001 в 05_PROMPTS/visual_prompts.pdf. Modern downtown Chicago street-level establishing shot, recognizable Loop architecture and everyday traffic; visual should imply hidden depth below without showing the tunnel yet; leave composition ready for a later downward transition/cutawa
- L3: SUB001;00:00:00.000;00:00:06.224;V5;subtitle;;Walk through downtown Chicago today, and almost nothing at street level tells you that another;50;;;lower_third;font=Montserrat SemiBold|size=46|color=#FFFFFF|position=bottom|safe_margin=0.07|stroke=#000000|stroke_width=3;cut;cut;EXACT;"English subtitle. Keep within title-safe; max 2 lines."
- L5: M01;00:00:00.000;00:02:33.030;A2;music;10_ASSETS_WORK/music/M01_Aftermath_Kevin_MacLeod.mp3;;0;00:00:00.000;;;gain_db=-27|ducking_db=-8|fade_in=1.0|fade_out=1.5|loop=true;fade;crossfade;EXACT;"dark subtle mystery, opening; музыка всегда ниже речи."
- L7: SUB002;00:00:06.224;00:00:11.057;V5;subtitle;;transportation network once existed roughly forty feet below the traffic.;50;;;lower_third;font=Montserrat SemiBold|size=46|color=#FFFFFF|position=bottom|safe_margin=0.07|stroke=#000000|stroke_width=3;cut;cut;EXACT;"English subtitle. Keep within title-safe; max 2 lines."
- L8: SUB003;00:00:11.057;00:00:13.080;V5;subtitle;;Not a subway.;50;;;lower_third;font=Montserrat SemiBold|size=46|color=#FFFFFF|position=bottom|safe_margin=0.07|stroke=#000000|stroke_width=3;cut;cut;EXACT;"English subtitle. Keep within title-safe; max 2 lines."
- L9: S002;00:00:11.520;00:00:13.080;V1;image;10_ASSETS_WORK/generated/S002_P002.png;;0;;;slow_push_in+documentary_photo;scale_from=1.00|scale_to=1.06|easing=ease_out;crossfade;crossfade;EXACT;Сгенерировать вручную по P002 в 05_PROMPTS/visual_prompts.pdf. Cutaway - generated reconstruction/diagram matched to narration.
- L10: S003;00:00:13.080;00:00:16.590;V1;image;10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg;;0;;;ken_burns+documentary_photo+film_grain;scale_from=1.00|scale_to=1.08|easing=ease_in_out|grain=0.10;crossfade;crossfade;EXACT;Архивный кадр A01. Use selected free/public-domain source with slow crop, pan, parallax, or map animation as appropriate. Акцент narration: A freight railroad.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/03_TIMELINE/timeline_schema.json\`
Keywords: subtitle, ass
- L10: "asset",
- L28: "V5": "subtitles/titles",
- L44: "subtitle"
- L48: "ASSISTED",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/04_DOWNLOADS/all_download_links.md\`
Keywords: ass
- L7: - Destination: `10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg`
- L11: - Destination: `10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png`
- L15: - Destination: `10_ASSETS_WORK/archive/A14_LOC_State_Street_1905.jpg`
- L19: - Destination: `10_ASSETS_WORK/archive/A13_LOC_State_Street_1903.jpg`
- L23: - Destination: `10_ASSETS_WORK/archive/A15_LOC_Wabash_Avenue_c1900.jpg`
- L27: - Destination: `10_ASSETS_WORK/archive/A08_IllinoisTelephoneAndTelegraphAd.png`
- L31: - Destination: `10_ASSETS_WORK/archive/A05_IllinoisTunnelConstruction.jpg`
- L35: - Destination: `10_ASSETS_WORK/archive/A07_IllinoisTunnelTestTrain.jpg`

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/04_DOWNLOADS/archive_downloads.csv\`
Keywords: ass
- L2: A01;A01_IllinoisTunnelIntersectionCloser.jpg;10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg;Перекресток тоннелей Illinois Tunnel Company;Anonymous work for hire, probably Illinois Tunnel Company;1905;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelIntersectionCloser.jpg;https://commons.wikimedia.org/wiki/File:IllinoisTunnelIntersectionCloser.jpg;Public domain in the United States;YELLOW;"Не требуется в США; credit источника рекомендуется";https://commons.w
- L3: A02;A02_IllinoisTunnelMap1910.png;10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png;Карта Illinois Tunnel Company;Illinois Tunnel Company;1910;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelMap1910.png;https://commons.wikimedia.org/wiki/File:IllinoisTunnelMap1910.png;Public domain in the United States;YELLOW;"Не требуется в США; credit рекомендуется";https://commons.wikimedia.org/wiki/File:IllinoisTunnelMap1910.png
- L4: A14;A14_LOC_State_Street_1905.jpg;10_ASSETS_WORK/archive/A14_LOC_State_Street_1905.jpg;State Street, Chicago;Detroit Publishing Co.;c.1905;https://cdn.loc.gov/service/pnp/det/4a10000/4a12000/4a12800/4a12894r.jpg;https://www.loc.gov/item/2016805496/;Library of Congress: No known restrictions on publication;GREEN;Credit Library of Congress, Detroit Publishing Company Collection;https://www.loc.gov/item/2016805496/
- L5: A13;A13_LOC_State_Street_1903.jpg;10_ASSETS_WORK/archive/A13_LOC_State_Street_1903.jpg;State Street noonday crowds;Underwood & Underwood;1903;https://cdn.loc.gov/service/pnp/stereo/1s10000/1s12000/1s12700/1s12706v.jpg;https://www.loc.gov/item/2014650313/;Library of Congress: No known restrictions on publication;GREEN;Credit Library of Congress / Underwood & Underwood рекомендуется;https://www.loc.gov/item/2014650313/
- L6: A15;A15_LOC_Wabash_Avenue_c1900.jpg;10_ASSETS_WORK/archive/A15_LOC_Wabash_Avenue_c1900.jpg;Wabash Ave., north from Adams St.;Detroit Publishing Co.;c.1900;https://cdn.loc.gov/service/pnp/det/4a00000/4a08000/4a08100/4a08136v.jpg;https://www.loc.gov/item/2016799520/;Library of Congress: No known restrictions on publication;GREEN;Credit Library of Congress, Detroit Publishing Company Collection;https://www.loc.gov/item/2016799520/
- L7: A08;A08_IllinoisTelephoneAndTelegraphAd.png;10_ASSETS_WORK/archive/A08_IllinoisTelephoneAndTelegraphAd.png;Illinois Telephone & Telegraph advertisement;Unknown;1912;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTelephoneAndTelegraphAd.png;https://commons.wikimedia.org/wiki/File:IllinoisTelephoneAndTelegraphAd.png;Public domain in the United States;YELLOW;"Не требуется в США; credit рекомендуется";https://commons.wikimedia.org/wiki/File:IllinoisTelephoneAndTelegraphAd.png
- L8: A05;A05_IllinoisTunnelConstruction.jpg;10_ASSETS_WORK/archive/A05_IllinoisTunnelConstruction.jpg;Строительство бокового conduit/tunnel;George W. Jackson (d. 1922);1902;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelConstruction.jpg;https://commons.wikimedia.org/wiki/File:IllinoisTunnelConstruction.jpg;"Public domain; Commons Public Domain Mark / life+70 note";GREEN;"Не требуется; credit рекомендуется";https://commons.wikimedia.org/wiki/File:IllinoisTunnelConstruction.jpg
- L9: A07;A07_IllinoisTunnelTestTrain.jpg;10_ASSETS_WORK/archive/A07_IllinoisTunnelTestTrain.jpg;Loaded test train in tunnel;Not credited;1904;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelTestTrain.jpg;https://commons.wikimedia.org/wiki/File:IllinoisTunnelTestTrain.jpg;Public domain in the United States;YELLOW;"Не требуется в США; credit рекомендуется";https://commons.wikimedia.org/wiki/File:IllinoisTunnelTestTrain.jpg

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/04_DOWNLOADS/music_downloads.csv\`
Keywords: ass
- L2: M01;Aftermath;Kevin MacLeod;00:00:00.000;00:02:33.030;M01_Aftermath_Kevin_MacLeod.mp3;10_ASSETS_WORK/music/M01_Aftermath_Kevin_MacLeod.mp3;https://incompetech.com/music/royalty-free/mp3-royaltyfree/Aftermath.mp3;https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100575;Creative Commons Attribution 4.0;https://creativecommons.org/licenses/by/4.0/;dark subtle mystery, opening;"""Aftermath"" Kevin MacLeod (incompetech.com) - Licensed under Creative Commons: By Attributio
- L3: M02;Ambiment;Kevin MacLeod;00:02:33.030;00:05:38.390;M02_Ambiment_Kevin_MacLeod.mp3;10_ASSETS_WORK/music/M02_Ambiment_Kevin_MacLeod.mp3;https://incompetech.com/music/royalty-free/mp3-royaltyfree/Ambiment.mp3;https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100630;Creative Commons Attribution 4.0;https://creativecommons.org/licenses/by/4.0/;calm investigative bed, origin and mechanics;"""Ambiment"" Kevin MacLeod (incompetech.com) - Licensed under Creative Commons: By
- L4: M03;Floating Cities;Kevin MacLeod;00:05:38.390;00:09:15.510;M03_Floating_Cities_Kevin_MacLeod.mp3;10_ASSETS_WORK/music/M03_Floating_Cities_Kevin_MacLeod.mp3;https://incompetech.com/music/royalty-free/mp3-royaltyfree/Floating%20Cities.mp3;https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1600018;Creative Commons Attribution 4.0;https://creativecommons.org/licenses/by/4.0/;restrained scale and systems bed;"""Floating Cities"" Kevin MacLeod (incompetech.com) - Licensed u
- L5: M04;Mesmerize;Kevin MacLeod;00:09:15.510;00:13:34.260;M04_Mesmerize_Kevin_MacLeod.mp3;10_ASSETS_WORK/music/M04_Mesmerize_Kevin_MacLeod.mp3;https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3;https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1500005;Creative Commons Attribution 4.0;https://creativecommons.org/licenses/by/4.0/;subtle analytical tension, economics and decline;"""Mesmerize"" Kevin MacLeod (incompetech.com) - Licensed under Creative Co
- L6: M05;Long Note Two;Kevin MacLeod;00:13:34.260;00:15:26.090;M05_Long_Note_Two_Kevin_MacLeod.mp3;10_ASSETS_WORK/music/M05_Long_Note_Two_Kevin_MacLeod.mp3;https://incompetech.com/music/royalty-free/mp3-royaltyfree/Long%20Note%20Two.mp3;https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100420;Creative Commons Attribution 4.0;https://creativecommons.org/licenses/by/4.0/;minimal dark bed, shutdown and empty infrastructure;"""Long Note Two"" Kevin MacLeod (incompetech.com) -
- L7: M06;Lightless Dawn;Kevin MacLeod;00:15:26.090;00:17:55.870;M06_Lightless_Dawn_Kevin_MacLeod.mp3;10_ASSETS_WORK/music/M06_Lightless_Dawn_Kevin_MacLeod.mp3;https://incompetech.com/music/royalty-free/mp3-royaltyfree/Lightless%20Dawn.mp3;https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100655;Creative Commons Attribution 4.0;https://creativecommons.org/licenses/by/4.0/;controlled tension for 1992 flood;"""Lightless Dawn"" Kevin MacLeod (incompetech.com) - Licensed under
- L8: M07;Peace of Mind;Kevin MacLeod;00:17:55.870;00:21:30.720;M07_Peace_of_Mind_Kevin_MacLeod.mp3;10_ASSETS_WORK/music/M07_Peace_of_Mind_Kevin_MacLeod.mp3;https://incompetech.com/music/royalty-free/mp3-royaltyfree/Peace%20of%20Mind.mp3;https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1200099;Creative Commons Attribution 4.0;https://creativecommons.org/licenses/by/4.0/;quiet reflective resolution and legacy;"""Peace of Mind"" Kevin MacLeod (incompetech.com) - Licensed und

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/04_DOWNLOADS/sfx_downloads.csv\`
Keywords: ass
- L2: SFX01;Technical room of an industry;SFX01_industrial_room.mp3;10_ASSETS_WORK/sfx/SFX01_industrial_room.mp3;https://bigsoundbank.com/UPLOAD/mp3/0504.mp3;https://bigsoundbank.com/technical-room-of-an-industry-s0504.html;CC0 / public-domain equivalent;https://bigsoundbank.com/technical-room-of-an-industry-s0504.html;"Not required; credit Joseph SARDIN / BigSoundBank appreciated"
- L3: SFX02;Passage of a train #1;SFX02_train_pass.mp3;10_ASSETS_WORK/sfx/SFX02_train_pass.mp3;https://bigsoundbank.com/UPLOAD/mp3/0900.mp3;https://bigsoundbank.com/train-passes-s0900.html;CC0 / public-domain equivalent;https://bigsoundbank.com/train-passes-s0900.html;"Not required; credit Joseph SARDIN / BigSoundBank appreciated"
- L4: SFX03;Train in Station #1;SFX03_train_station.mp3;10_ASSETS_WORK/sfx/SFX03_train_station.mp3;https://bigsoundbank.com/UPLOAD/mp3/2723.mp3;https://bigsoundbank.com/train-in-station-1-s2723.html;CC0 / public-domain equivalent;https://bigsoundbank.com/train-in-station-1-s2723.html;"Not required; credit Joseph SARDIN / BigSoundBank appreciated"

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/05_PROMPTS/prompt_index.csv\`
Keywords: subtitle, caption, ass, narration, burn
- L1: prompt_id;scene;start;end;asset;section;narration;visual;prompt;negative_prompt
- L2: P001;S001;00:00:00.000;00:00:11.520;10_ASSETS_WORK/generated/S001_P001.png;ANOTHER CHICAGO BELOW CHICAGO;Walk through downtown Chicago today, and almost nothing at street level tells you that another transportation network once existed roughly forty feet below the traffic.;"Modern downtown Chicago street-level establishing shot, recognizable Loop architecture and everyday traffic; visual should imply hidden depth below without showing the tunnel yet; leave composition ready for a later downward 
- L3: P002;S002;00:00:11.520;00:00:13.080;10_ASSETS_WORK/generated/S002_P002.png;ANOTHER CHICAGO BELOW CHICAGO;Not a subway.;Cutaway - generated reconstruction/diagram matched to narration.;"Create a 16:9 visual for S002 in a premium faceless YouTube documentary about Chicago's forgotten underground freight railroad. Time period/context: modern Chicago with historical underground reconstruction. Scene objective: Visualize this specific narration idea as one immediately readable documentary frame: Not 
- L4: P003;S004;00:00:16.590;00:00:29.860;10_ASSETS_WORK/generated/S004_P003.png;ANOTHER CHICAGO BELOW CHICAGO;Small electric locomotives hauled coal, merchandise, supplies, and ash through narrow tunnels beneath the Loop. The tracks connected with railroad freight houses. In some buildings, they reached directly into basement-level facilities.;Cutaway - generated reconstruction/diagram matched to narration.;"Create a 16:9 visual for S004 in a premium faceless YouTube documentary about Chicago's forgo
- L5: P004;S006;00:00:34.280;00:00:39.810;10_ASSETS_WORK/generated/S006_P004.png;ANOTHER CHICAGO BELOW CHICAGO;At its height, the network stretched roughly sixty miles beneath downtown Chicago.;"Modern or timeless Chicago downtown skyline / simplified city-scale establishing frame that can transition into an underground network overlay; emphasize the scale of the city, not tourism postcard aesthetics.";"Create a 16:9 visual for S006 in a premium faceless YouTube documentary about Chicago's forgotten u
- L6: P005;S007;00:00:39.810;00:00:50.010;10_ASSETS_WORK/generated/S007_P005.png;ANOTHER CHICAGO BELOW CHICAGO;For decades, freight moved through an underground grid while the city continued above it. Then, in July 1959, the trains stopped.;Empty Tunnel - generated reconstruction/diagram matched to narration.;"Create a 16:9 visual for S007 in a premium faceless YouTube documentary about Chicago's forgotten underground freight railroad. Time period/context: modern Chicago with historical underground re
- L7: P006;S008;00:00:50.010;00:00:53.940;10_ASSETS_WORK/generated/S008_P006.png;ANOTHER CHICAGO BELOW CHICAGO;The railroad disappeared as a working system.;Cutaway - generated reconstruction/diagram matched to narration.;"Create a 16:9 visual for S008 in a premium faceless YouTube documentary about Chicago's forgotten underground freight railroad. Time period/context: modern Chicago with historical underground reconstruction. Scene objective: Visualize this specific narration idea as one immediately 
- L8: P007;S010;00:00:55.620;00:01:01.590;10_ASSETS_WORK/generated/S010_P007.png;ANOTHER CHICAGO BELOW CHICAGO;So why did Chicago need an entire freight railroad beneath its streets?;Network Overlay - generated reconstruction/diagram matched to narration.;"Create a 16:9 visual for S010 in a premium faceless YouTube documentary about Chicago's forgotten underground freight railroad. Time period/context: modern Chicago with historical underground reconstruction. Scene objective: Visualize this specific 

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/06_LICENSES_FACTS/fact_map.csv\`
Keywords: ass
- L17: S125;12:22;Passenger subway construction around 1939 cut important parts of freight network;UChicago;https://www.lib.uchicago.edu/collex/exhibits/under-your-feet/chicagos-freight-tunnels/;High;UChicago states subway tunnels constructed in 1939 at the same level cut off important parts of the network.;LOCKED

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/06_LICENSES_FACTS/license_manifest.csv\`
Keywords: ass
- L1: type;id;asset;source_page;download_url;license;license_url;attribution;risk
- L2: archive;A01;10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg;https://commons.wikimedia.org/wiki/File:IllinoisTunnelIntersectionCloser.jpg;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelIntersectionCloser.jpg;Public domain in the United States;https://commons.wikimedia.org/wiki/File:IllinoisTunnelIntersectionCloser.jpg;"Не требуется в США; credit источника рекомендуется";YELLOW
- L3: archive;A02;10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png;https://commons.wikimedia.org/wiki/File:IllinoisTunnelMap1910.png;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelMap1910.png;Public domain in the United States;https://commons.wikimedia.org/wiki/File:IllinoisTunnelMap1910.png;"Не требуется в США; credit рекомендуется";YELLOW
- L4: archive;A14;10_ASSETS_WORK/archive/A14_LOC_State_Street_1905.jpg;https://www.loc.gov/item/2016805496/;https://cdn.loc.gov/service/pnp/det/4a10000/4a12000/4a12800/4a12894r.jpg;Library of Congress: No known restrictions on publication;https://www.loc.gov/item/2016805496/;Credit Library of Congress, Detroit Publishing Company Collection;GREEN
- L5: archive;A13;10_ASSETS_WORK/archive/A13_LOC_State_Street_1903.jpg;https://www.loc.gov/item/2014650313/;https://cdn.loc.gov/service/pnp/stereo/1s10000/1s12000/1s12700/1s12706v.jpg;Library of Congress: No known restrictions on publication;https://www.loc.gov/item/2014650313/;Credit Library of Congress / Underwood & Underwood рекомендуется;GREEN
- L6: archive;A15;10_ASSETS_WORK/archive/A15_LOC_Wabash_Avenue_c1900.jpg;https://www.loc.gov/item/2016799520/;https://cdn.loc.gov/service/pnp/det/4a00000/4a08000/4a08100/4a08136v.jpg;Library of Congress: No known restrictions on publication;https://www.loc.gov/item/2016799520/;Credit Library of Congress, Detroit Publishing Company Collection;GREEN
- L7: archive;A08;10_ASSETS_WORK/archive/A08_IllinoisTelephoneAndTelegraphAd.png;https://commons.wikimedia.org/wiki/File:IllinoisTelephoneAndTelegraphAd.png;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTelephoneAndTelegraphAd.png;Public domain in the United States;https://commons.wikimedia.org/wiki/File:IllinoisTelephoneAndTelegraphAd.png;"Не требуется в США; credit рекомендуется";YELLOW
- L8: archive;A05;10_ASSETS_WORK/archive/A05_IllinoisTunnelConstruction.jpg;https://commons.wikimedia.org/wiki/File:IllinoisTunnelConstruction.jpg;https://commons.wikimedia.org/wiki/Special:Redirect/file/IllinoisTunnelConstruction.jpg;"Public domain; Commons Public Domain Mark / life+70 note";https://commons.wikimedia.org/wiki/File:IllinoisTunnelConstruction.jpg;"Не требуется; credit рекомендуется";GREEN

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/07_SHORTS_REELS/reels_plan.csv\`
Keywords: ass
- L9: 8,Chicago’s Subway Cut Through an Older Railroad,Infrastructure generation conflict.,Chicago’s passenger subway arrived while the freight tunnels were still operating.,New passenger subway construction severed parts of the older freight network.,45-60s,9.4,Strong contradiction and highly visual diagram.,POST-LONG-FORM #8,12:15,12:34,18.6
- L13: 12,Why Good Infrastructure Becomes Obsolete,Big idea / channel thesis.,Chicago’s tunnel railroad did not disappear because one invention suddenly made it useless.,Infrastructure can lose the economy that justified it without mechanically failing.,60-80s,9.0,Strong intellectual shareability; narrower mass-market hook.,POST-LONG-FORM #12,19:33,21:26,112.1

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/09_TOOLS/_download_common.py\`
Keywords: resolve
- L3: ROOT=Path(__file__).resolve().parents[1]

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/09_TOOLS/check_links.py\`
Keywords: ass, resolve
- L3: ROOT=Path(__file__).resolve().parents[1]
- L27: print('\nLINK CHECK: PASS')

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/09_TOOLS/validate_project.py\`
Keywords: subtitle, ass, master, resolve, narration
- L3: ROOT=Path(__file__).resolve().parents[1]
- L21: expected=['scene','start','end','track','type','asset','text','z','source_in','source_out','preset','params','transition_in','transition_out','mode','notes']
- L24: tracks={'V1','V2','V3','V4','V5','A1','A2','A3','A4'}; types={'video','image','text','overlay','shape','voice','music','sfx','ambience','subtitle'}; modes={'EXACT','ASSISTED','AUTO'}
- L46: # subtitles compare count + end
- L47: subs=[r for r in rows if r['type']=='subtitle']
- L48: if len(subs)!=293: err(f'subtitle rows {len(subs)} !=293')
- L49: if subs and max(ms(r['end']) for r in subs)!=1290720: err('subtitle end != audio end')
- L51: master=read_csv(ROOT/'00_START_HERE/master_assets.csv'); bydest={r['destination']:r for r in master}

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_EDIT_WORK/asset_manifest.csv\`
Keywords: subtitle, srt, ass, master, voiceover
- L16: 00_START_HERE/master_assets.csv,master_assets.csv,OTHER,,,/Date(1789274127000)/,25227,normal,
- L17: 00_START_HERE/master_assets.json,master_assets.json,OTHER,,,/Date(1789274127000)/,60389,normal,
- L23: 01_AUDIO/voice.wav,voice.wav,VOICEOVER,1290.720000,,/Date(1789263721000)/,113841582,high,
- L25: 02_SCRIPT/voiceover_en.txt,voiceover_en.txt,SCRIPT,,,/Date(1789270647000)/,18095,high,
- L28: 03_TIMELINE/subtitles_en.srt,subtitles_en.srt,SUBTITLES,,,/Date(1789266817000)/,28007,high,
- L59: 10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg,A01_IllinoisTunnelIntersectionCloser.jpg,PHOTO,,1582x1195,/Date(1789275469833)/,334154,normal,
- L60: 10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png,A02_IllinoisTunnelMap1910.png,MAP,,1948x2596,/Date(1789275471058)/,2546087,normal,
- L61: 10_ASSETS_WORK/archive/A03_ChicagoTunnelFieldsTrain.jpg,A03_ChicagoTunnelFieldsTrain.jpg,PHOTO,,1280x925,/Date(1789275633830)/,201001,normal,

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_EDIT_WORK/codex_edit_state.json\`
Keywords: subtitle, ass, master, voiceover
- L5: "canonical_script": "02_SCRIPT/voiceover_en.txt",
- L7: "canonical_voiceover": "01_AUDIO/voice.wav",
- L14: "corrected_assets": {
- L33: "audio_master_completed": true,
- L34: "subtitle_alignment_completed": true

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_EDIT_WORK/edit_plan.md\`
Keywords: srt, ass, master
- L1: Voice is the unchanged 1290.720-second master. 1080p / 25 fps; full 720p proxy before final.
- L5: Five major chapter cards, a brief post-hook brand moment, final 18-second end screen. Seven music states follow existing chapter boundaries, with voice-driven ducking. English SRT delivered separately.
- L7: Corrections: replace 17 misleading technical/map or baked-editorial-text assets with existing relevant library sources.
- L13: 00:05:38.390 — THIS WASN’T ONE TUNNEL: The easiest way to underestimate Chicago’s freight tunnels is to picture one long underground passage.
- L17: 00:12:15.410 — THE CITY CHANGED AROUND THE RAILROAD: Chicago’s passenger subway arrived while the freight tunnels were still operating.

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_EDIT_WORK/edit_scenes.json\`
Keywords: ass, resolve, narration, burn
- L9: "asset": "10_ASSETS_WORK/generated/S001_P001.png",
- L10: "narration": "Walk through downtown Chicago today, and almost nothing at street level tells you that another transportation network once existed roughly forty feet below the traffic.",
- L13: "resolved_asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\12_\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u0438\\S001_P001.png",
- L26: "asset": "10_ASSETS_WORK/generated/S002_P002.png",
- L27: "narration": "Not a subway.",
- L28: "visual": "Cutaway - generated reconstruction/diagram matched to narration.",
- L30: "resolved_asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\12_\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u0438\\S002_P002.png",
- L43: "asset": "10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_EDIT_WORK/hia_edit_local.py\`
Keywords: subtitle, caption, srt, ass, final_upload, master, ffmpeg, resolve, voiceover, narration, timing, sync
- L22: meta=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]));dur=meta['format']['duration'];typ='VOICEOVER' if ex=='.wav' else 'MUSIC' if '/music/' in rel else 'SFX'
- L23: elif ex=='.srt':typ='SUBTITLES'
- L26: rows.append(dict(path=rel,filename=p.name,type=typ,duration=dur,resolution=res,modified=a['LastWriteTimeUtc'],size=a['Length'],priority='high' if typ in ('VOICEOVER','SCRIPT','SUBTITLES') else 'normal',notes=''))
- L27: with (W/'asset_manifest.csv').open('w',newline='',encoding='utf-8') as f:
- L31: p=R/s['asset']
- L32: if not p.exists():p=lookup.get(Path(s['asset']).name,p)
- L33: s['resolved_asset']=str(p)
- L35: (W/'resolved_scenes.json').write_text(json.dumps(scenes,indent=2),encoding='utf-8')

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_EDIT_WORK/inventory_raw.json\`
Keywords: subtitle, srt, ass, master, voiceover
- L1: ﻿[{"FullName":"C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\ARCHIVE_DOWNLOAD_REPORT.txt","Length":7806,"LastWriteTimeUtc":"\/Date(1789275477817)\/"},{"FullName":"C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\channel_branding_prompts.pdf","Length":59331,"LastWriteTimeUtc":"\/Date(1789279788961)\/"},{"FullName":"C:\\Users

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_EDIT_WORK/resolved_scenes.json\`
Keywords: ass, resolve, narration, burn
- L9: "asset": "10_ASSETS_WORK/generated/S001_P001.png",
- L10: "narration": "Walk through downtown Chicago today, and almost nothing at street level tells you that another transportation network once existed roughly forty feet below the traffic.",
- L13: "resolved_asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\12_\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u0438\\S001_P001.png"
- L22: "asset": "10_ASSETS_WORK/generated/S002_P002.png",
- L23: "narration": "Not a subway.",
- L24: "visual": "Cutaway - generated reconstruction/diagram matched to narration.",
- L26: "resolved_asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\12_\u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u0438\\S002_P002.png"
- L35: "asset": "10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_EDIT_WORK/script_segments.csv\`
Keywords: ass, narration
- L1: start,end,narration_summary,purpose,visual_type,primary_asset,secondary_asset,graphics,music_state
- L3: 70.32,153.68,THE PROBLEM ABOVE GROUND,The reason begins with a problem Chicago could see every day.,archive / reconstruction / explanatory detail,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\10_ASSETS_WORK\archive\A14_LOC_State_Street_1905.jpg,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\10_ASSETS_WORK\archive\A14_LOC_State_Street_1
- L4: 153.68,233.67,IT DIDN’T START AS A RAILROAD,Chicago’s underground freight railroad did not actually begin as a railroad.,archive / reconstruction / explanatory detail,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\10_ASSETS_WORK\archive\A08_IllinoisTelephoneAndTelegraphAd.png,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\10_ASSETS_WORK
- L6: 341.92,471.44,THIS WASN’T ONE TUNNEL,The easiest way to underestimate Chicago’s freight tunnels is to picture one long underground passage.,archive / reconstruction / explanatory detail,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\10_ASSETS_WORK\archive\A01_IllinoisTunnelIntersectionCloser.jpg,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_REA
- L7: 471.44,560.26,COAL IN. ASH OUT.,Coal explains why the tunnel railroad could make economic sense.,archive / reconstruction / explanatory detail,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\10_ASSETS_WORK\archive\A04_TunnelCoalDelivery.jpg,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\12_Генерации\S090_P042.png,restrained titles and re
- L10: 730.78,809.98,THE CITY CHANGED AROUND THE RAILROAD,Chicago’s passenger subway arrived while the freight tunnels were still operating.,archive / reconstruction / explanatory detail,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\12_Генерации\S124_P072.png,C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7\12_Генерации\S139_P084.png,restrained

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_QC/alignment_report.json\`
Keywords: srt
- L2: "reason": "Original SRT has varying errors around 3-4 seconds at quarter/middle/three-quarter samples.",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_QC/proxy_ffprobe.json\`
Keywords: caption
- L53: "captions": 0,
- L106: "captions": 0,

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_QC/proxy_qc.json\`
Keywords: subtitle, ass
- L12: "subtitle_cues": 320,
- L13: "subtitle_errors": [],
- L14: "visual_review": "PASS: opening, quarter, half, three-quarter, ending and five chapter cards inspected.",
- L15: "automated_pass": true

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_QC/voice_words.json\`
Keywords: ass, burn
- L1: [{"start": 0.0, "end": 0.26, "word": " Walk"}, {"start": 0.26, "end": 0.54, "word": " through"}, {"start": 0.54, "end": 1.02, "word": " downtown"}, {"start": 1.02, "end": 1.58, "word": " Chicago"}, {"start": 1.58, "end": 2.1, "word": " today"}, {"start": 2.1, "end": 2.98, "word": " and"}, {"start": 2.98, "end": 3.28, "word": " almost"}, {"start": 3.28, "end": 3.68, "word": " nothing"}, {"start": 3.68, "end": 3.86, "word": " at"}, {"start": 3.86, "end": 4.16, "word": " street"}, {"start": 4.16, "

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/qc/delivered_srt_validation.json\`
Keywords: srt
- L4: "actual_srt_matches_plan": true,

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/qc/motion_test_metrics.json\`
Keywords: ass
- L11: "pass": true
- L22: "pass": true
- L33: "pass": true

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/qc/proxy_metadata.json\`
Keywords: caption
- L53: "captions": 0,
- L106: "captions": 0,

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/qc/proxy_qc.json\`
Keywords: subtitle, ass
- L12: "subtitle_errors": [],
- L43: "technical_pass": true,
- L44: "motion_pass": true,
- L45: "initial_brightness_metric_pass": false,

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/qc/uncompressed_motion_diagnosis.json\`
Keywords: ass
- L8: "pass": true
- L16: "pass": true

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/hia_v2.py\`
Keywords: subtitle, caption, srt, ass, transcript, final_upload, ffmpeg, resolve
- L8: BASE=R/'_V2';W=BASE/'work';Q=BASE/'qc';F=BASE/'final';OLD=R/'_FINAL/HIA_CHICAGO_FINAL_UPLOAD.mp4'
- L18: for p in [W,Q,F,W/'assets',W/'overlays']:p.mkdir(parents=True,exist_ok=True)
- L19: if not (W/'state.json').exists():save(W/'state.json',{'revision':'V2','source_v1':str(OLD),'motion_tests_pass':False,'plan_complete':False,'proxy_complete':False,'proxy_qc_pass':False,'final_complete':False,'final_qc_pass':False})
- L21: keep=[OLD,R/'_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt',R/'_FINAL/EDIT_REPORT.md',R/'_EDIT_WORK/codex_edit_state.json'];save(W/'v1_snapshot.json',[{'path':str(p),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in keep])
- L35: im=ImageOps.fit(Image.open(s['resolved_asset']).convert('RGB'),(1920,1080));src=Q/f'test_{mode}.png';im.save(src)
- L38: start=time.time();run(['ffmpeg','-v','error','-y','-loop','1','-framerate','25','-i',str(src),'-vf',vf,'-filter_threads','2','-frames:v',str(n),'-an','-c:v','h264_nvenc','-preset','p4','-cq','19','-b:v','0',str(out)])
- L39: raw=run(['ffmpeg','-v','error','-ss','2','-i',str(out),'-t','2.8','-vf','crop=640:360:640:320,format=gray','-f','rawvideo','-']);a=np.frombuffer(raw,np.uint8).reshape(-1,360,640).astype(np.float32);mad=np.mean(np.abs(np.diff(a,axis=0)),axis=(1,2));steady=mad<.05
- L42: rec={'mode':mode,'duration':8,'seconds_to_render':round(time.time()-start,2),'comparisons':len(mad),'near_static':int(sum(steady)),'longest_near_static_run':maxrun,'mad_median':float(np.median(mad)),'mad_max':float(max(mad)),'pass':maxrun<=1};report.append(rec);print(json.dumps(rec),flush=True)

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/hia_v2_delivery_check.py\`
Keywords: caption, srt, ass, final_upload
- L2: cs=m.load(m.W/'captions.json')
- L3: bs=(m.F/'HIA_CHICAGO_V2.srt').read_text(encoding='utf-8').strip().split('\n\n')
- L4: assert len(bs)==len(cs)
- L12: assert abs(a-c['start'])<.0011 and abs(z-c['end'])<.0011 and l[2:]==c['lines']
- L13: assert a>=previous-.001 and z>a and len(l[2:])<=2 and max(map(len,l[2:]))<=42
- L17: old=(m.R/'_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt').read_text(encoding='utf-8').strip().split('\n\n')
- L19: assert texts==source
- L20: report={'cues':len(bs),'max_cps':max(cps),'actual_srt_matches_plan':True,'all_source_words_preserved':True}

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/hia_v2_finish.py\`
Keywords: srt
- L9: Final timestamps: 32,268 distinct presentation timestamps; every interval is 0.040 seconds. The delivered SRT was parsed independently: 338 cues, unchanged source words, no overlap, maximum 42 characters per line, maximum 19.92 characters/second. V1 size and modification timestamps were verified unchanged.
- L11: Evidence is retained in ../qc/: final_qc.json, final_offcenter_motion.json, uncompressed_motion_diagnosis.json, final_pts_validation.json, delivered_srt_validation.json, final_review.jpg. Small diagnostic tests reused final-render clips where possible; no additional full proxy or full final render was required.
- L16: for p in [m.F/'HIA_CHICAGO_V2.mp4',m.F/'HIA_CHICAGO_V2.srt',report]:

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/hia_v2_motion_diagnose.py\`
Keywords: ffmpeg
- L8: raw=m.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-t','2','-vf','crop=480:270:720:405,format=gray','-f','rawvideo','-'])

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/hia_v2_motion_roi.py\`
Keywords: ass, ffmpeg
- L9: raw=m.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(target),'-t','2','-vf',f"crop=480:270:{int(v['width']*.12)}:{int(v['height']*.18)},format=gray",'-f','rawvideo','-'])
- L19: report['initial_brightness_metric_pass']=report['motion_pass']
- L22: report['motion_pass']=all(x['pass'] for x in raw_checks) and all(x['longest_near_static_run']<=2 for x in results)
- L24: print('Reviewed motion gate:',report['motion_pass'])

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/hia_v2_raw_motion.py\`
Keywords: ass, ffmpeg
- L8: raw=m.run(['ffmpeg','-v','error','-threads','1','-framerate','25','-i',s['asset'],'-vf',vf,'-frames:v','50','-fps_mode','passthrough','-f','rawvideo','-'])
- L11: r={'mode':mode,'near_static':int(sum(d<.05)),'median':float(m.np.median(d)),'max':float(max(d)),'min':float(min(d)),'pass':bool(min(d)>.05 and max(d)<m.np.median(d)*2)}

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/shots.json\`
Keywords: ass
- L6: "asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_V2\\work\\assets\\opening_street.png",
- L22: "asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_V2\\work\\assets\\S002_P002_full_reconstruction.png",
- L37: "source": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\10_ASSETS_WORK\\archive\\A01_IllinoisTunnelIntersectionCloser.jpg",
- L38: "asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_V2\\work\\assets\\A01_IllinoisTunnelIntersectionCloser_full_archive.png",
- L54: "asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_V2\\work\\assets\\S004_P003_detail_reconstruction.png",
- L69: "source": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\10_ASSETS_WORK\\archive\\A02_IllinoisTunnelMap1910.png",
- L70: "asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_V2\\work\\assets\\A02_IllinoisTunnelMap1910_full_map.png",
- L86: "asset": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_V2\\work\\assets\\S006_P004_full_reconstruction.png",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/state.json\`
Keywords: caption, ass, final_upload
- L3: "source_v1": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_FINAL\\HIA_CHICAGO_FINAL_UPLOAD.mp4",
- L4: "motion_tests_pass": true,
- L7: "proxy_qc_pass": true,
- L9: "final_qc_pass": true,
- L10: "captions_complete": true,
- L11: "insert_tests_pass": true

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/_V2/work/v1_snapshot.json\`
Keywords: srt, final_upload
- L3: "path": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_FINAL\\HIA_CHICAGO_FINAL_UPLOAD.mp4",
- L8: "path": "C:\\Users\\KK\\Desktop\\Youtube 2\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\_FINAL\\HIA_CHICAGO_FINAL_UPLOAD.srt",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/DOWNLOAD_FAILURES.csv\`
Keywords: ass
- L1: asset_id;expected_filename;source_page;failed_url;reason;recommended_action

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/DOWNLOAD_REPORT.json\`
Keywords: ass
- L16: "media_validation": "PASS",
- L25: "Six Wikimedia images use official 1280px versions of the identical source assets. See DOWNLOAD_RECOVERY.json."

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/DOWNLOAD_SOURCE_AUDIT.json\`
Keywords: ass
- L9: "wgWMEPageLength\":1000,\"wbUserPreferredContentLanguages\":[\"en\"],\"wbUserSpecifiedLanguages\":[\"en\"],\"wbCopyright\":{\"version\":\"wikibase-1\",\"messageHtml\":\"By clicking \\\"publish\\\", you agree to the \\u003Ca href=\\\"/wiki/Commons:Copyrights\\\" class=\\\"mw-redirect\\\" title=\\\"Commons:Copyrights\\\"\\u003Eterms of use\\u003C/a\\u003E, and you irr",
- L10: ":\"wikibase-1\",\"messageHtml\":\"By clicking \\\"publish\\\", you agree to the \\u003Ca href=\\\"/wiki/Commons:Copyrights\\\" class=\\\"mw-redirect\\\" title=\\\"Commons:Copyrights\\\"\\u003Eterms of use\\u003C/a\\u003E, and you irrevocably agree to release your contribution under the \\u003Ca rel=\\\"nofollow\\\" class=\\\"external text\\\" href=\\\"https://cre",
- L11: "\", you agree to the \\u003Ca href=\\\"/wiki/Commons:Copyrights\\\" class=\\\"mw-redirect\\\" title=\\\"Commons:Copyrights\\\"\\u003Eterms of use\\u003C/a\\u003E, and you irrevocably agree to release your contribution under the \\u003Ca rel=\\\"nofollow\\\" class=\\\"external text\\\" href=\\\"https://creativecommons.org/publicdomain/zero/1.0/\\\"\\u003ECrea",
- L32: "wgWMEPageLength\":1000,\"wbUserPreferredContentLanguages\":[\"en\"],\"wbUserSpecifiedLanguages\":[\"en\"],\"wbCopyright\":{\"version\":\"wikibase-1\",\"messageHtml\":\"By clicking \\\"publish\\\", you agree to the \\u003Ca href=\\\"/wiki/Commons:Copyrights\\\" class=\\\"mw-redirect\\\" title=\\\"Commons:Copyrights\\\"\\u003Eterms of use\\u003C/a\\u003E, and you irr",
- L33: ":\"wikibase-1\",\"messageHtml\":\"By clicking \\\"publish\\\", you agree to the \\u003Ca href=\\\"/wiki/Commons:Copyrights\\\" class=\\\"mw-redirect\\\" title=\\\"Commons:Copyrights\\\"\\u003Eterms of use\\u003C/a\\u003E, and you irrevocably agree to release your contribution under the \\u003Ca rel=\\\"nofollow\\\" class=\\\"external text\\\" href=\\\"https://cre",
- L34: "\", you agree to the \\u003Ca href=\\\"/wiki/Commons:Copyrights\\\" class=\\\"mw-redirect\\\" title=\\\"Commons:Copyrights\\\"\\u003Eterms of use\\u003C/a\\u003E, and you irrevocably agree to release your contribution under the \\u003Ca rel=\\\"nofollow\\\" class=\\\"external text\\\" href=\\\"https://creativecommons.org/publicdomain/zero/1.0/\\\"\\u003ECrea",
- L77: "wgWMEPageLength\":2000,\"wbUserPreferredContentLanguages\":[\"en\"],\"wbUserSpecifiedLanguages\":[\"en\"],\"wbCopyright\":{\"version\":\"wikibase-1\",\"messageHtml\":\"By clicking \\\"publish\\\", you agree to the \\u003Ca href=\\\"/wiki/Commons:Copyrights\\\" class=\\\"mw-redirect\\\" title=\\\"Commons:Copyrights\\\"\\u003Eterms of use\\u003C/a\\u003E, and you irr",
- L78: ":\"wikibase-1\",\"messageHtml\":\"By clicking \\\"publish\\\", you agree to the \\u003Ca href=\\\"/wiki/Commons:Copyrights\\\" class=\\\"mw-redirect\\\" title=\\\"Commons:Copyrights\\\"\\u003Eterms of use\\u003C/a\\u003E, and you irrevocably agree to release your contribution under the \\u003Ca rel=\\\"nofollow\\\" class=\\\"external text\\\" href=\\\"https://cre",

### \`Hidden_Industrial_America_Chicago_CODEX_READY_v7/MEDIA_VALIDATION.json\`
Keywords: caption, ass
- L5: "destination": "10_ASSETS_WORK/archive/A01_IllinoisTunnelIntersectionCloser.jpg",
- L63: "captions": 0,
- L73: "filename": "C:\\Users\\KK\\Desktop\\Youtube\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\10_ASSETS_WORK\\archive\\A01_IllinoisTunnelIntersectionCloser.jpg",
- L92: "destination": "10_ASSETS_WORK/archive/A02_IllinoisTunnelMap1910.png",
- L146: "captions": 0,
- L156: "filename": "C:\\Users\\KK\\Desktop\\Youtube\\Hidden_Industrial_America_Chicago_CODEX_READY_v7\\10_ASSETS_WORK\\archive\\A02_IllinoisTunnelMap1910.png",
- L172: "destination": "10_ASSETS_WORK/archive/A14_LOC_State_Street_1905.jpg",
- L230: "captions": 0,
