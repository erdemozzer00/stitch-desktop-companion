param([string]$Destination)
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$source=Join-Path $repo '.local/phase-04/polished-trial'
if(-not $Destination){$Destination=Join-Path ([Environment]::GetFolderPath('Desktop')) 'Stitch - Hediye'}
$Destination=[IO.Path]::GetFullPath($Destination)
if(Test-Path -LiteralPath $Destination){throw 'Choose a new destination; existing package is preserved.'}
New-Item -ItemType Directory -Path $Destination | Out-Null
foreach($name in @('StitchPet.exe','StitchPet.exe.config','stitch.ico')){Copy-Item -LiteralPath (Join-Path $source $name) -Destination $Destination}
foreach($name in @('assets','carry')){Copy-Item -LiteralPath (Join-Path $source $name) -Destination $Destination -Recurse}
Copy-Item -LiteralPath "$PSScriptRoot/setup_personal_package.ps1" -Destination "$Destination/Kur.ps1"
@'
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Kur.ps1"
if errorlevel 1 pause
'@ | Set-Content -LiteralPath "$Destination/Kur.cmd" -Encoding ASCII
@'
STITCH

1. Bu klasörü bilgisayarında kalıcı olarak duracağı yere koy.
2. Kur.cmd dosyasına çift tıkla. Yönetici olarak çalıştırmana gerek yok.
3. Masaüstündeki Stitch kısayolu hazır. Windows oturumu açıldığında da otomatik gelir.

Stitch'e tıkla: el sallar. Basılı tutup sürükle: yerini değiştir.
Saat yanındaki Stitch ikonuna tıkla: boyut, gizle/göster ve çıkış.
İkon görünmüyorsa saat yanındaki yukarı oka bak.
Panelin dışına tıkla veya Esc: yalnızca paneli kapatır.
Stitch'i tekrar açmak ikinci karakter oluşturmaz; gizliyse mevcut olanı gösterir.

Otomatik açılışı kapatmak: Win+R, shell:startup yaz, bu klasördeki Stitch kısayolunu sil.
Tekrar açmak: Kur.cmd dosyasını çalıştır.
Tamamen kaldırmak: tray menüsünden Çıkış, başlangıç ve masaüstü Stitch kısayollarını sil,
ardından bu hediye klasörünü sil. Başka kurulum veya hesap yok.

Kurulumdan sonra klasörü taşımamalısın. Taşırsan eski iki kısayolu silip Kur.cmd'yi yeniden çalıştır.
Blender ve internet gerekmez. Windows 10/11 x64, .NET Framework 4.8 gerektirir.
Kişisel hediye; model ve görüntüler herkese açık dağıtım için hazırlanmadı.
'@ | Set-Content -LiteralPath "$Destination/Beni oku.txt" -Encoding UTF8
$files=Get-ChildItem -LiteralPath $Destination -File -Recurse
$record=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');path=$Destination;file_count=$files.Count;bytes=($files|Measure-Object Length -Sum).Sum;exe_sha256=(Get-FileHash "$Destination/StitchPet.exe").Hash.ToLowerInvariant();limits='Private standalone folder; target Windows 11 and actual sign-in remain pending.'}
$record|ConvertTo-Json|Set-Content "$repo/context/evidence/phase-05-package.json" -Encoding UTF8
$record|ConvertTo-Json
