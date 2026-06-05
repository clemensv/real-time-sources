<#
.SYNOPSIS
    ENTSO-E Fabric post-deploy hook: applies the shared KQL helper functions
    to the live `entsoe` KQL database and (re)builds the Real-Time Dashboard
    and the Map item against it.

.DESCRIPTION
    Run after the generic feeder deployment (which creates the `entsoe`
    Eventhouse / KQL DB and applies `kql/entsoe.kql`). This hook then:

      1. Applies `helpers.kql` — five reference/geometry helper functions
         consumed by both the dashboard and the map:
           PsrType()           B01..B25 production-type -> fuel/renewable/color
           EICZone()           EIC code  -> zone/country/lat/lon
           PriceColor(price)   €/MWh     -> hex on a green->red ramp
           ZonePriceMarkers()  DayAheadPricesLatest -> GeoJSON price points
           ZoneFlowLines()     CrossBorderPhysicalFlowsLatest -> GeoJSON lines
      2. Runs `build_dashboard.py` — creates/updates the 3-page
         `KQLDashboard` "ENTSO-E European Electricity Market".
      3. Runs `build_map.py` — creates/updates the `Map` item
         "ENTSO-E Market Map" with the flow-line and price-bubble layers.

    All three steps are idempotent. Authentication uses the signed-in Azure
    CLI context (`az login`) — Fabric API and Kusto management tokens are
    acquired via `az account get-access-token`.

.PARAMETER Context
    Optional hashtable passed by the generic deployer. Consumed keys:
        WorkspaceId, DatabaseId, EventhouseClusterUri, DatabaseName
#>
[CmdletBinding()]
param(
    [hashtable] $Context,
    [string]    $WorkspaceId   = "c98acd97-4363-4296-8323-b6ab21e53903",
    [string]    $KqlDatabaseId = "a08303ed-4148-4c4d-b0fd-7ad5eb882e68",
    [string]    $KustoUri      = "https://trd-fssgb36e98qh3fk58u.z2.kusto.fabric.microsoft.com",
    [string]    $KustoDatabase = "entsoe"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Context) {
    if ($Context.ContainsKey('WorkspaceId'))          { $WorkspaceId   = $Context.WorkspaceId }
    if ($Context.ContainsKey('DatabaseId'))           { $KqlDatabaseId = $Context.DatabaseId }
    if ($Context.ContainsKey('EventhouseClusterUri')) { $KustoUri      = $Context.EventhouseClusterUri }
    if ($Context.ContainsKey('DatabaseName'))         { $KustoDatabase = $Context.DatabaseName }
}

Write-Host "== ENTSO-E Fabric post-deploy ==" -ForegroundColor Cyan
Write-Host "   workspace : $WorkspaceId"
Write-Host "   kql db    : $KqlDatabaseId ($KustoDatabase)"
Write-Host "   cluster   : $KustoUri"

# ---------------------------------------------------------------------------
# 1. Apply helpers.kql to the live database (one .create-or-alter per call).
# ---------------------------------------------------------------------------
Write-Host "`n[1/3] Applying helpers.kql ..." -ForegroundColor Yellow
$kustoTok = az account get-access-token --resource $KustoUri --query accessToken -o tsv
$mgmt = "$KustoUri/v1/rest/mgmt"
$src  = Get-Content (Join-Path $here "helpers.kql") -Raw
$cmds = [System.Text.RegularExpressions.Regex]::Split($src, "(?=\.create-or-alter function)") |
        Where-Object { $_.Trim() -like '.create-or-alter*' }
foreach ($c in $cmds) {
    $name = ([regex]::Match($c, '\)\s*([A-Za-z_]+)\s*\(')).Groups[1].Value
    $bodyFile = New-TemporaryFile
    (@{ db = $KustoDatabase; csl = $c.Trim() } | ConvertTo-Json -Compress -Depth 20) |
        Set-Content $bodyFile -Encoding utf8
    try {
        Invoke-RestMethod -Uri $mgmt -Method Post -InFile $bodyFile `
            -Headers @{ Authorization = "Bearer $kustoTok"; 'Content-Type' = 'application/json; charset=utf-8' } | Out-Null
        Write-Host "      applied $name"
    } finally { Remove-Item $bodyFile -Force }
}

# ---------------------------------------------------------------------------
# 2. + 3. Build/refresh the dashboard and the map.
# ---------------------------------------------------------------------------
Write-Host "`n[2/3] Building Real-Time Dashboard ..." -ForegroundColor Yellow
python (Join-Path $here "build_dashboard.py") --workspace $WorkspaceId --db $KqlDatabaseId --cluster $KustoUri

Write-Host "`n[3/3] Building Map ..." -ForegroundColor Yellow
python (Join-Path $here "build_map.py") --workspace $WorkspaceId --db $KqlDatabaseId

Write-Host "`nDone. Open the items from the Real-Time Open Data workspace." -ForegroundColor Green
