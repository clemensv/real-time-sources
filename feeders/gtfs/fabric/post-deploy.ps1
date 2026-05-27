<#
.SYNOPSIS
    gtfs-specific post-deploy hook: wires the GTFS Fabric Map's Kusto-backed
    layers against a freshly deployed GTFS Eventhouse database.

.DESCRIPTION
    Auto-invoked by tools/deploy-fabric/deploy-fabric.ps1 (and the notebook
    variant) at the end of a generic deployment via the well-known path
    `<source>/fabric/post-deploy.ps1`. Can also be run standalone for
    re-wiring after a layer/colour/KQL change.

    The generic deployer has already applied `kql/gtfs.kql` which lays down:
        - bracketed base tables `[Routes]`, `[Stops]`, `[Trips]`, `[Shapes]`,
          `[Alert]`, `[TripUpdate]`, `[VehiclePosition]` (plus the rest of the
          GTFS-Schedule entities)
        - `<X>Latest` materialized views over each
        - derived flat tables `VehiclePositionsFlat` and `TripUpdateFlattened`

    This hook then installs ~15 helper functions in the source's KQL DB and
    wires the following Fabric Map vector layers onto an existing Map item:

        1.  Rail / subway / tram / ferry shapes
        2.  Bus route shapes
        3.  Live vehicles (bubbles, z12-16)
        4.  Live vehicles (oriented rectangles, z16+)
        5.  Major transit hubs
        6.  All stops (stratified to fit Fabric's 100k feature cap)
        7.  Service alerts attached to stops
        8.  Routes with active alerts (severity-coloured overlay)
        9.  Vehicle crowding
        10. Multi-modal stations
        11. Vehicle data freshness grid
        12. Delay heatmap
        13-15. Arrival boards (three zoom-banded variants)

    When invoked as a hook, the generic deployer passes a -Context hashtable
    containing the IDs created by the bootstrap. The Fabric Map item itself
    is NOT created by the generic deployer (the Fabric REST surface doesn't
    yet expose Map-item creation), so this hook needs the map item id, which
    it reads from the GTFS_FABRIC_MAP_ID environment variable. If that
    variable is missing the hook auto-creates a blank Map item named
    `gtfs-map` (overridable via GTFS_FABRIC_MAP_NAME) in the target workspace
    using the generic Fabric Items API (POST /v1/workspaces/{ws}/items with
    type=Map). If a Map item with the chosen name already exists it is reused.

.PARAMETER Context
    Hashtable provided by the generic deployer. Required keys consumed:
        WorkspaceId, DatabaseId, EventhouseClusterUri, DatabaseName
    Ignored keys: everything else.

.PARAMETER WorkspaceId
    Standalone-mode override. GUID of the Fabric workspace.

.PARAMETER MapId
    Standalone-mode override. GUID of the Fabric Map item. Defaults to
    $env:GTFS_FABRIC_MAP_ID.

.PARAMETER KqlDatabaseId
    Standalone-mode override. GUID of the KQL database with the GTFS tables.

.PARAMETER KustoUri
    Standalone-mode override. Full https URI of the Kusto cluster.

.PARAMETER KustoDatabase
    KQL database name (default: gtfs). Must match the name used by the
    generic deployer.

.EXAMPLE
    # Auto-invoked: the user does not run this directly.
    $env:GTFS_FABRIC_MAP_ID = "<map-guid>"
    ./tools/deploy-fabric/deploy-fabric.ps1 -Source gtfs `
        -ResourceGroup rg-gtfs -Workspace <ws>

.EXAMPLE
    # Standalone re-wire after a layer tweak:
    $env:GTFS_FABRIC_MAP_ID = "<map-guid>"
    ./post-deploy.ps1 `
        -WorkspaceId   "<ws-guid>" `
        -KqlDatabaseId "<kqldb-guid>" `
        -KustoUri      "https://trd-xxxxxxxx.z1.kusto.fabric.microsoft.com"
#>
[CmdletBinding()]
param(
    [hashtable] $Context,
    [string]    $WorkspaceId,
    [string]    $MapId          = $env:GTFS_FABRIC_MAP_ID,
    [string]    $KqlDatabaseId,
    [string]    $KustoUri,
    [string]    $KustoDatabase  = "gtfs"
)

$ErrorActionPreference = "Stop"

# Merge Context (hook invocation) with explicit params (standalone).
if ($Context) {
    if (-not $WorkspaceId   -and $Context.ContainsKey('WorkspaceId'))          { $WorkspaceId   = $Context.WorkspaceId }
    if (-not $KqlDatabaseId -and $Context.ContainsKey('DatabaseId'))           { $KqlDatabaseId = $Context.DatabaseId }
    if (-not $KustoUri      -and $Context.ContainsKey('EventhouseClusterUri')) { $KustoUri      = $Context.EventhouseClusterUri }
    if (-not $KustoDatabase -and $Context.ContainsKey('DatabaseName'))         { $KustoDatabase = $Context.DatabaseName }
}

if (-not $MapId) {
    if (-not $WorkspaceId) {
        throw "Cannot auto-create Map item: WorkspaceId not supplied (set -WorkspaceId or pass -Context with WorkspaceId)."
    }
    $mapName = if ($env:GTFS_FABRIC_MAP_NAME) { $env:GTFS_FABRIC_MAP_NAME } else { "gtfs-map" }
    Write-Host "  [gtfs post-deploy] GTFS_FABRIC_MAP_ID not set; auto-creating Map item '$mapName' in workspace $WorkspaceId..." -ForegroundColor Yellow
    $fabApi = "https://api.fabric.microsoft.com/v1"
    # Reuse if a Map by this name already exists
    $items = az rest --method GET `
        --url "$fabApi/workspaces/$WorkspaceId/items?type=Map" `
        --resource "https://api.fabric.microsoft.com" 2>&1 | ConvertFrom-Json
    $existing = $items.value | Where-Object { $_.displayName -eq $mapName } | Select-Object -First 1
    if ($existing) {
        $MapId = $existing.id
        Write-Host "  [gtfs post-deploy] Reusing existing Map '$mapName' (id $MapId)" -ForegroundColor Green
    } else {
        $tmpDir = if ($env:TEMP) { $env:TEMP } else { [System.IO.Path]::GetTempPath() }
        $bodyFile = Join-Path $tmpDir "map_create_$(Get-Random).json"
        (@{ displayName = $mapName; type = "Map" } | ConvertTo-Json -Compress) `
            | Out-File -Encoding utf8 -NoNewline $bodyFile
        $created = az rest --method POST `
            --url "$fabApi/workspaces/$WorkspaceId/items" `
            --resource "https://api.fabric.microsoft.com" `
            --body "@$bodyFile" `
            --headers "Content-Type=application/json" 2>&1 | ConvertFrom-Json
        if (-not $created.id) { throw "Failed to create Map item '$mapName'." }
        $MapId = $created.id
        Write-Host "  [gtfs post-deploy] Created Map '$mapName' (id $MapId)" -ForegroundColor Green
    }
    $env:GTFS_FABRIC_MAP_ID = $MapId
}

foreach ($pair in @(
    @('WorkspaceId',   $WorkspaceId),
    @('KqlDatabaseId', $KqlDatabaseId),
    @('KustoUri',      $KustoUri)
)) {
    if (-not $pair[1]) { throw "Missing required value: $($pair[0])" }
}

# Acquire tokens via az CLI if not provided in the environment.
if (-not $env:FABRIC_TOKEN) {
    Write-Host "  [gtfs post-deploy] Acquiring Fabric token via az CLI..."
    $env:FABRIC_TOKEN = (az account get-access-token `
        --resource "https://api.fabric.microsoft.com" `
        --query accessToken -o tsv)
}
if (-not $env:KUSTO_TOKEN) {
    # The Kusto audience must be the specific cluster URI: the generic
    # https://kusto.fabric.microsoft.com is not a registered AAD resource
    # principal in some tenants (e.g. Microsoft corp).
    Write-Host "  [gtfs post-deploy] Acquiring Kusto token via az CLI..."
    $env:KUSTO_TOKEN = (az account get-access-token `
        --resource $KustoUri `
        --query accessToken -o tsv)
}

$py = if ($env:PYTHON) { $env:PYTHON }
      elseif (Get-Command py -ErrorAction SilentlyContinue) { "py" }
      elseif (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" }
      else { "python" }
$script = Join-Path $PSScriptRoot "wire_gtfs_map.py"

& $py $script `
    --workspace-id $WorkspaceId `
    --map-id       $MapId `
    --kql-db-id    $KqlDatabaseId `
    --kusto-uri    $KustoUri `
    --kusto-db     $KustoDatabase
if ($LASTEXITCODE -ne 0) { throw "wire_gtfs_map.py exited with $LASTEXITCODE" }
