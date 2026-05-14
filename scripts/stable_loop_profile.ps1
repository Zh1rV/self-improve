param(
    [switch]$Start,
    [string]$Model = "gpt-5.3-codex",
    [int]$TimeoutSeconds = 1200,
    [switch]$NoTimeout
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = Split-Path -Parent $scriptDir
$runLoop = Join-Path $scriptDir "run_loop.py"
$selfIterate = Join-Path $scriptDir "self_iterate_model_once.py"

$stateFile = ".self-improve-loop-state.stable.json"
$logFile = ".self-improve-loop.stable.log"
$consoleOut = ".self-improve-console.stable.log"
$consoleErr = ".self-improve-console.stable.err.log"

$innerCommand = if ($NoTimeout) {
    "python `"$selfIterate`" --no-timeout --model $Model"
} else {
    "python `"$selfIterate`" --timeout-seconds $TimeoutSeconds --model $Model"
}
# Start-Process flattens ArgumentList into one command line, so the nested
# loop command must be quoted to survive as a single --command argument.
$commandArg = "`"$innerCommand`""

$loopArgs = @(
    "--cwd", $skillRoot,
    "--command", $commandArg,
    "--batch-size", "20",
    "--max-batches", "0",
    "--max-consecutive-failures", "8",
    "--retry-delay-seconds", "30",
    "--sleep-seconds", "2",
    "--state-file", $stateFile,
    "--log-file", $logFile,
    "--print-progress"
)

if (-not $Start) {
    Write-Output "Stable profile is prepared (not started)."
    Write-Output "Run this command to start:"
    $innerPreview = if ($NoTimeout) {
        "python `"$selfIterate`" --no-timeout --model $Model"
    } else {
        "python `"$selfIterate`" --timeout-seconds $TimeoutSeconds --model $Model"
    }
    $startPreview = "python `"$runLoop`" --cwd `"$skillRoot`" --command '$innerPreview' --batch-size 20 --max-batches 0 --max-consecutive-failures 8 --retry-delay-seconds 30 --sleep-seconds 2 --state-file $stateFile --log-file $logFile --print-progress"
    Write-Output $startPreview
    Write-Output "Fast self-test:"
    Write-Output "python `"$((Join-Path $scriptDir "self_test.py"))`""
    Write-Output "Watch log:"
    Write-Output "Get-Content `"$((Join-Path $skillRoot $logFile))`" -Wait -Tail 50"
    exit 0
}

$stopFile = Join-Path $skillRoot ".self-improve.stop"
if (Test-Path $stopFile) {
    Remove-Item $stopFile -Force
}

$outPath = Join-Path $skillRoot $consoleOut
$errPath = Join-Path $skillRoot $consoleErr
if (Test-Path $outPath) { Remove-Item $outPath -Force }
if (Test-Path $errPath) { Remove-Item $errPath -Force }

$argumentList = @($runLoop) + $loopArgs
$process = Start-Process -FilePath "python" `
    -ArgumentList $argumentList `
    -WorkingDirectory $skillRoot `
    -RedirectStandardOutput $outPath `
    -RedirectStandardError $errPath `
    -PassThru

Write-Output "Started stable loop profile."
Write-Output "PID=$($process.Id)"
Write-Output "STATE=$(Join-Path $skillRoot $stateFile)"
Write-Output "LOG=$(Join-Path $skillRoot $logFile)"
Write-Output "CONSOLE_OUT=$outPath"
Write-Output "CONSOLE_ERR=$errPath"
