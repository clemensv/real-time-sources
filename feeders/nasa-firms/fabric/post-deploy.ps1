<#
.SYNOPSIS
    NASA FIRMS Fabric post-deploy hook: applies the additive KQL helper
    functions and caching policies to the live `nasa-firms` KQL database and
    (re)builds the global OSINT Map item against it.

.DESCRIPTION
    Run after the generic feeder deployment (which creates the `nasa-firms`
    Eventhouse / KQL DB and applies `kql/nasa-firms.kql`). This hook then:

      1. Applies `helpers.kql` — additive geometry/reference helper functions
         consumed by the map, plus hot-cache policies for the dashboard window:
           FireColor(frp)            FRP (MW) -> hex heat-ramp colour
           FireRadius(frp)           FRP (MW) -> symbol bubble radius (px)
           ConfidenceRank(level)     low/nominal/high -> 1/2/3
           RecentFireDetections(..)  detections -> GeoJSON Point symbol layer
           FireHeat(..)              detections -> heatmap weight layer
           FireHotspots(..)          detections -> 1-degree grid intensity cells
      2. Runs `build_map.py` — creates/updates the `Map` item
         "NASA FIRMS Global Fire Map" with the hotspot and detection layers.

    All steps are idempotent. Authentication uses the signed-in Azure CLI
    context (`az login`) — Fabric API and Kusto management tokens are acquired
    via `az account get-access-token`.

.PARAMETER Context
    Optional hashtable passed by the generic deployer. Consumed keys:
        WorkspaceId, DatabaseId, EventhouseClusterUri, DatabaseName
#>
[CmdletBinding()]
param(
    [hashtable] $Context,
    [string]    $WorkspaceId   = $env:FABRIC_WORKSPACE_ID,
    [string]    $KqlDatabaseId = $env:FABRIC_KQL_DB_ID,
    [string]    $KustoUri      = $env:FABRIC_KUSTO_URI,
    [string]    $KustoDatabase = "nasa-firms"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Context) {
    if ($Context.ContainsKey('WorkspaceId'))          { $WorkspaceId   = $Context.WorkspaceId }
    if ($Context.ContainsKey('DatabaseId'))           { $KqlDatabaseId = $Context.DatabaseId }
    if ($Context.ContainsKey('EventhouseClusterUri')) { $KustoUri      = $Context.EventhouseClusterUri }
    if ($Context.ContainsKey('DatabaseName'))         { $KustoDatabase = $Context.DatabaseName }
}

foreach ($pair in @{ WorkspaceId = $WorkspaceId; KqlDatabaseId = $KqlDatabaseId; KustoUri = $KustoUri }.GetEnumerator()) {
    if (-not $pair.Value) {
        throw "Missing required value '$($pair.Key)'. Pass -Context or set FABRIC_WORKSPACE_ID / FABRIC_KQL_DB_ID / FABRIC_KUSTO_URI."
    }
}

Write-Host "== NASA FIRMS Fabric post-deploy ==" -ForegroundColor Cyan
Write-Host "   workspace : $WorkspaceId"
Write-Host "   kql db    : $KqlDatabaseId ($KustoDatabase)"
Write-Host "   cluster   : $KustoUri"

# ---------------------------------------------------------------------------
# 1. Apply helpers.kql to the live database (one statement per call). Each
#    top-level statement starts with '.' at column 0 (functions and policies).
# ---------------------------------------------------------------------------
Write-Host "`n[1/2] Applying helpers.kql ..." -ForegroundColor Yellow
$kustoTok = az account get-access-token --resource $KustoUri --query accessToken -o tsv
$mgmt = "$KustoUri/v1/rest/mgmt"
$src  = Get-Content (Join-Path $here "helpers.kql") -Raw
$cmds = [System.Text.RegularExpressions.Regex]::Split($src, "(?m)(?=^\.(create-or-alter function|alter ))") |
        Where-Object { $_.Trim() -like '.*' }
foreach ($c in $cmds) {
    $stmt = $c.Trim()
    if (-not $stmt) { continue }
    $bodyFile = New-TemporaryFile
    (@{ db = $KustoDatabase; csl = $stmt } | ConvertTo-Json -Compress -Depth 20) |
        Set-Content $bodyFile -Encoding utf8
    try {
        Invoke-RestMethod -Uri $mgmt -Method Post -InFile $bodyFile `
            -Headers @{ Authorization = "Bearer $kustoTok"; 'Content-Type' = 'application/json; charset=utf-8' } | Out-Null
        $label = ($stmt -split "`n")[0]
        Write-Host "      applied: $label"
    } finally { Remove-Item $bodyFile -Force }
}

# ---------------------------------------------------------------------------
# 2. Build/refresh the global fire map.
# ---------------------------------------------------------------------------
Write-Host "`n[2/2] Building Map ..." -ForegroundColor Yellow
python (Join-Path $here "build_map.py") --workspace $WorkspaceId --db $KqlDatabaseId

Write-Host "`nDone. Open the NASA FIRMS Global Fire Map from your workspace." -ForegroundColor Green
