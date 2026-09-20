param([string]$TrialDirectory, [string]$EvidenceName='phase-04-tray-ui-checks.json')
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$output=if($TrialDirectory){[IO.Path]::GetFullPath($TrialDirectory)}else{Join-Path $repo '.local/phase-04/polished-trial'}
$compiler=Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
& $compiler /nologo /target:exe /main:PolishChecks /platform:x64 /optimize+ /warnaserror+ /codepage:65001 `
    "/out:$output\PolishChecks.exe" "/win32manifest:$repo\host\app.manifest" `
    /reference:System.Windows.Forms.dll /reference:System.Drawing.dll `
    "$repo\host\PetSpike.cs" "$repo\host\CarryMotion.cs" "$repo\host\CompanionUi.cs" "$repo\host\PolishChecks.cs"
if($LASTEXITCODE -ne 0){throw 'Polish checks compilation failed.'}
$result=& "$output/PolishChecks.exe" $output
if($LASTEXITCODE -ne 0){throw 'Polish checks failed.'}
$report=$result | ConvertFrom-Json
$report | Add-Member checked_at_utc ([DateTime]::UtcNow.ToString('o'))
$report | Add-Member sources (@('PetSpike.cs','CarryMotion.cs','CompanionUi.cs','PolishChecks.cs') | ForEach-Object {
    @{name=$_;sha256=(Get-FileHash -LiteralPath "$repo/host/$_").Hash.ToLowerInvariant()}
})
$report | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 "$repo/context/evidence/$EvidenceName"
$result
