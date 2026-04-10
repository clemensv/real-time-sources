<#
.SYNOPSIS
    Sets up the Puget Sound Fabric Event Stream and KQL database.

.DESCRIPTION
    Creates or updates:
    1. A KQL database in an existing Eventhouse
    2. A raw CloudEvents landing table and typed tables via KQL scripts
    3. A Fabric Event Stream with a Custom Endpoint source and Eventhouse destination
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$WorkspaceId,

    [Parameter(Mandatory = $true)]
    [string]$EventhouseId,

    [string]$DatabaseName = "pugetsound",
    [string]$EventStreamName = "pugetsound-ingest"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ScriptDir))
$FabricApi = "https://api.fabric.microsoft.com/v1"
$StreamName = "$EventStreamName-stream"

function Invoke-FabricApi {
    param(
        [string]$Method,
        [string]$Url,
        [object]$Body
    )

    $azArgs = @("rest", "--method", $Method, "--url", $Url, "--resource", "https://api.fabric.microsoft.com")
    if ($Body) {
        $bodyFile = Join-Path $env:TEMP "fabric_api_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 20 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }

    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Fabric API error: $($result | Out-String)"
    }
    if ($result) {
        return $result | ConvertFrom-Json
    }
    return $null
}

function Invoke-KqlScript {
    param(
        [string]$QueryUri,
        [string]$Database,
        [string]$ScriptPath
    )

    Write-Host "  Applying $(Split-Path -Leaf $ScriptPath)..." -ForegroundColor Yellow
    $scriptText = Get-Content -Path $ScriptPath -Raw
    $body = @{
        csl = ".execute database script <|`n$scriptText"
        db = $Database
    }
    $bodyFile = Join-Path $env:TEMP "kql_body_$(Get-Random).json"
    [System.IO.File]::WriteAllText(
        $bodyFile,
        ($body | ConvertTo-Json -Compress),
        [System.Text.UTF8Encoding]::new($false)
    )

    $result = az rest `
        --method POST `
        --url "$QueryUri/v1/rest/mgmt" `
        --resource $QueryUri `
        --body "@$bodyFile" `
        --headers "Content-Type=application/json" 2>&1

    if ($LASTEXITCODE -ne 0) {
        throw "KQL script failed for $ScriptPath`n$result"
    }

    $parsed = $result | ConvertFrom-Json
    $rows = @()
    if ($parsed.Tables.Count -gt 0) {
        $rows = $parsed.Tables[0].Rows
    }
    $failed = @($rows | Where-Object { $_[3] -ne "Completed" })
    if ($failed.Count -gt 0) {
        throw "KQL script reported failed commands for $ScriptPath"
    }
    Write-Host "    Completed." -ForegroundColor Green
}

Write-Host "=== Puget Sound Fabric Setup ===" -ForegroundColor Cyan

Write-Host "`nVerifying workspace..." -ForegroundColor Yellow
$workspace = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId"
Write-Host "  Workspace: $($workspace.displayName)" -ForegroundColor Green

Write-Host "Verifying eventhouse..." -ForegroundColor Yellow
$eventhouse = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
Write-Host "  Eventhouse: $($eventhouse.displayName)" -ForegroundColor Green

$queryUri = $eventhouse.properties.queryServiceUri

Write-Host "`n[1/3] Creating KQL database '$DatabaseName'..." -ForegroundColor Yellow
$databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1

if ($existingDb) {
    $databaseId = $existingDb.id
    Write-Host "  Database already exists (ID: $databaseId)" -ForegroundColor DarkYellow
} else {
    $dbResult = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases" -Body @{
        displayName = $DatabaseName
        creationPayload = @{
            databaseType = "ReadWrite"
            parentEventhouseItemId = $EventhouseId
        }
    }
    if ($dbResult -and $dbResult.id) {
        $databaseId = $dbResult.id
    } else {
        Start-Sleep -Seconds 5
        $databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
        $existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
        $databaseId = $existingDb.id
    }
    Write-Host "  Database created (ID: $databaseId)" -ForegroundColor Green
}

Write-Host "  Applying KQL assets..." -ForegroundColor Yellow
Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName -ScriptPath (Join-Path $RepoRoot "noaa\kql\noaa.kql")
Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName -ScriptPath (Join-Path $RepoRoot "wsdot\kql\wsdot.kql")
Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName -ScriptPath (Join-Path $ScriptDir "pugetsound.kql")

Write-Host "`n[2/3] Creating Event Stream '$EventStreamName'..." -ForegroundColor Yellow
$eventstreams = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
$existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1

if ($existingEs) {
    $eventstreamId = $existingEs.id
    Write-Host "  Event Stream already exists (ID: $eventstreamId)" -ForegroundColor DarkYellow
} else {
    $esResult = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams" -Body @{ displayName = $EventStreamName }
    if ($esResult) {
        $eventstreamId = $esResult.id
    } else {
        Start-Sleep -Seconds 5
        $eventstreams = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
        $existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1
        $eventstreamId = $existingEs.id
    }
    Write-Host "  Event Stream created (ID: $eventstreamId)" -ForegroundColor Green
}

Write-Host "`n[3/3] Configuring Event Stream topology..." -ForegroundColor Yellow
$eventstreamDef = @{
    sources = @(
        @{
            name = "pugetsound-input"
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
                inputSerialization = @{
                    type = "Json"
                    properties = @{
                        encoding = "UTF8"
                    }
                }
            }
            inputNodes = @(
                @{
                    name = $StreamName
                }
            )
        }
    )
    streams = @(
        @{
            name = $StreamName
            type = "DefaultStream"
            properties = @{}
            inputNodes = @(
                @{
                    name = "pugetsound-input"
                }
            )
        }
    )
    compatibilityLevel = "1.1"
}

$eventstreamJson = $eventstreamDef | ConvertTo-Json -Depth 20
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
$updateFile = Join-Path $env:TEMP "pugetsound_es_update.json"
[System.IO.File]::WriteAllText(
    $updateFile,
    ($updateRequest | ConvertTo-Json -Depth 20 -Compress),
    [System.Text.UTF8Encoding]::new($false)
)

$updateResult = az rest `
    --method POST `
    --url "$FabricApi/workspaces/$WorkspaceId/eventstreams/$eventstreamId/updateDefinition" `
    --resource "https://api.fabric.microsoft.com" `
    --body "@$updateFile" `
    --headers "Content-Type=application/json" 2>&1

if ($LASTEXITCODE -ne 0) {
    throw "Failed to update Event Stream definition`n$updateResult"
}

Write-Host "  Event Stream topology updated." -ForegroundColor Green

Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "  Eventhouse:   $($eventhouse.displayName) ($EventhouseId)" -ForegroundColor White
Write-Host "  KQL Database: $DatabaseName ($databaseId)" -ForegroundColor White
Write-Host "  Event Stream: $EventStreamName ($eventstreamId)" -ForegroundColor White
Write-Host ""
Write-Host "Next step: retrieve the custom endpoint connection string from the Fabric portal and feed it into ..\deploy.ps1 or docker compose." -ForegroundColor Yellow
