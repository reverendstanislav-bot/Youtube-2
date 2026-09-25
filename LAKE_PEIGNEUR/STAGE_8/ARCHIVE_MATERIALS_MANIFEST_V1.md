# LAKE PEIGNEUR — ARCHIVE MATERIALS MANIFEST V1

Updated: 2026-09-25

Status: **ARCHIVE COLLECTION COMPLETE — REVIEW BEFORE PROMPT PACK**

GitHub Actions build:
- workflow: `Build Lake Peigneur Archive Pack`
- run: `36176288181`
- conclusion: **SUCCESS**
- artifact id: `10882273779`
- artifact name: `LAKE_PEIGNEUR_ARCHIVE_SOURCE_PACK_V1`
- artifact size: **491,271,292 bytes**
- artifact digest: `sha256:67e97d6d664ae14c908598494f3fb766918ff5c409e057e83ab2dc0fac16ba86`
- artifact retention: through **2026-10-25**

Inner production archive:
- `LAKE_PEIGNEUR_ARCHIVE_SOURCE_PACK_V1.zip`
- unpacked archive contents: **108 files**
- unpacked payload size represented in ZIP listing: **502,761,725 bytes**

## Included

### 01_PRIMARY_MSHA
- full 149-page MSHA 1981 Jefferson Island Mine Inundation report;
- extracted report text;
- Appendix T estimated drill-hole-location page as PDF + high-resolution JPEG;
- MSHA FY1981 annual report;
- relevant evacuation page extracted as PDF + JPEG.

### 02_MSHA_APPENDIX_EE_CONDITIONAL
- Appendix EE pages 120–149 rendered as JPEGs;
- page-caption index CSV;
- high-resolution embedded image extractions from the photo section;
- **40 extracted large RGB image files**;
- four Appendix EE contact sheets in editor helpers.

Rights state:
**CONDITIONAL_USE.**
These are genuine materials embedded in the federal report, but individual photograph credits are not reliably exposed in OCR. Do not automatically mark a frame HISTORICAL SOURCE until the chosen image has been individually provenance-checked.

### 03_USGS_HISTORICAL_GEOLOGY_PD
- USGS Bulletin 669;
- USGS Bulletin 845;
- USGS WRI 90-4060 salt-dome map;
- USGS Bulletin 1794 Gulf Coast salt domes.

Rights:
**PUBLIC DOMAIN federal material.**

### 04_USGS_HISTORICAL_MAPS_PD
- USGS Delcambre 1:24,000 historical topo, map date 1963;
- license note.

Rights:
**PUBLIC DOMAIN.**

### 05_PUBLIC_DOMAIN_CONTEXT
- USGS Landsat 8 Louisiana salt-dome-islands image;
- explicit public-domain source note.

### 06_CC_LICENSED_REFERENCE
- OpenStreetMap Lake Peigneur map — CC BY 2.5;
- later MAPPA PEIGNEUR schematic — CC BY 4.0, reference geometry only;
- attribution file included.

### 07_REFERENCE_ONLY_LINKS
Copyrighted/un-cleared sources are represented by links only:
- UPI;
- Louisiana Geological Survey catalogs;
- GCAGS/HGS articles;
- 64 Parishes;
- ONEOK;
- legal decisions.

No copyrighted article screenshots or unlicensed stock/video were copied into the archive.

### 08_EDITOR_HELPERS
- four Appendix EE contact sheets for fast visual review.

## Integrity

The archive contains:
- `ARCHIVE_ASSET_MANIFEST.csv`
- `SHA256SUMS.txt`
- `LICENSE_NOTES.md`
- `README_FIRST.md`

## Production gate

Do not start Stage 9 generation prompts until the archival material is reviewed against all 87 beats.

Required next pass:
1. inspect Appendix EE images;
2. individually trace/clear the strongest genuine historical frames;
3. replace reconstruction gaps wherever a cleared archive image genuinely covers the narration;
4. recalculate reconstruction count and cost;
5. only then write the final generation prompt pack.

Image generation performed during archive collection:
**0**
