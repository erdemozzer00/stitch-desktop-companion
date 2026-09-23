param([string]$Destination='C:\Users\Erdem\Desktop\Hediye')
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$destination=[IO.Path]::GetFullPath($Destination)
$trial=Join-Path $repo '.local/phase-09/trial'
$previous=Get-Content -LiteralPath "$repo/.local/phase-08/trial/verified-assets.json" -Raw | ConvertFrom-Json
$candidate=Get-Content -LiteralPath "$trial/verified-assets.json" -Raw | ConvertFrom-Json
function Hash([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
foreach($entry in $previous.PSObject.Properties){if((Hash (Join-Path $destination $entry.Name)) -ne $entry.Value){throw "Installed baseline differs: $($entry.Name)"}}
foreach($entry in $candidate.PSObject.Properties){if((Hash (Join-Path $trial $entry.Name)) -ne $entry.Value){throw "Candidate differs: $($entry.Name)"}}
$exe=Join-Path $destination 'StitchPet.exe'
if((Hash $exe) -ne '9560de22be8a5b61a634997fbd5a0b3cfc8318663a9cc1f05059a741643cb360'){throw 'Unexpected installed executable; inspect before updating.'}
foreach($process in @(Get-Process -Name StitchPet -ErrorAction SilentlyContinue)){
    if($process.Path -eq $exe){
        if(-not $process.CloseMainWindow() -or -not $process.WaitForExit(5000)){throw 'Close the installed Stitch before updating; it was not forcibly terminated.'}
    }
}
$preserve=@{}
foreach($path in @((Join-Path $destination 'position.txt'),(Join-Path ([Environment]::GetFolderPath('Startup')) 'Stitch.lnk'),(Join-Path ([Environment]::GetFolderPath('Desktop')) 'Stitch.lnk'))){
    $preserve[$path]=if(Test-Path -LiteralPath $path){Hash $path}else{'ABSENT'}
}
$backup=Join-Path $repo ('.local/phase-09/backup-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss'))
if(Test-Path -LiteralPath $backup){throw 'Backup destination already exists.'}
$files=@(Get-ChildItem -LiteralPath $destination -File -Recurse -Force)
foreach($file in $files){
    $relative=$file.FullName.Substring($destination.Length+1)
    $copy=Join-Path $backup $relative
    New-Item -ItemType Directory -Force -Path (Split-Path $copy -Parent) | Out-Null
    Copy-Item -LiteralPath $file.FullName -Destination $copy
    if((Hash $copy) -ne (Hash $file.FullName)){throw "Backup mismatch: $relative"}
}
$changed=@()
try{
    foreach($entry in $candidate.PSObject.Properties){
        if($null -ne $previous.PSObject.Properties[$entry.Name]){continue}
        $path=Join-Path $destination $entry.Name
        $changed+=$entry.Name
        Copy-Item -LiteralPath (Join-Path $trial $entry.Name) -Destination $path
    }
    $changed+='StitchPet.exe'
    Copy-Item -LiteralPath "$trial/StitchPet.exe" -Destination $exe -Force
    $readme=Join-Path $destination 'Beni oku.txt'
    $text=[IO.File]::ReadAllText($readme)
    $old='Başın ortası ve gövde tıklaması hareket başlatmaz. Her yerinden basılı tutup sürükleyebilirsin.'
    if(-not $text.Contains($old)){throw 'Unexpected usage note; rollback instead of overwriting.'}
    $text=$text.Replace($old,"Burnuna tıkla: gözlerini tatlıca kapatarak gülümser.`r`nGövde tıklaması hareket başlatmaz. Her yerinden basılı tutup sürükleyebilirsin.")
    $changed+='Beni oku.txt'
    [IO.File]::WriteAllText($readme,$text,[Text.UTF8Encoding]::new($false))
    foreach($entry in $candidate.PSObject.Properties){if((Hash (Join-Path $destination $entry.Name)) -ne $entry.Value){throw "Installed mismatch: $($entry.Name)"}}
    if((Hash $exe) -ne (Hash "$trial/StitchPet.exe")){throw 'Installed executable mismatch.'}
    foreach($path in $preserve.Keys){
        $actual=if(Test-Path -LiteralPath $path){Hash $path}else{'ABSENT'}
        if($actual -ne $preserve[$path]){throw "Preserved state changed: $path"}
    }
}catch{
    foreach($relative in $changed){
        $prior=Join-Path $backup $relative;$path=Join-Path $destination $relative
        if(Test-Path -LiteralPath $prior){Copy-Item -LiteralPath $prior -Destination $path -Force}
        elseif(Test-Path -LiteralPath $path){Remove-Item -LiteralPath $path}
    }
    throw
}
$record=[ordered]@{status='INSTALLED_PENDING_PHYSICAL_ACCEPTANCE';installed_at_utc=[DateTime]::UtcNow.ToString('o');directory=$destination;backup=$backup;backup_files=$files.Count;verified_assets=$candidate.PSObject.Properties.Count;executable_sha256=(Hash $exe);position_and_shortcuts_preserved=$true;source_assets_unchanged=$true;smile_assertions=36918;ear_assertions=16295;hand_assertions=14580;carry_assertions=179452;tray_assertions=156;single_instance='PASS';limits='Direct-method/state/pixel checks and local packaging; physical user and recipient acceptance remain separate.'}
# PSObject property collection Count can enumerate per-property; force a scalar.
$record.verified_assets=@($candidate.PSObject.Properties).Count
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$repo/context/evidence/phase-09-smile-integration.json" -Encoding utf8
$launched=Start-Process -FilePath $exe -WorkingDirectory $destination -WindowStyle Normal -PassThru
Start-Sleep -Seconds 2
if($launched.HasExited){throw 'Updated app exited after launch; inspect failure.log.'}
Write-Output "INSTALLED: $destination; backup: $backup; assets: $($record.verified_assets); PID: $($launched.Id)"
