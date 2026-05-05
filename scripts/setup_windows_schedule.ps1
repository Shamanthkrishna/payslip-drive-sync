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

# Resolve project root (one level above this scripts/ folder)
$root = Split-Path $PSScriptRoot -Parent
Set-Location -Path $root

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

# Primary trigger: daily at RunAt.
# StartWhenAvailable = if the machine was off when this fired, run it as soon as it boots.
$triggerDaily = New-ScheduledTaskTrigger -Daily -At $RunAt

# Backup trigger: at every user logon.
# This catches the case where the machine boots AFTER the daily window and StartWhenAvailable
# has already fired the task before the user logged in (e.g., network not yet available).
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 30) `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger @($triggerDaily, $triggerLogon) `
    -Settings $settings `
    -RunLevel Highest `
    -Description 'Automatic monthly payslip sync. Runs daily + at logon. Script-level window guards ensure it only syncs on days 6-12 of the month, and only once per month via state file.'

Write-Host ""
Write-Host "Scheduled task '$TaskName' created successfully." -ForegroundColor Green
Write-Host ""
Write-Host "Triggers:"
Write-Host "  - Daily at $RunAt (StartWhenAvailable covers missed runs when PC was off)"
Write-Host "  - At every logon (backup for late-boot / network-delay scenarios)"
Write-Host ""
Write-Host "Retry behaviour:"
Write-Host "  - Task Scheduler level: 3 restarts x 30 minutes apart (e.g., transient failures)"
Write-Host "  - Script level: $Attempts attempts, $RetryDelayMin minutes apart per invocation"
Write-Host "  - Monthly window: days $WindowStartDay-$WindowEndDay only; skips if already synced this month"
Write-Host ""
Write-Host "On failure after all retries an email will be sent to the configured EMAIL_RECIPIENT."
