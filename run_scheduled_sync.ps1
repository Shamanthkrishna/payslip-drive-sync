param(
    [int]$MaxMonths = 24,
    [int]$Attempts = 3,
    [int]$RetryDelayMin = 20,
    [int]$WindowStartDay = 6,
    [int]$WindowEndDay = 12
)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$pythonw = Join-Path $PSScriptRoot '.venv\Scripts\pythonw.exe'
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'

if (Test-Path $pythonw) {
    $py = $pythonw
} elseif (Test-Path $python) {
    $py = $python
} else {
    $py = 'python'
}

$arguments = @(
    'scheduled_sync.py',
    '--max-months', $MaxMonths,
    '--attempts', $Attempts,
    '--retry-delay-min', $RetryDelayMin,
    '--window-start-day', $WindowStartDay,
    '--window-end-day', $WindowEndDay
)

& $py @arguments
exit $LASTEXITCODE
