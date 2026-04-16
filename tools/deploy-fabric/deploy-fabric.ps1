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
    [string]$Workspace,

    [string]$Eventhouse,

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
if ([string]::IsNullOrWhiteSpace($Eventhouse)) { $Eventhouse = $Source -replace '-', '_' }
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
    $kqlUrl = "$RawBase/$Source/kql/$Source.kql"
    try {
        $null = Invoke-WebRequest -Uri $kqlUrl -Method Head -UseBasicParsing
        Write-OK "KQL script found (alternate name)"
    } catch {
        $kqlUrl = $null
        Write-Info "No KQL script — database schema step will be skipped"
    }
}


# Resolve workspace: accept name or GUID
$guidRx = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
if ($Workspace -match $guidRx) {
    $WorkspaceId = $Workspace
} else {
    $allWs = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces"
    $ws = $allWs.value | Where-Object { $_.displayName -eq $Workspace } | Select-Object -First 1
    if (-not $ws) { throw "Workspace '$Workspace' not found." }
    $WorkspaceId = $ws.id
}
$wsInfo = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId"
$CapacityId = $wsInfo.capacityId
if (-not $CapacityId) { throw "Could not determine capacity ID for workspace '$($wsInfo.displayName)'" }
Write-OK "Workspace: $($wsInfo.displayName) ($WorkspaceId)"

# Resolve eventhouse: accept name, GUID, or blank (auto-create)
$eventhouses = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
if ($Eventhouse -match $guidRx) {
    $EventhouseId = $Eventhouse
    $eventhouse = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
} else {
    $eventhouse = $eventhouses.value | Where-Object { $_.displayName -eq $Eventhouse } | Select-Object -First 1
    if ($eventhouse) {
        $EventhouseId = $eventhouse.id
        $eventhouse = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
    } else {
        Write-Host "  Creating Eventhouse '$Eventhouse'..." -ForegroundColor Yellow
        Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses" -Body @{ displayName = $Eventhouse } | Out-Null
        $EventhouseId = $null
        for ($i = 0; $i -lt 12; $i++) {
            Start-Sleep -Seconds 5
            $eventhouses = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
            $eh = $eventhouses.value | Where-Object { $_.displayName -eq $Eventhouse } | Select-Object -First 1
            if ($eh) { $EventhouseId = $eh.id; break }
            Write-Host "  Waiting for Eventhouse... ($([int](($i+1)*5))s)" -ForegroundColor Gray
        }
        if (-not $EventhouseId) { throw "Failed to create Eventhouse '$Eventhouse'." }
        $eventhouse = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
        Write-OK "Eventhouse created: $($eventhouse.displayName)"
    }
}
Write-OK "Eventhouse: $($eventhouse.displayName) ($EventhouseId)"
$queryUri = $eventhouse.properties.queryServiceUri

#  Step 1: Create KQL database with schema 

Write-Step "1/6" "Setting up KQL database '$DatabaseName'..."

$databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1

$kqlContent = $null
$filteredKql = $null
if ($kqlUrl) {
    $kqlContent = (Invoke-WebRequest -Uri $kqlUrl -UseBasicParsing).Content
    $filteredKql = Convert-KqlForFabricDefinition $kqlContent
}

if ($existingDb) {
    $databaseId = $existingDb.id
    Write-Info "Database already exists (ID: $databaseId)"
    if ($kqlContent) {
        Write-Step "2/6" "Updating KQL schema..."
        try {
            Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName -ScriptContent $kqlContent -Label "$Source.kql"
        } catch {
            Write-Host "  Falling back to Fabric definition API..." -ForegroundColor Yellow
            $schemaBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($filteredKql))
            $dbProps = @{ databaseType = "ReadWrite"; parentEventhouseItemId = $EventhouseId; oneLakeCachingPeriod = "P36500D"; oneLakeStandardStoragePeriod = "P36500D" }
            $dbPropsBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes(($dbProps | ConvertTo-Json -Compress)))
            Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases/$databaseId/updateDefinition" -Body @{ definition = @{ parts = @(
                @{ path = "DatabaseProperties.json"; payload = $dbPropsBase64; payloadType = "InlineBase64" },
                @{ path = "DatabaseSchema.kql"; payload = $schemaBase64; payloadType = "InlineBase64" }
            )}}
            Start-Sleep -Seconds 30
            Write-OK "Schema update submitted"
        }
    } else {
        Write-Step "2/6" "No KQL schema available — skipping"
    }
} else {
    # Create new database — with schema if available, without if not
    $dbProps = @{ databaseType = "ReadWrite"; parentEventhouseItemId = $EventhouseId; oneLakeCachingPeriod = "P36500D"; oneLakeStandardStoragePeriod = "P36500D" }
    $dbPropsBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes(($dbProps | ConvertTo-Json -Compress)))

    if ($filteredKql) {
        $schemaBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($filteredKql))
        $createBody = @{ displayName = $DatabaseName; definition = @{ parts = @(
            @{ path = "DatabaseProperties.json"; payload = $dbPropsBase64; payloadType = "InlineBase64" },
            @{ path = "DatabaseSchema.kql"; payload = $schemaBase64; payloadType = "InlineBase64" }
        )}}
        Write-Host "  Creating database with schema definition..." -ForegroundColor Gray
    } else {
        $createBody = @{ displayName = $DatabaseName; definition = @{ parts = @(
            @{ path = "DatabaseProperties.json"; payload = $dbPropsBase64; payloadType = "InlineBase64" }
        )}}
        Write-Host "  Creating database..." -ForegroundColor Gray
    }

    $createFile = Join-Path $TempDir "kql_create_$(Get-Random).json"
    [System.IO.File]::WriteAllText($createFile, ($createBody | ConvertTo-Json -Depth 10 -Compress), [System.Text.UTF8Encoding]::new($false))
    az rest --method POST --url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases" --resource "https://api.fabric.microsoft.com" --body "@$createFile" --headers "Content-Type=application/json" 2>&1 | Out-Null
    $databaseId = $null
    for ($i = 0; $i -lt 18; $i++) {
        Start-Sleep -Seconds 10
        $databases = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
        $existingDb = $databases.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
        if ($existingDb -and $existingDb.id) { $databaseId = $existingDb.id; break }
        Write-Host "  Provisioning... ($([int](($i+1)*10))s)" -ForegroundColor Gray
    }
    if (-not $databaseId) { throw "Database '$DatabaseName' was not found after 180 seconds." }
    Write-OK "Database created (ID: $databaseId)"
    if ($filteredKql) { Write-Step "2/6" "Schema applied via definition API" }
    else { Write-Step "2/6" "No KQL schema available — skipping" }
}

#  Step 3: Create Fabric Event Stream 

Write-Step "3/6" "Creating Event Stream '$EventStreamName'..."
$eventstreams = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
$existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1
if ($existingEs) {
    $eventstreamId = $existingEs.id
    Write-Info "Event Stream already exists (ID: $eventstreamId)"
} else {
    $esResult = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams" -Body @{ displayName = $EventStreamName }
    if ($esResult -and $esResult.id) { $eventstreamId = $esResult.id }
    else {
        Start-Sleep -Seconds 5
        $eventstreams = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventstreams"
        $existingEs = $eventstreams.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1
        $eventstreamId = $existingEs.id
    }
    Write-OK "Event Stream created (ID: $eventstreamId)"
}

#  Step 4: Configure Event Stream topology ─

Write-Step "4/6" "Configuring Event Stream topology..."
$sourceNodeName = "$Source-input"
$esDef = @{ compatibilityLevel = "1.1"
    sources = @(@{ name = $sourceNodeName; type = "CustomEndpoint"; properties = @{} })
    streams = @(@{ name = $StreamName; type = "DefaultStream"; properties = @{}; inputNodes = @(@{ name = $sourceNodeName }) })
    destinations = @(@{ name = "dispatch-kql"; type = "Eventhouse"; properties = @{
        dataIngestionMode = "ProcessedIngestion"; workspaceId = $WorkspaceId; itemId = $databaseId
        databaseName = $DatabaseName; tableName = "_cloudevents_dispatch"
        inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } }
    }; inputNodes = @(@{ name = $StreamName }) })
}
$esBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes(($esDef | ConvertTo-Json -Depth 20)))
$updateReq = @{ definition = @{ parts = @(@{ path = "eventstream.json"; payload = $esBase64; payloadType = "InlineBase64" }) } }
$updateFile = Join-Path $TempDir "es_update_$(Get-Random).json"
[System.IO.File]::WriteAllText($updateFile, ($updateReq | ConvertTo-Json -Depth 20 -Compress), [System.Text.UTF8Encoding]::new($false))
az rest --method POST --url "$FabricApi/workspaces/$WorkspaceId/eventstreams/$eventstreamId/updateDefinition" --resource "https://api.fabric.microsoft.com" --body "@$updateFile" --headers "Content-Type=application/json" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Failed to update Event Stream definition" }
Write-OK "Event Stream topology configured"

#  Step 5: Retrieve Custom Endpoint connection string 

Write-Step "5/6" "Retrieving Event Stream connection string..."
Start-Sleep -Seconds 5
$esConnectionString = $null
try {
    $cluster = Get-FabricClusterUrl
    $mwc = Get-FabricMwcToken -ClusterUrl $cluster.ClusterUrl -AadToken $cluster.AadToken -WsId $WorkspaceId -CapId $CapacityId -EventStreamId $eventstreamId
    $topologyRaw = az rest --method GET --uri "$FabricApi/workspaces/$WorkspaceId/eventstreams/$eventstreamId/topology" --resource "https://api.fabric.microsoft.com" 2>$null
    if ($topologyRaw) {
        $topology = $topologyRaw | ConvertFrom-Json
        $inputSource = $topology.sources | Where-Object { $_.type -eq "CustomEndpoint" } | Select-Object -First 1
        if ($inputSource) {
            Write-Host "  Datasource ID: $($inputSource.id)" -ForegroundColor Gray
            $esConnectionString = Get-EventStreamConnectionString -WsId $WorkspaceId -CapId $CapacityId -EventStreamId $eventstreamId -DatasourceId $inputSource.id -MwcToken $mwc.Token -TargetUriHost $mwc.TargetUriHost
        }
    }
} catch { Write-Warning "Could not retrieve connection string: $_" }
if ($esConnectionString) { Write-OK "Event Stream connection string retrieved" }
else {
    Write-Warning "Could not retrieve the connection string automatically."
    Write-Host "  Retrieve it from the Fabric portal: Event Stream '$EventStreamName' > Custom Endpoint" -ForegroundColor White
}

#  Step 6: Deploy ACI container ─

if (-not $SkipArm) {
    Write-Step "6/6" "Deploying ACI container..."
    $rgExists = az group exists --name $ResourceGroup 2>&1
    if ($rgExists -eq "false") {
        if (-not $Location) { throw "Resource group '$ResourceGroup' does not exist. Provide -Location to create it." }
        az group create --name $ResourceGroup --location $Location | Out-Null
        Write-OK "Created resource group '$ResourceGroup' in $Location"
    } else {
        if (-not $Location) { $Location = (az group show --name $ResourceGroup --query location -o tsv 2>&1).Trim() }
        Write-OK "Using resource group '$ResourceGroup' in $Location"
    }
    if ($esConnectionString) {
        $containerTemplateUrl = "$RawBase/$Source/azure-template.json"
        az deployment group create --resource-group $ResourceGroup --template-uri $containerTemplateUrl --parameters connectionString="$esConnectionString" containerGroupName=$ContainerGroupName -o none 2>&1 | Out-Null
    } else {
        az deployment group create --resource-group $ResourceGroup --template-uri $templateUrl --parameters containerGroupName=$ContainerGroupName -o none 2>&1 | Out-Null
    }
    if ($LASTEXITCODE -ne 0) { throw "ARM deployment failed" }
    Write-OK "Container deployed: $ContainerGroupName"
} else {
    Write-Step "6/6" "Skipping ARM deployment (--SkipArm)"
}

#  Summary ─

Write-Host "`n=== Deployment Complete ===" -ForegroundColor Cyan
Write-Host ""
if (-not $SkipArm) { Write-Host "  Container: $ContainerGroupName (in $ResourceGroup)" -ForegroundColor Gray }
Write-Host "  Eventhouse: $($eventhouse.displayName)" -ForegroundColor Gray
Write-Host "  KQL Database: $DatabaseName ($databaseId)" -ForegroundColor Gray
Write-Host "  Event Stream: $EventStreamName ($eventstreamId)" -ForegroundColor Gray
Write-Host ""
if ($esConnectionString) { Write-Host "  Status: Bridge is sending data to Fabric Event Stream." -ForegroundColor Green }
else { Write-Host "  Status: Fabric resources created. Retrieve connection string from portal." -ForegroundColor Yellow }
Write-Host ""