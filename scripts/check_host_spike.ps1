$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$output = Join-Path $repo '.local\phase-02\host-checks'
New-Item -ItemType Directory -Force -Path $output | Out-Null
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
& $compiler /nologo /target:exe /main:HostChecks /platform:x64 /optimize+ /warnaserror+ /codepage:65001 `
    "/out:$output\HostChecks.exe" "/win32manifest:$repo\host\app.manifest" `
    /reference:System.Windows.Forms.dll /reference:System.Drawing.dll "$repo\host\PetSpike.cs" "$repo\host\HostChecks.cs"
if ($LASTEXITCODE -ne 0) { throw 'Host check compilation failed.' }
$scratch = Join-Path $output ([DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff'))
$result = & "$output\HostChecks.exe" "$repo\.local\phase-02\host\assets" $scratch
if ($LASTEXITCODE -ne 0) { throw 'Host component checks failed; see console output. No acceptance evidence updated.' }
$report = $result | ConvertFrom-Json
$report | Add-Member -NotePropertyName 'checked_at_utc' -NotePropertyValue ([DateTime]::UtcNow.ToString('o'))
$report | Add-Member -NotePropertyName 'host_source_sha256' -NotePropertyValue ((Get-FileHash -LiteralPath "$repo\host\PetSpike.cs" -Algorithm SHA256).Hash.ToLowerInvariant())
$report | Add-Member -NotePropertyName 'checks_source_sha256' -NotePropertyValue ((Get-FileHash -LiteralPath "$repo\host\HostChecks.cs" -Algorithm SHA256).Hash.ToLowerInvariant())
$report | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath "$repo\context\evidence\phase-02-host-checks.json" -Encoding UTF8
$result
