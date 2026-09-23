param([switch]$NoLaunch)
$ErrorActionPreference='Stop'
function Install-StitchShortcuts([string]$PackageRoot,[string[]]$Paths){
$exe=Join-Path $PackageRoot 'StitchPet.exe'
$icon=Join-Path $PackageRoot 'stitch.ico'
foreach($file in @($exe,$icon,(Join-Path $PackageRoot 'assets/idle_0001.png'),(Join-Path $PackageRoot 'carry/anchors.csv'))){if(-not(Test-Path -LiteralPath $file)){throw "Missing package file: $file"}}
$shell=New-Object -ComObject WScript.Shell
# Validate both destinations before creating either shortcut.
$retarget=@()
foreach($path in $Paths){
    if(Test-Path -LiteralPath $path){
        $existing=$shell.CreateShortcut($path)
        if($existing.TargetPath -ne $exe){
            # Recognize shortcuts written by earlier versions even when their
            # old folder was moved/deleted. Do not overwrite arbitrary links.
            $owned=([IO.Path]::GetFileName($existing.TargetPath) -ieq 'StitchPet.exe') -and
                ($existing.Description -eq 'Stitch') -and [string]::IsNullOrWhiteSpace($existing.Arguments) -and
                ($existing.WorkingDirectory -ieq [IO.Path]::GetDirectoryName($existing.TargetPath))
            if(-not $owned){throw "An unrelated shortcut already exists: $path"}
            $retarget+= $path
        }
    }
}
if($retarget.Count -gt 0){
    $backup=Join-Path $PackageRoot ('.shortcut-backups/'+[Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $backup -Force | Out-Null
    for($i=0;$i -lt $retarget.Count;$i++){Copy-Item -LiteralPath $retarget[$i] -Destination (Join-Path $backup ("$i-Stitch.lnk"))}
}
foreach($path in $Paths){
    $link=$shell.CreateShortcut($path);$link.TargetPath=$exe;$link.Arguments='';$link.WorkingDirectory=$PackageRoot
    $link.IconLocation=$icon+',0';$link.Description='Stitch';$link.Save()
    $saved=$shell.CreateShortcut($path)
    if($saved.TargetPath -ne $exe -or $saved.IconLocation -ne ($icon+',0')){throw 'Shortcut verification failed.'}
}
}
$paths=@((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Stitch.lnk'),(Join-Path ([Environment]::GetFolderPath('Startup')) 'Stitch.lnk'))
Install-StitchShortcuts -PackageRoot $PSScriptRoot -Paths $paths
Write-Output 'Stitch ready. Desktop and sign-in shortcuts created.'
if(-not $NoLaunch){Start-Process -FilePath (Join-Path $PSScriptRoot 'StitchPet.exe') -WorkingDirectory $PSScriptRoot -WindowStyle Normal}
