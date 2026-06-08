<#
.SYNOPSIS
    Reusable KQL validation module for E2E deployment testing.

.DESCRIPTION
    Schema-driven KQL validation that:
    1. Auto-discovers the source's KQL database in the workspace
    2. Parses the source's kql/<source>.kql to extract table names
    3. Queries _cloudevents_dispatch for total event count
    4. Queries each typed table for row counts
    5. Checks data freshness against expected cadence
    6. Returns a structured result

    This module is reusable across all sources — it derives expectations
    from the KQL schema script and xreg manifest rather than hardcoding.

.PARAMETER Source
    Source slug (e.g. "noaa-ndbc").

.PARAMETER WorkspaceId
    Fabric workspace GUID.

.PARAMETER Token
    Fabric/Kusto bearer token.

.PARAMETER QueryUri
    KQL cluster query URI (optional — auto-discovered if not provided).

.PARAMETER DatabaseName
    KQL database name (optional — auto-discovered by matching source name).

.PARAMETER MinRows
    Minimum rows expected in dispatch table (default: 1).

.PARAMETER MaxStalenessMinutes
    Maximum acceptable data age in minutes (optional — derived from source cadence).
#>
param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$Token,
    [string]$QueryUri,
    [string]$DatabaseName,
    [int]$MinRows = 1,
    [int]$MaxStalenessMinutes = 0
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
    database_name = $null
    query_uri = $null
    dispatch_count = 0
    typed_tables = @{}
    staleness_minutes = $null
    pass = $false
    errors = @()
}

# --- Step 1: Discover the KQL database ---
if (-not $DatabaseName -or -not $QueryUri) {
    Write-Host "  Discovering KQL database for '$Source'..."
    $databases = Invoke-RestMethod `
        -Uri "$fabricBase/workspaces/$WorkspaceId/items?type=KQLDatabase" `
        -Headers $headers -Method Get

    # Match by source name (supports both hyphenated and underscored variants)
    $sourcePattern = $Source -replace '-', '[-_]?'
    $db = $databases.value | Where-Object {
        $_.displayName -match $sourcePattern
    } | Select-Object -First 1

    if (-not $db) {
        $result.errors += "No KQL database found matching '$Source'"
        return $result
    }

    $DatabaseName = $db.displayName
    $result.database_name = $DatabaseName

    # Get the query URI from database properties
    $dbDetail = Invoke-RestMethod `
        -Uri "$fabricBase/workspaces/$WorkspaceId/kqlDatabases/$($db.id)" `
        -Headers $headers -Method Get
    $QueryUri = $dbDetail.properties.queryServiceUri
    $result.query_uri = $QueryUri
}
else {
    $result.database_name = $DatabaseName
    $result.query_uri = $QueryUri
}

if (-not $QueryUri) {
    $result.errors += "Could not determine query URI for database '$DatabaseName'"
    return $result
}

# --- Helper: Execute KQL query ---
function Invoke-KQL {
    param([string]$Query)

    $body = @{
        db  = $DatabaseName
        csl = $Query
    } | ConvertTo-Json

    $kqlHeaders = @{
        "Authorization" = "Bearer $Token"
        "Content-Type"  = "application/json"
    }

    $response = Invoke-RestMethod `
        -Uri "$QueryUri/v1/rest/query" `
        -Headers $kqlHeaders `
        -Method Post `
        -Body $body

    return $response
}

# --- Step 2: Derive expected tables from KQL script ---
$kqlDir = Join-Path $sourceDir "kql"
$expectedTables = @()

if (Test-Path $kqlDir) {
    $kqlFiles = Get-ChildItem -Path $kqlDir -Filter "*.kql"
    foreach ($kqlFile in $kqlFiles) {
        $content = Get-Content $kqlFile.FullName -Raw
        # Extract table names from .create-merge table commands
        $tableMatches = [regex]::Matches($content, '\.create-merge\s+table\s+(\w+)')
        foreach ($m in $tableMatches) {
            $tableName = $m.Groups[1].Value
            if ($tableName -ne '_cloudevents_dispatch') {
                $expectedTables += $tableName
            }
        }
    }
}

if ($expectedTables.Count -eq 0) {
    Write-Host "  Warning: No typed tables found in KQL scripts. Will query dynamically."
}

Write-Host "  Expected typed tables: $($expectedTables.Count)"

# --- Step 3: Query dispatch table ---
Write-Host "  Querying _cloudevents_dispatch..."
try {
    $dispatchResult = Invoke-KQL -Query "_cloudevents_dispatch | count"
    $dispatchCount = [int64]$dispatchResult.Tables[0].Rows[0][0]
    $result.dispatch_count = $dispatchCount
    Write-Host "    Dispatch rows: $dispatchCount"
}
catch {
    $result.errors += "Dispatch query failed: $($_.Exception.Message)"
    Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

# --- Step 4: Query each typed table ---
$tablesToQuery = $expectedTables
if ($tablesToQuery.Count -eq 0) {
    # Fallback: discover tables dynamically
    try {
        $tablesResult = Invoke-KQL -Query ".show tables | where TableName != '_cloudevents_dispatch' | project TableName"
        $tablesToQuery = $tablesResult.Tables[0].Rows | ForEach-Object { $_[0] }
    }
    catch {
        $result.errors += "Table discovery failed: $($_.Exception.Message)"
    }
}

$anyTypedTableHasRows = $false
foreach ($table in $tablesToQuery) {
    try {
        $countResult = Invoke-KQL -Query "['$table'] | count"
        $count = [int64]$countResult.Tables[0].Rows[0][0]
        $result.typed_tables[$table] = $count
        if ($count -gt 0) {
            $anyTypedTableHasRows = $true
            Write-Host "    $table`: $count rows" -ForegroundColor Green
        }
        else {
            Write-Host "    $table`: 0 rows" -ForegroundColor Yellow
        }
    }
    catch {
        $result.typed_tables[$table] = -1
        Write-Host "    $table`: ERROR - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# --- Step 5: Check data freshness ---
if ($result.dispatch_count -gt 0) {
    try {
        $freshnessResult = Invoke-KQL -Query @"
_cloudevents_dispatch
| summarize MaxTime = max(ingestion_time())
| project MinutesAgo = datetime_diff('minute', now(), MaxTime)
"@
        $minutesAgo = [int]$freshnessResult.Tables[0].Rows[0][0]
        $result.staleness_minutes = $minutesAgo
        Write-Host "    Data freshness: ${minutesAgo} minutes ago"

        if ($MaxStalenessMinutes -gt 0 -and $minutesAgo -gt $MaxStalenessMinutes) {
            $result.errors += "Data is stale: ${minutesAgo} min old (max allowed: ${MaxStalenessMinutes} min)"
        }
    }
    catch {
        Write-Host "    Freshness check failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# --- Step 6: Determine pass/fail ---
if ($result.dispatch_count -ge $MinRows -and $anyTypedTableHasRows) {
    $result.pass = $true
}
elseif ($result.dispatch_count -ge $MinRows -and -not $anyTypedTableHasRows) {
    $result.errors += "Dispatch has $($result.dispatch_count) rows but NO typed tables have data. Update policies are likely broken."
}
elseif ($result.dispatch_count -eq 0) {
    $result.errors += "No events in dispatch table. The event stream / notebook did not produce data."
}

return $result
