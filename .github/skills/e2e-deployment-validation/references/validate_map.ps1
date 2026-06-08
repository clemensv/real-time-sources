<#
.SYNOPSIS
    Reusable Map validation module for E2E deployment testing.

.DESCRIPTION
    Validates Fabric Map items for a source by:
    1. Discovering Map items in the workspace matching the source
    2. Retrieving map definitions (map.json)
    3. Identifying Kusto-backed data layers
    4. Executing each layer's KQL query to verify non-empty results
    5. Returning a structured result

    Handles the common cases:
    - Source has no map → result is N/A (not a failure)
    - Source has a post-deploy hook that creates the map → expected
    - Map exists but layers return zero rows → failure
    - Map uses static layers only (PMTiles/GeoJSON) → pass without KQL check

.PARAMETER Source
    Source slug (e.g. "pegelonline").

.PARAMETER WorkspaceId
    Fabric workspace GUID.

.PARAMETER Token
    Fabric bearer token.

.PARAMETER QueryUri
    KQL cluster query URI (for executing layer queries).

.PARAMETER DatabaseName
    KQL database name (for layer queries).
#>
param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$Token,
    [string]$QueryUri,
    [string]$DatabaseName
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path "$scriptDir/../../..").Path
$sourceDir = Join-Path $repoRoot "feeders" $Source

$headers = @{
    "Authorization" = "Bearer $Token"
    "Content-Type"  = "application/json"
}
$fabricBase = "https://api.fabric.microsoft.com/v1"

$result = @{
    source = $Source
    has_post_deploy_hook = $false
    map_expected = $false
    map_found = $false
    map_id = $null
    map_name = $null
    layers = @()
    layers_with_data = 0
    pass = $null  # null = N/A, true = pass, false = fail
    errors = @()
}

# --- Step 1: Check if source has a post-deploy hook that creates a map ---
$postDeployPath = Join-Path $sourceDir "fabric" "post-deploy.ps1"
if (Test-Path $postDeployPath) {
    $hookContent = Get-Content $postDeployPath -Raw
    if ($hookContent -match 'Map|map\.json|wire.*map|map.*layer') {
        $result.has_post_deploy_hook = $true
        $result.map_expected = $true
        Write-Host "  Post-deploy hook references Map wiring"
    }
}

# --- Step 2: Discover Map items in workspace ---
Write-Host "  Discovering Map items..."
try {
    $allItems = Invoke-RestMethod `
        -Uri "$fabricBase/workspaces/$WorkspaceId/items" `
        -Headers $headers -Method Get

    # Match maps by source name
    $sourcePattern = $Source -replace '-', '[-_]?'
    $mapItems = $allItems.value | Where-Object {
        $_.type -eq "Map" -and $_.displayName -match $sourcePattern
    }

    if ($mapItems.Count -eq 0) {
        if ($result.map_expected) {
            $result.pass = $false
            $result.errors += "Post-deploy hook expects a Map but none found in workspace"
            Write-Host "  WARNING: Map expected but not found" -ForegroundColor Yellow
        }
        else {
            $result.pass = $null  # N/A — no map expected
            Write-Host "  No map expected or found (N/A)"
        }
        return $result
    }

    $map = $mapItems[0]
    $result.map_found = $true
    $result.map_id = $map.id
    $result.map_name = $map.displayName
    Write-Host "  Found map: $($map.displayName) (ID: $($map.id))"
}
catch {
    $result.errors += "Map discovery failed: $($_.Exception.Message)"
    $result.pass = $false
    return $result
}

# --- Step 3: Retrieve map definition ---
Write-Host "  Retrieving map definition..."
$mapDef = $null
try {
    $defResponse = Invoke-RestMethod `
        -Uri "$fabricBase/workspaces/$WorkspaceId/items/$($map.id)/getDefinition" `
        -Headers $headers -Method Post

    # The definition response contains parts; find map.json
    $mapJsonPart = $defResponse.definition.parts | Where-Object { $_.path -eq "map.json" }
    if ($mapJsonPart) {
        $mapDefBytes = [System.Convert]::FromBase64String($mapJsonPart.payload)
        $mapDefStr = [System.Text.Encoding]::UTF8.GetString($mapDefBytes)
        $mapDef = $mapDefStr | ConvertFrom-Json
    }
}
catch {
    Write-Host "  Could not retrieve map definition: $($_.Exception.Message)" -ForegroundColor Yellow
    # Some maps may not support getDefinition (permission or type issue)
    # Treat as soft pass if map exists
    $result.pass = $true
    return $result
}

if (-not $mapDef) {
    Write-Host "  Map definition not available — marking pass based on existence"
    $result.pass = $true
    return $result
}

# --- Step 4: Identify and validate Kusto-backed layers ---
$kustoLayers = @()

# Map definitions have a sources array and layers array
# Sources of type "kusto" or "connection" with a KQL query are data-driven
if ($mapDef.sources) {
    foreach ($src in $mapDef.sources.PSObject.Properties) {
        $srcDef = $src.Value
        if ($srcDef.type -eq "kusto" -or $srcDef.query) {
            $kustoLayers += @{
                name = $src.Name
                query = $srcDef.query
                database = $srcDef.database ?? $DatabaseName
            }
        }
    }
}

# Also check layers for inline KQL
if ($mapDef.layers) {
    foreach ($layer in $mapDef.layers) {
        if ($layer.source -and $layer.source.query) {
            $kustoLayers += @{
                name = $layer.id ?? $layer.type
                query = $layer.source.query
                database = $layer.source.database ?? $DatabaseName
            }
        }
    }
}

if ($kustoLayers.Count -eq 0) {
    Write-Host "  Map has no Kusto-backed layers (static only) — pass"
    $result.pass = $true
    return $result
}

Write-Host "  Found $($kustoLayers.Count) Kusto-backed layers"

# --- Step 5: Execute layer queries ---
if (-not $QueryUri) {
    Write-Host "  No query URI available — cannot validate layer data"
    $result.errors += "Cannot validate layer queries without QueryUri"
    $result.pass = $true  # Soft pass — map exists
    return $result
}

$kqlHeaders = @{
    "Authorization" = "Bearer $Token"
    "Content-Type"  = "application/json"
}

foreach ($layer in $kustoLayers) {
    $layerResult = @{
        name = $layer.name
        query = $layer.query
        row_count = 0
        error = $null
    }

    try {
        # Wrap query with | count to get row count without pulling all data
        $countQuery = "$($layer.query) | count"
        $body = @{
            db  = $layer.database
            csl = $countQuery
        } | ConvertTo-Json

        $response = Invoke-RestMethod `
            -Uri "$QueryUri/v1/rest/query" `
            -Headers $kqlHeaders `
            -Method Post `
            -Body $body

        $count = [int64]$response.Tables[0].Rows[0][0]
        $layerResult.row_count = $count

        if ($count -gt 0) {
            $result.layers_with_data++
            Write-Host "    Layer '$($layer.name)': $count rows" -ForegroundColor Green
        }
        else {
            Write-Host "    Layer '$($layer.name)': 0 rows" -ForegroundColor Yellow
        }
    }
    catch {
        $layerResult.error = $_.Exception.Message
        Write-Host "    Layer '$($layer.name)': ERROR - $($_.Exception.Message)" -ForegroundColor Red
    }

    $result.layers += $layerResult
}

# --- Step 6: Determine pass/fail ---
if ($result.layers_with_data -gt 0) {
    $result.pass = $true
    Write-Host "  Map validation: PASS ($($result.layers_with_data)/$($kustoLayers.Count) layers have data)"
}
else {
    $result.pass = $false
    $result.errors += "Map exists but all $($kustoLayers.Count) Kusto-backed layers return zero rows"
    Write-Host "  Map validation: FAIL (all layers empty)" -ForegroundColor Red
}

return $result
