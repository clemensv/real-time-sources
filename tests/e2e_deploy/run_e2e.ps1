<#
.SYNOPSIS
    Orchestrates E2E deployment validation for all sources.

.DESCRIPTION
    Discovers all sources with Azure templates and/or Fabric notebooks,
    creates a session directory, runs both Azure and Fabric tests
    sequentially (one source at a time), tracks results, and produces
    a summary.

.PARAMETER ConfigFile
    Path to config.json (default: ./config.json in script directory).

.PARAMETER Subscription
    Azure subscription (overrides config file).

.PARAMETER WorkspaceName
    Fabric workspace name (overrides config file).

.PARAMETER WorkspaceId
    Fabric workspace ID (overrides config file).

.PARAMETER Token
    Fabric bearer token (overrides config file).

.PARAMETER SkipAzure
    Skip all Azure tests.

.PARAMETER SkipFabric
    Skip all Fabric tests.

.PARAMETER OnlySource
    Test only this single source (for debugging).
#>
param(
    [string]$ConfigFile,
    [string]$Subscription,
    [string]$WorkspaceName,
    [string]$WorkspaceId,
    [string]$Token,
    [switch]$SkipAzure,
    [switch]$SkipFabric,
    [string]$OnlySource
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path "$scriptDir/../..").Path

# Load config
if (-not $ConfigFile) { $ConfigFile = Join-Path $scriptDir "config.json" }
$config = @{}
if (Test-Path $ConfigFile) {
    $config = Get-Content $ConfigFile | ConvertFrom-Json -AsHashtable
}

# Resolve parameters (CLI > env > config)
$sub = $Subscription
if (-not $sub) { $sub = $env:E2E_SUBSCRIPTION }
if (-not $sub -and $config.azure) { $sub = $config.azure.subscription }

$region = $env:E2E_REGION
if (-not $region -and $config.azure) { $region = $config.azure.region }
if (-not $region) { $region = "westeurope" }

$wsName = $WorkspaceName
if (-not $wsName) { $wsName = $env:E2E_FABRIC_WORKSPACE }
if (-not $wsName -and $config.fabric) { $wsName = $config.fabric.workspace_name }

$wsId = $WorkspaceId
if (-not $wsId -and $config.fabric) { $wsId = $config.fabric.workspace_id }

$tkn = $Token
if (-not $tkn) { $tkn = $env:E2E_FABRIC_TOKEN }

$timeoutAzure = if ($env:E2E_TIMEOUT_AZURE) { [int]$env:E2E_TIMEOUT_AZURE } elseif ($config.azure.timeout_seconds) { $config.azure.timeout_seconds } else { 600 }
$timeoutFabric = if ($env:E2E_TIMEOUT_FABRIC) { [int]$env:E2E_TIMEOUT_FABRIC } elseif ($config.fabric.timeout_seconds) { $config.fabric.timeout_seconds } else { 900 }

$skipAz = $SkipAzure -or ($env:E2E_SKIP_AZURE -eq "true")
$skipFab = $SkipFabric -or ($env:E2E_SKIP_FABRIC -eq "true")

$skipSources = @()
if ($config.skip_sources) { $skipSources = $config.skip_sources }

# Create session directory
$sessionTimestamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
$sessionDir = Join-Path $scriptDir "sessions" $sessionTimestamp
New-Item -ItemType Directory -Path $sessionDir -Force | Out-Null

# Copy checklist template
$templatePath = Join-Path $scriptDir "CHECKLIST_TEMPLATE.md"
$checklistPath = Join-Path $sessionDir "CHECKLIST.md"
if (Test-Path $templatePath) {
    $checklist = Get-Content $templatePath -Raw
    $checklist = $checklist -replace '\{SESSION_ID\}', $sessionTimestamp
    $checklist = $checklist -replace '\{TIMESTAMP\}', (Get-Date -Format "yyyy-MM-dd HH:mm:ss UTC")
    $checklist = $checklist -replace '\{SUBSCRIPTION\}', ($sub ?? "N/A")
    $checklist = $checklist -replace '\{WORKSPACE\}', ($wsName ?? "N/A")
    $checklist | Set-Content $checklistPath
}

# Start logging
$logPath = Join-Path $sessionDir "log.txt"
Start-Transcript -Path $logPath -Append

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  E2E Deployment Validation" -ForegroundColor Cyan
Write-Host "  Session: $sessionTimestamp" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Discover sources
$feedersDir = Join-Path $repoRoot "feeders"
$allSources = Get-ChildItem -Path $feedersDir -Directory | Select-Object -ExpandProperty Name | Sort-Object

if ($OnlySource) {
    $allSources = @($OnlySource)
}

# Filter out skipped sources
$allSources = $allSources | Where-Object { $_ -notin $skipSources }

# Categorize
$azureSources = @()
$fabricSources = @()

foreach ($src in $allSources) {
    $srcPath = Join-Path $feedersDir $src
    if (Test-Path (Join-Path $srcPath "azure-template.json")) {
        $azureSources += $src
    }
    if (Test-Path (Join-Path $srcPath "notebook")) {
        $fabricSources += $src
    }
}

Write-Host "Sources discovered:"
Write-Host "  Azure (ACI): $($azureSources.Count)"
Write-Host "  Fabric (Notebook): $($fabricSources.Count)"
Write-Host "  Skipped by config: $($skipSources.Count)"
Write-Host ""

# Results tracking
$results = @{
    session_id = $sessionTimestamp
    azure = @{ pass = 0; fail = 0; skip = 0; sources = @() }
    fabric = @{ pass = 0; fail = 0; skip = 0; sources = @() }
    issues_created = 0
    issues_amended = 0
    start_time = (Get-Date).ToString("o")
    end_time = $null
}

# --- Run Azure tests ---
if (-not $skipAz -and $sub) {
    Write-Host "--- Azure ACI Tests ---" -ForegroundColor Cyan
    foreach ($src in $azureSources) {
        Write-Host ""
        $r = & "$scriptDir/test_azure_aci.ps1" `
            -Source $src `
            -SessionDir $sessionDir `
            -Subscription $sub `
            -Region $region `
            -TimeoutSeconds $timeoutAzure

        $results.azure.sources += @{ source = $src; result = $r.result }
        switch ($r.result) {
            "pass" { $results.azure.pass++ }
            "fail" { $results.azure.fail++ }
            "skip" { $results.azure.skip++ }
        }
    }
}
elseif ($skipAz) {
    Write-Host "Azure tests: SKIPPED" -ForegroundColor Yellow
}
else {
    Write-Host "Azure tests: SKIPPED (no subscription configured)" -ForegroundColor Yellow
}

# --- Run Fabric tests ---
if (-not $skipFab -and $wsId -and $tkn) {
    Write-Host ""
    Write-Host "--- Fabric Notebook Tests ---" -ForegroundColor Cyan
    foreach ($src in $fabricSources) {
        Write-Host ""
        $r = & "$scriptDir/test_fabric_notebook.ps1" `
            -Source $src `
            -SessionDir $sessionDir `
            -WorkspaceName $wsName `
            -WorkspaceId $wsId `
            -Token $tkn `
            -TimeoutSeconds $timeoutFabric

        $results.fabric.sources += @{ source = $src; result = $r.result }
        switch ($r.result) {
            "pass" { $results.fabric.pass++ }
            "fail" { $results.fabric.fail++ }
            "skip" { $results.fabric.skip++ }
        }
    }
}
elseif ($skipFab) {
    Write-Host "Fabric tests: SKIPPED" -ForegroundColor Yellow
}
else {
    Write-Host "Fabric tests: SKIPPED (no workspace or token configured)" -ForegroundColor Yellow
}

# Finalize
$results.end_time = (Get-Date).ToString("o")

# Write summary
$summaryPath = Join-Path $sessionDir "summary.json"
$results | ConvertTo-Json -Depth 5 | Set-Content $summaryPath

# Print summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Azure:  $($results.azure.pass) pass / $($results.azure.fail) fail / $($results.azure.skip) skip"
Write-Host "  Fabric: $($results.fabric.pass) pass / $($results.fabric.fail) fail / $($results.fabric.skip) skip"
Write-Host "  Session: $sessionDir"
Write-Host ""

Stop-Transcript

# Return results
return $results
