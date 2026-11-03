$ErrorActionPreference = 'Stop'
$queueRoot = 'C:\YOUTUBE\Youtube 2\VIDEO 10\AUDIO\R5_1_HARRISON_QUEUE'
$pidFile = Join-Path $queueRoot 'worker.pid'
if (Test-Path -LiteralPath $pidFile) {
    $savedPid = ([IO.File]::ReadAllText($pidFile)).Trim()
    if ($savedPid -match '^\d+$') {
        $existingWorker = Get-CimInstance Win32_Process -Filter "ProcessId=$savedPid"
        if ($existingWorker -and $existingWorker.CommandLine -and $existingWorker.CommandLine.Contains($queueRoot) -and $existingWorker.CommandLine.Contains('voice_queue_worker.py')) {
            Write-Output "Queue worker already running: $savedPid"
            exit 0
        }
    }
}
$workerPath = Join-Path $queueRoot 'voice_queue_worker.py'
$queueInput = Join-Path $queueRoot '08_VOICE_JOBS_R5_1.json'
$workerArguments = @(('"' + $workerPath + '"'),'--queue',('"' + $queueInput + '"'),'--state-dir',('"' + $queueRoot + '"'))
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$process = Start-Process -FilePath (Get-Command python).Source -ArgumentList $workerArguments -WorkingDirectory $queueRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $queueRoot "worker_$stamp.stdout.log") -RedirectStandardError (Join-Path $queueRoot "worker_$stamp.stderr.log") -PassThru
$process.Id | Set-Content -LiteralPath $pidFile
Write-Output "Existing queue resumed by worker $($process.Id); no completion wait."
