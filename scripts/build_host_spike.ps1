param([switch]$Probe, [string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$output = if ($OutputDirectory) { [IO.Path]::GetFullPath($OutputDirectory) } else { Join-Path $repo '.local/phase-02/host' }
New-Item -ItemType Directory -Force -Path $output | Out-Null
$compiler = Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
& $compiler /nologo /target:winexe /platform:x64 /optimize+ /warnaserror+ /codepage:65001 `
    "/out:$output\StitchPet.exe" "/win32manifest:$repo\host\app.manifest" `
    /reference:System.Windows.Forms.dll /reference:System.Drawing.dll "$repo\host\PetSpike.cs"
if ($LASTEXITCODE -ne 0) { throw 'Host compilation failed.' }
'<configuration><startup><supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.8" /></startup></configuration>' |
    Set-Content -LiteralPath "$output/StitchPet.exe.config" -Encoding UTF8
$assets = Join-Path $output 'assets'
New-Item -ItemType Directory -Force -Path $assets | Out-Null
# Assets are installed only by update_host_motion.ps1 after manifest validation.
Write-Output "Built $output/StitchPet.exe"
if ($Probe) {
    # Explicit interactive test surface, intentionally visible for inspection.
    $process = Start-Process -FilePath "$output/StitchPet.exe" -ArgumentList '--probe' -PassThru
    $process.Id | Set-Content -LiteralPath "$output/process.pid"
    Write-Output "Interactive probe PID: $($process.Id)"
}
