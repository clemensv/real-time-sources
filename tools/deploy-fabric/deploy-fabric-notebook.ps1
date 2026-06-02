<#
.SYNOPSIS
    Deploys the bluesky/botfinder Fabric notebook into a Fabric workspace
    and binds it to the source's KQL database.

.DESCRIPTION
    Companion to deploy-fabric.ps1. Run after the source's KQL database is
    deployed. Steps:

    1. Resolves the Fabric workspace, eventhouse and KQL database.
    2. Loads the notebook JSON from this repo
       (bluesky/botfinder/notebook/botfinder.ipynb).
    3. Patches metadata.dependencies.kqlDatabases to bind the notebook to
       the resolved KQL database (workspaceId / itemId / displayName).
    4. Creates or updates the notebook item in the Fabric workspace.

    Parameters mirror deploy-fabric.ps1 — only the bluesky source is supported.

.PARAMETER Source
    Source name. Default 'bluesky'. Used to locate the notebook in the repo.

.PARAMETER ResourceGroup
    Azure resource group (kept for parity with deploy-fabric.ps1; not used).

.PARAMETER Location
    Azure region (kept for parity; not used).

.PARAMETER SubscriptionId
    Azure subscription ID or name. If set, runs 'az account set' first.

.PARAMETER Workspace
    Fabric workspace name or GUID.

.PARAMETER Eventhouse
    Fabric eventhouse name or GUID.

.PARAMETER DatabaseName
    KQL database name. Defaults to the source name (with '-' replaced by '_').

.PARAMETER NotebookName
    Display name for the Fabric notebook item. Default 'botfinder'.

.PARAMETER NotebookPath
    Override the notebook file path. Default resolves to the script's repo
    location (../../bluesky/botfinder/notebook/botfinder.ipynb).

.PARAMETER WhatIf
    Print actions without contacting Fabric.

.EXAMPLE
    ./deploy-fabric-notebook.ps1 -Source bluesky -ResourceGroup rg-streams `
        -Workspace "c98acd97-4363-4296-8323-b6ab21e53903" -Eventhouse bluesky
#>

param(
    [string]$Source = "bluesky",
    [string]$ResourceGroup,
    [string]$Location,
    [string]$SubscriptionId,

    [Parameter(Mandatory = $true)]
    [string]$Workspace,

    [string]$Eventhouse,
    [string]$DatabaseName,
    [string]$NotebookName = "botfinder",
    [string]$NotebookPath,

    [switch]$SkipPostDeployHook,

    [string]$Repo = "clemensv/real-time-sources",

    [string]$Branch = "main",

    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
$FabricApi = "https://api.fabric.microsoft.com/v1"
$RawBase   = "https://raw.githubusercontent.com/$Repo/$Branch"
$TempDir   = if ($env:TEMP) { $env:TEMP } elseif ($env:TMPDIR) { $env:TMPDIR } else { [System.IO.Path]::GetTempPath() }
$guidRx = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

if (-not $DatabaseName)            { $DatabaseName = $Source -replace '-', '_' }
if ([string]::IsNullOrWhiteSpace($Eventhouse)) { $Eventhouse = $Source -replace '-', '_' }

if (-not $NotebookPath) {
    $repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
    $NotebookPath = Join-Path $repoRoot "feeders/$Source/botfinder/notebook/botfinder.ipynb"
}

function Write-Step { param([string]$Step, [string]$Msg) Write-Host "`n[$Step] $Msg" -ForegroundColor Yellow }
function Write-OK   { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor Green }
function Write-Info { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor DarkYellow }

function ConvertFrom-AzCliJson {
    param(
        [AllowNull()]
        [object]$InputObject,
        [string]$Context = "Azure CLI output"
    )

    if ($null -eq $InputObject) { return $null }

    $text = if ($InputObject -is [string]) {
        $InputObject
    } else {
        $InputObject | Out-String
    }

    $trimmed = $text.Trim()
    if (-not $trimmed) { return $null }

    try {
        return $trimmed | ConvertFrom-Json
    } catch {
        # az rest sometimes prepends WARNING:/INFO: lines ahead of JSON.
        $jsonStarts = [regex]::Matches($trimmed, '(?m)^[\t ]*[\{\[]')
        foreach ($match in $jsonStarts) {
            $candidate = $trimmed.Substring($match.Index).Trim()
            try {
                return $candidate | ConvertFrom-Json
            } catch {
                continue
            }
        }
    }

    throw "Failed to parse JSON from $Context. Raw output:`n$trimmed"
}

function Resolve-AzSubscriptionContext {
    param([Parameter(Mandatory = $true)] [string]$Subscription)

    az account set --subscription $Subscription --only-show-errors 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to set subscription '$Subscription' (name or ID)."
    }

    $account = az account show --only-show-errors --output json 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to resolve the active Azure subscription after selecting '$Subscription': $($account | Out-String)"
    }

    $parsed = ConvertFrom-AzCliJson -InputObject $account -Context "az account show output for subscription '$Subscription'"
    return [pscustomobject]@{
        Id   = $parsed.id
        Name = $parsed.name
    }
}

function Invoke-FabricApi {
    param([string]$Method, [string]$Url, [object]$Body)
    $azArgs = @("rest", "--method", $Method, "--url", $Url,
                "--resource", "https://api.fabric.microsoft.com",
                "--only-show-errors", "--output", "json")
    if ($Body) {
        $bodyFile = Join-Path $env:TEMP "fabric_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 30 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Fabric API error ($Method $Url): $($result | Out-String)" }
    if ($result) { return ConvertFrom-AzCliJson -InputObject $result -Context "Fabric API response ($Method $Url)" }
    return $null
}

function ConvertTo-GitHubContentsPath {
    param([Parameter(Mandatory = $true)] [string]$Path)

    return ((($Path -replace '\\', '/') -split '/') |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        ForEach-Object { [System.Uri]::EscapeDataString($_) }) -join '/'
}

function Expand-GitHubDirectoryToPath {
    param(
        [Parameter(Mandatory = $true)] [string]$Repo,
        [Parameter(Mandatory = $true)] [string]$Branch,
        [Parameter(Mandatory = $true)] [string]$SourcePath,
        [Parameter(Mandatory = $true)] [string]$DestinationPath,
        [string]$RootPath = $SourcePath
    )

    $contentsPath = ConvertTo-GitHubContentsPath -Path $SourcePath
    $url = "https://api.github.com/repos/$Repo/contents/$($contentsPath)?ref=$([System.Uri]::EscapeDataString($Branch))"
    $headers = @{ "User-Agent" = "GitHubCopilotCLI/1.0" }

    foreach ($item in (Invoke-RestMethod -Uri $url -Headers $headers -ErrorAction Stop)) {
        if ($item.type -eq 'dir') {
            Expand-GitHubDirectoryToPath -Repo $Repo -Branch $Branch -SourcePath $item.path -DestinationPath $DestinationPath -RootPath $RootPath
            continue
        }

        if ($item.type -ne 'file' -or [string]::IsNullOrWhiteSpace($item.download_url)) {
            continue
        }

        $relativePath = $item.path.Substring($RootPath.Length).TrimStart([char[]]@('/', '\'))
        $targetPath = Join-Path $DestinationPath ($relativePath -replace '/', '\')
        $targetDir = Split-Path -Parent $targetPath
        if ($targetDir -and -not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }

        Invoke-WebRequest -Uri $item.download_url -OutFile $targetPath -UseBasicParsing -ErrorAction Stop | Out-Null
    }
}

# ── Optional post-deploy hook (shared convention with deploy-fabric.ps1) ─
# A source MAY ship a {Source}/fabric/post-deploy.ps1 to perform extra
# Fabric wiring (Map layers, dashboards, environment seeding, …). The hook
# is auto-discovered (local working tree first, then $RawBase fallback) and
# invoked with a -Context hashtable.
function Invoke-SourcePostDeployHook {
    param([Parameter(Mandatory)] [hashtable]$Context)

    if ($SkipPostDeployHook) {
        Write-Info "Post-deploy hook skipped (-SkipPostDeployHook)"
        return
    }

    $rel = "feeders/$Source/fabric/post-deploy.ps1"
    $hookPath = $null
    try {
        $repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..") -ErrorAction Stop
        $candidate = Join-Path $repoRoot $rel
        if (Test-Path $candidate) { $hookPath = $candidate; Write-Info "Post-deploy hook found locally: $hookPath" }
    } catch { }
    if (-not $hookPath) {
        try {
            $tmp = Join-Path $TempDir "post-deploy-$Source-$([Guid]::NewGuid().ToString('N'))"
            New-Item -ItemType Directory -Path $tmp -Force | Out-Null
            Expand-GitHubDirectoryToPath -Repo $Repo -Branch $Branch -SourcePath "feeders/$Source/fabric" -DestinationPath $tmp
            $hookPath = Join-Path $tmp "post-deploy.ps1"
            if (-not (Test-Path $hookPath)) {
                throw "Downloaded hook bundle did not contain post-deploy.ps1."
            }
            Write-Info "Post-deploy hook bundle downloaded from $RawBase/feeders/$Source/fabric/"
        } catch {
            Write-Info "No post-deploy hook for '$Source' (looked for $rel) — skipping"
            return
        }
    }

    Write-Step "post" "Running post-deploy hook ($Source/fabric/post-deploy.ps1)..."
    try {
        & $hookPath -Context $Context
        if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
            throw "Post-deploy hook exited with code $LASTEXITCODE"
        }
        Write-OK "Post-deploy hook completed"
    } catch {
        Write-Warning "Post-deploy hook failed: $($_.Exception.Message)"
        throw
    }
}

Write-Host "=== botfinder Notebook Deployment ===" -ForegroundColor Cyan
Write-Host "  Source:        $Source"        -ForegroundColor White
Write-Host "  Workspace:     $Workspace"     -ForegroundColor White
Write-Host "  Eventhouse:    $Eventhouse"    -ForegroundColor White
Write-Host "  KQL Database:  $DatabaseName"  -ForegroundColor White
Write-Host "  Notebook:      $NotebookName"  -ForegroundColor White
Write-Host "  Notebook file: $NotebookPath"  -ForegroundColor White

if ($SubscriptionId) {
    $selectedSubscription = Resolve-AzSubscriptionContext -Subscription $SubscriptionId
    $SubscriptionId = $selectedSubscription.Id
    Write-OK "Subscription set: $($selectedSubscription.Name) ($SubscriptionId)"
}

if (-not (Test-Path $NotebookPath)) {
    throw "Notebook file not found: $NotebookPath"
}

# 1. Resolve workspace
Write-Step "1/4" "Resolving Fabric workspace..."
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

# 2. Resolve eventhouse + database (auto-create on a clean workspace)
Write-Step "2/4" "Resolving Eventhouse and KQL database..."
$ehList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
if ($Eventhouse -match $guidRx) {
    $eh = $ehList.value | Where-Object { $_.id -eq $Eventhouse } | Select-Object -First 1
} else {
    $eh = $ehList.value | Where-Object { $_.displayName -eq $Eventhouse } | Select-Object -First 1
}
if (-not $eh) {
    if ($Eventhouse -match $guidRx) {
        throw "Eventhouse with id '$Eventhouse' not found in workspace (cannot auto-create by GUID)."
    }
    Write-Host "  Creating Eventhouse '$Eventhouse'..." -ForegroundColor Yellow
    Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses" -Body @{ displayName = $Eventhouse } | Out-Null
    for ($i = 0; $i -lt 12 -and -not $eh; $i++) {
        Start-Sleep -Seconds 5
        $ehList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
        $eh = $ehList.value | Where-Object { $_.displayName -eq $Eventhouse } | Select-Object -First 1
    }
    if (-not $eh) { throw "Failed to create Eventhouse '$Eventhouse'." }
}
# Fetch full details (queryServiceUri populates lazily right after create)
$ehDetails = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$($eh.id)"
for ($i = 0; $i -lt 6 -and (-not $ehDetails -or -not $ehDetails.properties.queryServiceUri); $i++) {
    Start-Sleep -Seconds 5
    $ehDetails = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$($eh.id)"
}
if (-not $ehDetails -or -not $ehDetails.properties.queryServiceUri) {
    throw "Eventhouse '$($eh.displayName)' has no queryServiceUri after wait."
}
$eh = $ehDetails
Write-OK "Eventhouse: $($eh.displayName) ($($eh.id))"

$dbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$db = $dbList.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
if (-not $db) {
    Write-Host "  Creating KQL database '$DatabaseName'..." -ForegroundColor Yellow
    $dbProps = @{ databaseType = "ReadWrite"; parentEventhouseItemId = $eh.id; oneLakeCachingPeriod = "P36500D"; oneLakeStandardStoragePeriod = "P36500D" }
    Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases" -Body @{ displayName = $DatabaseName; creationPayload = $dbProps } | Out-Null
    for ($i = 0; $i -lt 12 -and -not $db; $i++) {
        Start-Sleep -Seconds 5
        $dbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
        $db = $dbList.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
    }
    if (-not $db) { throw "Failed to create KQL database '$DatabaseName'." }
}
Write-OK "KQL database: $($db.displayName) ($($db.id))"

$queryUri = $eh.properties.queryServiceUri
if (-not $queryUri) { throw "Eventhouse '$($eh.displayName)' has no queryServiceUri." }
Write-OK "Query URI:    $queryUri"

# 3. Patch notebook metadata.dependencies.kqlDatabases AND parameters cell
Write-Step "3/4" "Patching notebook KQL binding and parameters..."
$nbJson = Get-Content -LiteralPath $NotebookPath -Raw -Encoding UTF8
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

# Patch the parameters cell - replace KUSTO_URI / KUSTO_DATABASE defaults so
# the notebook works even if notebookutils.kql.listDatabases() is unavailable.
$paramsPatched = $false
foreach ($cell in $nb.cells) {
    if ($cell.cell_type -ne 'code') { continue }
    $tags = @()
    if ($cell.metadata -and $cell.metadata.tags) { $tags = @($cell.metadata.tags) }
    if ($tags -notcontains 'parameters') { continue }

    $srcLines = @($cell.source) | ForEach-Object { $_ }
    $newLines = foreach ($line in $srcLines) {
        if     ($line -match '^\s*KUSTO_URI\s*=')      { "KUSTO_URI      = `"$queryUri`"`n" }
        elseif ($line -match '^\s*KUSTO_DATABASE\s*=') { "KUSTO_DATABASE = `"$($db.displayName)`"`n" }
        else                                           { $line }
    }
    $cell.source = @($newLines)
    $paramsPatched = $true
    break
}
if ($paramsPatched) { Write-OK 'Patched parameters cell with KUSTO_URI / KUSTO_DATABASE' }
else                { Write-Info "No parameters-tagged cell found - skipped param patch" }

$tmpNb = Join-Path $env:TEMP "botfinder_patched_$(Get-Random).ipynb"
[System.IO.File]::WriteAllText($tmpNb, ($nb | ConvertTo-Json -Depth 50), [System.Text.UTF8Encoding]::new($false))
Write-OK "Patched notebook written to $tmpNb"

# 4. Create or update notebook item
Write-Step "4/4" "Uploading notebook to Fabric..."
$nbBytes  = [System.IO.File]::ReadAllBytes($tmpNb)
$nbBase64 = [Convert]::ToBase64String($nbBytes)
$definition = @{
    format = "ipynb"
    parts  = @(
        @{ path = "notebook-content.ipynb"; payload = $nbBase64; payloadType = "InlineBase64" }
    )
}

$nbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/notebooks"
$existing = $nbList.value | Where-Object { $_.displayName -eq $NotebookName } | Select-Object -First 1

if ($WhatIf) {
    if ($existing) {
        Write-Info "[WhatIf] Would call updateDefinition for notebook '$NotebookName' ($($existing.id))"
    } else {
        Write-Info "[WhatIf] Would create notebook '$NotebookName'"
    }
    Write-Host "`n=== Done (WhatIf) ===" -ForegroundColor Cyan
    return
}

if ($existing) {
    Invoke-FabricApi -Method POST `
        -Url "$FabricApi/workspaces/$WorkspaceId/notebooks/$($existing.id)/updateDefinition" `
        -Body @{ definition = $definition } | Out-Null
    Write-OK "Updated existing notebook '$NotebookName' ($($existing.id))"
    $notebookId = $existing.id
} else {
    $createBody = @{ displayName = $NotebookName; definition = $definition }
    $createResp = Invoke-FabricApi -Method POST `
        -Url "$FabricApi/workspaces/$WorkspaceId/notebooks" -Body $createBody
    if ($createResp -and $createResp.id) {
        $notebookId = $createResp.id
    } else {
        $nbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/notebooks"
        $created = $nbList.value | Where-Object { $_.displayName -eq $NotebookName } | Select-Object -First 1
        if (-not $created) { throw "Notebook '$NotebookName' was not found after create." }
        $notebookId = $created.id
    }
    Write-OK "Created notebook '$NotebookName' ($notebookId)"
}

Write-Host "`n=== Notebook Deployment Complete ===" -ForegroundColor Cyan
Write-Host "  Notebook:     $NotebookName ($notebookId)" -ForegroundColor Gray
Write-Host "  Workspace:    $($wsInfo.displayName)"      -ForegroundColor Gray
Write-Host "  KQL Database: $($db.displayName) ($($db.id))" -ForegroundColor Gray
Write-Host ""
Write-Host "  Open in Fabric portal:" -ForegroundColor White
Write-Host "    https://app.fabric.microsoft.com/groups/$WorkspaceId/synapsenotebooks/$notebookId" -ForegroundColor Cyan
Write-Host ""

# ── Optional post-deploy hook ───────────────────────────────────────────
$hookContext = @{
    Source                 = $Source
    Mode                   = 'notebook'
    SubscriptionId         = $SubscriptionId
    Repo                   = $Repo
    Branch                 = $Branch
    RawBase                = $RawBase
    FabricApi              = $FabricApi
    TempDir                = $TempDir
    WorkspaceId            = $WorkspaceId
    WorkspaceName          = $wsInfo.displayName
    EventhouseId           = $eh.id
    EventhouseName         = $eh.displayName
    EventhouseClusterUri   = $queryUri
    DatabaseId             = $db.id
    DatabaseName           = $db.displayName
    NotebookId             = $notebookId
    NotebookName           = $NotebookName
}
Invoke-SourcePostDeployHook -Context $hookContext
