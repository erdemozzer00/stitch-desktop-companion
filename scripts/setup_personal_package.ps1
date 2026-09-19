param([switch]$NoLaunch)
$ErrorActionPreference='Stop'
$exe=Join-Path $PSScriptRoot 'StitchPet.exe'
$icon=Join-Path $PSScriptRoot 'stitch.ico'
foreach($file in @($exe,$icon,(Join-Path $PSScriptRoot 'assets/idle_0001.png'),(Join-Path $PSScriptRoot 'carry/anchors.csv'))){if(-not(Test-Path -LiteralPath $file)){throw "Missing package file: $file"}}
$shell=New-Object -ComObject WScript.Shell
$paths=@((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Stitch.lnk'),(Join-Path ([Environment]::GetFolderPath('Startup')) 'Stitch.lnk'))
# Validate both destinations before creating either shortcut.
foreach($path in $paths){
    if(Test-Path -LiteralPath $path){$existing=$shell.CreateShortcut($path);if($existing.TargetPath -ne $exe){throw "An unrelated shortcut already exists: $path"}}
}
foreach($path in $paths){
    $link=$shell.CreateShortcut($path);$link.TargetPath=$exe;$link.Arguments='';$link.WorkingDirectory=$PSScriptRoot
    $link.IconLocation=$icon+',0';$link.Description='Stitch';$link.Save()
    $saved=$shell.CreateShortcut($path)
    if($saved.TargetPath -ne $exe -or $saved.IconLocation -ne ($icon+',0')){throw 'Shortcut verification failed.'}
}
Write-Output 'Stitch ready. Desktop and sign-in shortcuts created.'
if(-not $NoLaunch){Start-Process -FilePath $exe -WorkingDirectory $PSScriptRoot -WindowStyle Normal}
