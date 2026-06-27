$script:RequiredXrcgVersion = '0.10.15'

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

    # Codegen self-test (postmortem P2): py_compile every freshly generated
    # producer package so a malformed xrcg/avrotize emission -- a `{time}`
    # subject placeholder colliding with the injected `_time` envelope param
    # (duplicate-argument SyntaxError), a numeric-leading enum symbol, or empty
    # template output -- fails here at generation time instead of at container
    # start. Single fleet-wide injection point: every generate_producer.ps1
    # routes through Convert-GeneratedPyprojects.
    Test-GeneratedProducers -ProducerDirs ($producerDirs | ForEach-Object { $_.FullName })
}

function Test-GeneratedProducers {
    <#
    .SYNOPSIS
    Compile-check freshly generated producer packages (postmortem P2).

    .DESCRIPTION
    Runs tools/ci/verify_generated_producer.py over each generated *_producer*
    directory. A SyntaxError in generated code throws here so the generator
    stops with a clear, actionable error instead of shipping a producer that
    crashes on first import. Never hand-edit generated code -- fix the xreg
    manifest and regenerate.
    #>
    param(
        [string[]] $ProducerDirs = @()
    )

    if (-not $ProducerDirs -or $ProducerDirs.Count -eq 0) { return }

    $verifier = Join-Path $PSScriptRoot "ci/verify_generated_producer.py"
    if (-not (Test-Path $verifier)) {
        Write-Warning "verify_generated_producer.py not found at $verifier; skipping codegen self-test."
        return
    }

    & python $verifier @ProducerDirs
    if ($LASTEXITCODE -ne 0) {
        throw "Generated producer self-test failed (py_compile errors in generated code). Fix the xreg manifest and regenerate; never hand-edit generated output."
    }
}