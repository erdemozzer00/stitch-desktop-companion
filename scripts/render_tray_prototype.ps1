$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$output=Join-Path $repo '.local/phase-04/tray-visual-prototype'
New-Item -ItemType Directory -Force -Path $output | Out-Null
$compiler=Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
& $compiler /nologo /target:exe /codepage:65001 /warnaserror+ /reference:System.Drawing.dll "/out:$output\TrayVisualPrototype.exe" "$repo\scripts\TrayVisualPrototype.cs"
if($LASTEXITCODE -ne 0){throw 'Prototype compilation failed.'}
& "$output/TrayVisualPrototype.exe" "$repo/.local/phase-03/appearance-final/idle/idle_0001.png" $output
if($LASTEXITCODE -ne 0){throw 'Prototype rendering failed.'}
Write-Output $output
