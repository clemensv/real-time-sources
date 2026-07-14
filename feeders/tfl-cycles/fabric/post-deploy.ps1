<#
.SYNOPSIS
    tfl-cycles-specific post-deploy hook: wires the TfL Santander Cycles Fabric
    Map's Kusto-backed layers against a freshly deployed tfl-cycles Eventhouse
    database.

.DESCRIPTION
    Auto-invoked by tools/deploy-fabric/deploy-fabric.ps1 (and the notebook
    variant) at the end of a generic deployment via the well-known path
    `<source>/fabric/post-deploy.ps1`. Can also be run standalone for
    re-wiring after a layer/colour/KQL change (e.g. to re-fit the basemap
    bounding box once station data has arrived).

    The generic deployer has already applied `kql/tfl-cycles.kql` which lays
    down:
        - bracketed CloudEvents tables
          `['UK.Gov.TfL.Cycles.StationInformation']` (station identity +
          location + capacity) and `['UK.Gov.TfL.Cycles.StationStatus']`
          (live bike/dock availability)
        - a `<X>Latest` materialized view over each, keyed by `station_id`

    This hook then installs a couple of helper functions in the source's KQL
    DB and wires the following Fabric Map vector layers onto an existing Map
    item:

        1.  Station availability (bubbles, coloured by bike-availability state,
            sized by capacity) - on by default
        2.  Station labels (name + live counts, z14+) - on by default
        3.  Empty docks (same stations, coloured by empty-dock supply) - off

    When invoked as a hook, the generic deployer passes a -Context hashtable
    containing the IDs created by the bootstrap. The Fabric Map item itself
    is NOT created by the generic deployer (the Fabric REST surface doesn't
    yet expose Map-item creation), so this hook needs the map item id, which
    it reads from the TFL_CYCLES_FABRIC_MAP_ID environment variable. If that
    variable is missing the hook auto-creates a blank Map item named
    `tfl-cycles-map` (overridable via TFL_CYCLES_FABRIC_MAP_NAME) in the
    target workspace using the generic Fabric Items API
    (POST /v1/workspaces/{ws}/items with type=Map). If a Map item with the
    chosen name already exists it is reused.

.PARAMETER Context
    Hashtable provided by the generic deployer. Required keys consumed:
        WorkspaceId, DatabaseId, EventhouseClusterUri, DatabaseName
    Ignored keys: everything else.

.PARAMETER WorkspaceId
    Standalone-mode override. GUID of the Fabric workspace.

.PARAMETER MapId
    Standalone-mode override. GUID of the Fabric Map item. Defaults to
    $env:TFL_CYCLES_FABRIC_MAP_ID.

.PARAMETER KqlDatabaseId
    Standalone-mode override. GUID of the KQL database with the tfl-cycles
    tables.

.PARAMETER KustoUri
    Standalone-mode override. Full https URI of the Kusto cluster.

.PARAMETER KustoDatabase
    KQL database name (default: tfl_cycles). Must match the name used by the
    generic deployer.

.EXAMPLE
    # Auto-invoked: the user does not run this directly.
    $env:TFL_CYCLES_FABRIC_MAP_ID = "<map-guid>"
    ./tools/deploy-fabric/deploy-fabric.ps1 -Source tfl-cycles `
        -ResourceGroup rg-tfl -Workspace <ws>

.EXAMPLE
    # Standalone re-wire / re-fit the bbox after data arrives:
    $env:TFL_CYCLES_FABRIC_MAP_ID = "<map-guid>"
    ./post-deploy.ps1 `
        -WorkspaceId   "<ws-guid>" `
        -KqlDatabaseId "<kqldb-guid>" `
        -KustoUri      "https://trd-xxxxxxxx.z1.kusto.fabric.microsoft.com"
#>
[CmdletBinding()]
param(
    [hashtable] $Context,
    [string]    $WorkspaceId,
    [string]    $MapId          = $env:TFL_CYCLES_FABRIC_MAP_ID,
    [string]    $KqlDatabaseId,
    [string]    $KustoUri,
    [string]    $KustoDatabase  = "tfl_cycles"
)

$ErrorActionPreference = "Stop"
$kustoDatabaseBound = $PSBoundParameters.ContainsKey('KustoDatabase')

function Get-KustoAccessToken {
    param(
        [Parameter(Mandatory = $true)]
        [string]$KustoUri
    )

    $resources = @(
        "https://kusto.kusto.windows.net",
        $KustoUri
    ) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique

    foreach ($resource in $resources) {
        $token = az account get-access-token --resource $resource --query accessToken -o tsv 2>$null
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($token)) {
            return $token.Trim()
        }
    }

    throw "Failed to acquire a Kusto access token for $KustoUri."
}

# Merge Context (hook invocation) with explicit params (standalone).
if ($Context) {
    if (-not $WorkspaceId   -and $Context.ContainsKey('WorkspaceId'))          { $WorkspaceId   = $Context.WorkspaceId }
    if (-not $KqlDatabaseId -and $Context.ContainsKey('DatabaseId'))           { $KqlDatabaseId = $Context.DatabaseId }
    if (-not $KustoUri      -and $Context.ContainsKey('EventhouseClusterUri')) { $KustoUri      = $Context.EventhouseClusterUri }
    if (-not $kustoDatabaseBound -and $Context.ContainsKey('DatabaseName'))    { $KustoDatabase = $Context.DatabaseName }
}

if (-not $MapId) {
    if (-not $WorkspaceId) {
        throw "Cannot auto-create Map item: WorkspaceId not supplied (set -WorkspaceId or pass -Context with WorkspaceId)."
    }
    $mapName = if ($env:TFL_CYCLES_FABRIC_MAP_NAME) { $env:TFL_CYCLES_FABRIC_MAP_NAME } else { "tfl-cycles-map" }
    Write-Host "  [tfl-cycles post-deploy] TFL_CYCLES_FABRIC_MAP_ID not set; auto-creating Map item '$mapName' in workspace $WorkspaceId..." -ForegroundColor Yellow
    $fabApi = "https://api.fabric.microsoft.com/v1"
    # Reuse if a Map by this name already exists
    $items = az rest --method GET `
        --url "$fabApi/workspaces/$WorkspaceId/items?type=Map" `
        --resource "https://api.fabric.microsoft.com" 2>&1 | ConvertFrom-Json
    $existing = $items.value | Where-Object { $_.displayName -eq $mapName } | Select-Object -First 1
    if ($existing) {
        $MapId = $existing.id
        Write-Host "  [tfl-cycles post-deploy] Reusing existing Map '$mapName' (id $MapId)" -ForegroundColor Green
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
        Write-Host "  [tfl-cycles post-deploy] Created Map '$mapName' (id $MapId)" -ForegroundColor Green
    }
    $env:TFL_CYCLES_FABRIC_MAP_ID = $MapId
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
    Write-Host "  [tfl-cycles post-deploy] Acquiring Fabric token via az CLI..."
    $env:FABRIC_TOKEN = (az account get-access-token `
        --resource "https://api.fabric.microsoft.com" `
        --query accessToken -o tsv)
}
if (-not $env:KUSTO_TOKEN) {
    Write-Host "  [tfl-cycles post-deploy] Acquiring Kusto token via az CLI..."
    $env:KUSTO_TOKEN = Get-KustoAccessToken -KustoUri $KustoUri
}

$py = if ($env:PYTHON) { $env:PYTHON }
      elseif (Get-Command py -ErrorAction SilentlyContinue) { "py" }
      elseif (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" }
      else { "python" }
$script = Join-Path $PSScriptRoot "wire_tfl_cycles_map.py"

& $py $script `
    --workspace-id $WorkspaceId `
    --map-id       $MapId `
    --kql-db-id    $KqlDatabaseId `
    --kusto-uri    $KustoUri `
    --kusto-db     $KustoDatabase
if ($LASTEXITCODE -ne 0) { Write-Warning "wire_tfl_cycles_map.py exited with $LASTEXITCODE (map wiring failed but core deployment succeeded)" }
