# Automated build script for TrinityCore/Alpha Project repack (Windows)
# Usage: Run this script from PowerShell in the root of your source directory

$ErrorActionPreference = 'Stop'

# 1. Set variables
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BuildDir = Join-Path $SourceDir 'build'
$VSWhere = "$env:ProgramFiles(x86)\Microsoft Visual Studio\Installer\vswhere.exe"

Write-Host "[1/7] Source directory: $SourceDir"
Write-Host "[2/7] Build directory: $BuildDir"

# 2. Create build directory if needed
if (!(Test-Path $BuildDir)) {
    Write-Host "Creating build directory..."
    New-Item -ItemType Directory -Path $BuildDir | Out-Null
}

# 3. Find Visual Studio and run CMake
$VSVersion = ''
$VSPath = ''
if (Test-Path $VSWhere) {
    $VSPath = & $VSWhere -latest -products * -requires Microsoft.Component.MSBuild -property installationPath
    if ($VSPath -match '2022') { $VSVersion = 'Visual Studio 17 2022' }
    elseif ($VSPath -match '2019') { $VSVersion = 'Visual Studio 16 2019' }
}
if (-not $VSVersion) { $VSVersion = 'Visual Studio 16 2019' }
Write-Host "[3/7] Using generator: $VSVersion"

Push-Location $BuildDir
Write-Host "Running CMake..."
cmake .. -G "$VSVersion" -A x64

# 4. Build the solution
Write-Host "[4/7] Building ALL_BUILD..."
$Solution = Join-Path $BuildDir 'TrinityCore.sln'
if (!(Test-Path $Solution)) { throw "Solution file not found: $Solution" }

# Find MSBuild
$MSBuild = "$env:ProgramFiles(x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
if (!(Test-Path $MSBuild)) {
    $MSBuild = "$env:ProgramFiles(x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
}
if (!(Test-Path $MSBuild)) {
    $MSBuild = "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\MSBuild.exe"
}
if (!(Test-Path $MSBuild)) {
    $MSBuild = "C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe"
}
if (!(Test-Path $MSBuild)) {
    $MSBuild = "msbuild"
}

& $MSBuild $Solution /p:Configuration=Release /m

# 5. Copy required DLLs
Write-Host "[5/7] Copying required DLLs..."
$BinDir = Join-Path $BuildDir 'bin/Release'
$OpenSSLDirs = @("C:\OpenSSL-Win64\bin", "C:\OpenSSL-Win32\bin")
$MySQLDirs = @("C:\Program Files\MySQL\MySQL Server 8.0\bin", "C:\Program Files\MySQL\MySQL Server 5.7\bin", "C:\Program Files\MySQL\MySQL Server 5.6\bin")

foreach ($dir in $OpenSSLDirs) {
    if (Test-Path (Join-Path $dir 'libeay32.dll')) { Copy-Item (Join-Path $dir 'libeay32.dll') $BinDir -Force }
    if (Test-Path (Join-Path $dir 'ssleay32.dll')) { Copy-Item (Join-Path $dir 'ssleay32.dll') $BinDir -Force }
}
foreach ($dir in $MySQLDirs) {
    if (Test-Path (Join-Path $dir 'libmysql.dll')) { Copy-Item (Join-Path $dir 'libmysql.dll') $BinDir -Force }
}

# 6. Print status
Write-Host "[6/7] Build complete. Binaries are in: $BinDir"
if (Test-Path (Join-Path $BinDir 'worldserver.exe')) {
    Write-Host "[7/7] Ready to run:"
    Write-Host "  Worldserver: $BinDir\worldserver.exe"
    Write-Host "  Authserver:  $BinDir\authserver.exe"
} else {
    Write-Host "Build failed or binaries not found. Check the output above for errors."
}

Pop-Location 