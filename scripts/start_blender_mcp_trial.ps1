param(
    [string]$Blender = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$trialDir = Join-Path $repoRoot '.local/phase-02/mcp-trial'
$sourceAddon = Join-Path $repoRoot '.local/runtime/blender-mcp-official/addon'
if (-not (Test-Path -LiteralPath $sourceAddon)) { throw 'Install the reviewed official source first; see tooling research notes.' }
if (Get-NetTCPConnection -LocalPort 9877 -State Listen -ErrorAction SilentlyContinue) { throw 'Trial port 9877 is already in use.' }
New-Item -ItemType Directory -Force -Path $trialDir | Out-Null
$trialBlend = Join-Path $trialDir 'stitch-trial.blend'
# Preserve an existing trial copy; the bootstrap never saves changes to it.
if (-not (Test-Path -LiteralPath $trialBlend)) {
    Copy-Item -LiteralPath (Join-Path $repoRoot '.local/phase-01/stitch-stage.blend') -Destination $trialBlend
}
$previousBlenderResources = $env:BLENDER_USER_RESOURCES
try {
    $env:BLENDER_USER_RESOURCES = Join-Path $trialDir 'blender-profile'
    $trialArguments = @(
        '--disable-autoexec', '--online-mode', '--threads', '4',
        '--no-window-focus', '--window-geometry', '0', '0', '1200', '850',
        ('"' + $trialBlend + '"'), '--python-exit-code', '1', '--python',
        ('"' + (Join-Path $PSScriptRoot 'blender_mcp_trial_bootstrap.py') + '"')
    )
    $trialProcess = Start-Process -FilePath $Blender -ArgumentList $trialArguments -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $trialDir 'blender-stdout.log') `
        -RedirectStandardError (Join-Path $trialDir 'blender-stderr.log')
    $trialProcess.Id | Set-Content (Join-Path $trialDir 'blender.pid')
    Write-Output ('Started isolated Blender trial PID ' + $trialProcess.Id)
} finally {
    $env:BLENDER_USER_RESOURCES = $previousBlenderResources
}
