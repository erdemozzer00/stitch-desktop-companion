$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$output=Join-Path $repo '.local/phase-04/polished-trial'
$compiler=Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
& $compiler /nologo /target:exe /main:BuildShortcutIcon /codepage:65001 /warnaserror+ /reference:System.Drawing.dll /reference:System.Windows.Forms.dll `
    "/out:$output\BuildShortcutIcon.exe" "$repo\scripts\BuildShortcutIcon.cs" "$repo\host\CompanionUi.cs" "$repo\host\PetSpike.cs" "$repo\host\CarryMotion.cs"
if($LASTEXITCODE -ne 0){throw 'Icon generator compilation failed.'}
& "$output/BuildShortcutIcon.exe" "$output/assets/idle_0001.png" "$output/stitch.ico"
if($LASTEXITCODE -ne 0){throw 'Icon validation failed.'}
