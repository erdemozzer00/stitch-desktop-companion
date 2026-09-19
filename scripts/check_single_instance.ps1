param([string]$Directory='.local/phase-04/polished-trial')
$ErrorActionPreference='Stop'
$directory=[IO.Path]::GetFullPath($Directory)
$exe=Join-Path $directory 'StitchPet.exe'
Add-Type @'
using System;using System.Text;using System.Runtime.InteropServices;
public static class InstanceWindows {
 public delegate bool Visit(IntPtr w,IntPtr p);
 [DllImport("user32.dll")] static extern bool EnumWindows(Visit v,IntPtr p);
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr w,out uint p);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern int GetWindowText(IntPtr w,StringBuilder s,int n);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr w,int n);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr w);
 [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr w,uint m,IntPtr a,IntPtr b);
 public static IntPtr Find(uint pid){IntPtr result=IntPtr.Zero;EnumWindows(delegate(IntPtr w,IntPtr p){uint id;GetWindowThreadProcessId(w,out id);var s=new StringBuilder(100);GetWindowText(w,s,100);if(id==pid && s.ToString()=="Stitch")result=w;return true;},IntPtr.Zero);return result;}
}
'@
$children=@()
try{
    $first=Start-Process $exe -PassThru;$children+=$first
    $deadline=[DateTime]::UtcNow.AddSeconds(8)
    do{$handle=[InstanceWindows]::Find($first.Id);if($handle -ne [IntPtr]::Zero){break};Start-Sleep -Milliseconds 100}while([DateTime]::UtcNow -lt $deadline)
    if($handle -eq [IntPtr]::Zero){throw 'Primary did not open.'}
    [InstanceWindows]::ShowWindow($handle,0)|Out-Null
    $second=Start-Process $exe -PassThru;$children+=$second
    if(-not $second.WaitForExit(3000)){throw 'Duplicate instance stayed running.'}
    Start-Sleep -Milliseconds 500
    if(-not [InstanceWindows]::IsWindowVisible($handle)){throw 'Existing hidden pet was not restored.'}
    $burst=1..4|ForEach-Object{Start-Process $exe -PassThru};$children+=$burst
    foreach($p in $burst){if(-not $p.WaitForExit(3000)){throw 'Concurrent duplicate stayed running.'}}
    if($first.HasExited){throw 'Primary unexpectedly exited.'}
    Write-Output 'PASS: duplicate and four concurrent launches exited; hidden primary restored.'
}finally{
    foreach($p in $children){if(-not $p.HasExited){$h=[InstanceWindows]::Find($p.Id);if($h -ne [IntPtr]::Zero){[InstanceWindows]::PostMessage($h,0x10,[IntPtr]::Zero,[IntPtr]::Zero)|Out-Null};if(-not $p.WaitForExit(3000)){Write-Warning "Check process $($p.Id) did not close."}}}
}
