<#
.SYNOPSIS
    Statically validates Fabric notebook deployment assets for feeder sources.

.DESCRIPTION
    Walks feeders/ and checks catalog notebook opt-in consistency, Fabric
    notebook cell hygiene, source wheel build prerequisites, and optional
    source-specific Fabric post-deploy hook contracts.
#>
[CmdletBinding()]
param(
    [string]$FeederSlug,
    [string]$OutJson,
    [switch]$FailOnWarning
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$feedersRoot = Join-Path $repoRoot "feeders"
$catalogPath = Join-Path $repoRoot "catalog.json"

function New-Check {
    param(
        [Parameter(Mandatory)] [string]$Id,
        [Parameter(Mandatory)] [ValidateSet('ok', 'warning', 'blocker')] [string]$Severity,
        [Parameter(Mandatory)] [string]$Message
    )
    [pscustomobject]@{
        id       = $Id
        severity = $Severity
        message  = $Message
    }
}

function Get-CodeText {
    param([object]$Notebook)
    $parts = New-Object System.Collections.Generic.List[string]
    if (-not $Notebook.cells) { return "" }
    foreach ($cell in @($Notebook.cells)) {
        if ($cell.cell_type -ne 'code') { continue }
        if ($null -eq $cell.source) { continue }
        if ($cell.source -is [array]) {
            $parts.Add((@($cell.source) -join ""))
        } else {
            $parts.Add([string]$cell.source)
        }
    }
    return ($parts -join "`n")
}

function Get-ParameterCellText {
    param([object]$Notebook)
    $parts = New-Object System.Collections.Generic.List[string]
    if (-not $Notebook.cells) { return "" }
    foreach ($cell in @($Notebook.cells)) {
        if ($cell.cell_type -ne 'code') { continue }
        $tags = @()
        if ($cell.metadata -and $cell.metadata.tags) { $tags = @($cell.metadata.tags) }
        if ($tags -notcontains 'parameters') { continue }
        if ($cell.source -is [array]) { $parts.Add((@($cell.source) -join "")) }
        elseif ($null -ne $cell.source) { $parts.Add([string]$cell.source) }
    }

    return ($parts -join "`n")
}

function Get-NotebookWheelSource {
    param([object]$Notebook)
    $codeText = Get-CodeText -Notebook $Notebook
    $match = [regex]::Match($codeText, '/lakehouse/default/Files/wheels/(?<source>[^/''"`]+?)/\*\.whl')
    if ($match.Success) { return $match.Groups['source'].Value }
    return $null
}

function Test-Notebook {
    param(
        [Parameter(Mandatory)] [string]$Slug,
        [Parameter(Mandatory)] [string]$NotebookPath
    )

    $checks = New-Object System.Collections.Generic.List[object]
    try {
        $notebook = Get-Content -LiteralPath $NotebookPath -Raw -Encoding UTF8 | ConvertFrom-Json -Depth 100
        $codeText = Get-CodeText -Notebook $notebook
        $parameterText = Get-ParameterCellText -Notebook $notebook

        if ($codeText -match 'asyncio\.run\s*\(') {
            $checks.Add((New-Check 'no-asyncio-run' 'blocker' 'Code cells call asyncio.run(...); Fabric notebooks must run the bridge in a worker thread.'))
        } else {
            $checks.Add((New-Check 'no-asyncio-run' 'ok' 'No asyncio.run(...) call found in code cells.'))
        }

        if ($codeText -match '(?m)^\s*(%pip\s+install|!pip\s+install|%conda\s+install)\b') {
            $checks.Add((New-Check 'no-inline-installs' 'blocker' 'Code cells contain %pip/!pip/%conda install; Fabric Environment wheels must provide dependencies.'))
        } else {
            $checks.Add((New-Check 'no-inline-installs' 'ok' 'No inline package installation magic found.'))
        }

        $langGroup = $null
        if ($notebook.metadata -and $notebook.metadata.microsoft) { $langGroup = $notebook.metadata.microsoft.language_group }
        if ($langGroup -eq 'jupyter_python') {
            $checks.Add((New-Check 'python-notebook-kernel' 'ok' 'Notebook uses the pure-Python (jupyter_python) kernel.'))
        } elseif ($langGroup -eq 'synapse_pyspark') {
            $checks.Add((New-Check 'python-notebook-kernel' 'blocker' 'Notebook uses the synapse_pyspark (Spark) kernel; feeder notebooks must use the pure-Python kernel (metadata.microsoft.language_group = "jupyter_python").'))
        } else {
            $checks.Add((New-Check 'python-notebook-kernel' 'warning' "Notebook metadata.microsoft.language_group is '$langGroup'; expected 'jupyter_python'."))
        }

        if ($codeText -like '*/lakehouse/default/Files/feeder-state/*') {
            $checks.Add((New-Check 'onelake-feeder-state-log' 'ok' 'Notebook references /lakehouse/default/Files/feeder-state/.'))
        } elseif ($codeText -match '(/lakehouse/default/Files/|last-run\.log|LOG_PATH|STATE_FILE)') {
            $checks.Add((New-Check 'onelake-feeder-state-log' 'warning' 'Notebook has a logging/state path, but not the canonical /lakehouse/default/Files/feeder-state/ path.'))
        } else {
            $checks.Add((New-Check 'onelake-feeder-state-log' 'blocker' 'Notebook has no detectable OneLake logging or state-file path.'))
        }

        if ($codeText.Contains('notebookutils.notebook.exit(')) {
            $checks.Add((New-Check 'notebook-exit-on-failure' 'ok' 'Notebook calls notebookutils.notebook.exit(...).'))
        } else {
            $checks.Add((New-Check 'notebook-exit-on-failure' 'warning' 'Notebook does not call notebookutils.notebook.exit(...); scheduled failures may be opaque.'))
        }

        if ($parameterText -match '(?m)^\s*CONNECTION_STRING\s*=\s*[''\"]') {
            $checks.Add((New-Check 'connection-string-not-parameter' 'blocker' 'Parameters cell declares CONNECTION_STRING as a string literal; the notebook must resolve it at runtime via the Topology API.'))
        } else {
            $checks.Add((New-Check 'connection-string-not-parameter' 'ok' 'No CONNECTION_STRING parameter assignment found.'))
        }

        if ($codeText -match 'eventstreams/.+?/topology|/sources/.+?/connection|notebookutils\.credentials\.getToken\(' -or $codeText -match 'mssparkutils\.credentials\.getToken\(') {
            $checks.Add((New-Check 'topology-connection-lookup' 'ok' 'Notebook appears to resolve the Event Stream connection string at runtime.'))
        } else {
            $checks.Add((New-Check 'topology-connection-lookup' 'warning' 'No obvious notebookutils/mssparkutils Topology API connection-string lookup found.'))
        }

        if ($codeText -match 'threading\.Thread|concurrent\.futures') {
            $checks.Add((New-Check 'bridge-off-thread' 'ok' 'Notebook uses a worker-thread pattern for bridge execution.'))
        } else {
            $checks.Add((New-Check 'bridge-off-thread' 'warning' 'No threading.Thread or concurrent.futures bridge invocation pattern found.'))
        }
    } catch {
        $checks.Add((New-Check 'notebook-json-parse' 'blocker' "Notebook could not be parsed as JSON: $($_.Exception.Message)"))
    }
    return $checks.ToArray()
}

function Test-PostDeployHook {
    param(
        [Parameter(Mandatory)] [string]$HookPath
    )

    $checks = New-Object System.Collections.Generic.List[object]
    $tokens = $null
    $parseErrors = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($HookPath, [ref]$tokens, [ref]$parseErrors)

    if ($parseErrors -and $parseErrors.Count -gt 0) {
        $msg = ($parseErrors | ForEach-Object { "$($_.Extent.StartLineNumber):$($_.Extent.StartColumnNumber) $($_.Message)" }) -join '; '
        $checks.Add((New-Check 'post-deploy-parse' 'blocker' "PowerShell parse errors: $msg"))
        return $checks.ToArray()
    }
    $checks.Add((New-Check 'post-deploy-parse' 'ok' 'Post-deploy hook parses successfully.'))

    $contextParam = $null
    if ($ast.ParamBlock) {
        $contextParam = @($ast.ParamBlock.Parameters | Where-Object { $_.Name.VariablePath.UserPath -eq 'Context' } | Select-Object -First 1)
    }
    if ($contextParam -and $contextParam.StaticType -eq [hashtable]) {
        $checks.Add((New-Check 'post-deploy-context-param' 'ok' 'First param block declares [hashtable] $Context.'))
    } else {
        $checks.Add((New-Check 'post-deploy-context-param' 'blocker' 'First param(...) block must declare [hashtable] $Context for deploy-fabric.ps1 hook invocation.'))
    }

    $text = Get-Content -LiteralPath $HookPath -Raw -Encoding UTF8
    if ($text -match '\$Context\.(WorkspaceId|EventhouseId|DatabaseId|EventstreamId)') {
        $checks.Add((New-Check 'post-deploy-context-use' 'ok' 'Hook references deployment context IDs.'))
    } else {
        $checks.Add((New-Check 'post-deploy-context-use' 'warning' 'Hook does not reference WorkspaceId/EventhouseId/DatabaseId/EventstreamId from $Context.'))
    }

    $hookDir = Split-Path -Parent $HookPath
    $candidates = New-Object System.Collections.Generic.List[string]
    foreach ($m in [regex]::Matches($text, '(?is)Join-Path\s+\$PSScriptRoot\s+(["''])(?<rel>[^"'']+)\1')) {
        $rel = $m.Groups['rel'].Value
        if ($rel -and -not ($rel -match '[\$\*\?]')) { $candidates.Add((Join-Path $hookDir $rel)) }
    }
    foreach ($m in [regex]::Matches($text, '(?is)Resolve-Path\s+(["''])(?<path>[^"'']+)\1')) {
        $p = $m.Groups['path'].Value
        if (-not $p -or $p -match '[\$\*\?]') { continue }
        if ([System.IO.Path]::IsPathRooted($p)) { $candidates.Add($p) }
        else { $candidates.Add((Join-Path $hookDir $p)) }
    }
    foreach ($m in [regex]::Matches($text, '(?is)Resolve-Path\s+(["''])(?<path>\$PSScriptRoot[\\/][^"'']+)\1')) {
        $p = $m.Groups['path'].Value -replace '^\$PSScriptRoot[\\/]', ''
        if ($p -and -not ($p -match '[\$\*\?]')) { $candidates.Add((Join-Path $hookDir $p)) }
    }

    $missing = @($candidates | Select-Object -Unique | Where-Object { -not (Test-Path -LiteralPath $_) })
    if ($missing.Count -gt 0) {
        $relMissing = $missing | ForEach-Object { Resolve-Path -LiteralPath $_ -Relative -ErrorAction SilentlyContinue; if (-not $?) { $_ } }
        $checks.Add((New-Check 'post-deploy-referenced-files' 'blocker' ("Hook references missing sibling file(s): " + (($missing | ForEach-Object { Split-Path -Leaf $_ }) -join ', '))))
    } else {
        $checks.Add((New-Check 'post-deploy-referenced-files' 'ok' 'All literal files resolved from $PSScriptRoot/Resolve-Path exist.'))
    }

    return $checks.ToArray()
}

if (-not (Test-Path -LiteralPath $catalogPath)) { throw "catalog.json not found: $catalogPath" }
if (-not (Test-Path -LiteralPath $feedersRoot)) { throw "feeders directory not found: $feedersRoot" }

$catalog = Get-Content -LiteralPath $catalogPath -Raw -Encoding UTF8 | ConvertFrom-Json -Depth 100
$catalogById = @{}
foreach ($entry in @($catalog)) { if ($entry.id) { $catalogById[[string]$entry.id] = $entry } }

$feederDirs = @(Get-ChildItem -LiteralPath $feedersRoot -Directory | Sort-Object Name)
if ($FeederSlug) {
    $selected = @($feederDirs | Where-Object { $_.Name -eq $FeederSlug })
    if ($selected.Count -eq 0) { throw "FeederSlug '$FeederSlug' not found under $feedersRoot" }
} else {
    $selected = @($feederDirs | Where-Object {
        $slug = $_.Name
        $entry = $catalogById[$slug]
        $notebookOptIn = ($entry -and $entry.PSObject.Properties.Name -contains 'notebook' -and $entry.notebook -eq $true)
        $expectedNotebook = Join-Path $_.FullName "notebook\$slug-feed.ipynb"
        $postDeployHook = Join-Path $_.FullName "fabric\post-deploy.ps1"
        $notebookOptIn -or (Test-Path -LiteralPath $expectedNotebook) -or (Test-Path -LiteralPath $postDeployHook)
    })
}

$sourceReports = New-Object System.Collections.Generic.List[object]
foreach ($dir in $selected) {
    $slug = $dir.Name
    $entry = $catalogById[$slug]
    $hasCatalogEntry = $null -ne $entry
    $notebookOptIn = ($entry -and $entry.PSObject.Properties.Name -contains 'notebook' -and $entry.notebook -eq $true)
    $notebookPath = Join-Path $dir.FullName "notebook\$slug-feed.ipynb"
    $notebookPresent = Test-Path -LiteralPath $notebookPath
    $hookPath = Join-Path $dir.FullName "fabric\post-deploy.ps1"
    $hookPresent = Test-Path -LiteralPath $hookPath
    $checks = New-Object System.Collections.Generic.List[object]

    if (-not $hasCatalogEntry) {
        $checks.Add((New-Check 'catalog-entry' 'blocker' 'No catalog.json entry exists for this feeder.'))
    } else {
        $checks.Add((New-Check 'catalog-entry' 'ok' 'catalog.json entry found.'))
    }

    if ($notebookOptIn -and -not $notebookPresent) {
        $checks.Add((New-Check 'catalog-notebook-opt-in' 'blocker' "catalog.json sets notebook=true but $slug-feed.ipynb is missing."))
    } elseif ($notebookPresent -and -not $notebookOptIn) {
        $checks.Add((New-Check 'catalog-notebook-opt-in' 'blocker' "Notebook file exists but catalog.json does not set notebook=true."))
    } else {
        $checks.Add((New-Check 'catalog-notebook-opt-in' 'ok' 'catalog.json notebook flag and notebook file presence are consistent.'))
    }

    if ($notebookPresent) {
        foreach ($check in (Test-Notebook -Slug $slug -NotebookPath $notebookPath)) { $checks.Add($check) }
    }

    if ($notebookOptIn) {
        $pyproject = Join-Path $dir.FullName "pyproject.toml"
        $nestedPyprojects = @(Get-ChildItem -LiteralPath $dir.FullName -Directory | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "pyproject.toml") })
        if (Test-Path -LiteralPath $pyproject) {
            $checks.Add((New-Check 'pyproject-buildable' 'ok' 'Root pyproject.toml is present for Fabric Environment wheel build.'))
        } elseif ($nestedPyprojects.Count -gt 0) {
            $checks.Add((New-Check 'pyproject-buildable' 'ok' ("Nested build package(s) found: " + (($nestedPyprojects | Select-Object -ExpandProperty Name) -join ', '))))
        } else {
            $wheelSource = $null
            if ($notebookPresent) {
                try {
                    $notebook = Get-Content -LiteralPath $notebookPath -Raw -Encoding UTF8 | ConvertFrom-Json -Depth 100
                    $wheelSource = Get-NotebookWheelSource -Notebook $notebook
                } catch {
                    $wheelSource = $null
                }
            }
            if ($wheelSource -and $wheelSource -ne $slug) {
                $wheelSourceDir = Join-Path $feedersRoot $wheelSource
                $wheelSourcePyproject = Join-Path $wheelSourceDir "pyproject.toml"
                $wheelSourceNested = @()
                if (Test-Path -LiteralPath $wheelSourceDir) {
                    $wheelSourceNested = @(Get-ChildItem -LiteralPath $wheelSourceDir -Directory | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "pyproject.toml") })
                }
                if ((Test-Path -LiteralPath $wheelSourcePyproject) -or $wheelSourceNested.Count -gt 0) {
                    $checks.Add((New-Check 'pyproject-buildable' 'ok' "Config-only notebook wrapper loads wheels from buildable feeder '$wheelSource'."))
                } else {
                    $checks.Add((New-Check 'pyproject-buildable' 'blocker' "Notebook loads wheels from '$wheelSource', but no buildable feeder package was found there."))
                }
            } else {
                $checks.Add((New-Check 'pyproject-buildable' 'blocker' 'No root or immediate child pyproject.toml found; Fabric Environment wheel build has no source package.'))
            }
        }
    }

    if ($hookPresent) {
        foreach ($check in (Test-PostDeployHook -HookPath $hookPath)) { $checks.Add($check) }
    }

    $sourceReports.Add([pscustomobject]@{
        slug                     = $slug
        notebook_opt_in          = [bool]$notebookOptIn
        notebook_file_present    = [bool]$notebookPresent
        post_deploy_hook_present = [bool]$hookPresent
        checks                   = $checks.ToArray()
    })
}

$sourceArray = $sourceReports.ToArray()
$totalBlockers = @($sourceArray.checks | Where-Object { $_.severity -eq 'blocker' }).Count
$totalWarnings = @($sourceArray.checks | Where-Object { $_.severity -eq 'warning' }).Count
$report = [pscustomobject]@{
    summary = [pscustomobject]@{
        sources_checked = $sourceArray.Count
        blockers        = $totalBlockers
        warnings        = $totalWarnings
    }
    sources = $sourceArray
}

$table = $sourceArray | ForEach-Object {
    [pscustomobject]@{
        Source   = $_.slug
        OptIn    = $_.notebook_opt_in
        Notebook = $_.notebook_file_present
        Hook     = $_.post_deploy_hook_present
        PASS     = @($_.checks | Where-Object severity -eq 'ok').Count
        WARN     = @($_.checks | Where-Object severity -eq 'warning').Count
        BLOCK    = @($_.checks | Where-Object severity -eq 'blocker').Count
    }
}
$table | Format-Table -AutoSize | Out-Host
Write-Host ("Sources: {0} total, {1} blockers, {2} warnings" -f $sourceArray.Count, $totalBlockers, $totalWarnings)

if ($OutJson) {
    $outPath = if ([System.IO.Path]::IsPathRooted($OutJson)) { $OutJson } else { Join-Path (Get-Location) $OutJson }
    $outDir = Split-Path -Parent $outPath
    if ($outDir -and -not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
    $report | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $outPath -Encoding UTF8
    Write-Host "JSON report: $outPath"
}

if ($totalBlockers -gt 0 -or ($FailOnWarning -and $totalWarnings -gt 0)) { exit 1 }
exit 0
