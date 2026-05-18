<#
.SYNOPSIS
    Deploys a real-time-source feeder as a Fabric notebook (instead of an
    ACI container). The notebook runs the source's bridge package via
    `python -m <source> feed --once` on each invocation.

.DESCRIPTION
    Two-stage workflow that delegates Fabric infra setup to the existing
    deploy-fabric.ps1 script:

      Stage A. Calls deploy-fabric.ps1 with -SkipArm to:
                - resolve/create the Fabric workspace
                - resolve/create the Eventhouse + KQL database + apply schema
                - create the Event Stream and bind its custom-endpoint
                - retrieve the Event Stream connection string (written to
                  a temp file via the new -OutCsFile switch)

      Stage B. Patches the source's notebook
              (<source>/notebook/<source>-feed.ipynb):
                - sets CONNECTION_STRING from Stage A
                - sets STATE_FILE to a Lakehouse path
                - sets SOURCE_REF to the deploy branch (default 'main')
                - binds metadata.dependencies.kqlDatabases to the source DB
              and uploads it to the Fabric workspace.

    The user then runs / schedules the notebook from the Fabric portal.
    A Data Factory pipeline + schedule trigger can be added in a future
    iteration; for the prototype the notebook is the only artifact.

.PARAMETER Source
    Source name (folder name in this repo). Currently only 'pegelonline'
    ships a notebook; this script is generic so other sources can opt in
    by adding <source>/notebook/<source>-feed.ipynb.

.PARAMETER Workspace
    Fabric workspace name or GUID.

.PARAMETER Eventhouse
    Fabric eventhouse name. Default: source name (with '-' -> '_').

.PARAMETER DatabaseName
    KQL database name. Default: source name (with '-' -> '_').

.PARAMETER SubscriptionId
    Azure subscription ID used by Stage A.

.PARAMETER ResourceGroup
    Required by Stage A's deploy-fabric.ps1 contract (used as scratch).
    Not actually used for ACI since -SkipArm is set.

.PARAMETER Location
    Azure region (parity with Stage A).

.PARAMETER Repo
    GitHub repo for `pip install git+...`. Default 'clemensv/real-time-sources'.

.PARAMETER Branch
    Branch to install from. Default 'main'.

.PARAMETER NotebookName
    Display name of the Fabric notebook item. Default '<source>-feed'.

.PARAMETER StatePath
    Lakehouse-mounted directory used by the bridge for dedupe state.
    Default '/lakehouse/default/Files/feeder-state/<source>'.

.PARAMETER PollingInterval
    Bridge polling interval in seconds (used if ONCE_MODE is disabled).
    Default 900 (matches pegelonline's native upstream cadence).

.PARAMETER OnceMode
    If $true (default), the bridge exits after one polling cycle. Use
    in scheduled runs. Set to $false to let the bridge loop forever
    (e.g., always-on Spark session).

.PARAMETER SkipInfra
    Skip Stage A. Use when the KQL DB / Event Stream already exist and
    you pass -ConnectionString directly.

.PARAMETER ConnectionString
    Event Stream custom-endpoint connection string. If provided with
    -SkipInfra, Stage A is bypassed.

.EXAMPLE
    ./deploy-feeder-notebook.ps1 -Source pegelonline `
        -SubscriptionId 041abda7-... `
        -ResourceGroup rg-pegelonline-test `
        -Workspace ContosoRealTimeTest `
        -Eventhouse ContosoRealTimeTest-eh
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [string]$ResourceGroup = "rg-$($PSBoundParameters['Source'])-notebook",
    [string]$Location,
    [string]$SubscriptionId,

    [Parameter(Mandatory = $true)]
    [string]$Workspace,

    [string]$Eventhouse,
    [string]$DatabaseName,

    [string]$Repo = "clemensv/real-time-sources",
    [string]$Branch = "main",

    [string]$NotebookName,
    [string]$StatePath,
    [int]$PollingInterval = 900,
    [bool]$OnceMode = $true,

    [switch]$SkipInfra,
    [string]$ConnectionString
)

$ErrorActionPreference = "Stop"
$FabricApi = "https://api.fabric.microsoft.com/v1"
$guidRx = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
$TempDir = if ($env:TEMP) { $env:TEMP } elseif ($env:TMPDIR) { $env:TMPDIR } else { [System.IO.Path]::GetTempPath() }

if (-not $DatabaseName)            { $DatabaseName = $Source -replace '-', '_' }
if ([string]::IsNullOrWhiteSpace($Eventhouse)) { $Eventhouse = $Source -replace '-', '_' }
if (-not $NotebookName)            { $NotebookName = "$Source-feed" }
if (-not $StatePath)               { $StatePath    = "/lakehouse/default/Files/feeder-state/$Source" }

$repoRoot     = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$notebookPath = Join-Path $repoRoot "$Source/notebook/$Source-feed.ipynb"
if (-not (Test-Path $notebookPath)) {
    throw "Notebook not found: $notebookPath`nAdd <source>/notebook/<source>-feed.ipynb to enable notebook deploy for this source."
}

function Write-Step { param([string]$Step, [string]$Msg) Write-Host "`n[$Step] $Msg" -ForegroundColor Yellow }
function Write-OK   { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor Green }
function Write-Info { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor DarkYellow }

function Invoke-FabricApi {
    param([string]$Method, [string]$Url, [object]$Body)
    $azArgs = @("rest", "--method", $Method, "--url", $Url, "--resource", "https://api.fabric.microsoft.com")
    if ($Body) {
        $bodyFile = Join-Path $TempDir "fabric_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 30 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Fabric API error ($Method $Url): $($result | Out-String)" }
    if ($result) { return $result | ConvertFrom-Json }
    return $null
}

Write-Host "=== $Source Notebook Feeder Deployment ===" -ForegroundColor Cyan
Write-Host "  Source:           $Source"          -ForegroundColor White
Write-Host "  Workspace:        $Workspace"       -ForegroundColor White
Write-Host "  Eventhouse:       $Eventhouse"      -ForegroundColor White
Write-Host "  KQL Database:     $DatabaseName"    -ForegroundColor White
Write-Host "  Notebook:         $NotebookName"    -ForegroundColor White
Write-Host "  Notebook file:    $notebookPath"    -ForegroundColor White
Write-Host "  Source ref:       $Repo@$Branch"    -ForegroundColor White
Write-Host "  Polling interval: $PollingInterval s (once-mode=$OnceMode)" -ForegroundColor White

# ── Stage A: Fabric infra + connection string ─────────────────────────────
$esConnectionString = $ConnectionString
if (-not $SkipInfra) {
    Write-Step "A" "Setting up Fabric infra via deploy-fabric.ps1 -SkipArm..."
    $csFile = Join-Path $TempDir "feeder_cs_$(Get-Random).txt"
    $deployFabric = Join-Path $PSScriptRoot "deploy-fabric.ps1"
    if (-not (Test-Path $deployFabric)) { throw "deploy-fabric.ps1 not found alongside this script." }

    $fwdArgs = @(
        '-Source', $Source,
        '-ResourceGroup', $ResourceGroup,
        '-Workspace', $Workspace,
        '-Eventhouse', $Eventhouse,
        '-DatabaseName', $DatabaseName,
        '-Repo', $Repo,
        '-Branch', $Branch,
        '-OutCsFile', $csFile,
        '-SkipArm'
    )
    if ($Location)       { $fwdArgs += @('-Location', $Location) }
    if ($SubscriptionId) { $fwdArgs += @('-SubscriptionId', $SubscriptionId) }

    & $deployFabric @fwdArgs
    if ($LASTEXITCODE -ne 0 -and -not (Test-Path $csFile)) {
        throw "deploy-fabric.ps1 failed; aborting notebook deploy."
    }
    if (Test-Path $csFile) {
        $esConnectionString = (Get-Content -Raw -LiteralPath $csFile).Trim()
        Remove-Item $csFile -ErrorAction SilentlyContinue
    }
}

if (-not $esConnectionString) {
    throw "No Event Stream connection string available. Pass -ConnectionString manually or rerun without -SkipInfra."
}
Write-OK "Connection string ready (length=$($esConnectionString.Length))"

# ── Stage B: Resolve workspace + KQL DB ───────────────────────────────────
Write-Step "B/1" "Resolving Fabric workspace..."
if ($SubscriptionId -and -not $SkipInfra) {
    # already set by deploy-fabric.ps1
} elseif ($SubscriptionId) {
    az account set --subscription $SubscriptionId 2>&1 | Out-Null
}

if ($Workspace -match $guidRx) {
    $WorkspaceId = $Workspace
} else {
    $allWs = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces"
    $ws = $allWs.value | Where-Object { $_.displayName -eq $Workspace } | Select-Object -First 1
    if (-not $ws) { throw "Workspace '$Workspace' not found." }
    $WorkspaceId = $ws.id
}
$wsInfo = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId"
Write-OK "Workspace: $($wsInfo.displayName) ($WorkspaceId)"

Write-Step "B/2" "Resolving KQL database..."
$ehList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
$eh = $ehList.value | Where-Object { $_.displayName -eq $Eventhouse -or $_.id -eq $Eventhouse } | Select-Object -First 1
if (-not $eh) { throw "Eventhouse '$Eventhouse' not found in workspace." }
Write-OK "Eventhouse: $($eh.displayName) ($($eh.id))"

$dbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$db = $dbList.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
if (-not $db) { throw "KQL database '$DatabaseName' not found. Stage A should have created it." }
Write-OK "KQL database: $($db.displayName) ($($db.id))"

$queryUri = $eh.properties.queryServiceUri

# ── Stage B/3: Patch notebook ─────────────────────────────────────────────
Write-Step "B/3" "Patching notebook parameters + KQL binding..."
$nbJson = Get-Content -LiteralPath $notebookPath -Raw -Encoding UTF8
$nb = $nbJson | ConvertFrom-Json

if (-not $nb.metadata)              { $nb | Add-Member -NotePropertyName metadata     -NotePropertyValue ([pscustomobject]@{}) -Force }
if (-not $nb.metadata.dependencies) { $nb.metadata | Add-Member -NotePropertyName dependencies -NotePropertyValue ([pscustomobject]@{}) -Force }
$kqlBinding = @(
    [pscustomobject]@{
        name        = $db.displayName
        displayName = $db.displayName
        workspaceId = $WorkspaceId
        itemId      = $db.id
    }
)
$nb.metadata.dependencies | Add-Member -NotePropertyName kqlDatabases -NotePropertyValue $kqlBinding -Force

$onceLiteral = if ($OnceMode) { "True" } else { "False" }
# Escape quotes/backslashes in CS to safely embed in a Python string literal.
$csPyLiteral = $esConnectionString -replace '\\', '\\' -replace '"', '\"'

$paramsPatched = $false
foreach ($cell in $nb.cells) {
    if ($cell.cell_type -ne 'code') { continue }
    $tags = @()
    if ($cell.metadata -and $cell.metadata.tags) { $tags = @($cell.metadata.tags) }
    if ($tags -notcontains 'parameters') { continue }

    $srcLines = @($cell.source) | ForEach-Object { $_ }
    $newLines = foreach ($line in $srcLines) {
        if     ($line -match '^\s*CONNECTION_STRING\s*=') { "CONNECTION_STRING = `"$csPyLiteral`"`n" }
        elseif ($line -match '^\s*STATE_FILE\s*=')        { "STATE_FILE        = `"$StatePath/state.json`"`n" }
        elseif ($line -match '^\s*POLLING_INTERVAL\s*=')  { "POLLING_INTERVAL  = $PollingInterval`n" }
        elseif ($line -match '^\s*ONCE_MODE\s*=')         { "ONCE_MODE         = $onceLiteral`n" }
        elseif ($line -match '^\s*KUSTO_URI\s*=')         { "KUSTO_URI         = `"$queryUri`"`n" }
        elseif ($line -match '^\s*KUSTO_DATABASE\s*=')    { "KUSTO_DATABASE    = `"$($db.displayName)`"`n" }
        elseif ($line -match '^\s*SOURCE_REF\s*=')        { "SOURCE_REF        = `"$Branch`"`n" }
        else                                              { $line }
    }
    $cell.source = @($newLines)
    $paramsPatched = $true
    break
}
if (-not $paramsPatched) { throw "Notebook has no 'parameters'-tagged cell to patch." }
Write-OK "Parameters cell patched."

$tmpNb = Join-Path $TempDir "$Source`_feed_$(Get-Random).ipynb"
[System.IO.File]::WriteAllText($tmpNb, ($nb | ConvertTo-Json -Depth 50), [System.Text.UTF8Encoding]::new($false))

# ── Stage B/4: Upload notebook ────────────────────────────────────────────
Write-Step "B/4" "Uploading notebook to Fabric workspace..."
$nbBytes  = [System.IO.File]::ReadAllBytes($tmpNb)
$nbBase64 = [Convert]::ToBase64String($nbBytes)
$definition = @{
    format = "ipynb"
    parts  = @(@{ path = "notebook-content.ipynb"; payload = $nbBase64; payloadType = "InlineBase64" })
}

$nbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/notebooks"
$existing = $nbList.value | Where-Object { $_.displayName -eq $NotebookName } | Select-Object -First 1

if ($existing) {
    Invoke-FabricApi -Method POST `
        -Url "$FabricApi/workspaces/$WorkspaceId/notebooks/$($existing.id)/updateDefinition" `
        -Body @{ definition = $definition } | Out-Null
    Write-OK "Updated existing notebook '$NotebookName' ($($existing.id))"
    $notebookId = $existing.id
} else {
    $createBody = @{ displayName = $NotebookName; definition = $definition }
    $createResp = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/notebooks" -Body $createBody
    if ($createResp -and $createResp.id) {
        $notebookId = $createResp.id
    } else {
        $nbList2 = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/notebooks"
        $created = $nbList2.value | Where-Object { $_.displayName -eq $NotebookName } | Select-Object -First 1
        if (-not $created) { throw "Notebook '$NotebookName' was not found after create." }
        $notebookId = $created.id
    }
    Write-OK "Created notebook '$NotebookName' ($notebookId)"
}

Remove-Item $tmpNb -ErrorAction SilentlyContinue

Write-Host "`n=== Notebook Feeder Deployment Complete ===" -ForegroundColor Cyan
Write-Host "  Notebook:     $NotebookName ($notebookId)" -ForegroundColor Gray
Write-Host "  Workspace:    $($wsInfo.displayName) ($WorkspaceId)" -ForegroundColor Gray
Write-Host "  KQL Database: $($db.displayName) ($($db.id))" -ForegroundColor Gray
Write-Host "  State path:   $StatePath  (Lakehouse Files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Open in Fabric portal:" -ForegroundColor White
Write-Host "    https://app.fabric.microsoft.com/groups/$WorkspaceId/synapsenotebooks/$notebookId" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor White
Write-Host "    1. Attach a Lakehouse to the notebook (workspace default Lakehouse recommended)." -ForegroundColor White
Write-Host "    2. Click 'Run all' to execute one polling cycle, OR schedule the notebook from the portal." -ForegroundColor White
Write-Host "    3. For production scheduling, create a Data Factory pipeline that runs the notebook at the source's native cadence." -ForegroundColor White
