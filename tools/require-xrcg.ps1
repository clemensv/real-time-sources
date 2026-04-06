$script:RequiredXrcgVersion = '0.10.1'

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