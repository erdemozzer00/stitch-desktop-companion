param([switch]$Launch)
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$phase=[IO.Path]::GetFullPath((Join-Path $repo '.local/phase-04'))
$candidate=Join-Path $phase 'polished-trial'
$installed=Join-Path $phase 'native-trial'
$exe=Join-Path $installed 'StitchPet.exe'
$manifest=Get-Content -LiteralPath "$phase/carry-final/bank-manifest.json" -Raw | ConvertFrom-Json
if($manifest.size -ne 400 -or $manifest.samples -ne 24){throw 'Expected final-quality carry assets.'}
foreach($property in $manifest.frames.PSObject.Properties){
    if((Get-FileHash -LiteralPath "$candidate/carry/$($property.Name)").Hash.ToLowerInvariant() -ne $property.Value.sha256){throw 'Candidate carry hash mismatch.'}
}
foreach($clip in @('idle','wave','entries')){
    $base=Get-Content -LiteralPath "$repo/.local/phase-03/appearance-final/$clip/manifest.json" -Raw | ConvertFrom-Json
    foreach($property in $base.frame_sha256.PSObject.Properties){
        if((Get-FileHash -LiteralPath "$candidate/assets/$($property.Name)").Hash.ToLowerInvariant() -ne $property.Value){throw 'Candidate baseline hash mismatch.'}
    }
}
# Close only this exact trial's own pet window, not its independent probe panel
# or the accepted Phase 03 installation. No forced process termination.
Add-Type @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public static class StitchTrialClose {
 public delegate bool Visitor(IntPtr window,IntPtr parameter);
 [DllImport("user32.dll")] static extern bool EnumWindows(Visitor visit,IntPtr p);
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr w,out uint pid);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern int GetWindowText(IntPtr w,StringBuilder text,int max);
 [DllImport("user32.dll")] static extern bool PostMessage(IntPtr w,uint msg,IntPtr a,IntPtr b);
 public static void Close(uint wanted) {
  EnumWindows(delegate(IntPtr w,IntPtr p){uint pid;GetWindowThreadProcessId(w,out pid);
   if(pid==wanted){StringBuilder title=new StringBuilder(200);GetWindowText(w,title,200);
    if(title.ToString()=="Stitch" || title.ToString()=="Stitch floating prototype")PostMessage(w,0x0010,IntPtr.Zero,IntPtr.Zero);}
   return true;},IntPtr.Zero);
 }
}
'@
foreach($process in @(Get-Process StitchPet -ErrorAction SilentlyContinue | Where-Object {$_.Path -eq $exe})){
    [StitchTrialClose]::Close([uint32]$process.Id)
    if(-not $process.WaitForExit(5000)){throw 'Trial did not close gracefully; no files replaced.'}
}
$backup=Join-Path $phase ('native-backup-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff'))
Copy-Item -LiteralPath $installed -Destination $backup -Recurse
$settings=Join-Path $installed 'position.txt'
$settingsBefore=if(Test-Path -LiteralPath $settings){(Get-FileHash -LiteralPath $settings).Hash}else{$null}
try{
    foreach($name in @('StitchPet.exe','StitchPet.exe.config','trial-assets.json')){
        Copy-Item -LiteralPath (Join-Path $candidate $name) -Destination (Join-Path $installed $name) -Force
    }
    foreach($folder in @('assets','carry')){Copy-Item -Path "$candidate/$folder/*" -Destination "$installed/$folder" -Force}
    foreach($property in $manifest.frames.PSObject.Properties){
        if((Get-FileHash -LiteralPath "$installed/carry/$($property.Name)").Hash.ToLowerInvariant() -ne $property.Value.sha256){throw 'Installed carry hash mismatch.'}
    }
    $settingsAfter=if(Test-Path -LiteralPath $settings){(Get-FileHash -LiteralPath $settings).Hash}else{$null}
    if($settingsAfter -ne $settingsBefore){throw 'Settings changed during replacement.'}
}catch{
    Copy-Item -Path "$backup/*" -Destination $installed -Recurse -Force
    throw
}
$record=[ordered]@{status='PASS';updated_at_utc=[DateTime]::UtcNow.ToString('o');backup=$backup;revision='phase04-open-eye-400-controls';
    executable_sha256=(Get-FileHash -LiteralPath $exe).Hash.ToLowerInvariant();carry_frames=45;carry_size=400;settings_preserved=$true;
    original_phase03_installation_changed=$false;limits='Updated isolated trial; user visual and physical UI acceptance still required.'}
$record | ConvertTo-Json | Set-Content -Encoding UTF8 "$repo/context/evidence/phase-04-polished-install.json"
$record | ConvertTo-Json
if($Launch){& "$PSScriptRoot/start_carry_trial.ps1" -DesktopShortcut}
