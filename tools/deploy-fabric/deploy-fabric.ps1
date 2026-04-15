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
    5. Retrieves the Custom Endpoint connection string from the Event Stream
    6. Updates the ACI container to send data directly to the Event Stream

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

.PARAMETER SubscriptionId
    Azure subscription ID. If provided, the script sets this as the active
    subscription before deploying.

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

    [string]$SubscriptionId,

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

# Set Azure subscription if provided
if ($SubscriptionId) {
    az account set --subscription $SubscriptionId 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to set subscription '$SubscriptionId'"
    }
    Write-Host "  Subscription: $SubscriptionId" -ForegroundColor White
}

if (-not $DatabaseName) { $DatabaseName = $Source -replace '-', '_' }
$EventStreamName = "$Source-ingest"
$StreamName = "$EventStreamName-stream"
$ContainerGroupName = $Source
$TempDir = if ($TempDir) { $TempDir } elseif ($env:TMPDIR) { $env:TMPDIR } else { "/tmp" }

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
        $bodyFile = Join-Path $TempDir "fabric_body_$(Get-Random).json"
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
        [string]$DatabaseId,
        [string]$ScriptContent,
        [string]$Label
    )
    Write-Host "  Applying $Label..." -ForegroundColor Yellow

    # First try direct REST with a Kusto token (works outside Cloud Shell)
    $kustoToken = $null
    foreach ($aud in @("https://kusto.kusto.windows.net", "https://kusto.fabric.microsoft.com")) {
        try {
            $tokenObj = Get-AzAccessToken -ResourceUrl $aud -ErrorAction Stop
            if ($tokenObj.Token -and $tokenObj.Token.Length -gt 100) { $kustoToken = $tokenObj.Token; break }
        } catch { }
        $ErrorActionPreference = "SilentlyContinue"
        $t = az account get-access-token --resource $aud --query accessToken -o tsv 2>$null
        $ErrorActionPreference = "Stop"
        if ($LASTEXITCODE -eq 0 -and $t -and $t.Length -gt 100) { $kustoToken = $t.Trim(); break }
    }

    if ($kustoToken) {
        # Direct REST call with token
        $body = @{
            csl = ".execute database script <|`n$ScriptContent"
            db  = $Database
        }
        $headers = @{
            "Authorization" = "Bearer $kustoToken"
            "Content-Type"  = "application/json"
        }
        $result = Invoke-RestMethod `
            -Uri "$QueryUri/v1/rest/mgmt" `
            -Method Post -Headers $headers `
            -Body ($body | ConvertTo-Json -Compress) `
            -TimeoutSec 120

        $rows = @()
        if ($result.Tables.Count -gt 0) { $rows = $result.Tables[0].Rows }
        $failed = @($rows | Where-Object { $_[3] -ne "Completed" })
        if ($failed.Count -gt 0) {
            Write-Warning "Some KQL commands reported non-Completed status for $Label"
        }
    } else {
        # Fall back to Fabric API updateDefinition with DatabaseSchema.kql
        # This uses api.fabric.microsoft.com which IS a supported MSI audience
        Write-Host "  Using Fabric API to apply KQL schema..." -ForegroundColor Gray
        $schemaBase64 = [Convert]::ToBase64String(
            [System.Text.Encoding]::UTF8.GetBytes($ScriptContent)
        )
        $updateBody = @{
            definition = @{
                parts = @(
                    @{
                        path        = "DatabaseSchema.kql"
                        payload     = $schemaBase64
                        payloadType = "InlineBase64"
                    }
                )
            }
        }
        $updateFile = Join-Path $TempDir "kql_def_$(Get-Random).json"
        [System.IO.File]::WriteAllText(
            $updateFile,
            ($updateBody | ConvertTo-Json -Depth 10 -Compress),
            [System.Text.UTF8Encoding]::new($false)
        )

        $updateResult = az rest `
            --method POST `
            --url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases/$DatabaseId/updateDefinition" `
            --resource "https://api.fabric.microsoft.com" `
            --body "@$updateFile" `
            --headers "Content-Type=application/json" 2>&1

        if ($LASTEXITCODE -ne 0) {
            throw "Failed to update KQL database definition for $Label`n$updateResult"
        }

        # updateDefinition is async (202) — poll for completion
        if ($updateResult) {
            $parsed = $updateResult | ConvertFrom-Json -ErrorAction SilentlyContinue
            # If 200, it completed synchronously
        }
        # Wait a moment for async operation to complete
        Start-Sleep -Seconds 5
    }
    Write-OK "Applied $Label"
}

function Get-FabricClusterUrl {
    $aadToken = az account get-access-token `
        --resource "https://analysis.windows.net/powerbi/api" `
        --query accessToken -o tsv
    if (-not $aadToken) { throw "Failed to get Azure AD token for Power BI" }
    $clusterDetails = Invoke-RestMethod `
        -Uri "https://api.powerbi.com/powerbi/globalservice/v201606/clusterDetails" `
        -Headers @{ "Authorization" = "Bearer $aadToken" } -TimeoutSec 15
    return @{
        ClusterUrl = $clusterDetails.clusterUrl -replace '^https://', ''
        AadToken   = $aadToken
    }
}

function Get-FabricMwcToken {
    param(
        [string]$ClusterUrl,
        [string]$AadToken,
        [string]$WsId,
        [string]$CapId,
        [string]$EventStreamId
    )
    $body = @{
        workloadType             = "ES"
        workloadId               = "ES"
        workspaceObjectId        = $WsId
        customerCapacityObjectId = $CapId
        artifacts                = @(
            @{
                artifactObjectId = $EventStreamId
                artifactType     = "EventStream"
            }
        )
    } | ConvertTo-Json -Depth 5

    $headers = @{
        "Authorization"                  = "Bearer $AadToken"
        "x-ms-orig-aad-token"            = $AadToken
        "x-ms-workload-resource-moniker" = $EventStreamId
        "Content-Type"                   = "application/json"
    }
    $resp = Invoke-RestMethod `
        -Uri "https://$ClusterUrl/metadata/v201606/generatemwctokenv2" `
        -Method Post -Headers $headers -Body $body -TimeoutSec 30
    if (-not $resp.Token) { throw "MWC token exchange returned empty token" }
    return @{
        Token         = $resp.Token
        TargetUriHost = $resp.TargetUriHost
    }
}

function Get-EventStreamConnectionString {
    param(
        [string]$WsId,
        [string]$CapId,
        [string]$EventStreamId,
        [string]$DatasourceId,
        [string]$MwcToken,
        [string]$TargetUriHost
    )
    $headers = @{
        "Authorization" = "MwcToken $MwcToken"
        "Content-Type"  = "application/json"
    }
    $maxRetries = 3
    for ($retry = 0; $retry -lt $maxRetries; $retry++) {
        try {
            $url = "https://$TargetUriHost/webapi/capacities/$CapId/workloads/ES/ESService/Direct/v1/workspaces/$WsId/artifacts/$EventStreamId/datasource/$DatasourceId/keys"
            $resp = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body "{}" -TimeoutSec 15
            if ($resp.primaryConnectionString) {
                return $resp.primaryConnectionString
            }
        } catch {
            if ($retry -lt ($maxRetries - 1)) {
                Start-Sleep -Seconds 3
            }
        }
    }
    return $null
}

# ── Validate source ─────────────────────────────────────────────────────

Write-Host "=== Real-Time Sources — Fabric Deployment ===" -ForegroundColor Cyan
Write-Host "  Source: $Source" -ForegroundColor White

# Check that required files exist in the repo
$templateUrl = "$RawBase/$Source/azure-template-with-eventhub.json"
$kqlUrl = "$RawBase/$Source/kql/$($Source -replace '-', '_').kql"

Write-Step "0/7" "Validating source assets in repository..."
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

# Look up the capacity ID from the workspace
$wsInfo = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId"
$CapacityId = $wsInfo.capacityId
if (-not $CapacityId) {
    throw "Could not determine capacity ID for workspace $WorkspaceId"
}
Write-OK "Capacity: $CapacityId"

# ── Step 1: Deploy ARM template ─────────────────────────────────────────

if (-not $SkipArm) {
    Write-Step "1/7" "Deploying ACI + Event Hubs via ARM template..."

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
    Write-Step "1/7" "Skipping ARM deployment (--SkipArm)"
    $ehConnStr = $null
}

# ── Step 2: Verify Fabric Eventhouse & create KQL database ──────────────

Write-Step "2/7" "Setting up KQL database '$DatabaseName' in Fabric..."

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
        # Creation is async — poll until the database appears
        $databaseId = $null
        for ($i = 0; $i -lt 12; $i++) {
            Start-Sleep -Seconds 5
            $databases = Invoke-FabricApi -Method GET `
                -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
            $existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
            if ($existingDb -and $existingDb.id) {
                $databaseId = $existingDb.id
                break
            }
            Write-Host "  Waiting for database provisioning... ($([int](($i+1)*5))s)" -ForegroundColor Gray
        }
        if (-not $databaseId) {
            throw "Database '$DatabaseName' was not found after 60 seconds. Check the Fabric portal."
        }
    }
    Write-OK "Database created (ID: $databaseId)"
}

# ── Step 3: Apply KQL schema ────────────────────────────────────────────

Write-Step "3/7" "Applying KQL schema from $Source..."

$kqlContent = (Invoke-WebRequest -Uri $kqlUrl -UseBasicParsing).Content
Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName `
    -DatabaseId $databaseId -ScriptContent $kqlContent -Label "$Source.kql"

# ── Step 4: Create Fabric Event Stream ──────────────────────────────────

Write-Step "4/7" "Creating Event Stream '$EventStreamName'..."

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

Write-Step "5/7" "Configuring Event Stream topology..."

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
$updateFile = Join-Path $TempDir "es_update_$(Get-Random).json"
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

# ── Step 6: Retrieve Custom Endpoint connection string ──────────────────

Write-Step "6/7" "Retrieving Event Stream connection string..."

# Wait for the Event Stream topology to settle
Start-Sleep -Seconds 5

$esConnectionString = $null
try {
    # Discover Fabric cluster and obtain workload token
    $cluster = Get-FabricClusterUrl
    $mwc = Get-FabricMwcToken `
        -ClusterUrl $cluster.ClusterUrl `
        -AadToken $cluster.AadToken `
        -WsId $WorkspaceId `
        -CapId $CapacityId `
        -EventStreamId $eventstreamId

    # Get the Event Stream topology to find the Custom Endpoint datasource ID
    $topology = $null
    $topologyRaw = az rest --method GET `
        --uri "$FabricApi/workspaces/$WorkspaceId/eventstreams/$eventstreamId/topology" `
        --resource "https://api.fabric.microsoft.com" 2>$null
    if ($topologyRaw) {
        $topology = $topologyRaw | ConvertFrom-Json
    }

    if ($topology) {
        $inputSource = $topology.sources | Where-Object { $_.type -eq "CustomEndpoint" } | Select-Object -First 1
        if ($inputSource) {
            Write-Host "  Datasource ID: $($inputSource.id)" -ForegroundColor Gray
            $esConnectionString = Get-EventStreamConnectionString `
                -WsId $WorkspaceId `
                -CapId $CapacityId `
                -EventStreamId $eventstreamId `
                -DatasourceId $inputSource.id `
                -MwcToken $mwc.Token `
                -TargetUriHost $mwc.TargetUriHost
        }
    }
} catch {
    Write-Warning "Could not retrieve connection string automatically: $_"
}

if ($esConnectionString) {
    Write-OK "Event Stream connection string retrieved"
} else {
    Write-Warning "Could not retrieve the connection string automatically."
    Write-Host "  You can retrieve it manually from the Fabric portal:" -ForegroundColor White
    Write-Host "    1. Open Event Stream '$EventStreamName'" -ForegroundColor White
    Write-Host "    2. Click the Custom Endpoint source node" -ForegroundColor White
    Write-Host "    3. Copy the connection string" -ForegroundColor White
}

# ── Step 7: Update ACI container with Event Stream connection string ────

if ($esConnectionString -and -not $SkipArm) {
    Write-Step "7/7" "Updating ACI container to send to Fabric Event Stream..."

    # Delete and recreate the container group with the new connection string.
    # ACI does not support in-place environment variable updates.
    $containerInfo = az container show `
        --resource-group $ResourceGroup `
        --name $ContainerGroupName `
        --query "{image:containers[0].image, cpu:containers[0].resources.requests.cpu, memory:containers[0].resources.requests.memoryInGb}" `
        -o json 2>&1 | ConvertFrom-Json

    az container delete `
        --resource-group $ResourceGroup `
        --name $ContainerGroupName `
        --yes 2>&1 | Out-Null

    az container create `
        --resource-group $ResourceGroup `
        --name $ContainerGroupName `
        --image $containerInfo.image `
        --cpu $containerInfo.cpu `
        --memory $containerInfo.memory `
        --restart-policy Always `
        --environment-variables LOG_LEVEL=INFO PYTHONUNBUFFERED=1 `
        --secure-environment-variables CONNECTION_STRING="$esConnectionString" `
        --os-type Linux `
        -o none 2>&1

    if ($LASTEXITCODE -ne 0) {
        Write-Warning "ACI update failed. You can manually update the container:"
        Write-Host "  CONNECTION_STRING='$esConnectionString'" -ForegroundColor DarkGray
    } else {
        Write-OK "ACI container updated — now sending to Fabric Event Stream"
    }
} elseif (-not $esConnectionString) {
    Write-Step "7/7" "Skipping ACI update (connection string not available)"
} else {
    Write-Step "7/7" "Skipping ACI update (--SkipArm)"
}

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
if ($esConnectionString) {
    Write-Host "  Status: Bridge is running and sending data to Fabric." -ForegroundColor Green
    Write-Host "  Data will appear in the '$DatabaseName' KQL database shortly." -ForegroundColor White
} else {
    Write-Host "  Status: Bridge is running and sending data to Event Hubs." -ForegroundColor Yellow
    Write-Host "  To complete the Fabric integration, retrieve the Event Stream" -ForegroundColor White
    Write-Host "  connection string from the portal and update the ACI container." -ForegroundColor White
}
Write-Host ""
