param([string]$TrialDirectory)
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$trial=if($TrialDirectory){[IO.Path]::GetFullPath($TrialDirectory)}else{Join-Path $repo '.local\phase-09\trial'}
$compiler=Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
& $compiler /nologo /target:exe /main:SmileChecks /platform:x64 /optimize+ /warnaserror+ /codepage:65001 "/out:$trial\SmileChecks.exe" "/win32manifest:$repo\host\app.manifest" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll "$repo\host\PetSpike.cs" "$repo\host\CarryMotion.cs" "$repo\host\CompanionUi.cs" "$repo\host\SmileChecks.cs"
if($LASTEXITCODE -ne 0){throw 'Smile checks compile failed.'}
$scratch=Join-Path $trial ('smile-checks-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff'))
& "$trial\SmileChecks.exe" $trial $scratch "$repo\.local\phase-08\trial"
if($LASTEXITCODE -ne 0){throw 'Smile checks failed.'}
