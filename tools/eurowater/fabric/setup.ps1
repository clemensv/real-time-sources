<#
.SYNOPSIS
    Sets up the Eurowater Fabric Event Stream and KQL database using the Fabric CLI.

.DESCRIPTION
    Creates:
    1. A KQL database (Eventhouse) with Stations and Measurements tables
    2. A Fabric Event Stream with:
       - Custom input endpoint (returns the connection string for the ACI container group)
       - SQL operator that normalizes all 8 European water service events
       - KQL database output destination

    Prerequisites:
    - Microsoft Fabric CLI (fab) installed: https://learn.microsoft.com/fabric/cli
    - Authenticated: fab login
    - A Fabric workspace created

.PARAMETER WorkspaceName
    The Fabric workspace name.

.PARAMETER EventhouseName
    Name for the KQL Eventhouse. Defaults to 'eurowater'.

.PARAMETER DatabaseName
    Name for the KQL database. Defaults to 'eurowater'.

.PARAMETER EventStreamName
    Name for the Fabric Event Stream. Defaults to 'eurowater-ingest'.

.EXAMPLE
    ./setup.ps1 -WorkspaceName "MyWorkspace"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$WorkspaceName,

    [string]$EventhouseName = "eurowater",
    [string]$DatabaseName = "eurowater",
    [string]$EventStreamName = "eurowater-ingest"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Eurowater Fabric Setup ===" -ForegroundColor Cyan

# ---------------------------------------------------------------------------
# 1. Create KQL Eventhouse and Database
# ---------------------------------------------------------------------------
Write-Host "`n[1/5] Creating KQL Eventhouse '$EventhouseName'..." -ForegroundColor Yellow
fab eventhouse create --workspace $WorkspaceName --name $EventhouseName 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Eventhouse may already exist, continuing..." -ForegroundColor DarkYellow
}

Write-Host "[2/5] Creating KQL Database '$DatabaseName'..." -ForegroundColor Yellow
fab kqldatabase create --workspace $WorkspaceName --eventhouse $EventhouseName --name $DatabaseName 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Database may already exist, continuing..." -ForegroundColor DarkYellow
}

# Run the KQL schema setup script
Write-Host "  Applying KQL schema (tables, mappings, views)..."
$kqlScript = Get-Content -Path (Join-Path $ScriptDir "kql_database.kql") -Raw
fab kqldatabase execute `
    --workspace $WorkspaceName `
    --eventhouse $EventhouseName `
    --database $DatabaseName `
    --script $kqlScript

# ---------------------------------------------------------------------------
# 2. Create Fabric Event Stream
# ---------------------------------------------------------------------------
Write-Host "`n[3/5] Creating Event Stream '$EventStreamName'..." -ForegroundColor Yellow
fab eventstream create --workspace $WorkspaceName --name $EventStreamName 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Event Stream may already exist, continuing..." -ForegroundColor DarkYellow
}

# ---------------------------------------------------------------------------
# 3. Add Custom Input (returns connection string for containers)
# ---------------------------------------------------------------------------
Write-Host "[4/5] Adding custom input endpoint..." -ForegroundColor Yellow
$inputResult = fab eventstream add-source `
    --workspace $WorkspaceName `
    --eventstream $EventStreamName `
    --source-type "custom-endpoint" `
    --name "eurowater-input" `
    --format "json" | ConvertFrom-Json

$connectionString = $inputResult.connectionString
if ($connectionString) {
    Write-Host "  Custom input endpoint created." -ForegroundColor Green
    Write-Host "  Connection String:" -ForegroundColor Green
    Write-Host "  $connectionString" -ForegroundColor White
} else {
    Write-Host "  Custom input endpoint created. Retrieve the connection string from the Fabric portal." -ForegroundColor DarkYellow
}

# ---------------------------------------------------------------------------
# 4. Add SQL Operator for normalization
# ---------------------------------------------------------------------------
Write-Host "`n[5/5] Adding SQL normalization operator..." -ForegroundColor Yellow

$stationsSql = Get-Content -Path (Join-Path $ScriptDir "normalize_stations.sql") -Raw
$measurementsSql = Get-Content -Path (Join-Path $ScriptDir "normalize_measurements.sql") -Raw

# Combine both queries into a single SQL operator
$combinedSql = @"
-- Station normalization
$stationsSql

-- Measurement normalization
$measurementsSql
"@

fab eventstream add-operator `
    --workspace $WorkspaceName `
    --eventstream $EventStreamName `
    --operator-type "sql" `
    --name "normalize" `
    --input "eurowater-input" `
    --query $combinedSql

# ---------------------------------------------------------------------------
# 5. Add KQL Database destination
# ---------------------------------------------------------------------------
Write-Host "  Adding KQL database destination for Stations..." -ForegroundColor Yellow
fab eventstream add-destination `
    --workspace $WorkspaceName `
    --eventstream $EventStreamName `
    --destination-type "kql-database" `
    --name "stations-kql" `
    --input "normalize" `
    --output-name "StationOutput" `
    --eventhouse $EventhouseName `
    --database $DatabaseName `
    --table "Stations" `
    --mapping "StationsMapping" `
    --format "json"

Write-Host "  Adding KQL database destination for Measurements..." -ForegroundColor Yellow
fab eventstream add-destination `
    --workspace $WorkspaceName `
    --eventstream $EventStreamName `
    --destination-type "kql-database" `
    --name "measurements-kql" `
    --input "normalize" `
    --output-name "MeasurementOutput" `
    --eventhouse $EventhouseName `
    --database $DatabaseName `
    --table "Measurements" `
    --mapping "MeasurementsMapping" `
    --format "json"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Resources created in workspace '$WorkspaceName':" -ForegroundColor White
Write-Host "  - Eventhouse:   $EventhouseName" -ForegroundColor White
Write-Host "  - KQL Database: $DatabaseName (tables: Stations, Measurements)" -ForegroundColor White
Write-Host "  - Event Stream: $EventStreamName" -ForegroundColor White
Write-Host "    - Input:      eurowater-input (custom endpoint)" -ForegroundColor White
Write-Host "    - Operator:   normalize (SQL - station & measurement normalization)" -ForegroundColor White
Write-Host "    - Output:     stations-kql, measurements-kql -> KQL database" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Use the connection string above to deploy the ACI container group:" -ForegroundColor White
Write-Host "     ../deploy.ps1 -ResourceGroupName eurowater-rg -ConnectionString '<connection-string>'" -ForegroundColor DarkGray
Write-Host "  2. Or use Docker Compose:" -ForegroundColor White
Write-Host "     CONNECTION_STRING='<connection-string>' docker compose -f ../docker-compose.yml up -d" -ForegroundColor DarkGray
Write-Host ""
