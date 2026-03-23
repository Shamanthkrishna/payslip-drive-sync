param(
    [string]$TaskName = 'PayslipSync_Auto',
    [string]$RunAt = '09:00',
    [int]$MaxMonths = 24,
    [int]$Attempts = 3,
    [int]$RetryDelayMin = 20,
    [int]$WindowStartDay = 6,
    [int]$WindowEndDay = 12
)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$runScript = Join-Path $PSScriptRoot 'run_scheduled_sync.ps1'
if (-not (Test-Path $runScript)) {
    throw "Missing script: $runScript"
}

$actionArgs = @(
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-WindowStyle', 'Hidden',
    '-File', "`"$runScript`"",
    '-MaxMonths', $MaxMonths,
    '-Attempts', $Attempts,
    '-RetryDelayMin', $RetryDelayMin,
    '-WindowStartDay', $WindowStartDay,
    '-WindowEndDay', $WindowEndDay
) -join ' '

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $actionArgs
$trigger = New-ScheduledTaskTrigger -Daily -At $RunAt
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 30)

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description 'Automatic monthly payslip sync with retry window and background execution'

Write-Host "Scheduled task '$TaskName' created successfully."
Write-Host "Runs daily at $RunAt in background, but sync only executes during day $WindowStartDay-$WindowEndDay each month."
Write-Host "Task-level restart on failure: 3 times every 30 minutes."
Write-Host "Script-level retries per run: $Attempts attempts, $RetryDelayMin minutes apart."
