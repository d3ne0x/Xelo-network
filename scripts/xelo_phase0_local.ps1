# Run from any directory; no GitHub Actions minutes required.
# Usage: .\scripts\xelo_phase0_local.ps1 [-FullBuild]
[CmdletBinding()]
param([switch]$FullBuild)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

function Assert-LastExitCode {
    param([string]$Step)
    if ($LASTEXITCODE -ne 0) { throw "$Step failed with exit code $LASTEXITCODE" }
}

Push-Location $RepoRoot
try {
    Write-Host '==> XELO Phase 0: lightweight guard and preset tests'
    & python -m compileall -q scripts/xelo_verify_free_build.py tests/xelo_phase0
    Assert-LastExitCode 'Python syntax validation'
    & python -m unittest discover -s tests/xelo_phase0 -p 'test_*.py' -v
    Assert-LastExitCode 'Phase 0 unit tests'

    if (-not $FullBuild) {
        Write-Host '==> Checks passed. Full C++ build was not requested.'
        return
    }
    if (-not $env:VCPKG_ROOT) { throw 'VCPKG_ROOT is required for the Windows full build.' }

    & (Join-Path $PSScriptRoot 'bootstrap-deps.ps1') -Arch x64
    Assert-LastExitCode 'OpenTelemetry bootstrap'
    & cmake --preset windows-x64-free
    Assert-LastExitCode 'MPL-only CMake configure'
    & python scripts/xelo_verify_free_build.py --cache build-windows-x64-free/CMakeCache.txt
    Assert-LastExitCode 'Free build guard'
    & cmake --build --preset windows-x64-free-release --parallel 2
    Assert-LastExitCode 'Windows x64 build'
    Write-Host '==> Windows MPL-only build finished. Run functional tests only in an isolated VM.'
}
finally {
    Pop-Location
}
