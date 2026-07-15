<#
.SYNOPSIS
    open-charge-map-specific post-deploy hook: wires the Open Charge Map Fabric
    Map's Kusto-backed layers against a freshly deployed open-charge-map
    Eventhouse database.

.DESCRIPTION
    Auto-invoked by tools/deploy-fabric/deploy-fabric.ps1 (and the notebook
    variant) at the end of a generic deployment via the well-known path
    `<source>/fabric/post-deploy.ps1`. Can also be run standalone for
    re-wiring after a layer/colour/KQL change (e.g. to re-fit the basemap
    bounding box once charging-location data has arrived).

    The generic deployer has already applied `kql/open-charge-map.kql` which
    lays down a CloudEvents-shaped schema whose table and materialized-view
    names are bracket-quoted and dotted (generated `-Qualified -Namespace
    IO.OpenChargeMap`), including:
        - the base table `['IO.OpenChargeMap.ChargingLocation']` (charging
          location identity, WGS84 location, denormalized operator/usage/status
          labels, freshness timestamps and the itemized connections array)
        - the materialized view `['IO.OpenChargeMap.ChargingLocationLatest']`
          (`arg_max(___time, *) by ___type, ___source, ___subject`, one row per
          `poi_id` in its latest state) - the single source for every map layer

    This hook then installs a couple of helper functions in the source's KQL
    DB and wires the following Fabric Map vector layers onto an existing Map
    item (Open Charge Map is a STATIC point feed - charging stations do not
    move - so it is styled like a station network, not moving vehicles):

        1.  Charging locations (bubbles, coloured by operational status, sized
            by `number_of_points`) - on by default
        2.  Labels (operator name / address title, z13+) - on by default
        3.  Usage type (same locations, coloured Public vs Private vs Other) -
            off by default
        4.  Non-operational (`is_operational == false` overlay) - off by default

    When invoked as a hook, the generic deployer passes a -Context hashtable
    containing the IDs created by the bootstrap. The Fabric Map item itself
    is NOT created by the generic deployer (the Fabric REST surface doesn't
    yet expose Map-item creation), so this hook needs the map item id, which
    it reads from the OPEN_CHARGE_MAP_FABRIC_MAP_ID environment variable. If
    that variable is missing the hook auto-creates a blank Map item named
    `open-charge-map-map` (overridable via OPEN_CHARGE_MAP_FABRIC_MAP_NAME) in
    the target workspace using the generic Fabric Items API
    (POST /v1/workspaces/{ws}/items with type=Map). If a Map item with the
    chosen name already exists it is reused.

    Standalone defaults for the ContosoRealTimeTest workspace are baked into
    the parameter block below, so the script can be run with no arguments to
    re-wire that environment. An explicit parameter or a -Context value always
    overrides the baked default (the same $PSBoundParameters precedence
    tfl-cycles uses for -KustoDatabase, extended to all four coordinates).

.PARAMETER Context
    Hashtable provided by the generic deployer. Required keys consumed:
        WorkspaceId, DatabaseId, EventhouseClusterUri, DatabaseName
    Ignored keys: everything else.

.PARAMETER WorkspaceId
    Standalone-mode override. GUID of the Fabric workspace. Defaults to the
    ContosoRealTimeTest workspace.

.PARAMETER MapId
    Standalone-mode override. GUID of the Fabric Map item. Defaults to
    $env:OPEN_CHARGE_MAP_FABRIC_MAP_ID.

.PARAMETER KqlDatabaseId
    Standalone-mode override. GUID of the KQL database with the open-charge-map
    tables. Defaults to the deployed `open_charge_map` database id.

.PARAMETER KustoUri
    Standalone-mode override. Full https URI of the Kusto cluster. Defaults to
    the deployed Eventhouse query URI.

.PARAMETER KustoDatabase
    KQL database name (default: open_charge_map). Must match the name used by
    the generic deployer.

.EXAMPLE
    # Auto-invoked: the user does not run this directly.
    $env:OPEN_CHARGE_MAP_FABRIC_MAP_ID = "<map-guid>"
    ./tools/deploy-fabric/deploy-fabric.ps1 -Source open-charge-map `
        -ResourceGroup rg-ocm -Workspace <ws>

.EXAMPLE
    # Standalone re-wire / re-fit the bbox after data arrives (zero args needed;
    # baked ContosoRealTimeTest defaults are used):
    $env:OPEN_CHARGE_MAP_FABRIC_MAP_ID = "<map-guid>"
    ./post-deploy.ps1
#>
[CmdletBinding()]
param(
    [hashtable] $Context,
    [string]    $WorkspaceId    = "ecdb6d7f-a7b3-4458-9110-f629cfc5a2cb",
    [string]    $MapId          = $env:OPEN_CHARGE_MAP_FABRIC_MAP_ID,
    [string]    $KqlDatabaseId  = "2504feb4-cb5c-422a-a5e1-70675050dbc6",
    [string]    $KustoUri       = "https://trd-dsjrg5phyh6an0x58y.z6.kusto.fabric.microsoft.com",
    [string]    $KustoDatabase  = "open_charge_map"
)

# Reference: Eventhouse `open_charge_map` id 99dcbacc-6c80-4f2e-b56b-42c85345ca60
# (the cluster is reached via the -KustoUri query endpoint above).

$ErrorActionPreference = "Stop"
$workspaceIdBound   = $PSBoundParameters.ContainsKey('WorkspaceId')
$kqlDatabaseIdBound = $PSBoundParameters.ContainsKey('KqlDatabaseId')
$kustoUriBound      = $PSBoundParameters.ContainsKey('KustoUri')
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

# Merge Context (hook invocation) with explicit params (standalone). An explicit
# parameter or a -Context value overrides the baked standalone default; when a
# param was passed explicitly on the command line it wins over -Context.
if ($Context) {
    if (-not $workspaceIdBound   -and $Context.ContainsKey('WorkspaceId'))          { $WorkspaceId   = $Context.WorkspaceId }
    if (-not $kqlDatabaseIdBound -and $Context.ContainsKey('DatabaseId'))           { $KqlDatabaseId = $Context.DatabaseId }
    if (-not $kustoUriBound      -and $Context.ContainsKey('EventhouseClusterUri')) { $KustoUri      = $Context.EventhouseClusterUri }
    if (-not $kustoDatabaseBound -and $Context.ContainsKey('DatabaseName'))         { $KustoDatabase = $Context.DatabaseName }
}

if (-not $MapId) {
    if (-not $WorkspaceId) {
        throw "Cannot auto-create Map item: WorkspaceId not supplied (set -WorkspaceId or pass -Context with WorkspaceId)."
    }
    $mapName = if ($env:OPEN_CHARGE_MAP_FABRIC_MAP_NAME) { $env:OPEN_CHARGE_MAP_FABRIC_MAP_NAME } else { "open-charge-map-map" }
    Write-Host "  [open-charge-map post-deploy] OPEN_CHARGE_MAP_FABRIC_MAP_ID not set; auto-creating Map item '$mapName' in workspace $WorkspaceId..." -ForegroundColor Yellow
    $fabApi = "https://api.fabric.microsoft.com/v1"
    # Reuse if a Map by this name already exists
    $items = az rest --method GET `
        --url "$fabApi/workspaces/$WorkspaceId/items?type=Map" `
        --resource "https://api.fabric.microsoft.com" 2>&1 | ConvertFrom-Json
    $existing = $items.value | Where-Object { $_.displayName -eq $mapName } | Select-Object -First 1
    if ($existing) {
        $MapId = $existing.id
        Write-Host "  [open-charge-map post-deploy] Reusing existing Map '$mapName' (id $MapId)" -ForegroundColor Green
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
        Write-Host "  [open-charge-map post-deploy] Created Map '$mapName' (id $MapId)" -ForegroundColor Green
    }
    $env:OPEN_CHARGE_MAP_FABRIC_MAP_ID = $MapId
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
    Write-Host "  [open-charge-map post-deploy] Acquiring Fabric token via az CLI..."
    $env:FABRIC_TOKEN = (az account get-access-token `
        --resource "https://api.fabric.microsoft.com" `
        --query accessToken -o tsv)
}
if (-not $env:KUSTO_TOKEN) {
    Write-Host "  [open-charge-map post-deploy] Acquiring Kusto token via az CLI..."
    $env:KUSTO_TOKEN = Get-KustoAccessToken -KustoUri $KustoUri
}

$py = if ($env:PYTHON) { $env:PYTHON }
      elseif (Get-Command py -ErrorAction SilentlyContinue) { "py" }
      elseif (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" }
      else { "python" }
$script = Join-Path $PSScriptRoot "wire_open_charge_map_map.py"

& $py $script `
    --workspace-id $WorkspaceId `
    --map-id       $MapId `
    --kql-db-id    $KqlDatabaseId `
    --kusto-uri    $KustoUri `
    --kusto-db     $KustoDatabase
if ($LASTEXITCODE -ne 0) { Write-Warning "wire_open_charge_map_map.py exited with $LASTEXITCODE (map wiring failed but core deployment succeeded)" }