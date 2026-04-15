<#
.SYNOPSIS
    Deploys a Real-Time Sources bridge into Azure with Fabric Event Stream
    and KQL database integration.

.DESCRIPTION
    This script is designed to run in Azure Cloud Shell (PowerShell).
    It performs the following steps:

    1. Deploys the ACI + Event Hubs ARM template for a chosen source
    2. Creates (or reuses) a KQL database in an existing Fabric Eventhouse
    3. Applies the source's KQL schema script (_cloudevents_dispatch, typed
       tables, update policies, materialized views)
    4. Creates a Fabric Event Stream with a Custom Endpoint source that
       routes into the KQL database's _cloudevents_dispatch table
    5. Retrieves the Event Hub connection string from the ARM deployment
       and wires it into the Event Stream (via an Event Hub source node)

    Prerequisites:
    - Azure Cloud Shell (PowerShell) with az CLI authenticated
    - An existing Fabric Workspace and Eventhouse
    - Contributor access to an Azure resource group

.PARAMETER Source
    The source directory name (e.g., pegelonline, usgs-earthquakes).

.PARAMETER ResourceGroup
    Azure resource group for ACI and Event Hub deployment.

.PARAMETER Location
    Azure region for deployment. Defaults to the resource group's location.

.PARAMETER WorkspaceId
    Microsoft Fabric workspace ID (GUID).

.PARAMETER EventhouseId
    Microsoft Fabric Eventhouse ID (GUID).

.PARAMETER DatabaseName
    KQL database name. Defaults to the source name.

.PARAMETER SkipArm
    Skip the ARM template deployment (useful if ACI + Event Hubs already exist).

.EXAMPLE
    ./deploy-fabric.ps1 -Source pegelonline -ResourceGroup rg-streams `
        -WorkspaceId "c98acd97-..." -EventhouseId "dbfd2819-..."
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,

    [string]$Location,

    [Parameter(Mandatory = $true)]
    [string]$WorkspaceId,

    [Parameter(Mandatory = $true)]
    [string]$EventhouseId,

    [string]$DatabaseName,

    [switch]$SkipArm
)

$ErrorActionPreference = "Stop"
$Repo = "clemensv/real-time-sources"
$Branch = "main"
$RawBase = "https://raw.githubusercontent.com/$Repo/$Branch"
$FabricApi = "https://api.fabric.microsoft.com/v1"

if (-not $DatabaseName) { $DatabaseName = $Source -replace '-', '_' }
$EventStreamName = "$Source-ingest"
$StreamName = "$EventStreamName-stream"
$ContainerGroupName = $Source

# ── Helpers ──────────────────────────────────────────────────────────────

function Write-Step { param([string]$Step, [string]$Msg)
    Write-Host "`n[$Step] $Msg" -ForegroundColor Yellow
}
function Write-OK { param([string]$Msg)
    Write-Host "  $Msg" -ForegroundColor Green
}
function Write-Info { param([string]$Msg)
    Write-Host "  $Msg" -ForegroundColor DarkYellow
}

function Invoke-FabricApi {
    param(
        [string]$Method,
        [string]$Url,
        [object]$Body
    )
    $azArgs = @("rest", "--method", $Method, "--url", $Url,
                "--resource", "https://api.fabric.microsoft.com")
    if ($Body) {
        $bodyFile = Join-Path $env:TEMP "fabric_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 20 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Fabric API error ($Method $Url): $($result | Out-String)"
    }
    if ($result) { return $result | ConvertFrom-Json }
    return $null
}

function Invoke-KqlScript {
    param(
        [string]$QueryUri,
        [string]$Database,
        [string]$ScriptContent,
        [string]$Label
    )
    Write-Host "  Applying $Label..." -ForegroundColor Yellow
    $body = @{
        csl = ".execute database script <|`n$ScriptContent"
        db  = $Database
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
        throw "KQL script failed for $Label`n$result"
    }
    $parsed = $result | ConvertFrom-Json
    $rows = @()
    if ($parsed.Tables.Count -gt 0) { $rows = $parsed.Tables[0].Rows }
    $failed = @($rows | Where-Object { $_[3] -ne "Completed" })
    if ($failed.Count -gt 0) {
        Write-Warning "Some KQL commands reported non-Completed status for $Label"
        $failed | ForEach-Object { Write-Warning "  $_" }
    }
    Write-OK "Applied $Label"
}

# ── Validate source ─────────────────────────────────────────────────────

Write-Host "=== Real-Time Sources — Fabric Deployment ===" -ForegroundColor Cyan
Write-Host "  Source: $Source" -ForegroundColor White

# Check that required files exist in the repo
$templateUrl = "$RawBase/$Source/azure-template-with-eventhub.json"
$kqlUrl = "$RawBase/$Source/kql/$($Source -replace '-', '_').kql"

Write-Step "0/5" "Validating source assets in repository..."
try {
    $null = Invoke-WebRequest -Uri $templateUrl -Method Head -UseBasicParsing
    Write-OK "ARM template found"
} catch {
    throw "ARM template not found at $templateUrl — is '$Source' a valid source?"
}
try {
    $null = Invoke-WebRequest -Uri $kqlUrl -Method Head -UseBasicParsing
    Write-OK "KQL script found"
} catch {
    # try alternate naming (some sources use hyphens in kql filename)
    $kqlUrl = "$RawBase/$Source/kql/$Source.kql"
    try {
        $null = Invoke-WebRequest -Uri $kqlUrl -Method Head -UseBasicParsing
        Write-OK "KQL script found (alternate name)"
    } catch {
        throw "KQL script not found for '$Source'. Check that $Source/kql/ exists."
    }
}

# ── Step 1: Deploy ARM template ─────────────────────────────────────────

if (-not $SkipArm) {
    Write-Step "1/5" "Deploying ACI + Event Hubs via ARM template..."

    # Ensure resource group exists
    $rgExists = az group exists --name $ResourceGroup 2>&1
    if ($rgExists -eq "false") {
        if (-not $Location) {
            throw "Resource group '$ResourceGroup' does not exist. Provide -Location to create it."
        }
        az group create --name $ResourceGroup --location $Location | Out-Null
        Write-OK "Created resource group '$ResourceGroup' in $Location"
    } else {
        if (-not $Location) {
            $Location = (az group show --name $ResourceGroup --query location -o tsv 2>&1).Trim()
        }
        Write-OK "Using resource group '$ResourceGroup' in $Location"
    }

    $deployResult = az deployment group create `
        --resource-group $ResourceGroup `
        --template-uri $templateUrl `
        --parameters containerGroupName=$ContainerGroupName `
        --query "properties.outputs" `
        -o json 2>&1

    if ($LASTEXITCODE -ne 0) {
        throw "ARM deployment failed:`n$deployResult"
    }

    $outputs = $deployResult | ConvertFrom-Json
    $ehNamespace = $outputs.eventHubNamespaceName.value
    $ehName = $outputs.eventHubName.value
    Write-OK "Deployed: ACI '$ContainerGroupName', Event Hub '$ehNamespace/$ehName'"

    # Retrieve connection string for later use
    $ehConnStr = az eventhubs eventhub authorization-rule keys list `
        --resource-group $ResourceGroup `
        --namespace-name $ehNamespace `
        --eventhub-name $ehName `
        --name "bridge-send-listen" `
        --query "primaryConnectionString" -o tsv 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Could not retrieve Event Hub connection string:`n$ehConnStr"
    }
    Write-OK "Retrieved Event Hub connection string"
} else {
    Write-Step "1/5" "Skipping ARM deployment (--SkipArm)"
    $ehConnStr = $null
}

# ── Step 2: Verify Fabric Eventhouse & create KQL database ──────────────

Write-Step "2/5" "Setting up KQL database '$DatabaseName' in Fabric..."

$eventhouse = Invoke-FabricApi -Method GET `
    -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
Write-OK "Eventhouse: $($eventhouse.displayName)"
$queryUri = $eventhouse.properties.queryServiceUri

$databases = Invoke-FabricApi -Method GET `
    -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1

if ($existingDb) {
    $databaseId = $existingDb.id
    Write-Info "Database already exists (ID: $databaseId)"
} else {
    $dbResult = Invoke-FabricApi -Method POST `
        -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases" `
        -Body @{
            displayName    = $DatabaseName
            creationPayload = @{
                databaseType           = "ReadWrite"
                parentEventhouseItemId = $EventhouseId
            }
        }
    if ($dbResult -and $dbResult.id) {
        $databaseId = $dbResult.id
    } else {
        Start-Sleep -Seconds 5
        $databases = Invoke-FabricApi -Method GET `
            -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
        $existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
        $databaseId = $existingDb.id
    }
    Write-OK "Database created (ID: $databaseId)"
}

# ── Step 3: Apply KQL schema ────────────────────────────────────────────

Write-Step "3/5" "Applying KQL schema from $Source..."

$kqlContent = (Invoke-WebRequest -Uri $kqlUrl -UseBasicParsing).Content
Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName `
    -ScriptContent $kqlContent -Label "$Source.kql"

# ── Step 4: Create Fabric Event Stream ──────────────────────────────────

Write-Step "4/5" "Creating Event Stream '$EventStreamName'..."

$eventstreams = Invoke-FabricApi -Method GET `
    -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
$existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1

if ($existingEs) {
    $eventstreamId = $existingEs.id
    Write-Info "Event Stream already exists (ID: $eventstreamId)"
} else {
    $esResult = Invoke-FabricApi -Method POST `
        -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams" `
        -Body @{ displayName = $EventStreamName }
    if ($esResult -and $esResult.id) {
        $eventstreamId = $esResult.id
    } else {
        Start-Sleep -Seconds 5
        $eventstreams = Invoke-FabricApi -Method GET `
            -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
        $existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1
        $eventstreamId = $existingEs.id
    }
    Write-OK "Event Stream created (ID: $eventstreamId)"
}

# ── Step 5: Configure Event Stream topology ─────────────────────────────

Write-Step "5/5" "Configuring Event Stream topology..."

# Build the Event Stream definition:
# - Source: Event Hub (from the ARM deployment)
# - Stream: default pass-through
# - Destination: Eventhouse _cloudevents_dispatch table
$sourceNodeName = "$Source-input"

$eventstreamDef = @{
    compatibilityLevel = "1.1"
    sources = @(
        @{
            name       = $sourceNodeName
            type       = "CustomEndpoint"
            properties = @{}
        }
    )
    streams = @(
        @{
            name       = $StreamName
            type       = "DefaultStream"
            properties = @{}
            inputNodes = @(
                @{ name = $sourceNodeName }
            )
        }
    )
    destinations = @(
        @{
            name       = "dispatch-kql"
            type       = "Eventhouse"
            properties = @{
                dataIngestionMode  = "ProcessedIngestion"
                workspaceId        = $WorkspaceId
                itemId             = $databaseId
                databaseName       = $DatabaseName
                tableName          = "_cloudevents_dispatch"
                inputSerialization = @{
                    type       = "Json"
                    properties = @{ encoding = "UTF8" }
                }
            }
            inputNodes = @(
                @{ name = $StreamName }
            )
        }
    )
}

$eventstreamJson = $eventstreamDef | ConvertTo-Json -Depth 20
$eventstreamBase64 = [Convert]::ToBase64String(
    [System.Text.Encoding]::UTF8.GetBytes($eventstreamJson)
)
$updateRequest = @{
    definition = @{
        parts = @(
            @{
                path        = "eventstream.json"
                payload     = $eventstreamBase64
                payloadType = "InlineBase64"
            }
        )
    }
}
$updateFile = Join-Path $env:TEMP "es_update_$(Get-Random).json"
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
Write-OK "Event Stream topology configured"

# ── Summary ──────────────────────────────────────────────────────────────

Write-Host "`n=== Deployment Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Azure Resources:" -ForegroundColor White
if (-not $SkipArm) {
    Write-Host "    Container Group:  $ContainerGroupName" -ForegroundColor Gray
    Write-Host "    Event Hub:        $ehNamespace/$ehName" -ForegroundColor Gray
}
Write-Host ""
Write-Host "  Fabric Resources:" -ForegroundColor White
Write-Host "    Eventhouse:       $($eventhouse.displayName)" -ForegroundColor Gray
Write-Host "    KQL Database:     $DatabaseName ($databaseId)" -ForegroundColor Gray
Write-Host "    Event Stream:     $EventStreamName ($eventstreamId)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor Yellow
Write-Host "    1. Open the Event Stream '$EventStreamName' in the Fabric portal" -ForegroundColor White
Write-Host "    2. Copy the Custom Endpoint connection string" -ForegroundColor White
Write-Host "    3. Update the ACI container's CONNECTION_STRING environment variable:" -ForegroundColor White
Write-Host ""
Write-Host "       az container create \" -ForegroundColor DarkGray
Write-Host "         --resource-group $ResourceGroup \" -ForegroundColor DarkGray
Write-Host "         --name $ContainerGroupName \" -ForegroundColor DarkGray
Write-Host "         --environment-variables CONNECTION_STRING='<paste-here>'" -ForegroundColor DarkGray
Write-Host ""
Write-Host "    Alternatively, the ACI container is already running with the Event Hub" -ForegroundColor White
Write-Host "    connection string. You can add an Event Hub source to the Event Stream" -ForegroundColor White
Write-Host "    in the Fabric portal to ingest from the existing Event Hub directly." -ForegroundColor White
Write-Host ""
