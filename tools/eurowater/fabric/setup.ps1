<#
.SYNOPSIS
    Sets up the Eurowater Fabric Event Stream and KQL database using the Fabric REST API.

.DESCRIPTION
    Creates:
    1. A KQL database in an existing Eventhouse with Stations and Measurements tables
    2. A Fabric Event Stream with:
       - Custom input endpoint (retrieve the connection string from the Fabric portal)
       - SQL operator that normalizes all 8 European water service events
       - Eventhouse KQL database output destinations (Stations, Measurements)

    Prerequisites:
    - Azure CLI (az) installed and authenticated: az login
    - Permissions to create items in the Fabric workspace

.PARAMETER WorkspaceId
    The Fabric workspace ID (GUID).

.PARAMETER EventhouseId
    The existing Eventhouse item ID (GUID) to create the database in.

.PARAMETER DatabaseName
    Name for the KQL database. Defaults to 'eurowater'.

.PARAMETER EventStreamName
    Name for the Fabric Event Stream. Defaults to 'eurowater-ingest'.

.EXAMPLE
    ./setup.ps1 -WorkspaceId "c98acd97-4363-4296-8323-b6ab21e53903" -EventhouseId "dbfd2819-2879-4ae7-bff2-95619ad7b8e7"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$WorkspaceId,

    [Parameter(Mandatory = $true)]
    [string]$EventhouseId,

    [string]$DatabaseName = "eurowater",
    [string]$EventStreamName = "eurowater-ingest"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FabricApi = "https://api.fabric.microsoft.com/v1"
$StreamName = "$EventStreamName-stream"

function Invoke-FabricApi {
    param([string]$Method, [string]$Url, [object]$Body)
    $azArgs = @("rest", "--method", $Method, "--url", $Url, "--resource", "https://api.fabric.microsoft.com")
    if ($Body) {
        $bodyFile = Join-Path $env:TEMP "fabric_api_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 10 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        $errorText = $result | Out-String
        if ($errorText -match '"message"\s*:\s*"([^"]+)"') { return $null }
        throw "Fabric API error: $errorText"
    }
    if ($result) { return $result | ConvertFrom-Json }
    return $null
}

Write-Host "=== Eurowater Fabric Setup ===" -ForegroundColor Cyan

# Verify workspace
Write-Host "`nVerifying workspace..." -ForegroundColor Yellow
$workspace = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId"
if (-not $workspace) { throw "Workspace $WorkspaceId not found" }
Write-Host "  Workspace: $($workspace.displayName)" -ForegroundColor Green

# Verify eventhouse
Write-Host "Verifying eventhouse..." -ForegroundColor Yellow
$eventhouse = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
if (-not $eventhouse) { throw "Eventhouse $EventhouseId not found" }
Write-Host "  Eventhouse: $($eventhouse.displayName)" -ForegroundColor Green

$queryUri = $eventhouse.properties.queryServiceUri

# ---------------------------------------------------------------------------
# 1. Create KQL Database
# ---------------------------------------------------------------------------
Write-Host "`n[1/4] Creating KQL Database '$DatabaseName'..." -ForegroundColor Yellow

# Check if database already exists
$databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName }

if ($existingDb) {
    $databaseId = $existingDb.id
    Write-Host "  Database already exists (ID: $databaseId)" -ForegroundColor DarkYellow
} else {
    $dbBody = @{
        displayName = $DatabaseName
        creationPayload = @{
            databaseType = "ReadWrite"
            parentEventhouseItemId = $EventhouseId
        }
    }
    $dbResult = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases" -Body $dbBody
    if ($dbResult) {
        $databaseId = $dbResult.id
    } else {
        Start-Sleep -Seconds 5
        $databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
        $existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName }
        $databaseId = $existingDb.id
    }
    Write-Host "  Database created (ID: $databaseId)" -ForegroundColor Green
}

# Apply KQL schema
Write-Host "  Applying KQL schema (tables, mappings, views)..." -ForegroundColor Yellow
$kqlScript = Get-Content -Path (Join-Path $ScriptDir "kql_database.kql") -Raw
$kqlClean = ($kqlScript -split "`n" | Where-Object { $_ -notmatch '^\s*//' }) -join "`n"
$kqlBody = @{ csl = ".execute database script <|`n$kqlClean"; db = $DatabaseName }
$kqlBodyFile = Join-Path $env:TEMP "kql_schema_body.json"
$kqlBodyJson = $kqlBody | ConvertTo-Json -Compress
[System.IO.File]::WriteAllText($kqlBodyFile, $kqlBodyJson, [System.Text.UTF8Encoding]::new($false))

$schemaResult = az rest --method POST --url "$queryUri/v1/rest/mgmt" --resource $queryUri --body "@$kqlBodyFile" --headers "Content-Type=application/json" 2>&1 | ConvertFrom-Json
$completed = ($schemaResult.Tables[0].Rows | Where-Object { $_[3] -eq 'Completed' }).Count
$failed = ($schemaResult.Tables[0].Rows | Where-Object { $_[3] -ne 'Completed' }).Count
Write-Host "  Schema applied: $completed commands completed, $failed failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })

# ---------------------------------------------------------------------------
# 2. Create Event Stream
# ---------------------------------------------------------------------------
Write-Host "`n[2/4] Creating Event Stream '$EventStreamName'..." -ForegroundColor Yellow

$eventstreams = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
$existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName }

if ($existingEs) {
    $eventstreamId = $existingEs.id
    Write-Host "  Event Stream already exists (ID: $eventstreamId)" -ForegroundColor DarkYellow
} else {
    $esBody = @{ displayName = $EventStreamName }
    $esResult = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams" -Body $esBody
    if ($esResult) {
        $eventstreamId = $esResult.id
    } else {
        Start-Sleep -Seconds 5
        $eventstreams = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
        $existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName }
        $eventstreamId = $existingEs.id
    }
    Write-Host "  Event Stream created (ID: $eventstreamId)" -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# 3. Build and apply Event Stream definition
# ---------------------------------------------------------------------------
Write-Host "`n[3/4] Configuring Event Stream topology..." -ForegroundColor Yellow

# Read and prepare SQL
$stationSql = Get-Content (Join-Path $ScriptDir "normalize_stations.sql") -Raw
$measurementSql = Get-Content (Join-Path $ScriptDir "normalize_measurements.sql") -Raw

$stationSql = $stationSql -replace 'FROM EventInput', "FROM [$StreamName]"
$measurementSql = $measurementSql -replace 'FROM EventInput', "FROM [$StreamName]"

$stationSql = ($stationSql -split "`n" | Where-Object { $_ -notmatch '^\s*--' -and $_.Trim() -ne '' }) -join "`n"
$measurementSql = ($measurementSql -split "`n" | Where-Object { $_ -notmatch '^\s*--' -and $_.Trim() -ne '' }) -join "`n"

$combinedSql = "$stationSql`n`n$measurementSql"

$eventstreamDef = @{
    sources = @(
        @{
            name = "eurowater-input"
            type = "CustomEndpoint"
            properties = @{}
        }
    )
    destinations = @(
        @{
            name = "stations-kql"
            type = "Eventhouse"
            properties = @{
                dataIngestionMode = "ProcessedIngestion"
                workspaceId = $WorkspaceId
                itemId = $databaseId
                databaseName = $DatabaseName
                tableName = "Stations"
                inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } }
            }
            inputNodes = @( @{ name = "StationOutput" } )
        },
        @{
            name = "measurements-kql"
            type = "Eventhouse"
            properties = @{
                dataIngestionMode = "ProcessedIngestion"
                workspaceId = $WorkspaceId
                itemId = $databaseId
                databaseName = $DatabaseName
                tableName = "Measurements"
                inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } }
            }
            inputNodes = @( @{ name = "MeasurementOutput" } )
        }
    )
    streams = @(
        @{
            name = $StreamName
            type = "DefaultStream"
            properties = @{}
            inputNodes = @( @{ name = "eurowater-input" } )
        },
        @{
            name = "StationOutput"
            type = "DerivedStream"
            properties = @{ inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } } }
            inputNodes = @( @{ name = "normalize" } )
        },
        @{
            name = "MeasurementOutput"
            type = "DerivedStream"
            properties = @{ inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } } }
            inputNodes = @( @{ name = "normalize" } )
        }
    )
    operators = @(
        @{
            name = "normalize"
            type = "SQL"
            inputNodes = @( @{ name = $StreamName } )
            properties = @{ query = $combinedSql }
        }
    )
    compatibilityLevel = "1.1"
}

$eventstreamJson = $eventstreamDef | ConvertTo-Json -Depth 10
$eventstreamBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($eventstreamJson))

$updateRequest = @{
    definition = @{
        parts = @(
            @{
                path = "eventstream.json"
                payload = $eventstreamBase64
                payloadType = "InlineBase64"
            }
        )
    }
}

$updateBody = $updateRequest | ConvertTo-Json -Depth 10 -Compress
$updateFile = Join-Path $env:TEMP "es_update_body.json"
[System.IO.File]::WriteAllText($updateFile, $updateBody, [System.Text.UTF8Encoding]::new($false))

$result = az rest --method POST `
    --url "$FabricApi/workspaces/$WorkspaceId/eventstreams/$eventstreamId/updateDefinition" `
    --resource "https://api.fabric.microsoft.com" `
    --body "@$updateFile" `
    --headers "Content-Type=application/json" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "  Error: $result" -ForegroundColor Red
    throw "Failed to update Event Stream definition"
}
Write-Host "  Topology configured:" -ForegroundColor Green
Write-Host "    Source:       eurowater-input (Custom Endpoint)" -ForegroundColor White
Write-Host "    Operator:     normalize (SQL - 8 water services)" -ForegroundColor White
Write-Host "    Destinations: stations-kql, measurements-kql -> $DatabaseName" -ForegroundColor White

# ---------------------------------------------------------------------------
# 4. Summary
# ---------------------------------------------------------------------------
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Resources in workspace '$($workspace.displayName)':" -ForegroundColor White
Write-Host "  - Eventhouse:   $($eventhouse.displayName) ($EventhouseId)" -ForegroundColor White
Write-Host "  - KQL Database: $DatabaseName ($databaseId)" -ForegroundColor White
Write-Host "  - Event Stream: $EventStreamName ($eventstreamId)" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Open the Event Stream in the Fabric portal to get the Custom Endpoint connection string" -ForegroundColor White
Write-Host "  2. Deploy the ACI container group:" -ForegroundColor White
Write-Host "     ../deploy.ps1 -ResourceGroupName eurowater-rg -ConnectionString '<connection-string>'" -ForegroundColor DarkGray
Write-Host "  3. Or use Docker Compose:" -ForegroundColor White
Write-Host "     CONNECTION_STRING='<connection-string>' docker compose -f ../docker-compose.yml up -d" -ForegroundColor DarkGray
Write-Host ""
