param([string]$TrialDirectory)
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$trial=if($TrialDirectory){[IO.Path]::GetFullPath($TrialDirectory)}else{Join-Path $repo '.local\phase-08\trial'}
$compiler=Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
& $compiler /nologo /target:exe /main:EarChecks /platform:x64 /optimize+ /warnaserror+ /codepage:65001 "/out:$trial\EarChecks.exe" "/win32manifest:$repo\host\app.manifest" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll "$repo\host\PetSpike.cs" "$repo\host\CarryMotion.cs" "$repo\host\CompanionUi.cs" "$repo\host\EarChecks.cs"
if($LASTEXITCODE -ne 0){throw 'Ear checks compile failed.'}
$scratch=Join-Path $trial ('ear-checks-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff'))
& "$trial\EarChecks.exe" $trial $scratch
if($LASTEXITCODE -ne 0){throw 'Ear gesture checks failed.'}
