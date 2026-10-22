param([string]$Destination = (Join-Path $PSScriptRoot "PROJECT_PLUTO_HIA_ARCHIVE"), [switch]$IncludeNative)
$ErrorActionPreference = "Stop"
$Base = "https://github.com/reverendstanislav-bot/Youtube-2/releases/download/"
$Assets = @(
  @{Folder="01_FULL_MOVIES_MP4";Tag="project-pluto-full-mp4-F020-20261021";Name="F020_FULL_SOURCE.mp4"},
  @{Folder="01_FULL_MOVIES_MP4";Tag="project-pluto-full-mp4-F026-20261021";Name="F026_FULL_SOURCE.mp4"},
  @{Folder="01_FULL_MOVIES_MP4";Tag="project-pluto-full-mp4-F031-20261021";Name="F031_FULL_SOURCE.mp4"},
  @{Folder="01_FULL_MOVIES_MP4";Tag="project-pluto-full-mp4-F011-20261021";Name="F011_FULL_SOURCE.mp4"},
  @{Folder="01_FULL_MOVIES_MP4";Tag="project-pluto-full-mp4-F013-20261021";Name="F013_FULL_SOURCE.mp4"},
  @{Folder="01_FULL_MOVIES_MP4";Tag="project-pluto-full-mp4-F015-20261021";Name="F015_FULL_SOURCE.mp4"},
  @{Folder="01_FULL_MOVIES_MP4";Tag="project-pluto-full-mp4-F018-20261021";Name="F018_FULL_SOURCE.mp4"},
  @{Folder="02_SELECTED_SCENES";Tag="project-pluto-40-scene-bank-20261021";Name="PROJECT_PLUTO_40_REAL_CONTEXT_SCENES.zip"},
  @{Folder="02_SELECTED_SCENES";Tag="project-pluto-40-scene-bank-20261021";Name="SCENE_BANK_40_SOURCE_IN_OUT.csv"},
  @{Folder="03_REAL_HISTORICAL_PHOTOS";Tag="project-pluto-39-real-historical-photos-20261021";Name="PROJECT_PLUTO_REAL_HISTORICAL_PHOTOS_39_FILES.zip"},
  @{Folder="03_REAL_HISTORICAL_PHOTOS";Tag="project-pluto-39-real-historical-photos-20261021";Name="PHOTO_MASTER_INDEX.csv"},
  @{Folder="04_PRIMARY_PLUTO_REPORTS";Tag="project-pluto-authentic-primary-documents-20261021";Name="DOC-01.pdf"},
  @{Folder="04_PRIMARY_PLUTO_REPORTS";Tag="project-pluto-authentic-primary-documents-20261021";Name="DOC-02.pdf"},
  @{Folder="04_PRIMARY_PLUTO_REPORTS";Tag="project-pluto-authentic-primary-documents-20261021";Name="DOC-03.pdf"},
  @{Folder="04_PRIMARY_PLUTO_REPORTS";Tag="project-pluto-authentic-primary-documents-20261021";Name="DOC-04.pdf"},
  @{Folder="04_PRIMARY_PLUTO_REPORTS";Tag="project-pluto-authentic-primary-documents-20261021";Name="DOC-05.pdf"},
  @{Folder="04_PRIMARY_PLUTO_REPORTS";Tag="project-pluto-authentic-primary-documents-20261021";Name="DOCUMENT_MANIFEST.json"}
)
if ($IncludeNative) {
  $Assets += @(
    @{Folder="00_UNCHANGED_NATIVE_SOURCE_FILES";Tag="project-pluto-archive-batch1-20261021";Name="F020.webm"},
    @{Folder="00_UNCHANGED_NATIVE_SOURCE_FILES";Tag="project-pluto-archive-batch1-20261021";Name="F026.webm"},
    @{Folder="00_UNCHANGED_NATIVE_SOURCE_FILES";Tag="project-pluto-archive-batch1-20261021";Name="F031.ogv"},
    @{Folder="00_UNCHANGED_NATIVE_SOURCE_FILES";Tag="project-pluto-context-source-F011-20261021";Name="F011.webm"},
    @{Folder="00_UNCHANGED_NATIVE_SOURCE_FILES";Tag="project-pluto-context-source-F013-20261021";Name="F013.webm"},
    @{Folder="00_UNCHANGED_NATIVE_SOURCE_FILES";Tag="project-pluto-context-source-F015-20261021";Name="F015.webm"},
    @{Folder="00_UNCHANGED_NATIVE_SOURCE_FILES";Tag="project-pluto-context-source-F018-20261021";Name="F018.webm"}
  )
}
$results = New-Object System.Collections.ArrayList
foreach ($a in $Assets) {
  $dir=Join-Path $Destination $a.Folder
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $target=Join-Path $dir $a.Name
  $url=$Base + $a.Tag + "/" + $a.Name
  try {
    Write-Host ("DOWNLOAD " + $a.Name)
    Invoke-WebRequest -Uri $url -OutFile $target -UseBasicParsing -MaximumRedirection 10 -TimeoutSec 1800
    $size=(Get-Item $target).Length
    if ($size -lt 1000) { throw ("Truncated media file: " + $a.Name) }
    $hash=(Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
    [void]$results.Add([PSCustomObject]@{Folder=$a.Folder; File=$a.Name; Bytes=$size; SHA256=$hash; Status="DOWNLOADED"; Source=$url})
  } catch {
    Write-Warning ("FAILED " + $a.Name + " : " + $_.Exception.Message)
    [void]$results.Add([PSCustomObject]@{Folder=$a.Folder; File=$a.Name; Bytes=0; SHA256=""; Status="FAILED"; Source=$url})
  }
}
New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$results | Export-Csv -Path (Join-Path $Destination "DOWNLOAD_VERIFY_SHA256.csv") -NoTypeInformation -Encoding UTF8
Write-Host ("Total downloaded " + ($results | Where-Object Status -eq "DOWNLOADED").Count + " of " + $results.Count)
if (($results | Where-Object Status -eq "FAILED").Count -gt 0) { throw "Not all sources downloaded. Review DOWNLOAD_VERIFY_SHA256.csv and rerun this script." }
Write-Host ("Complete: " + $Destination)
