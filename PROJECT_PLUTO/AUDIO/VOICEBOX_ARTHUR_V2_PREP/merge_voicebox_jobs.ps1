param(
    [string]$PackageDir = $PSScriptRoot
)

$ErrorActionPreference = 'Stop'
$package = [IO.Path]::GetFullPath($PackageDir)
$wavDir = Join-Path $package 'GENERATED_WAV'
$output = Join-Path $package 'PROJECT_PLUTO_ARTHUR_V2_ASSEMBLY_MASTER_48K_MONO_S24.wav'
$tempDir = Join-Path $package '_merge_temp'

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw 'ffmpeg not found' }
if (-not (Get-Command ffprobe -ErrorAction SilentlyContinue)) { throw 'ffprobe not found' }
if (Test-Path -LiteralPath $output) { throw "Output already exists: $output" }
if (Test-Path -LiteralPath $tempDir) { throw "Temporary directory already exists: $tempDir" }

$expected = 1..8 | ForEach-Object {
    $ch = 'CH{0:D2}' -f $_
    Join-Path $wavDir ('PROJECT_PLUTO_V2_JOB_{0:D2}_{1}.wav' -f $_, $ch)
}
$missing = @($expected | Where-Object { -not (Test-Path -LiteralPath $_ -PathType Leaf) })
if ($missing.Count -gt 0) { throw "Missing generated WAV files: $($missing -join ', ')" }

New-Item -ItemType Directory -Path $tempDir | Out-Null
$converted = @()
for ($i = 0; $i -lt $expected.Count; $i++) {
    $dest = Join-Path $tempDir ('JOB_{0:D2}.wav' -f ($i + 1))
    & ffmpeg -v error -xerror -i $expected[$i] -vn -ar 48000 -ac 1 -c:a pcm_s24le $dest
    if ($LASTEXITCODE -ne 0) { throw "Conversion failed for $($expected[$i])" }
    $converted += $dest
}

$silence = Join-Path $tempDir 'SILENCE_600MS.wav'
& ffmpeg -v error -xerror -f lavfi -i 'anullsrc=r=48000:cl=mono' -t 0.600 -c:a pcm_s24le $silence
if ($LASTEXITCODE -ne 0) { throw 'Silence generation failed' }

$concatFile = Join-Path $tempDir 'concat.txt'
$concatLines = @()
for ($i = 0; $i -lt $converted.Count; $i++) {
    $concatLines += "file '$($converted[$i].Replace("'", "''"))'"
    if ($i -lt $converted.Count - 1) {
        $concatLines += "file '$($silence.Replace("'", "''"))'"
    }
}
[IO.File]::WriteAllLines($concatFile, $concatLines, [Text.UTF8Encoding]::new($false))

& ffmpeg -v error -xerror -f concat -safe 0 -i $concatFile -c:a pcm_s24le -ar 48000 -ac 1 $output
if ($LASTEXITCODE -ne 0) { throw 'Master assembly failed' }
& ffmpeg -v error -xerror -i $output -f null NUL
if ($LASTEXITCODE -ne 0) { throw 'Master full decode failed' }

$probe = & ffprobe -v error -show_entries 'format=duration:stream=codec_name,sample_rate,channels,bits_per_sample' -of json $output
[IO.File]::WriteAllText((Join-Path $package 'MASTER_FFPROBE.json'), $probe, [Text.UTF8Encoding]::new($false))
$hash = (Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText((Join-Path $package 'MASTER_SHA256.txt'), "$hash  $([IO.Path]::GetFileName($output))`n", [Text.UTF8Encoding]::new($false))

Get-ChildItem -LiteralPath $tempDir -File | Remove-Item -Force
Remove-Item -LiteralPath $tempDir -Force
Write-Output "ASSEMBLY_COMPLETE $output"
