<#
.SYNOPSIS
    Sets up the Kystverket AIS Fabric Event Stream and KQL database using the Fabric REST API.

.DESCRIPTION
    Creates:
    1. A KQL database in an existing Eventhouse with 5 AIS typed tables,
       materialized views, and analysis functions
    2. A Fabric Event Stream with:
       - Custom input endpoint (retrieve the connection string from the Fabric portal)
       - Direct routing to the _cloudevents_dispatch table
       - KQL update policies split events into typed tables

    Prerequisites:
    - Azure CLI (az) installed and authenticated: az login
    - Permissions to create items in the Fabric workspace

.PARAMETER WorkspaceId
    The Fabric workspace ID (GUID).

.PARAMETER EventhouseId
    The existing Eventhouse item ID (GUID) to create the database in.

.PARAMETER DatabaseName
    Name for the KQL database. Defaults to 'kystverket-ais'.

.PARAMETER EventStreamName
    Name for the Fabric Event Stream. Defaults to 'kystverket-ais-ingest'.

.EXAMPLE
    ./setup.ps1 -WorkspaceId "c98acd97-..." -EventhouseId "dbfd2819-..."
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$WorkspaceId,

    [Parameter(Mandatory = $true)]
    [string]$EventhouseId,

    [string]$DatabaseName = "kystverket-ais",
    [string]$EventStreamName = "kystverket-ais-ingest"
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

Write-Host "=== Kystverket AIS Fabric Setup ===" -ForegroundColor Cyan

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
Write-Host "`n[1/3] Creating KQL Database '$DatabaseName'..." -ForegroundColor Yellow

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
Write-Host "  Applying KQL schema (tables, update policies, views, functions)..." -ForegroundColor Yellow
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
Write-Host "`n[2/3] Creating Event Stream '$EventStreamName'..." -ForegroundColor Yellow

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
Write-Host "`n[3/3] Configuring Event Stream topology..." -ForegroundColor Yellow

# No SQL operator needed — CloudEvents route directly to _cloudevents_dispatch,
# and KQL update policies split events into the 5 typed tables.
$eventstreamDef = @{
    sources = @(
        @{
            name = "ais-input"
            type = "CustomEndpoint"
            properties = @{}
        }
    )
    destinations = @(
        @{
            name = "dispatch-kql"
            type = "Eventhouse"
            properties = @{
                dataIngestionMode = "ProcessedIngestion"
                workspaceId = $WorkspaceId
                itemId = $databaseId
                databaseName = $DatabaseName
                tableName = "_cloudevents_dispatch"
                inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } }
                mappingRuleName = "_cloudevents_dispatch_json"
            }
            inputNodes = @( @{ name = $StreamName } )
        }
    )
    streams = @(
        @{
            name = $StreamName
            type = "DefaultStream"
            properties = @{}
            inputNodes = @( @{ name = "ais-input" } )
        }
    )
    operators = @()
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
Write-Host "    Source:      ais-input (Custom Endpoint)" -ForegroundColor White
Write-Host "    Destination: dispatch-kql -> $DatabaseName._cloudevents_dispatch" -ForegroundColor White
Write-Host "    Routing:     KQL update policies -> 5 typed AIS tables" -ForegroundColor White

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Resources in workspace '$($workspace.displayName)':" -ForegroundColor White
Write-Host "  - Eventhouse:   $($eventhouse.displayName) ($EventhouseId)" -ForegroundColor White
Write-Host "  - KQL Database: $DatabaseName ($databaseId)" -ForegroundColor White
Write-Host "  - Event Stream: $EventStreamName ($eventstreamId)" -ForegroundColor White
Write-Host ""
Write-Host "Tables:" -ForegroundColor White
Write-Host "  - _cloudevents_dispatch  (ingestion target)" -ForegroundColor White
Write-Host "  - PositionReportClassA   (AIS types 1,2,3)" -ForegroundColor White
Write-Host "  - StaticVoyageData       (AIS type 5)" -ForegroundColor White
Write-Host "  - PositionReportClassB   (AIS types 18,19)" -ForegroundColor White
Write-Host "  - StaticDataClassB       (AIS type 24)" -ForegroundColor White
Write-Host "  - AidToNavigation        (AIS type 21)" -ForegroundColor White
Write-Host ""
Write-Host "Materialized views: PositionClassALatest, PositionClassBLatest," -ForegroundColor White
Write-Host "  StaticVoyageDataLatest, StaticDataClassBLatest, AidToNavigationLatest" -ForegroundColor White
Write-Host ""
Write-Host "Functions: VesselPositions(), AISStatistics()" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Open the Event Stream in the Fabric portal to get the Custom Endpoint connection string" -ForegroundColor White
Write-Host "  2. Deploy the container:" -ForegroundColor White
Write-Host "     az container create ... --environment-variables CONNECTION_STRING='<connection-string>'" -ForegroundColor DarkGray
Write-Host "  3. Or use the ARM template:" -ForegroundColor White
Write-Host "     az deployment group create --template-file ../azure-template.json --parameters connectionStringSecret='<cs>'" -ForegroundColor DarkGray
Write-Host "  4. Or run locally:" -ForegroundColor White
Write-Host "     CONNECTION_STRING='<connection-string>' python -m kystverket_ais stream" -ForegroundColor DarkGray
Write-Host ""
