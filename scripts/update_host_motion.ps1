param([Parameter(Mandatory=$true)][string]$Python, [switch]$Launch)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$phase = (Resolve-Path -LiteralPath (Join-Path $repo '.local/phase-03')).Path
$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff')
$candidate = Join-Path $phase "host-candidate-$stamp"
$installed = [IO.Path]::GetFullPath((Join-Path $repo '.local/phase-02/host'))
$exe = Join-Path $installed 'StitchPet.exe'
& $Python "$PSScriptRoot/stage_host_motion.py" "$candidate/assets"
if ($LASTEXITCODE -ne 0) { throw 'Asset staging failed; installed host unchanged.' }
& "$PSScriptRoot/build_host_spike.ps1" -OutputDirectory $candidate
& "$PSScriptRoot/check_host_spike.ps1" -AssetsDirectory "$candidate/assets" -Live

# Touch only the exact installed companion process, never a same-name unrelated app.
Get-Process StitchPet -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $exe } | ForEach-Object {
    if (-not $_.CloseMainWindow()) { throw 'Close the current Stitch from its tray menu before updating.' }
    if (-not $_.WaitForExit(5000)) { throw 'Stitch did not close gracefully; installed host unchanged.' }
}
$backup = [IO.Path]::GetFullPath((Join-Path $phase "host-backup-$stamp"))
$oldAssets = [IO.Path]::GetFullPath((Join-Path $installed 'assets'))
$savedAssets = [IO.Path]::GetFullPath((Join-Path $candidate 'replaced-assets'))
if (-not $backup.StartsWith($phase + '\') -or $oldAssets -ne (Join-Path $installed 'assets') -or
    -not $savedAssets.StartsWith($phase + '\')) { throw 'Unexpected deployment paths.' }
Copy-Item -LiteralPath $installed -Destination $backup -Recurse
$position = Join-Path $installed 'position.txt'
$settingsBefore = if (Test-Path -LiteralPath $position) { (Get-FileHash -LiteralPath $position).Hash } else { $null }
try {
    Move-Item -LiteralPath $oldAssets -Destination $savedAssets
    Copy-Item -LiteralPath "$candidate/assets" -Destination $oldAssets -Recurse
    foreach ($name in @('StitchPet.exe', 'StitchPet.exe.config', 'motion-manifest.json')) {
        Copy-Item -LiteralPath (Join-Path $candidate $name) -Destination (Join-Path $installed $name) -Force
    }
    $manifest = Get-Content -LiteralPath "$installed/motion-manifest.json" -Raw | ConvertFrom-Json
    foreach ($property in $manifest.frame_sha256.PSObject.Properties) {
        if ((Get-FileHash -LiteralPath (Join-Path $oldAssets $property.Name)).Hash.ToLowerInvariant() -ne $property.Value) {
            throw "Installed frame hash mismatch: $($property.Name)"
        }
    }
    $settingsAfter = if (Test-Path -LiteralPath $position) { (Get-FileHash -LiteralPath $position).Hash } else { $null }
    if ($settingsBefore -ne $settingsAfter) { throw 'Installed settings changed unexpectedly.' }
} catch {
    # Restore files without deleting either candidate or backup evidence.
    Copy-Item -Path "$backup/*" -Destination $installed -Recurse -Force
    throw
}
$record = [ordered]@{
    status = 'PASS'; installed_at_utc = [DateTime]::UtcNow.ToString('o'); revision = $manifest.revision
    executable_sha256 = (Get-FileHash -LiteralPath $exe).Hash.ToLowerInvariant()
    frames = $manifest.frames; original_host_backup = $backup; settings_preserved = $true
    limits = 'Live smoke uses application methods, not physical mouse input. Appearance remains a 320px draft.'
}
$record | ConvertTo-Json | Set-Content -LiteralPath "$repo/context/evidence/phase-03-host-install.json" -Encoding UTF8
Write-Output "Installed $exe; preserved old host at $backup"
if ($Launch) {
    $process = Start-Process -FilePath $exe -WindowStyle Hidden -PassThru
    $process.Id | Set-Content -LiteralPath "$installed/process.pid"
    Write-Output "Launched Stitch PID $($process.Id)"
}
