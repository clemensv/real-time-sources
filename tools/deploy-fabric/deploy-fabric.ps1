<#
.SYNOPSIS
    Deploys the Fabric-side artifacts for a Real-Time Sources bridge
    (Eventhouse / KQL database / Event Stream / source-specific post-deploy
    hook). This script does NOT deploy any Azure infrastructure (no
    Resource Group, no Container Instance, no Event Hubs namespace).

.DESCRIPTION
    This script is designed to run in Azure Cloud Shell (PowerShell). It is
    the Fabric-only variant invoked by the gh-pages portal's "Fabric only"
    deployment mode. The feeder (the process that actually pushes upstream
    data into the Event Stream) is the user's responsibility — they can run
    the source's Docker image anywhere (laptop, on-prem, Azure Container
    Instance, Kubernetes, …) using the connection string this script writes
    out via -OutCsFile, or they can deploy the Fabric-notebook feeder
    variant via the sibling deploy-feeder-notebook.ps1 script.

    Steps performed:
    1. Resolve the target Workspace / Eventhouse (create the Eventhouse
       on demand if it doesn't exist).
    2. Create (or reuse) a KQL database in the Eventhouse.
    3. Apply the source's KQL schema script (_cloudevents_dispatch, typed
       tables, update policies, materialized views, helper functions).
    4. Create a Fabric Event Stream with a Custom Endpoint source that
       routes into the KQL database's _cloudevents_dispatch table.
    5. Retrieve the Custom Endpoint connection string from the Event Stream
       (optionally written to -OutCsFile for downstream feeder wiring).
    6. Run the source's optional post-deploy hook
       (<source>/fabric/post-deploy.ps1) — typically used to wire Fabric
       Map items, ingest static reference data, etc.

    Prerequisites:
    - Azure Cloud Shell (PowerShell) with az CLI authenticated against an
      identity that has Contributor on the target Fabric workspace.
    - A target Fabric Workspace (will be looked up by name or GUID).

.PARAMETER Source
    The source directory name (e.g., pegelonline, usgs-earthquakes).

.PARAMETER SubscriptionId
    Azure subscription ID or name. If provided, the script sets this as the
    active subscription for Fabric token acquisition.

.PARAMETER Workspace
    Microsoft Fabric workspace name OR GUID.

.PARAMETER Eventhouse
    Microsoft Fabric Eventhouse name OR GUID. Will be created on demand if
    it does not already exist in the workspace.

.PARAMETER DatabaseName
    KQL database name. Defaults to the source name (with hyphens converted
    to underscores).

.PARAMETER SkipPostDeployHook
    Skip the source-specific post-deploy hook even if one exists.

.PARAMETER OutCsFile
    Optional path; if provided, the Event Stream Custom Endpoint connection
    string is written to this file (UTF-8, no trailing newline). Use this
    string to configure the feeder of your choice.

.EXAMPLE
    ./deploy-fabric.ps1 -Source pegelonline `
        -Workspace "ContosoRealTime" -Eventhouse "ContosoRealTime-eh"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [string]$SubscriptionId,

    [Parameter(Mandatory = $true)]
    [string]$Workspace,

    [string]$Eventhouse,

    [string]$DatabaseName,

    [switch]$SkipPostDeployHook,

    [string]$Repo = "clemensv/real-time-sources",

    [string]$Branch = "main",

    [string]$OutCsFile,

    # Deprecated / ignored. Retained so old gh-pages portal commands keep
    # working; these parameters had meaning when this script also deployed
    # an ACI feeder, which it no longer does.
    [string]$ResourceGroup,
    [string]$Location,
    [switch]$SkipArm
)

$ErrorActionPreference = "Stop"
$RawBase = "https://raw.githubusercontent.com/$Repo/$Branch"
$FabricApi = "https://api.fabric.microsoft.com/v1"
$TempDir = if ($env:TEMP) { $env:TEMP } elseif ($env:TMPDIR) { $env:TMPDIR } else { [System.IO.Path]::GetTempPath() }

if (-not $DatabaseName) { $DatabaseName = $Source -replace '-', '_' }
if ([string]::IsNullOrWhiteSpace($Eventhouse)) { $Eventhouse = $Source -replace '-', '_' }
$EventStreamName = "$Source-ingest"
$StreamName = "$EventStreamName-stream"

if ($ResourceGroup -or $Location -or $SkipArm) {
    Write-Warning "  -ResourceGroup / -Location / -SkipArm are no longer used by deploy-fabric.ps1 (Fabric-only)."
    Write-Warning "  Deploy the upstream feeder separately (Docker, ACI portal template, or deploy-feeder-notebook.ps1)."
}

# ── Helpers ──────────────────────────────────────────────────────────────

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

function Write-Step { param([string]$Step, [string]$Msg)
    Write-Host "`n[$Step] $Msg" -ForegroundColor Yellow
}
function Write-OK { param([string]$Msg)
    Write-Host "  $Msg" -ForegroundColor Green
}
function Write-Info { param([string]$Msg)
    Write-Host "  $Msg" -ForegroundColor DarkYellow
}

# Set Azure subscription if provided
if ($SubscriptionId) {
    $selectedSubscription = Resolve-AzSubscriptionContext -Subscription $SubscriptionId
    $SubscriptionId = $selectedSubscription.Id
    Write-Host "  Subscription: $($selectedSubscription.Name) ($SubscriptionId)" -ForegroundColor White
}

function Convert-KqlForFabricDefinition {
    # Filters a .kql script so it conforms to the restricted command set that
    # the Fabric KQL "DatabaseSchema.kql" definition API accepts. Commands that
    # the API rejects are dropped or rewritten:
    #   .alter table X docstring ...           → dropped (cosmetic)
    #   .alter table X column-docstrings ...   → dropped (cosmetic)
    #   .drop materialized-view X ifexists;    → dropped
    #   .create materialized-view ...          → .create-or-alter materialized-view ...
    # All other commands (.create-merge table, .create-or-alter function,
    # .create-or-alter materialized-view, .create-or-alter table ... ingestion
    # ... mapping, .alter table ... policy ...) pass through unchanged.
    param([string]$Script)
    if (-not $Script) { return $Script }
    $commands = [regex]::Split($Script, '(?m)^\s*$\r?\n')
    $out = @()
    foreach ($cmd in $commands) {
        $trim = $cmd.Trim()
        if (-not $trim) { continue }
        if ($trim -match '^\.alter\s+table\s+\S+\s+docstring\b') { continue }
        if ($trim -match '^\.alter\s+table\s+\S+\s+column-docstrings\b') { continue }
        if ($trim -match '^\.drop\s+materialized-view\b') { continue }
        if ($trim -match '^\.create\s+materialized-view\b') {
            $trim = $trim -replace '^\.create\s+materialized-view\b', '.create-or-alter materialized-view'
        }
        $out += $trim
    }
    return ($out -join "`n`n")
}

function Invoke-FabricApi {
    param(
        [string]$Method,
        [string]$Url,
        [object]$Body
    )
    $azArgs = @("rest", "--method", $Method, "--url", $Url,
                "--resource", "https://api.fabric.microsoft.com",
                "--only-show-errors", "--output", "json")
    if ($Body) {
        $bodyFile = Join-Path $TempDir "fabric_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 20 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Fabric API error ($Method $Url): $($result | Out-String)"
    }
    if ($result) { return ConvertFrom-AzCliJson -InputObject $result -Context "Fabric API response ($Method $Url)" }
    return $null
}

function Invoke-KqlScript {
    param(
        [string]$QueryUri,
        [string]$Database,
        [string]$ScriptContent,
        [string]$Label
    )
    Write-Host "  Applying $Label..." -ForegroundColor Yellow
    $body = @{
        csl = ".execute database script <|`n$ScriptContent"
        db  = $Database
    }
    $bodyFile = Join-Path $TempDir "kql_body_$(Get-Random).json"
    [System.IO.File]::WriteAllText(
        $bodyFile,
        ($body | ConvertTo-Json -Compress),
        [System.Text.UTF8Encoding]::new($false)
    )
    $result = az rest `
        --method POST `
        --url "$QueryUri/v1/rest/mgmt" `
        --resource $QueryUri `
        --body "@$bodyFile" `
        --headers "Content-Type=application/json" `
        --only-show-errors `
        --output json 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "KQL script failed for $Label`n$result"
    }
    $parsed = ConvertFrom-AzCliJson -InputObject $result -Context "KQL management response for $Label"
    $rows = @()
    if ($parsed.Tables.Count -gt 0) { $rows = $parsed.Tables[0].Rows }
    $failed = @($rows | Where-Object { $_[3] -ne "Completed" })
    if ($failed.Count -gt 0) {
        Write-Warning "Some KQL commands reported non-Completed status for $Label"
        $failed | ForEach-Object { Write-Warning "  $_" }
    }
    Write-OK "Applied $Label"
}

function Get-EventStreamConnectionString {
    <#
    Retrieve the CustomEndpoint primary connection string for an Event Stream
    using the public Fabric Topology API:

      GET /workspaces/{ws}/eventstreams/{es}/topology
      GET /workspaces/{ws}/eventstreams/{es}/sources/{src}/connection

    Replaces the legacy 7-step MWC (Power BI workload token) dance. Documented at
    https://learn.microsoft.com/en-us/rest/api/fabric/eventstream/topology/get-eventstream-source-connection
    #>
    param(
        [string]$WsId,
        [string]$EventStreamId
    )
    $maxRetries = 20   # topology endpoint may take 5+ min to register
    $lastErr = $null
    for ($retry = 0; $retry -lt $maxRetries; $retry++) {
        try {
            $topo = Invoke-FabricApi -Method GET `
                -Url "$FabricApi/workspaces/$WsId/eventstreams/$EventStreamId/topology"
            $src = $topo.sources | Where-Object { $_.type -eq "CustomEndpoint" } | Select-Object -First 1
            if (-not $src) { throw "Event Stream has no CustomEndpoint source." }

            $conn = Invoke-FabricApi -Method GET `
                -Url "$FabricApi/workspaces/$WsId/eventstreams/$EventStreamId/sources/$($src.id)/connection"
            $cs = $conn.accessKeys.primaryConnectionString
            if ($cs) {
                return [pscustomobject]@{
                    PrimaryConnectionString = $cs
                    Namespace               = $conn.fullyQualifiedNamespace
                    EventHubName            = $conn.eventHubName
                    SourceId                = $src.id
                }
            }
            $lastErr = "Empty primaryConnectionString in /sources/{id}/connection response"
        } catch {
            $lastErr = $_.Exception.Message
            if ($_.ErrorDetails -and $_.ErrorDetails.Message) { $lastErr += " | $($_.ErrorDetails.Message)" }
        }
        if ($retry -lt ($maxRetries - 1)) { Start-Sleep -Seconds 30 }
    }
    Write-Warning "Get-EventStreamConnectionString failed after $maxRetries tries: $lastErr"
    return $null
}

function Wait-EventStreamTopologyReady {
    param(
        [string]$WsId,
        [string]$EventStreamId,
        [int]$TimeoutSeconds = 120,
        [int]$PollSeconds = 15
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $lastStatus = ""
    while ((Get-Date) -lt $deadline) {
        try {
            $topo = Invoke-FabricApi -Method GET `
                -Url "$FabricApi/workspaces/$WsId/eventstreams/$EventStreamId/topology"
            $sourceStates = @($topo.sources | ForEach-Object { "$($_.name):$($_.status)" })
            $destinationStates = @($topo.destinations | ForEach-Object { "$($_.name):$($_.status)" })
            $lastStatus = (@($sourceStates) + @($destinationStates)) -join "; "

            # Detect permanently failed sources early — no point waiting the full timeout
            $failedSources = @($topo.sources | Where-Object { $_.status -eq "Failed" })
            if ($failedSources.Count -gt 0) {
                $destinations = @($topo.destinations | Where-Object { $_.type -eq "Eventhouse" })
                $destinationsReady = $destinations.Count -gt 0 -and @($destinations | Where-Object { $_.status -ne "Running" }).Count -eq 0
                if ($destinationsReady) {
                    # Source failed but destination is running — custom endpoint provisioning failed.
                    # Signal to caller to delete and recreate the Event Stream.
                    throw "Event Stream source node(s) permanently Failed: $($failedSources | ForEach-Object { $_.name } | Join-String -Separator ', '). Destination is Running. Recreate the Event Stream or check the custom endpoint configuration."
                }
            }

            $sourcesReady = @($topo.sources | Where-Object { $_.type -eq "CustomEndpoint" -and $_.status -eq "Running" }).Count -gt 0
            $destinations = @($topo.destinations | Where-Object { $_.type -eq "Eventhouse" })
            $destinationsReady = $destinations.Count -gt 0 -and @($destinations | Where-Object { $_.status -ne "Running" }).Count -eq 0
            if ($sourcesReady -and $destinationsReady) {
                Write-OK "Event Stream source and Eventhouse destination are Running"
                return
            }
            Write-Info "Waiting for Event Stream topology... $lastStatus"
        } catch {
            if ($_.Exception.Message -match "permanently Failed") { throw }
            $lastStatus = $_.Exception.Message
            Write-Info "Waiting for Event Stream topology... $lastStatus"
        }
        Start-Sleep -Seconds $PollSeconds
    }
    # Non-fatal: the topology endpoint may lag workload registration by 5-15 min under load.
    # Log a warning and continue — the notebook run will succeed once the ES backend catches up.
    Write-Warning "Event Stream topology did not reach Running within ${TimeoutSeconds}s. Proceeding anyway. Last status: $lastStatus"
}

# ── Optional post-deploy hook ───────────────────────────────────────────
# Each source MAY ship a {Source}/fabric/post-deploy.ps1 to perform extra
# wiring (Fabric Map layers, dashboards, environment seeding, …). The hook
# is auto-discovered (local working tree first, then $RawBase as fallback)
# and invoked with a -Context hashtable carrying every ID the source
# bootstrap might need. Hook authors can ignore keys they don't care about.
function Invoke-SourcePostDeployHook {
    param([Parameter(Mandatory)] [hashtable]$Context)

    if ($SkipPostDeployHook) {
        Write-Info "Post-deploy hook skipped (-SkipPostDeployHook)"
        return
    }

    $rel = "feeders/$Source/fabric/post-deploy.ps1"
    $localPath = $null
    try {
        $repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..") -ErrorAction Stop
        $candidate = Join-Path $repoRoot $rel
        if (Test-Path $candidate) { $localPath = $candidate }
    } catch { }

    $hookPath = $null
    if ($localPath) {
        $hookPath = $localPath
        Write-Info "Post-deploy hook found locally: $hookPath"
    } else {
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

    Write-Step "6/6" "Running post-deploy hook ($Source/fabric/post-deploy.ps1)..."
    try {
        & $hookPath -Context $Context
        if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
            Write-Warning "Post-deploy hook exited with code $LASTEXITCODE (non-fatal: core deployment succeeded)"
            Write-Warning "Re-run the hook manually if needed:"
            Write-Warning "  pwsh $hookPath -Context <hashtable>"
            $global:LASTEXITCODE = 0  # reset so deploy-feeder-notebook.ps1 does not abort
        } else {
            Write-OK "Post-deploy hook completed"
        }
    } catch {
        Write-Warning "Post-deploy hook failed: $($_.Exception.Message)"
        Write-Warning "Core deployment was successful; re-run the hook manually:"
        Write-Warning "  pwsh $hookPath -Context <hashtable>"
    }
}

# ── Validate source ─────────────────────────────────────────────────────

Write-Host "=== Real-Time Sources — Fabric Deployment ===" -ForegroundColor Cyan
Write-Host "  Source: $Source" -ForegroundColor White

# Cleanup-on-failure trap: delete any items we created if the script fails
trap {
    Write-Warning "Deploy failed — running cleanup to avoid workspace degradation..."
    Invoke-FailureCleanup
    break
}

# Check that the source's KQL schema script exists in the repo
$kqlUrl = "$RawBase/feeders/$Source/kql/$($Source -replace '-', '_').kql"

Write-Step "0/6" "Validating source assets in repository..."
try {
    $null = Invoke-WebRequest -Uri $kqlUrl -Method Head -UseBasicParsing
    Write-OK "KQL script found"
} catch {
    $kqlUrl = "$RawBase/feeders/$Source/kql/$Source.kql"
    try {
        $null = Invoke-WebRequest -Uri $kqlUrl -Method Head -UseBasicParsing
        Write-OK "KQL script found (alternate name)"
    } catch {
        $kqlUrl = $null
        Write-Info "No KQL script — database schema step will be skipped"
    }
}


# Resolve workspace: accept name or GUID
$guidRx = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
if ($Workspace -match $guidRx) {
    $WorkspaceId = $Workspace
} else {
    $allWs = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces"
    $ws = $allWs.value | Where-Object { $_.displayName -eq $Workspace } | Select-Object -First 1
    if (-not $ws) { throw "Workspace '$Workspace' not found." }
    $WorkspaceId = $ws.id
}
$wsInfo = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId"
$CapacityId = $wsInfo.capacityId
if (-not $CapacityId) { throw "Could not determine capacity ID for workspace '$($wsInfo.displayName)'" }
Write-OK "Workspace: $($wsInfo.displayName) ($WorkspaceId)"

# Track items created in this run so we can clean up on failure
$script:createdEventhouseId  = $null
$script:createdEvenstreamId  = $null
$script:createdDatabaseId    = $null
$script:createdNotebookId    = $null
$script:kqlDbLroFailed       = $false

function Invoke-FailureCleanup {
    $tok = az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv 2>$null
    if (-not $tok) { return }
    $ch = @{ Authorization = "Bearer $tok" }
    foreach ($pair in @(
        @($script:createdNotebookId,  "Notebook"),
        @($script:createdEvenstreamId, "Eventstream"),
        @($script:createdDatabaseId,  "KQLDatabase"),
        @($script:createdEventhouseId, "Eventhouse")
    )) {
        $itemId = $pair[0]; $label = $pair[1]
        if ($itemId) {
            try {
                Invoke-RestMethod "https://api.fabric.microsoft.com/v1/workspaces/$WorkspaceId/items/$itemId" `
                    -Method Delete -Headers $ch | Out-Null
                Write-Host "  [cleanup] Deleted $label $itemId" -ForegroundColor DarkGray
            } catch {}
        }
    }
}

$eventhouses = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
$ehDetails = $null
$EventhouseId = $null
if ($Eventhouse -match $guidRx) {
    $EventhouseId = $Eventhouse
} else {
    $match = $eventhouses.value | Where-Object { $_.displayName -eq $Eventhouse } | Select-Object -First 1
    if ($match) {
        $EventhouseId = $match.id
    } else {
        Write-Host "  Creating Eventhouse '$Eventhouse'..." -ForegroundColor Yellow
        Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses" -Body @{ displayName = $Eventhouse } | Out-Null
        for ($i = 0; $i -lt 12; $i++) {
            Start-Sleep -Seconds 5
            $eventhouses = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
            $eh = $eventhouses.value | Where-Object { $_.displayName -eq $Eventhouse } | Select-Object -First 1
            if ($eh) { $EventhouseId = $eh.id; break }
            Write-Host "  Waiting for Eventhouse... ($([int](($i+1)*5))s)" -ForegroundColor Gray
        }
        if (-not $EventhouseId) { throw "Failed to create Eventhouse '$Eventhouse'." }
        $script:createdEventhouseId = $EventhouseId  # track for cleanup-on-failure
    }
}
if (-not $EventhouseId) { throw "Could not resolve Eventhouse ID for '$Eventhouse'." }
# Fetch full details for queryServiceUri (retry once if first call returns null)
$ehDetails = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
if (-not $ehDetails -or -not $ehDetails.properties.queryServiceUri) {
    Start-Sleep -Seconds 5
    $ehDetails = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
}
if (-not $ehDetails -or -not $ehDetails.properties.queryServiceUri) {
    throw "Could not fetch eventhouse details (id=$EventhouseId)."
}
Write-OK "Eventhouse: $($ehDetails.displayName) ($EventhouseId)"
$queryUri = $ehDetails.properties.queryServiceUri

#  Step 1: Create KQL database with schema 

Write-Step "1/6" "Setting up KQL database '$DatabaseName'..."

$databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1

# If DB not yet visible, wait up to 30s — Eventhouse auto-creates it within seconds but the list may lag
if (-not $existingDb) {
    for ($i = 0; $i -lt 6; $i++) {
        Start-Sleep -Seconds 5
        $databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
        $existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
        if ($existingDb) { break }
    }
}

$kqlContent = $null
$filteredKql = $null
if ($kqlUrl) {
    $kqlContent = (Invoke-WebRequest -Uri $kqlUrl -UseBasicParsing).Content
    $filteredKql = Convert-KqlForFabricDefinition $kqlContent
}

if ($existingDb) {
    $databaseId = $existingDb.id
    Write-Info "Database already exists (ID: $databaseId)"
    # Verify the existing database is still usable by checking if the Eventhouse parent matches
    $dbStaleness = $false
    if ($kqlContent) {
        Write-Step "2/6" "Updating KQL schema..."
        try {
            Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName -ScriptContent $kqlContent -Label "$Source.kql"
        } catch {
            Write-Host "  Falling back to Fabric definition API..." -ForegroundColor Yellow
            $schemaBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($filteredKql))
            $dbProps = @{ databaseType = "ReadWrite"; parentEventhouseItemId = $EventhouseId; oneLakeCachingPeriod = "P36500D"; oneLakeStandardStoragePeriod = "P36500D" }
            $dbPropsBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes(($dbProps | ConvertTo-Json -Compress)))
            try {
                Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases/$databaseId/updateDefinition" -Body @{ definition = @{ parts = @(
                    @{ path = "DatabaseProperties.json"; payload = $dbPropsBase64; payloadType = "InlineBase64" },
                    @{ path = "DatabaseSchema.kql"; payload = $schemaBase64; payloadType = "InlineBase64" }
                )}}
                Start-Sleep -Seconds 30
                Write-OK "Schema update submitted"
            } catch {
                # updateDefinition failed (e.g. ItemNotFound / stale orphan from a prior deploy).
                # Delete the stale database entry and fall through to the create path.
                Write-Host "  updateDefinition failed ($_). Deleting stale DB and recreating..." -ForegroundColor Yellow
                try {
                    Invoke-FabricApi -Method DELETE -Url "$FabricApi/workspaces/$WorkspaceId/items/$databaseId" | Out-Null
                    Start-Sleep -Seconds 5
                } catch {
                    Write-Host "  Could not delete stale DB (ignoring): $_" -ForegroundColor Yellow
                }
                $dbStaleness = $true
            }
        }
    } else {
        Write-Step "2/6" "No KQL schema available — skipping"
    }
    if (-not $dbStaleness) {
        # existingDb path done — skip the create block below
    }
}
if (-not $existingDb -or $dbStaleness) {
    # Always create DB without schema, then apply schema via dataplane.
    # The definition API path silently fails to apply schemas in many cases
    # (LRO succeeds but tables don't materialize), so we use .execute database
    # script which gives per-command success/failure status.
    $dbProps = @{ databaseType = "ReadWrite"; parentEventhouseItemId = $EventhouseId; oneLakeCachingPeriod = "P36500D"; oneLakeStandardStoragePeriod = "P36500D" }
    $dbPropsBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes(($dbProps | ConvertTo-Json -Compress)))
    $createBody = @{ displayName = $DatabaseName; definition = @{ parts = @(
        @{ path = "DatabaseProperties.json"; payload = $dbPropsBase64; payloadType = "InlineBase64" }
    )}}
    Write-Host "  Creating database..." -ForegroundColor Gray

    $createFile = Join-Path $TempDir "kql_create_$(Get-Random).json"
    [System.IO.File]::WriteAllText($createFile, ($createBody | ConvertTo-Json -Depth 10 -Compress), [System.Text.UTF8Encoding]::new($false))
    # Use Invoke-WebRequest so we can capture the Operation Location header and surface async failures
    $accessToken = az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv
    $createResp = Invoke-WebRequest -Uri "$FabricApi/workspaces/$WorkspaceId/kqlDatabases" -Method POST `
        -Headers @{ Authorization="Bearer $accessToken"; "Content-Type"="application/json" } `
        -Body ($createBody | ConvertTo-Json -Depth 10 -Compress) -SkipHttpErrorCheck
    if ($createResp.StatusCode -eq 409) {
        # Eventhouse auto-creates a DB with the same name; wait for it to appear in the list
        Write-Host "  Database '$DatabaseName' already exists (auto-created with Eventhouse); waiting for it to appear..." -ForegroundColor Yellow
    } elseif ($createResp.StatusCode -ge 400) {
        throw "kqlDatabases POST returned $($createResp.StatusCode): $($createResp.Content)"
    }
    $opLoc = $createResp.Headers['Location'] | Select-Object -First 1
    if ($createResp.StatusCode -eq 202 -and $opLoc) {
        Write-Host "  Tracking LRO $opLoc" -ForegroundColor Gray
        for ($i = 0; $i -lt 36; $i++) {
            Start-Sleep -Seconds 10
            $op = Invoke-RestMethod -Uri ([uri]$opLoc) -Headers @{ Authorization = "Bearer $accessToken" } -SkipHttpErrorCheck
            if ($op.status -eq 'Succeeded') { Write-OK "Database provisioned"; break }
            if ($op.status -eq 'Failed') {
                # UnknownError/ParentEventhouseItemWasNotFound: Eventhouse not yet ready.
                # Fall through to the poll loop; if DB doesn't appear, we retry the POST.
                Write-Host "  KQL DB creation LRO failed ($($op.error.errorCode)); will retry in poll loop..." -ForegroundColor Yellow
                $script:kqlDbLroFailed = $true
                break
            }
            Write-Host "  LRO: $($op.status) ($([int](($i+1)*10))s)" -ForegroundColor DarkGray
        }
    }
    $databaseId = $null
    # Retry POST every 60s — Eventhouse KQL infra may not be ready immediately.
    # Each retry checks the DB list first; if it appears (auto-created), we're done.
    $maxRetries = 20  # up to 20 POST attempts × ~60s each = ~20 min total
    for ($attempt = 0; $attempt -lt $maxRetries -and -not $databaseId; $attempt++) {
        if ($attempt -gt 0) {
            Write-Host "  Retrying KQL DB create (attempt $($attempt+1)/$maxRetries)..." -ForegroundColor Yellow
            $accessToken = az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv
            $retryResp = Invoke-WebRequest -Uri "$FabricApi/workspaces/$WorkspaceId/kqlDatabases" -Method POST `
                -Headers @{ Authorization="Bearer $accessToken"; "Content-Type"="application/json" } `
                -Body ($createBody | ConvertTo-Json -Depth 10 -Compress) -SkipHttpErrorCheck
            if ($retryResp.StatusCode -eq 409) {
                Write-Host "  DB now exists (auto-created), continuing poll..." -ForegroundColor Yellow
            } elseif ($retryResp.StatusCode -eq 202) {
                $retryOpLoc = $retryResp.Headers['Location'] | Select-Object -First 1
                if ($retryOpLoc) {
                    for ($j = 0; $j -lt 6; $j++) {
                        Start-Sleep -Seconds 10
                        $retryOp = Invoke-RestMethod -Uri ([uri]$retryOpLoc) -Headers @{ Authorization = "Bearer $accessToken" } -SkipHttpErrorCheck
                        if ($retryOp.status -eq 'Succeeded') { Write-OK "Database provisioned (attempt $($attempt+1))"; break }
                        if ($retryOp.status -eq 'Failed') {
                            Write-Host "  Retry LRO failed ($($retryOp.error.errorCode)), will re-check list..." -ForegroundColor Yellow; break
                        }
                        Write-Host "  Retry LRO: $($retryOp.status)" -ForegroundColor DarkGray
                    }
                }
            }
        }
        # Poll for up to 60s for the DB to appear (auto-created or from this POST)
        for ($i = 0; $i -lt 6; $i++) {
            Start-Sleep -Seconds 10
            $databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
            $existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
            if ($existingDb -and $existingDb.id) { $databaseId = $existingDb.id; break }
            try {
                $ehDbs = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId/kqlDatabases"
                $existingDb = $ehDbs.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
                if ($existingDb -and $existingDb.id) { $databaseId = $existingDb.id; break }
            } catch {}
            Write-Host "  Provisioning... ($([int]($attempt*60 + ($i+1)*10))s)" -ForegroundColor Gray
        }
    }
    if (-not $databaseId) { throw "Database '$DatabaseName' was not found after $($maxRetries) retries (~$($maxRetries * 60)s)." }
    Write-OK "Database created (ID: $databaseId)"
    $script:createdDatabaseId = $databaseId  # track for cleanup-on-failure

    if ($kqlContent) {
        Write-Step "2/6" "Applying KQL schema via dataplane..."
        # Brief delay to let the new DB's query/mgmt endpoint become ready
        Start-Sleep -Seconds 20
        $maxAttempts = 6
        for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
            try {
                Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName -ScriptContent $kqlContent -Label "$Source.kql"
                break
            } catch {
                if ($attempt -eq $maxAttempts) { throw }
                Write-Host "  Schema apply attempt $attempt failed: $($_.Exception.Message.Split([Environment]::NewLine)[0]); retrying in 15s..." -ForegroundColor DarkYellow
                Start-Sleep -Seconds 15
            }
        }
    } else {
        Write-Step "2/6" "No KQL schema available — skipping"
    }
}

#  Steps 3+4: Create Fabric Event Stream with inline topology definition
# Creating with the full definition in the initial POST avoids the separate updateDefinition
# call, which was unreliable (EntityNotFound for 5-10+ min under workspace load).

Write-Step "3/6" "Creating Event Stream '$EventStreamName' with topology..."
$sourceNodeName = "$Source-input"
$esDef = @{ compatibilityLevel = "1.1"
    sources = @(@{ name = $sourceNodeName; type = "CustomEndpoint"; properties = @{} })
    streams = @(@{ name = $StreamName; type = "DefaultStream"; properties = @{}; inputNodes = @(@{ name = $sourceNodeName }) })
    operators = @()
    destinations = @(@{ name = "dispatch-kql"; type = "Eventhouse"; properties = @{
        dataIngestionMode = "ProcessedIngestion"; workspaceId = $WorkspaceId; itemId = $databaseId
        databaseName = $DatabaseName; tableName = "_cloudevents_dispatch"
        inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } }
    }; inputNodes = @(@{ name = $StreamName }) })
}
$esBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes(($esDef | ConvertTo-Json -Depth 20)))
$esCreateBody = @{ displayName = $EventStreamName; definition = @{ parts = @(@{ path = "eventstream.json"; payload = $esBase64; payloadType = "InlineBase64" }) } }
$esCreateFile = Join-Path $TempDir "es_create_$(Get-Random).json"
[System.IO.File]::WriteAllText($esCreateFile, ($esCreateBody | ConvertTo-Json -Depth 20 -Compress), [System.Text.UTF8Encoding]::new($false))

$eventstreams = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
$existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1
if ($existingEs) {
    $eventstreamId = $existingEs.id
    Write-Info "Event Stream already exists (ID: $eventstreamId)"
    # Verify accessible — may be a stale entry from a prior cleanup
    try {
        Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams/$eventstreamId" | Out-Null
    } catch {
        Write-Host "  Event Stream not accessible; deleting stale entry and recreating..." -ForegroundColor Yellow
        try { Invoke-FabricApi -Method DELETE -Url "$FabricApi/workspaces/$WorkspaceId/items/$eventstreamId" | Out-Null } catch {}
        Start-Sleep -Seconds 15
        $existingEs = $null; $eventstreamId = $null
    }
}
if (-not $existingEs) {
    # Create with full topology inline — avoids unreliable two-step create+updateDefinition.
    # Retry up to 5 times with 30s gaps; on 409 the ES already exists from a prior attempt.
    $maxEsAttempts = 5
    for ($esAttempt = 0; $esAttempt -lt $maxEsAttempts -and -not $eventstreamId; $esAttempt++) {
        if ($esAttempt -gt 0) {
            Write-Host "  Event Stream not found — retrying POST (attempt $($esAttempt+1)/$maxEsAttempts)..." -ForegroundColor Yellow
            Start-Sleep -Seconds 30
        }
        $accessToken = az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv
        $esResp = Invoke-WebRequest -Uri "$FabricApi/workspaces/$WorkspaceId/eventstreams" -Method POST `
            -Headers @{ Authorization = "Bearer $accessToken"; "Content-Type" = "application/json" } `
            -Body ([System.IO.File]::ReadAllText($esCreateFile)) -SkipHttpErrorCheck
        if ($esResp.StatusCode -eq 409) {
            Write-Host "  Event Stream already exists (from prior attempt), searching list..." -ForegroundColor Yellow
        } elseif ($esResp.StatusCode -ge 400) {
            $errContent = $esResp.Content
            if ($errContent -match 'EventStreamBadWebRequest|dependent items do not exist') {
                # KQL DB indexed by runner but not yet visible to Event Stream service — retry after delay
                Write-Host "  ES creation: KQL DB not yet visible to Event Stream service (retry $($esAttempt+1)/$maxEsAttempts in 30s)..." -ForegroundColor Yellow
                Start-Sleep -Seconds 30
                continue
            }
            throw "Event Stream creation returned $($esResp.StatusCode): $errContent"
        } else {
            $esBody = $esResp.Content | ConvertFrom-Json -ErrorAction SilentlyContinue
            if ($esBody -and $esBody.id) {
                $eventstreamId = $esBody.id
            } else {
                $lroUrl = $esResp.Headers['Location'] | Select-Object -First 1
                if ($lroUrl) {
                    Write-Host "  Event Stream creation async (LRO attempt $($esAttempt+1))..." -ForegroundColor Gray
                    for ($i = 0; $i -lt 30; $i++) {
                        Start-Sleep -Seconds 10
                        $op = Invoke-RestMethod $lroUrl -Headers @{ Authorization = "Bearer $accessToken" } -SkipHttpErrorCheck -ErrorAction SilentlyContinue
                        if ($op.status -eq 'Succeeded') { Write-Host "  LRO Succeeded ($([int](($i+1)*10))s)"; break }
                        if ($op.status -in @('Failed','Cancelled')) { Write-Host "  LRO $($op.status) — will retry POST"; break }
                        Write-Host "  LRO: $($op.status) ($([int](($i+1)*10))s)" -ForegroundColor Gray
                    }
                }
            }
        }
        # Poll up to 90s for the Event Stream to appear in the list
        if (-not $eventstreamId) {
            for ($i = 0; $i -lt 18; $i++) {
                Start-Sleep -Seconds 5
                $eventstreams = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
                $existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1
                if ($existingEs -and $existingEs.id) { $eventstreamId = $existingEs.id; break }
                Write-Host "  Waiting for Event Stream in list... ($([int](($i+1)*5))s, attempt $($esAttempt+1))" -ForegroundColor Gray
            }
        }
    }
    if (-not $eventstreamId) { throw "Event Stream '$EventStreamName' not found after $maxEsAttempts creation attempts" }
    Write-OK "Event Stream created with topology (ID: $eventstreamId)"
    $script:createdEvenstreamId = $eventstreamId
}

Write-Step "4/6" "Event Stream topology configured inline (no separate updateDefinition needed)"
$topoAttempts = 3
for ($topoTry = 0; $topoTry -lt $topoAttempts; $topoTry++) {
    try {
        Wait-EventStreamTopologyReady -WsId $WorkspaceId -EventStreamId $eventstreamId
        break  # topology is ready (or non-fatally timed out)
    } catch {
        if ($_.Exception.Message -match "permanently Failed" -and $topoTry -lt ($topoAttempts - 1)) {
            Write-Host "  Source node permanently Failed — deleting and recreating Event Stream (attempt $($topoTry+2)/$topoAttempts)..." -ForegroundColor Yellow
            try { Invoke-FabricApi -Method DELETE -Url "$FabricApi/workspaces/$WorkspaceId/items/$eventstreamId" | Out-Null } catch {}
            Start-Sleep -Seconds 30
            # Recreate
            $accessToken = az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv
            $esResp2 = Invoke-WebRequest -Uri "$FabricApi/workspaces/$WorkspaceId/eventstreams" -Method POST `
                -Headers @{ Authorization = "Bearer $accessToken"; "Content-Type" = "application/json" } `
                -Body ([System.IO.File]::ReadAllText($esCreateFile)) -SkipHttpErrorCheck
            if ($esResp2.StatusCode -ge 400) { throw "ES recreate failed: $($esResp2.Content)" }
            $esBody2 = $esResp2.Content | ConvertFrom-Json -EA SilentlyContinue
            if ($esBody2 -and $esBody2.id) { $eventstreamId = $esBody2.id }
            else {
                $lroUrl2 = $esResp2.Headers['Location'] | Select-Object -First 1
                if ($lroUrl2) {
                    for ($i = 0; $i -lt 30; $i++) {
                        Start-Sleep -Seconds 10
                        $op2 = Invoke-RestMethod $lroUrl2 -Headers @{ Authorization = "Bearer $accessToken" } -SkipHttpErrorCheck -EA SilentlyContinue
                        if ($op2.status -eq 'Succeeded') { break }
                        if ($op2.status -in @('Failed','Cancelled')) { throw "ES recreate LRO $($op2.status)" }
                    }
                }
                # Poll for the new ES
                for ($i = 0; $i -lt 18; $i++) {
                    Start-Sleep -Seconds 5
                    $eventstreams2 = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
                    $newEs = $eventstreams2.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1
                    if ($newEs -and $newEs.id) { $eventstreamId = $newEs.id; break }
                }
            }
            if (-not $eventstreamId) { throw "Event Stream not found after recreate" }
            Write-OK "Event Stream recreated (ID: $eventstreamId)"
            $script:createdEvenstreamId = $eventstreamId
        } else {
            throw  # re-throw on last attempt or non-retryable error
        }
    }
}

#  Step 5: Retrieve Custom Endpoint connection string 

Write-Step "5/6" "Retrieving Event Stream connection string..."
$esConnectionString = $null
try {
    $csInfo = Get-EventStreamConnectionString -WsId $WorkspaceId -EventStreamId $eventstreamId
    if ($csInfo) {
        Write-Host "  Source ID:   $($csInfo.SourceId)"     -ForegroundColor Gray
        Write-Host "  Namespace:   $($csInfo.Namespace)"     -ForegroundColor Gray
        Write-Host "  EventHub:    $($csInfo.EventHubName)"  -ForegroundColor Gray
        $esConnectionString = $csInfo.PrimaryConnectionString
    }
} catch { Write-Warning "Could not retrieve connection string: $_" }
if ($esConnectionString) { Write-OK "Event Stream connection string retrieved" }
else {
    Write-Warning "Could not retrieve the connection string automatically."
    Write-Host "  Retrieve it from the Fabric portal: Event Stream '$EventStreamName' > Custom Endpoint" -ForegroundColor White
}

if ($OutCsFile -and $esConnectionString) {
    Set-Content -Path $OutCsFile -Value $esConnectionString -Encoding UTF8 -NoNewline
    Write-Host "  Connection string written to: $OutCsFile" -ForegroundColor Gray
}

# ── Optional post-deploy hook ───────────────────────────────────────────

$hookContext = @{
    Source                 = $Source
    SubscriptionId         = $SubscriptionId
    Repo                   = $Repo
    Branch                 = $Branch
    RawBase                = $RawBase
    FabricApi              = $FabricApi
    TempDir                = $TempDir
    WorkspaceId            = $WorkspaceId
    WorkspaceName          = $wsInfo.displayName
    EventhouseId           = $EventhouseId
    EventhouseName         = $ehDetails.displayName
    EventhouseClusterUri   = $ehDetails.properties.queryServiceUri
    DatabaseId             = $databaseId
    DatabaseName           = $DatabaseName
    EventstreamId          = $eventstreamId
    EventstreamName        = $EventStreamName
    ConnectionString       = $esConnectionString
}
Invoke-SourcePostDeployHook -Context $hookContext

#  Summary ─

Write-Host "`n=== Deployment Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Eventhouse: $($ehDetails.displayName)" -ForegroundColor Gray
Write-Host "  KQL Database: $DatabaseName ($databaseId)" -ForegroundColor Gray
Write-Host "  Event Stream: $EventStreamName ($eventstreamId)" -ForegroundColor Gray
Write-Host ""
if ($OutCsFile -and $esConnectionString) {
    Write-Host "  Status: Fabric resources created. Connection string written to $OutCsFile." -ForegroundColor Green
    Write-Host "  Use that connection string to run the feeder of your choice (Docker, ACI, k8s, …)." -ForegroundColor DarkGray
} elseif ($esConnectionString) {
    Write-Host "  Status: Fabric resources created. Use the Event Stream connection string to wire a feeder." -ForegroundColor Green
} else {
    Write-Host "  Status: Fabric resources created. Retrieve connection string from portal." -ForegroundColor Yellow
}
Write-Host ""