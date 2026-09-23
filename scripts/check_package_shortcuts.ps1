$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$source=Join-Path $PSScriptRoot 'setup_personal_package.ps1'
$tokens=$null;$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile($source,[ref]$tokens,[ref]$errors)
if($errors.Count){throw $errors[0]}
# Execute the unchanged production function against isolated real .lnk files.
$function=$ast.Find({param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq 'Install-StitchShortcuts'},$true)
. ([ScriptBlock]::Create($function.Extent.Text))
$root=Join-Path $repo ('.local/phase-09/setup-checks-'+[Guid]::NewGuid().ToString('N'))
$package=Join-Path $root 'new gift'
foreach($directory in @($package,"$package/assets","$package/carry","$root/desktop","$root/startup")){New-Item -ItemType Directory -Path $directory -Force | Out-Null}
foreach($name in @('StitchPet.exe','stitch.ico','assets/idle_0001.png','carry/anchors.csv')){[IO.File]::WriteAllText((Join-Path $package $name),'fixture')}
$paths=@("$root/desktop/Stitch.lnk","$root/startup/Stitch.lnk")
$shell=New-Object -ComObject WScript.Shell
function Check([bool]$condition,[string]$message){if(-not $condition){throw $message}}
function Assert-Targets{
    foreach($path in $paths){
        $link=$shell.CreateShortcut($path)
        Check ($link.TargetPath -eq "$package\StitchPet.exe") 'Target mismatch'
        Check ($link.WorkingDirectory -eq $package) 'Working directory mismatch'
        Check ($link.IconLocation -eq "$package\stitch.ico,0") 'Icon mismatch'
    }
}
Install-StitchShortcuts $package $paths
Assert-Targets
Install-StitchShortcuts $package $paths
Assert-Targets
# Prior installation has been deleted: ownership metadata must still allow migration.
foreach($path in $paths){
    $link=$shell.CreateShortcut($path);$link.TargetPath="$root\removed old gift\StitchPet.exe"
    $link.WorkingDirectory="$root\removed old gift";$link.Description='Stitch';$link.Arguments='';$link.Save()
}
$oldHashes=@($paths | ForEach-Object{(Get-FileHash -LiteralPath $_).Hash})
Install-StitchShortcuts $package $paths
Assert-Targets
$backups=@(Get-ChildItem -LiteralPath "$package/.shortcut-backups" -Filter '*.lnk' -Recurse)
Check ($backups.Count -eq 2) 'Both prior links must be backed up'
$backupHashes=@($backups | ForEach-Object{(Get-FileHash -LiteralPath $_.FullName).Hash})
foreach($hash in $oldHashes){Check ($backupHashes -contains $hash) 'Backup bytes differ'}
# An unrelated second link must stop before either link changes.
$link=$shell.CreateShortcut($paths[0]);$link.TargetPath="$root\old\StitchPet.exe";$link.WorkingDirectory="$root\old";$link.Description='Stitch';$link.Save()
$link=$shell.CreateShortcut($paths[1]);$link.TargetPath="$env:WINDIR\System32\notepad.exe";$link.Description='Notes';$link.Save()
$before=@($paths | ForEach-Object{(Get-FileHash -LiteralPath $_).Hash})
$rejected=$false
try{Install-StitchShortcuts $package $paths}catch{if($_.Exception.Message -notlike 'An unrelated shortcut*'){throw};$rejected=$true}
Check $rejected 'Unrelated shortcut accepted'
for($i=0;$i -lt 2;$i++){Check ((Get-FileHash -LiteralPath $paths[$i]).Hash -eq $before[$i]) 'Failed preflight modified a link'}
Write-Output 'PASS: fresh install, repeated install, moved/deleted old folder, exact shortcut backups, unrelated-link preflight. Real desktop/startup untouched.'
