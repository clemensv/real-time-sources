$script:RequiredXrcgVersion = '0.10.13'

function Assert-XrcgVersion {
    param(
        [string] $RequiredVersion = $script:RequiredXrcgVersion
    )

    $command = Get-Command xrcg -ErrorAction SilentlyContinue
    if (-not $command) {
        throw "xrcg $RequiredVersion is required for producer generation. Install it with 'python -m pip install --upgrade xrcg==$RequiredVersion' and ensure the xrcg CLI is on PATH."
    }

    $versionOutput = & $command.Source --version 2>$null | Out-String
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($versionOutput)) {
        throw "Failed to determine the installed xrcg version. Expected xrcg $RequiredVersion."
    }

    $versionMatch = [regex]::Match($versionOutput, '(?<version>\d+\.\d+\.\d+(?:[-A-Za-z0-9\.]+)?)')
    if (-not $versionMatch.Success) {
        throw "Unable to parse the installed xrcg version from: $versionOutput"
    }

    $installedVersion = $versionMatch.Groups['version'].Value
    if ($installedVersion -ne $RequiredVersion) {
        throw "xrcg $RequiredVersion is required for producer generation, but PATH resolves to $installedVersion. Install it with 'python -m pip install --upgrade xrcg==$RequiredVersion' and re-run the generator."
    }

    Write-Host "Using xrcg $installedVersion" -ForegroundColor DarkGray
}

function Convert-GeneratedPyprojects {
    <#
    .SYNOPSIS
    Converts generated producer pyproject.toml files from poetry-core to
    setuptools + setuptools-scm so wheel versions are derived from git tags.

    .DESCRIPTION
    Call this at the end of generate_producer.ps1 after all xrcg generate
    calls. It finds all pyproject.toml files under the current directory's
    *_producer* folders and converts them in-place.
    #>
    param(
        [string] $SourceDir = $PWD.Path
    )

    $converter = Join-Path $PSScriptRoot "convert-pyproject-to-setuptools-scm.py"
    if (-not (Test-Path $converter)) {
        Write-Warning "convert-pyproject-to-setuptools-scm.py not found at $converter; skipping pyproject conversion."
        return
    }

    $producerDirs = Get-ChildItem -Directory $SourceDir -Filter "*_producer*"
    $converted = 0
    foreach ($dir in $producerDirs) {
        $pyprojects = Get-ChildItem -Recurse -Filter "pyproject.toml" -Path $dir.FullName
        foreach ($f in $pyprojects) {
            & python $converter --path $f.FullName 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) { $converted++ }
        }
    }

    if ($converted -gt 0) {
        Write-Host "Converted $converted generated pyproject.toml file(s) to setuptools-scm" -ForegroundColor DarkGray
    }
}