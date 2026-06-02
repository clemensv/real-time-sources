<#
.SYNOPSIS
    pegelonline-specific post-deploy hook: ingests the per-station river
    polylines into the `RiverSegments` table and wires the 8 Kusto-backed
    river-line layers into an existing Fabric Map item.

.DESCRIPTION
    Auto-invoked by tools/deploy-fabric/deploy-fabric.ps1 (and the notebook
    variant) at the end of a generic deployment via the well-known path
    `<source>/fabric/post-deploy.ps1`. Can also be run standalone for
    re-wiring after a layer/colour/KQL change.

    The generic deployer has already applied `kql/pegelonline.kql` which
    defines all the helper functions consumed by the map
    (StateSegments, NavSegments, TrendBase + TrendSegments{1h,3h,6h,24h},
    FreshSegments, StationLabels). This hook then:

      1. Ingests `river_geometries.kql` (~1900 `.append` commands) into the
         `RiverSegments` table. Throttles via per-command retry on HTTP 429.
      2. Runs `wire_pegelonline_map.py` to (re)create 8 layers:
         hydrological state, navigation state, 1h/3h/6h/24h trend,
         data freshness, station labels.

    When invoked as a hook, the generic deployer passes a -Context hashtable
    containing the IDs created by the bootstrap. The Fabric Map item itself
    is NOT created by the generic deployer (the Fabric REST surface doesn't
    yet expose Map-item creation), so this hook needs the map item id, which
    it reads from the PEGELONLINE_FABRIC_MAP_ID environment variable. If
    that variable is missing the hook auto-creates a blank Map item named
    `pegelonline-map` (overridable via PEGELONLINE_FABRIC_MAP_NAME) in the
    target workspace using the generic Fabric Items API
    (POST /v1/workspaces/{ws}/items with type=Map). If a Map item with the
    chosen name already exists it is reused.

.PARAMETER Context
    Hashtable provided by the generic deployer. Required keys consumed:
        WorkspaceId, DatabaseId, EventhouseClusterUri
    Ignored keys: everything else.
#>
[CmdletBinding()]
param(
    [hashtable] $Context,
    [string]    $WorkspaceId,
    [string]    $MapId          = $env:PEGELONLINE_FABRIC_MAP_ID,
    [string]    $KqlDatabaseId,
    [string]    $KustoUri,
    [string]    $KustoDatabase  = "pegelonline"
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
    $mapName = if ($env:PEGELONLINE_FABRIC_MAP_NAME) { $env:PEGELONLINE_FABRIC_MAP_NAME } else { "pegelonline-map" }
    Write-Host "  [pegelonline post-deploy] PEGELONLINE_FABRIC_MAP_ID not set; auto-creating Map item '$mapName' in workspace $WorkspaceId..." -ForegroundColor Yellow
    $fabApi = "https://api.fabric.microsoft.com/v1"
    # Reuse if a Map by this name already exists
    $items = az rest --method GET `
        --url "$fabApi/workspaces/$WorkspaceId/items?type=Map" `
        --resource "https://api.fabric.microsoft.com" 2>&1 | ConvertFrom-Json
    $existing = $items.value | Where-Object { $_.displayName -eq $mapName } | Select-Object -First 1
    if ($existing) {
        $MapId = $existing.id
        Write-Host "  [pegelonline post-deploy] Reusing existing Map '$mapName' (id $MapId)" -ForegroundColor Green
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
        Write-Host "  [pegelonline post-deploy] Created Map '$mapName' (id $MapId)" -ForegroundColor Green
    }
    $env:PEGELONLINE_FABRIC_MAP_ID = $MapId
}

foreach ($pair in @(
    @('WorkspaceId',   $WorkspaceId),
    @('KqlDatabaseId', $KqlDatabaseId),
    @('KustoUri',      $KustoUri)
)) {
    if (-not $pair[1]) { throw "Missing required value: $($pair[0])" }
}

if (-not $env:FABRIC_TOKEN) {
    Write-Host "  [pegelonline post-deploy] Acquiring Fabric token via az CLI..."
    $env:FABRIC_TOKEN = (az account get-access-token `
        --resource "https://api.fabric.microsoft.com" `
        --query accessToken -o tsv)
}
if (-not $env:KUSTO_TOKEN) {
    Write-Host "  [pegelonline post-deploy] Acquiring Kusto token via az CLI..."
    $env:KUSTO_TOKEN = Get-KustoAccessToken -KustoUri $KustoUri
}

$py = if ($env:PYTHON) { $env:PYTHON } else { "python" }

# ---- Ingest RiverSegments (per-station river polylines) ----
# river_geometries.kql contains exactly 3 commands separated by blank lines:
#   1. .drop table RiverSegments ifexists
#   2. .create table RiverSegments (...)
#   3. .ingest inline into table RiverSegments with (format='multijson') <|
#      <one JSON object per line for ~1900 segments>
# The third command's payload is part of the same command body (everything
# after the `<|`), so a simple split on blank lines is safe: the multijson
# rows do not contain blank lines.
$riverKql = Join-Path $PSScriptRoot "river_geometries.kql"
if (Test-Path $riverKql) {
    Write-Host "  [pegelonline post-deploy] Ingesting RiverSegments from $riverKql ..."
    $src = Get-Content $riverKql -Raw
    $cmds = $src -split "`r?`n`r?`n" | Where-Object { $_.Trim().Length -gt 0 }
    $h = @{ 'Authorization' = "Bearer $($env:KUSTO_TOKEN)"; 'Content-Type' = 'application/json; charset=utf-8' }
    $mgmtUrl = "$KustoUri/v1/rest/mgmt"
    foreach ($c in $cmds) {
        $head = $c.Substring(0, [Math]::Min(80, $c.Length)).Replace("`n", ' ')
        Write-Host "    EXEC: $head ..." -ForegroundColor DarkGray
        $body = (@{ db = $KustoDatabase; csl = $c } | ConvertTo-Json -Compress -Depth 50)
        $tries = 0
        while ($true) {
            $tries++
            try {
                Invoke-RestMethod -Uri $mgmtUrl -Method Post -Headers $h -Body $body -ErrorAction Stop | Out-Null
                break
            } catch {
                if ($tries -lt 4 -and $_.Exception.Message -match '429|TooManyRequests') {
                    Start-Sleep -Milliseconds (500 * $tries)
                } else {
                    throw "RiverSegments command failed: $head`n$($_.Exception.Message)"
                }
            }
        }
    }
    Write-Host "  [pegelonline post-deploy] RiverSegments: $($cmds.Count) commands executed (drop + create + single multijson ingest)."
} else {
    Write-Host "  [pegelonline post-deploy] $riverKql not present; skipping RiverSegments ingest." -ForegroundColor DarkYellow
    Write-Host "  Regenerate via:  python pegelonline/fabric/build_river_geometries.py  (requires MAPS_KEY)" -ForegroundColor DarkYellow
}

$script = Join-Path $PSScriptRoot "wire_pegelonline_map.py"

& $py $script `
    --workspace-id $WorkspaceId `
    --map-id       $MapId `
    --kql-db-id    $KqlDatabaseId `
    --kusto-uri    $KustoUri `
    --kusto-db     $KustoDatabase
if ($LASTEXITCODE -ne 0) { throw "wire_pegelonline_map.py exited with $LASTEXITCODE" }
