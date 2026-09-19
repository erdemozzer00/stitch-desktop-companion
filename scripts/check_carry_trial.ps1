param([switch]$Live)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$trial = Join-Path $repo '.local/phase-04/native-trial'
$compiler = Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
& $compiler /nologo /target:exe /main:CarryChecks /platform:x64 /optimize+ /warnaserror+ /codepage:65001 `
    "/out:$trial\CarryChecks.exe" "/win32manifest:$repo\host\app.manifest" `
    /reference:System.Windows.Forms.dll /reference:System.Drawing.dll `
    "$repo\host\PetSpike.cs" "$repo\host\CarryMotion.cs" "$repo\host\CarryChecks.cs"
if ($LASTEXITCODE -ne 0) { throw 'Carry checks compilation failed.' }
$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff')
$modes = if ($Live) { @('--live-baseline','--live-carry') } else { @('component') }
foreach ($mode in $modes) {
    $scratch = Join-Path $trial "checks-$stamp-$mode"
    $result = if ($mode -eq 'component') { & "$trial/CarryChecks.exe" $trial $scratch } else { & "$trial/CarryChecks.exe" $trial $scratch $mode }
    if ($LASTEXITCODE -ne 0) { throw "Carry check failed: $mode" }
    $report = $result | ConvertFrom-Json
    $report | Add-Member checked_at_utc ([DateTime]::UtcNow.ToString('o'))
    $report | Add-Member sources (@('PetSpike.cs','CarryMotion.cs','CarryChecks.cs') | ForEach-Object {
        @{ name = $_; sha256 = (Get-FileHash -LiteralPath "$repo/host/$_").Hash.ToLowerInvariant() }
    })
    $report | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 "$repo/context/evidence/phase-04-native-$($mode.TrimStart('-')).json"
    $result
}
