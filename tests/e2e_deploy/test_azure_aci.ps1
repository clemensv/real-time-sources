<#
.SYNOPSIS
    Runs E2E validation for a single source on Azure (ACI + Event Hubs).

.DESCRIPTION
    1. Creates a temporary resource group
    2. Deploys Event Hubs namespace + hub
    3. Deploys the source's ACI container
    4. Waits for messages on the Event Hub
    5. Validates CloudEvents envelope and schema
    6. Tears down the resource group

.PARAMETER Source
    Source directory name (e.g. "noaa-ndbc").

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

# Validate source has an ARM template
$armTemplate = Join-Path $sourceDir "azure-template.json"
if (-not (Test-Path $armTemplate)) {
    Write-Warning "Source '$Source' has no azure-template.json — skipping Azure test."
    return @{ result = "skip"; reason = "no-arm-template" }
}

# Check for required API keys (source-specific)
$envCheck = & "$scriptDir/check_env_keys.ps1" -Source $Source -Target azure 2>$null
if ($envCheck -and $envCheck.missing) {
    Write-Warning "Source '$Source' missing env keys: $($envCheck.missing -join ', ') — skipping."
    return @{ result = "skip"; reason = "missing-api-keys"; keys = $envCheck.missing }
}

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$rgName = "e2e-$Source-$timestamp"
$ehNamespace = "e2e$($Source -replace '[^a-z0-9]','')$timestamp"
$ehName = $Source -replace '[^a-z0-9-]', ''
$sessionId = Split-Path -Leaf $SessionDir

Write-Host "=== Azure E2E: $Source ===" -ForegroundColor Cyan
Write-Host "Resource Group: $rgName"
Write-Host "Event Hub: $ehNamespace/$ehName"

$result = @{
    source = $Source
    target = "azure"
    result = "fail"
    steps = @{}
    messages_received = 0
    error = $null
}

try {
    # Step 1: Create resource group
    Write-Host "[1/7] Creating resource group..."
    az group create --name $rgName --location $Region --subscription $Subscription --output none
    $result.steps["rg_created"] = $true

    # Step 2: Deploy Event Hubs namespace
    Write-Host "[2/7] Deploying Event Hubs namespace..."
    az eventhubs namespace create `
        --name $ehNamespace `
        --resource-group $rgName `
        --subscription $Subscription `
        --location $Region `
        --sku Standard `
        --capacity 1 `
        --output none
    $result.steps["eh_namespace"] = $true

    # Step 3: Create Event Hub entity
    Write-Host "[3/7] Creating Event Hub entity..."
    az eventhubs eventhub create `
        --name $ehName `
        --namespace-name $ehNamespace `
        --resource-group $rgName `
        --subscription $Subscription `
        --partition-count 2 `
        --output none
    $result.steps["eh_entity"] = $true

    # Step 4: Get connection string
    Write-Host "[4/7] Getting connection string..."
    $connStr = az eventhubs namespace authorization-rule keys list `
        --resource-group $rgName `
        --namespace-name $ehNamespace `
        --name RootManageSharedAccessKey `
        --subscription $Subscription `
        --query primaryConnectionString --output tsv
    $fullConnStr = "$connStr;EntityPath=$ehName"

    # Step 5: Deploy ACI container
    Write-Host "[5/7] Deploying ACI container..."
    $templateParams = @{
        "CONNECTION_STRING" = @{ "value" = $fullConnStr }
    }
    $paramsFile = Join-Path $SessionDir "$Source-azure-params.json"
    @{ "`$schema" = "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#"; contentVersion = "1.0.0.0"; parameters = $templateParams } | ConvertTo-Json -Depth 5 | Set-Content $paramsFile

    az deployment group create `
        --resource-group $rgName `
        --subscription $Subscription `
        --template-file $armTemplate `
        --parameters "@$paramsFile" `
        --output none 2>&1 | ForEach-Object { Write-Host "  $_" }
    $result.steps["aci_deployed"] = $true

    # Step 6: Wait for container to start
    Write-Host "[6/7] Waiting for container to reach Running state..."
    $aciStartTimeout = 120
    $aciStart = Get-Date
    $running = $false
    while (((Get-Date) - $aciStart).TotalSeconds -lt $aciStartTimeout) {
        $containers = az container list --resource-group $rgName --subscription $Subscription --query "[].{name:name,state:instanceView.state}" --output json 2>$null | ConvertFrom-Json
        if ($containers | Where-Object { $_.state -eq "Running" }) {
            $running = $true
            break
        }
        Start-Sleep -Seconds 10
    }
    if (-not $running) {
        throw "ACI container did not reach Running state within ${aciStartTimeout}s"
    }
    $result.steps["aci_running"] = $true

    # Step 7: Consume messages from Event Hub
    Write-Host "[7/7] Consuming messages (timeout: ${TimeoutSeconds}s)..."
    $consumeStart = Get-Date
    $messages = @()

    # Use the Event Hubs SDK via Python to consume
    $consumerScript = @"
import sys, json, time, os
from azure.eventhub import EventHubConsumerClient

conn_str = sys.argv[1]
eh_name = sys.argv[2]
timeout = int(sys.argv[3])
min_msgs = int(sys.argv[4])

messages = []
start = time.time()

def on_event(partition_context, event):
    if event:
        props = {k: str(v) for k, v in (event.properties or {}).items()}
        messages.append({
            "partition": partition_context.partition_id,
            "offset": event.offset,
            "properties": props,
            "body_size": len(event.body_as_str())
        })
    partition_context.update_checkpoint(event)

client = EventHubConsumerClient.from_connection_string(conn_str, consumer_group="`$Default", eventhub_name=eh_name)
try:
    with client:
        while len(messages) < min_msgs and (time.time() - start) < timeout:
            client.receive(on_event=on_event, starting_position="-1", max_wait_time=30)
            if len(messages) >= min_msgs:
                break
except Exception as e:
    print(json.dumps({"error": str(e), "messages": messages}))
    sys.exit(1)

print(json.dumps({"messages": messages, "count": len(messages)}))
"@
    $consumerScriptPath = Join-Path $SessionDir "$Source-consumer.py"
    $consumerScript | Set-Content $consumerScriptPath

    $pyResult = python $consumerScriptPath $fullConnStr $ehName $TimeoutSeconds $MinMessages 2>&1 | Out-String
    $consumeResult = $pyResult | ConvertFrom-Json

    if ($consumeResult.error) {
        throw "Event Hub consumer error: $($consumeResult.error)"
    }

    $result.messages_received = $consumeResult.count
    if ($consumeResult.count -ge $MinMessages) {
        $result.steps["messages_received"] = $true
        $result.result = "pass"
        Write-Host "  Received $($consumeResult.count) messages" -ForegroundColor Green
    }
    else {
        throw "Only received $($consumeResult.count) messages (expected >= $MinMessages)"
    }
}
catch {
    $result.error = $_.Exception.Message
    Write-Host "FAIL: $($_.Exception.Message)" -ForegroundColor Red

    # File issue
    & "$scriptDir/issue_tracker.ps1" `
        -Source $Source `
        -Target azure `
        -ErrorMessage $_.Exception.Message `
        -SessionId $sessionId `
        -Repo "clemensv/real-time-sources"
}
finally {
    # Cleanup: delete the resource group
    Write-Host "Cleaning up resource group $rgName..."
    az group delete --name $rgName --subscription $Subscription --yes --no-wait 2>$null
    $result.steps["rg_deleted"] = $true

    # Remove temp files
    Remove-Item -Path (Join-Path $SessionDir "$Source-azure-params.json") -ErrorAction SilentlyContinue
    Remove-Item -Path (Join-Path $SessionDir "$Source-consumer.py") -ErrorAction SilentlyContinue
}

# Write result
$resultFile = Join-Path $SessionDir "$Source-azure-result.json"
$result | ConvertTo-Json -Depth 5 | Set-Content $resultFile
Write-Host "Result: $($result.result)" -ForegroundColor $(if ($result.result -eq "pass") { "Green" } else { "Red" })

return $result
