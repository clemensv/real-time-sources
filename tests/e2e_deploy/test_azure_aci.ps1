<#
.SYNOPSIS
    Runs E2E validation for a single source on Azure ACI with a specified transport variant.

.DESCRIPTION
    Supports three broker/transport variants:
      - eventhub: ACI + Event Hubs (Kafka protocol)
      - servicebus: ACI + Service Bus (AMQP 1.0)
      - eventgrid-mqtt: ACI + Event Grid namespace (MQTT v5)

    For each variant:
    1. Creates a temporary resource group
    2. Deploys the source's ARM template (which includes broker + ACI)
    3. Waits for messages on the broker
    4. Validates CloudEvents envelope and schema
    5. Tears down the resource group

.PARAMETER Source
    Source directory name (e.g. "noaa-ndbc").

.PARAMETER Variant
    Transport variant: "eventhub", "servicebus", or "eventgrid-mqtt".

.PARAMETER SessionDir
    Path to the session directory for logging results.

.PARAMETER Subscription
    Azure subscription name or ID.

.PARAMETER Region
    Azure region (default: westeurope).

.PARAMETER TimeoutSeconds
    Max seconds to wait for messages (default: 600).

.PARAMETER MinMessages
    Minimum messages expected (default: 1).
#>
param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][ValidateSet("eventhub","servicebus","eventgrid-mqtt")][string]$Variant,
    [Parameter(Mandatory)][string]$SessionDir,
    [Parameter(Mandatory)][string]$Subscription,
    [string]$Region = "westeurope",
    [int]$TimeoutSeconds = 600,
    [int]$MinMessages = 1
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path "$scriptDir/../..").Path
$sourceDir = Join-Path $repoRoot "feeders" $Source

# Map variant to ARM template filename
$templateMap = @{
    "eventhub"       = "azure-template-with-eventhub.json"
    "servicebus"     = "azure-template-with-servicebus.json"
    "eventgrid-mqtt" = "azure-template-with-eventgrid-mqtt.json"
}
$rgSuffix = @{
    "eventhub"       = "eh"
    "servicebus"     = "sb"
    "eventgrid-mqtt" = "eg"
}

$templateFile = $templateMap[$Variant]
$armTemplate = Join-Path $sourceDir $templateFile

if (-not (Test-Path $armTemplate)) {
    Write-Warning "Source '$Source' has no $templateFile — skipping $Variant test."
    return @{ result = "skip"; reason = "no-arm-template"; variant = $Variant }
}

# Check for required API keys (source-specific)
$envCheck = & "$scriptDir/check_env_keys.ps1" -Source $Source -Target azure 2>$null
if ($envCheck -and $envCheck.missing) {
    Write-Warning "Source '$Source' missing env keys: $($envCheck.missing -join ', ') — skipping."
    return @{ result = "skip"; reason = "missing-api-keys"; keys = $envCheck.missing; variant = $Variant }
}

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$suffix = $rgSuffix[$Variant]
$rgName = "e2e-$Source-$suffix-$timestamp"
$sessionId = Split-Path -Leaf $SessionDir

Write-Host "=== Azure E2E ($Variant): $Source ===" -ForegroundColor Cyan
Write-Host "Resource Group: $rgName"
Write-Host "Template: $templateFile"

$result = @{
    source = $Source
    variant = $Variant
    target = "azure"
    result = "fail"
    steps = @{}
    messages_received = 0
    error = $null
}

try {
    # Step 1: Create resource group
    Write-Host "[1/4] Creating resource group..."
    az group create --name $rgName --location $Region --subscription $Subscription --output none
    $result.steps["rg_created"] = $true

    # Step 2: Deploy ARM template (includes broker + ACI)
    Write-Host "[2/4] Deploying $templateFile..."
    az deployment group create `
        --resource-group $rgName `
        --subscription $Subscription `
        --template-file $armTemplate `
        --output none 2>&1 | ForEach-Object { Write-Host "  $_" }
    $result.steps["deployment_complete"] = $true

    # Step 3: Wait for container to start
    # NOTE: `az container list` may return empty instanceView.state; use `az container show` instead.
    Write-Host "[3/4] Waiting for ACI container to reach Running state..."
    $aciStartTimeout = 180
    $aciStart = Get-Date
    $running = $false
    $containerName = az container list --resource-group $rgName --subscription $Subscription `
        --query "[0].name" --output tsv 2>$null
    while (((Get-Date) - $aciStart).TotalSeconds -lt $aciStartTimeout) {
        if (-not $containerName) {
            $containerName = az container list --resource-group $rgName --subscription $Subscription `
                --query "[0].name" --output tsv 2>$null
        }
        if ($containerName) {
            $state = az container show --resource-group $rgName --name $containerName `
                --subscription $Subscription --query "instanceView.state" --output tsv 2>$null
            if ($state -eq "Running") {
                $running = $true
                break
            }
        }
        Start-Sleep -Seconds 10
    }
    if (-not $running) {
        throw "ACI container did not reach Running state within ${aciStartTimeout}s"
    }
    $result.steps["aci_running"] = $true

    # Step 4: Validate messages on the broker
    Write-Host "[4/4] Validating messages on $Variant broker (timeout: ${TimeoutSeconds}s)..."

    switch ($Variant) {
        "eventhub" {
            # Get the Event Hub connection string from the deployment outputs
            $outputs = az deployment group show --resource-group $rgName --subscription $Subscription `
                --name (Get-ChildItem $armTemplate).BaseName `
                --query "properties.outputs" --output json 2>$null | ConvertFrom-Json
            # Fallback: list Event Hubs namespaces in the RG
            $ehNs = az eventhubs namespace list --resource-group $rgName --subscription $Subscription `
                --query "[0].name" --output tsv
            $ehEntities = az eventhubs eventhub list --resource-group $rgName --namespace-name $ehNs `
                --subscription $Subscription --query "[].name" --output tsv
            $ehName = $ehEntities | Select-Object -First 1
            $connStr = az eventhubs namespace authorization-rule keys list `
                --resource-group $rgName --namespace-name $ehNs `
                --name RootManageSharedAccessKey --subscription $Subscription `
                --query primaryConnectionString --output tsv
            $fullConnStr = "$connStr;EntityPath=$ehName"

            $msgCount = & "$scriptDir/validate_eventhub.ps1" `
                -ConnectionString $fullConnStr `
                -EventHubName $ehName `
                -TimeoutSeconds $TimeoutSeconds `
                -MinMessages $MinMessages `
                -SessionDir $SessionDir `
                -Source $Source
            $result.messages_received = $msgCount
        }
        "servicebus" {
            # Get the Service Bus namespace from the RG
            $sbNs = az servicebus namespace list --resource-group $rgName --subscription $Subscription `
                --query "[0].name" --output tsv
            $sbNsId = az servicebus namespace show --resource-group $rgName --namespace-name $sbNs `
                --subscription $Subscription --query id --output tsv

            # Assign Azure Service Bus Data Receiver to current user — ARM template does not do this.
            # Without this, DefaultAzureCredential gets amqp:unauthorized-access (Listen claim required).
            $myObjectId = az ad signed-in-user show --query id --output tsv
            Write-Host "  Assigning Azure Service Bus Data Receiver to test identity..."
            az role assignment create --assignee $myObjectId --role "Azure Service Bus Data Receiver" `
                --scope $sbNsId --output none --subscription $Subscription
            Start-Sleep -Seconds 30  # allow RBAC propagation

            # Find queues (prefer queue over topic for standard SKU)
            $queues = az servicebus queue list --resource-group $rgName --namespace-name $sbNs `
                --subscription $Subscription --query "[].name" --output tsv
            $entityName = if ($queues) { $queues | Select-Object -First 1 } else {
                az servicebus topic list --resource-group $rgName --namespace-name $sbNs `
                    --subscription $Subscription --query "[0].name" --output tsv
            }

            $msgCount = & "$scriptDir/validate_servicebus.ps1" `
                -FullyQualifiedNamespace "$sbNs.servicebus.windows.net" `
                -EntityName $entityName `
                -EntityType ($(if ($queues) { "queue" } else { "topic" })) `
                -TimeoutSeconds $TimeoutSeconds `
                -MinMessages $MinMessages `
                -SessionDir $SessionDir `
                -Source $Source
            $result.messages_received = $msgCount
        }
        "eventgrid-mqtt" {
            # Get the Event Grid namespace hostname from deployment
            $egNs = az eventgrid namespace list --resource-group $rgName --subscription $Subscription `
                --query "[0]" --output json 2>$null | ConvertFrom-Json
            $mqttHostname = $egNs.topicSpacesConfiguration.hostname

            $msgCount = & "$scriptDir/validate_mqtt.ps1" `
                -Hostname $mqttHostname `
                -ResourceGroup $rgName `
                -Subscription $Subscription `
                -TimeoutSeconds $TimeoutSeconds `
                -MinMessages $MinMessages `
                -SessionDir $SessionDir `
                -Source $Source
            $result.messages_received = $msgCount
        }
    }

    if ($result.messages_received -ge $MinMessages) {
        $result.steps["messages_validated"] = $true
        $result.result = "pass"
        Write-Host "  Received $($result.messages_received) messages" -ForegroundColor Green
    }
    else {
        throw "Only received $($result.messages_received) messages (expected >= $MinMessages)"
    }
}
catch {
    $result.error = $_.Exception.Message
    Write-Host "FAIL: $($_.Exception.Message)" -ForegroundColor Red

    # File issue
    & "$scriptDir/issue_tracker.ps1" `
        -Source $Source `
        -Target "azure-$Variant" `
        -ErrorMessage $_.Exception.Message `
        -SessionId $sessionId `
        -Repo "clemensv/real-time-sources"
}
finally {
    # Cleanup: delete the resource group
    Write-Host "Cleaning up resource group $rgName..."
    az group delete --name $rgName --subscription $Subscription --yes --no-wait 2>$null
    $result.steps["rg_deleted"] = $true
}

# Write result
$resultFile = Join-Path $SessionDir "$Source-azure-$Variant-result.json"
$result | ConvertTo-Json -Depth 5 | Set-Content $resultFile
Write-Host "Result ($Variant): $($result.result)" -ForegroundColor $(if ($result.result -eq "pass") { "Green" } else { "Red" })

return $result
