param([switch]$DesktopShortcut,[switch]$Probe)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$trial = [IO.Path]::GetFullPath((Join-Path $repo '.local/phase-04/native-trial'))
$exe = Join-Path $trial 'StitchPet.exe'
foreach ($path in @($exe, "$trial/trial-assets.json", "$trial/assets/idle_0001.png", "$trial/carry/anchors.csv")) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Build and stage the isolated trial first: $path" }
}
$arguments = '"--carry=' + (Join-Path $trial 'carry') + '"'
if($Probe){$arguments+=' --probe'}
if ($DesktopShortcut) {
    $shortcutPath = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Stitch - Tasima Denemesi.lnk'
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    if ((Test-Path -LiteralPath $shortcutPath) -and $shortcut.TargetPath -ne $exe) {
        throw 'An unrelated shortcut already uses the trial name.'
    }
    $shortcut.TargetPath = $exe
    $shortcut.Arguments = $arguments
    $shortcut.WorkingDirectory = $trial
    $shortcut.Description = 'Isolated open-eye carry trial; accepted Stitch installation remains separate.'
    $shortcut.Save()
}
# Avoid starting a second copy of this trial through this helper. Full app-wide
# duplicate-instance handling remains Phase 05 work.
$running = @(Get-Process StitchPet -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $exe })
if ($running.Count -gt 0) { Write-Output "Trial is already running (PID $($running[0].Id))."; return }
$process = Start-Process -FilePath $exe -ArgumentList $arguments -WorkingDirectory $trial -WindowStyle Normal -PassThru
Start-Sleep -Milliseconds 900
$process.Refresh()
if ($process.HasExited) { throw 'Trial exited during launch; inspect its failure.log.' }
$record = [ordered]@{
    status = 'RUNNING_AT_CHECK'; checked_at_utc = [DateTime]::UtcNow.ToString('o'); pid = $process.Id
    executable_sha256 = (Get-FileHash -LiteralPath $exe).Hash.ToLowerInvariant()
    revision = 'phase04-tray-remote'; installed_baseline_changed = $false
    limits = 'Process launch verified only. Physical mouse and user visual acceptance are pending.'
}
$record | ConvertTo-Json | Set-Content -Encoding UTF8 "$repo/context/evidence/phase-04-native-launch.json"
$record | ConvertTo-Json
