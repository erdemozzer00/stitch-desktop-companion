param([string]$TrialDirectory)
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$trial=if($TrialDirectory){[IO.Path]::GetFullPath($TrialDirectory)}else{Join-Path $repo '.local\phase-07\trial'}
$compiler=Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
& $compiler /nologo /target:exe /main:HandChecks /platform:x64 /optimize+ /warnaserror+ /codepage:65001 "/out:$trial\HandChecks.exe" "/win32manifest:$repo\host\app.manifest" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll "$repo\host\PetSpike.cs" "$repo\host\CarryMotion.cs" "$repo\host\CompanionUi.cs" "$repo\host\HandChecks.cs"
if($LASTEXITCODE -ne 0){throw 'Hand checks compile failed.'}
$scratch=Join-Path $trial ('hand-checks-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff'))
& "$trial\HandChecks.exe" $trial $scratch
if($LASTEXITCODE -ne 0){throw 'Hand gesture checks failed.'}
