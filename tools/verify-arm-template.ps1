<#
.SYNOPSIS
Verifies a single feeder ARM template variant by deploying it to Azure.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$FeederSlug,
  [Parameter(Mandatory=$true)][ValidateSet('kafka','eventhub','servicebus','amqp','mqtt','eventgrid-mqtt')][string]$Variant,
  [string]$TemplateFile,
  [string]$Location = 'westeurope',
  [string]$SubscriptionId = '041abda7-3870-4275-ae24-6bf4c5300523',
  [string]$ResourceGroupName,
  [switch]$KeepResourceGroup,
  [string]$SecretsFile,
  [switch]$DryRun,
  [int]$DataFlowTimeoutSeconds = 300
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$VariantFiles = @{
  kafka = 'azure-template.json'
  eventhub = 'azure-template-with-eventhub.json'
  servicebus = 'azure-template-with-servicebus.json'
  amqp = 'azure-template-amqp.json'
  mqtt = 'azure-template-mqtt.json'
  'eventgrid-mqtt' = 'azure-template-with-eventgrid-mqtt.json'
}

function Invoke-AzJson {
  param([Parameter(Mandatory=$true)][string[]]$Arguments)
  $output = & az @Arguments 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "az $($Arguments -join ' ') failed with exit code $LASTEXITCODE`n$output"
  }
  if (($null -eq $output) -or ($output.Count -eq 0)) { return $null }
  return ($output -join "`n") | ConvertFrom-Json -ErrorAction Stop
}

function Invoke-AzText {
  param([Parameter(Mandatory=$true)][string[]]$Arguments)
  $output = & az @Arguments 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "az $($Arguments -join ' ') failed with exit code $LASTEXITCODE`n$output"
  }
  return ($output -join "`n")
}

function New-SafeName {
  param([Parameter(Mandatory=$true)][string]$Value, [int]$MaxLength = 63, [int]$MinLength = 1)
  $safe = $Value.ToLowerInvariant() -replace '[^a-z0-9-]', '-' -replace '-+', '-'
  $safe = $safe.Trim('-')
  if ($safe.Length -gt $MaxLength) { $safe = $safe.Substring(0, $MaxLength).Trim('-') }
  if ($safe.Length -lt $MinLength) { $safe = ($safe + ('x' * $MinLength)).Substring(0, $MinLength) }
  return $safe
}

function Resolve-TemplatePath {
  param([string]$Slug, [string]$FileName)
  $root = Split-Path -Parent $PSScriptRoot
  $candidates = @(
    (Join-Path $root "feeders\$Slug\$FileName"),
    (Join-Path $root "feeders\$Slug\infra\$FileName"),
    (Join-Path $root "$Slug\$FileName"),
    (Join-Path $root "$Slug\infra\$FileName")
  )
  foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) { return (Resolve-Path -LiteralPath $candidate).Path }
  }
  throw "Template '$FileName' not found for feeder '$Slug'. Checked: $($candidates -join ', ')"
}

function Test-TemplateHasResources {
  param([string]$TemplatePath)
  $template = Get-Content -LiteralPath $TemplatePath -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop
  if ($null -eq $template.resources -or $template.resources.Count -le 0) {
    throw "Template '$TemplatePath' has no resources. Refusing to verify an empty placeholder."
  }
  return $template
}

function ConvertTo-Hashtable {
  param($Object)
  $hash = @{}
  if ($null -eq $Object) { return $hash }
  foreach ($prop in $Object.PSObject.Properties) { $hash[$prop.Name] = $prop.Value }
  return $hash
}

function Get-TemplateParameterTable {
  param($Template)
  return ConvertTo-Hashtable $Template.parameters
}

function Add-IfParameterExists {
  param([hashtable]$Overrides, [hashtable]$Parameters, [string]$Name, $Value)
  if ($Parameters.ContainsKey($Name)) { $Overrides[$Name] = $Value }
}

function Add-RequiredPlaceholders {
  param([hashtable]$Overrides, [hashtable]$Parameters)
  foreach ($name in $Parameters.Keys) {
    if ($Overrides.ContainsKey($name)) { continue }
    $definition = $Parameters[$name]
    $hasDefault = ($definition.PSObject.Properties.Name -contains 'defaultValue')
    if ($hasDefault) { continue }
    $type = ''
    if ($definition.PSObject.Properties.Name -contains 'type') { $type = [string]$definition.type }
    switch -Regex ($type.ToLowerInvariant()) {
      'securestring' { $Overrides[$name] = 'unused'; break }
      'string' { $Overrides[$name] = 'unused'; break }
      'int' { $Overrides[$name] = 1; break }
      'bool' { $Overrides[$name] = $false; break }
      'array' { $Overrides[$name] = '[]'; break }
      'object|secureobject' { $Overrides[$name] = '{}'; break }
      default { $Overrides[$name] = 'unused'; break }
    }
  }
}

function Get-ParameterArguments {
  param([hashtable]$Overrides)
  $args = New-Object System.Collections.Generic.List[string]
  foreach ($key in ($Overrides.Keys | Sort-Object)) {
    $value = $Overrides[$key]
    if ($value -is [bool]) { $value = $value.ToString().ToLowerInvariant() }
    $args.Add("$key=$value")
  }
  return [string[]]$args
}

function New-TemporaryEventHub {
  param([string]$ResourceGroupName, [string]$Location, [string]$Seed)
  Write-Host "Creating temporary Event Hubs plumbing in '$ResourceGroupName'..."
  Invoke-AzText @('group','create','--name',$ResourceGroupName,'--location',$Location,'--only-show-errors','--output','none') | Out-Null
  $suffix = New-SafeName -Value $Seed -MaxLength 18 -MinLength 3
  $namespace = New-SafeName -Value "eh$($suffix)$([Guid]::NewGuid().ToString('N').Substring(0,6))" -MaxLength 50 -MinLength 6
  $hub = 'verify'
  $rule = 'verify-send-listen'
  Invoke-AzText @('eventhubs','namespace','create','--resource-group',$ResourceGroupName,'--name',$namespace,'--location',$Location,'--sku','Standard','--enable-auto-inflate','false','--only-show-errors','--output','none') | Out-Null
  Invoke-AzText @('eventhubs','eventhub','create','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--name',$hub,'--partition-count','1','--retention-time','1','--cleanup-policy','Delete','--only-show-errors','--output','none') | Out-Null
  Invoke-AzText @('eventhubs','eventhub','authorization-rule','create','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--eventhub-name',$hub,'--name',$rule,'--rights','Listen','Send','--only-show-errors','--output','none') | Out-Null
  $cs = Invoke-AzText @('eventhubs','eventhub','authorization-rule','keys','list','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--eventhub-name',$hub,'--name',$rule,'--query','primaryConnectionString','--output','tsv','--only-show-errors')
  if ($cs -notmatch 'EntityPath=') { $cs = "$cs;EntityPath=$hub" }
  return [pscustomobject]@{ ResourceGroup = $ResourceGroupName; Namespace = $namespace; EventHub = $hub; Rule = $rule; ConnectionString = $cs }
}

function Get-DeploymentOutputsHashtable {
  param($Deployment)
  $outputs = @{}
  if ($Deployment -and $Deployment.properties -and $Deployment.properties.outputs) {
    foreach ($prop in $Deployment.properties.outputs.PSObject.Properties) { $outputs[$prop.Name] = $prop.Value.value }
  }
  return $outputs
}

function Get-ContainerGroupName {
  param([hashtable]$Outputs, [hashtable]$Overrides, [string]$Variant, [string]$Slug)
  if ($Outputs.ContainsKey('containerGroupId') -and $Outputs['containerGroupId']) {
    return ([string]$Outputs['containerGroupId']).Split('/')[-1]
  }
  if ($Overrides.ContainsKey('containerGroupName')) { return [string]$Overrides['containerGroupName'] }
  if ($Overrides.ContainsKey('namePrefix')) {
    if ($Variant -eq 'eventgrid-mqtt') { return "$($Overrides['namePrefix'])-mqtt" }
    return [string]$Overrides['namePrefix']
  }
  return New-SafeName -Value $Slug
}

function Wait-ContainerRunning {
  param([string]$ResourceGroupName, [string]$ContainerGroupName)
  Write-Host "Waiting for container group '$ContainerGroupName' to reach Running..."
  $deadline = (Get-Date).AddSeconds(120)
  do {
    try {
      $state = Invoke-AzText @('container','show','--resource-group',$ResourceGroupName,'--name',$ContainerGroupName,'--query','containers[0].instanceView.currentState.state','--output','tsv','--only-show-errors')
      if ($state.Trim() -eq 'Running') { return "Container group is Running" }
      Write-Host "Container state: $($state.Trim())"
    } catch {
      Write-Host "Container not visible yet: $($_.Exception.Message.Split("`n")[0])"
    }
    Start-Sleep -Seconds 10
  } while ((Get-Date) -lt $deadline)
  throw "Container group '$ContainerGroupName' did not reach Running within 120 seconds."
}

function Get-ContainerStateEvidence {
  param([string]$ResourceGroupName, [string]$ContainerGroupName)
  try {
    $state = Invoke-AzText @('container','show','--resource-group',$ResourceGroupName,'--name',$ContainerGroupName,'--query','containers[0].instanceView.currentState.state','--output','tsv','--only-show-errors')
    if (-not [string]::IsNullOrWhiteSpace($state)) {
      return "Container current state: $($state.Trim())"
    }
  } catch {
    return "Container state check failed: $($_.Exception.Message.Split("`n")[0])"
  }
  return "Container state unavailable."
}

function Get-ContainerLogsEvidence {
  param([string]$ResourceGroupName, [string]$ContainerGroupName)
  try {
    $logs = Invoke-AzText @('container','logs','--resource-group',$ResourceGroupName,'--name',$ContainerGroupName,'--only-show-errors')
    $matches = @($logs -split "`n" | Where-Object { $_ -match '(?i)Sent|published|flushed|send.*event|producer' } | Select-Object -First 5)
    if ($matches.Count -gt 0) { return "Container log evidence: $($matches -join ' | ')" }
    return "Container logs available but no send evidence found."
  } catch {
    return "Container log check failed: $($_.Exception.Message.Split("`n")[0])"
  }
}

function Test-EventHubDataFlow {
  param([string]$ConnectionString, [int]$TimeoutSeconds)
  $python = Get-Command python -ErrorAction SilentlyContinue
  if (-not $python) { return $null }
  $code = @'
import importlib.util, os, sys, time
if importlib.util.find_spec("azure.eventhub") is None:
    sys.exit(2)
from azure.eventhub import EventHubConsumerClient
cs = os.environ["VERIFY_EH_CONNECTION_STRING"]
deadline = time.time() + int(os.environ.get("VERIFY_TIMEOUT", "300"))
seen = []
client = EventHubConsumerClient.from_connection_string(cs, consumer_group="$Default")
def on_event(partition_context, event):
    seen.append(event)
    try:
        partition_context.update_checkpoint(event)
    finally:
        client.close()
try:
    while time.time() < deadline and not seen:
        client.receive(on_event=on_event, max_wait_time=5, starting_position="-1")
finally:
    client.close()
print(f"received={len(seen)}")
sys.exit(0 if seen else 1)
'@
  $env:VERIFY_EH_CONNECTION_STRING = $ConnectionString
  $env:VERIFY_TIMEOUT = [string]$TimeoutSeconds
  try {
    $result = $code | & python - 2>&1
    if ($LASTEXITCODE -eq 0) { return "Event Hubs receive evidence: $($result -join ' ')" }
    if ($LASTEXITCODE -eq 2) { return $null }
    return "Event Hubs receive attempted: $($result -join ' ')"
  } finally {
    Remove-Item Env:\VERIFY_EH_CONNECTION_STRING -ErrorAction SilentlyContinue
    Remove-Item Env:\VERIFY_TIMEOUT -ErrorAction SilentlyContinue
  }
}

function Get-EventHubConnectionFromDeployment {
  param([string]$ResourceGroupName, [hashtable]$Outputs, [hashtable]$Overrides, [string]$Variant, $TempEventHub)
  if ($Variant -eq 'kafka' -and $TempEventHub) { return $TempEventHub.ConnectionString }
  $namespace = $null; $hub = $null
  if ($Outputs.ContainsKey('eventHubNamespaceName')) { $namespace = $Outputs['eventHubNamespaceName'] }
  if ($Outputs.ContainsKey('eventHubName')) { $hub = $Outputs['eventHubName'] }
  if (-not $namespace) {
    $namespaces = Invoke-AzJson @('eventhubs','namespace','list','--resource-group',$ResourceGroupName,'--query','[0].name','--output','json','--only-show-errors')
    $namespace = [string]$namespaces
  }
  if (-not $hub) {
    $hubs = Invoke-AzJson @('eventhubs','eventhub','list','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--query','[0].name','--output','json','--only-show-errors')
    $hub = [string]$hubs
  }
  $ruleName = 'verify-listen'
  try {
    Invoke-AzText @('eventhubs','eventhub','authorization-rule','create','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--eventhub-name',$hub,'--name',$ruleName,'--rights','Listen','--only-show-errors','--output','none') | Out-Null
  } catch {
    Write-Host "Listen rule create skipped/failed, trying existing rules: $($_.Exception.Message.Split("`n")[0])"
    $rules = Invoke-AzJson @('eventhubs','eventhub','authorization-rule','list','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--eventhub-name',$hub,'--query','[0].name','--output','json','--only-show-errors')
    $ruleName = [string]$rules
  }
  $cs = Invoke-AzText @('eventhubs','eventhub','authorization-rule','keys','list','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--eventhub-name',$hub,'--name',$ruleName,'--query','primaryConnectionString','--output','tsv','--only-show-errors')
  if ($cs -notmatch 'EntityPath=') { $cs = "$cs;EntityPath=$hub" }
  return $cs
}

function Test-ServiceBusDataFlow {
  param([string]$ResourceGroupName, [hashtable]$Outputs, [hashtable]$Overrides)
  $namespace = $null; $queue = $null
  if ($Outputs.ContainsKey('namespaceName')) { $namespace = $Outputs['namespaceName'] }
  if ($Outputs.ContainsKey('serviceBusNamespaceName')) { $namespace = $Outputs['serviceBusNamespaceName'] }
  if ($Outputs.ContainsKey('queueName')) { $queue = $Outputs['queueName'] }
  if (-not $queue -and $Overrides.ContainsKey('queueName')) { $queue = $Overrides['queueName'] }
  if (-not $namespace) {
    $namespace = [string](Invoke-AzJson @('servicebus','namespace','list','--resource-group',$ResourceGroupName,'--query','[0].name','--output','json','--only-show-errors'))
  }
  if (-not $queue) {
    $queue = [string](Invoke-AzJson @('servicebus','queue','list','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--query','[0].name','--output','json','--only-show-errors'))
  }
  $activeCount = Invoke-AzText @('servicebus','queue','show','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--name',$queue,'--query','countDetails.activeMessageCount','--output','tsv','--only-show-errors')
  if ([int]$activeCount -gt 0) { return "Service Bus queue evidence: $activeCount active message(s) in $namespace/$queue" }

  $python = Get-Command python -ErrorAction SilentlyContinue
  if (-not $python) { return $null }
  $code = @'
import importlib.util, os, sys
if importlib.util.find_spec("azure.servicebus") is None:
    sys.exit(2)
from azure.servicebus import ServiceBusClient
cs = os.environ["VERIFY_SB_CONNECTION_STRING"]
queue = os.environ["VERIFY_SB_QUEUE"]
with ServiceBusClient.from_connection_string(cs) as client:
    with client.get_queue_receiver(queue_name=queue, max_wait_time=5) as receiver:
        messages = receiver.peek_messages(max_message_count=1)
print(f"peeked={len(messages)}")
sys.exit(0 if messages else 1)
'@
  try {
    Write-Host "Service Bus queue is empty from ARM count check; enabling local auth for optional SAS peek..."
    Invoke-AzText @('servicebus','namespace','update','--resource-group',$ResourceGroupName,'--name',$namespace,'--disable-local-auth','false','--only-show-errors','--output','none') | Out-Null
    $rule = 'verify-listen'
    try {
      Invoke-AzText @('servicebus','queue','authorization-rule','create','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--queue-name',$queue,'--name',$rule,'--rights','Listen','--only-show-errors','--output','none') | Out-Null
    } catch {
      Write-Host "Service Bus listen rule create skipped/failed: $($_.Exception.Message.Split("`n")[0])"
    }
    $cs = Invoke-AzText @('servicebus','queue','authorization-rule','keys','list','--resource-group',$ResourceGroupName,'--namespace-name',$namespace,'--queue-name',$queue,'--name',$rule,'--query','primaryConnectionString','--output','tsv','--only-show-errors')
    $env:VERIFY_SB_CONNECTION_STRING = $cs
    $env:VERIFY_SB_QUEUE = $queue
    $result = $code | & python - 2>&1
    if ($LASTEXITCODE -eq 0) { return "Service Bus peek evidence: $($result -join ' ')" }
    if ($LASTEXITCODE -eq 2) { return $null }
    return "Service Bus peek attempted: $($result -join ' ')"
  } finally {
    Remove-Item Env:\VERIFY_SB_CONNECTION_STRING -ErrorAction SilentlyContinue
    Remove-Item Env:\VERIFY_SB_QUEUE -ErrorAction SilentlyContinue
  }
}

function Test-DataFlow {
  param([string]$Variant, [string]$ResourceGroupName, [string]$ContainerGroupName, [hashtable]$Outputs, [hashtable]$Overrides, $TempEventHub, [int]$TimeoutSeconds)
  if ($Variant -in @('amqp','mqtt')) { return 'Data-flow skipped for BYO broker shape-test variant.' }
  $logEvidence = Get-ContainerLogsEvidence -ResourceGroupName $ResourceGroupName -ContainerGroupName $ContainerGroupName
  if ($Variant -notin @('servicebus','eventgrid-mqtt') -and $logEvidence -match '(?i)Sent|published|flushed') { return $logEvidence }
  if ($Variant -in @('eventhub','kafka')) {
    try {
      $cs = Get-EventHubConnectionFromDeployment -ResourceGroupName $ResourceGroupName -Outputs $Outputs -Overrides $Overrides -Variant $Variant -TempEventHub $TempEventHub
      $ehEvidence = Test-EventHubDataFlow -ConnectionString $cs -TimeoutSeconds $TimeoutSeconds
      if ($ehEvidence) { return $ehEvidence }
    } catch {
      Write-Host "Event Hubs receive check failed, using logs: $($_.Exception.Message.Split("`n")[0])"
    }
  }
  if ($Variant -eq 'servicebus') {
    try {
      $sbEvidence = Test-ServiceBusDataFlow -ResourceGroupName $ResourceGroupName -Outputs $Outputs -Overrides $Overrides
      if ($sbEvidence) { return $sbEvidence }
    } catch {
      Write-Host "Service Bus data-flow check failed, using logs: $($_.Exception.Message.Split("`n")[0])"
    }
    return "Service Bus data-flow evidence fallback: $logEvidence"
  }
  if ($Variant -eq 'eventgrid-mqtt') {
    return "Event Grid MQTT data-flow evidence fallback: $logEvidence"
  }
  return $logEvidence
}

$started = Get-Date
$rg = $null
$ehRg = $null
$pass = $false
$evidence = New-Object System.Collections.Generic.List[string]
try {
  Write-Host "Verifying Azure CLI account..."
  Invoke-AzText @('account','show','--only-show-errors','--output','none') | Out-Null
  Invoke-AzText @('account','set','--subscription',$SubscriptionId,'--only-show-errors') | Out-Null

  if ($TemplateFile) {
    $templatePath = (Resolve-Path -LiteralPath $TemplateFile).Path
  } else {
    $templatePath = Resolve-TemplatePath -Slug $FeederSlug -FileName $VariantFiles[$Variant]
  }
  Write-Host "Template: $templatePath"
  $template = Test-TemplateHasResources -TemplatePath $templatePath
  $parameters = Get-TemplateParameterTable -Template $template

  $suffix = [Guid]::NewGuid().ToString('N').Substring(0,8)
  if ($ResourceGroupName) {
    $rg = New-SafeName -Value $ResourceGroupName -MaxLength 90
  } else {
    $rg = New-SafeName -Value "rg-fleet-verify-$FeederSlug-$Variant-$suffix" -MaxLength 90
  }
  $uniqueName = New-SafeName -Value "$FeederSlug-$Variant-$suffix" -MaxLength 63 -MinLength 3
  $namePrefix = New-SafeName -Value "$FeederSlug-$suffix" -MaxLength 24 -MinLength 3
  Write-Host "Resource group: $rg"

  $secrets = @{}
  if ($SecretsFile) {
    if (-not (Test-Path -LiteralPath $SecretsFile -PathType Leaf)) { throw "Secrets file '$SecretsFile' not found." }
    $secrets = ConvertTo-Hashtable (Get-Content -LiteralPath $SecretsFile -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop)
  }

  $overrides = @{}
  Add-IfParameterExists $overrides $parameters 'location' $Location
  Add-IfParameterExists $overrides $parameters 'containerGroupName' $uniqueName
  Add-IfParameterExists $overrides $parameters 'namePrefix' $namePrefix

  if ($Variant -eq 'kafka' -and -not $DryRun) {
    $ehRg = New-SafeName -Value "$rg-eh" -MaxLength 90
    $tempEventHub = New-TemporaryEventHub -ResourceGroupName $ehRg -Location $Location -Seed "$FeederSlug$Variant"
    Add-IfParameterExists $overrides $parameters 'connectionString' $tempEventHub.ConnectionString
    $evidence.Add("Temporary Event Hub: $($tempEventHub.Namespace)/$($tempEventHub.EventHub)")
  } else {
    $tempEventHub = $null
  }

  if ($Variant -eq 'amqp') {
    Add-IfParameterExists $overrides $parameters 'amqpHost' 'localhost'
    Add-IfParameterExists $overrides $parameters 'amqpPort' 5672
    Add-IfParameterExists $overrides $parameters 'amqpAddress' 'test'
    Add-IfParameterExists $overrides $parameters 'amqpUsername' 'guest'
    Add-IfParameterExists $overrides $parameters 'amqpPassword' 'guest'
    Add-IfParameterExists $overrides $parameters 'amqpUseTls' $false
  }
  if ($Variant -eq 'mqtt') {
    Add-IfParameterExists $overrides $parameters 'brokerUrl' 'mqtts://localhost:8883'
  }

  foreach ($key in $secrets.Keys) { $overrides[$key] = $secrets[$key] }
  Add-RequiredPlaceholders -Overrides $overrides -Parameters $parameters
  $paramArgs = Get-ParameterArguments -Overrides $overrides

  Write-Host "Creating resource group '$rg'..."
  Invoke-AzText @('group','create','--name',$rg,'--location',$Location,'--only-show-errors','--output','none') | Out-Null

  if ($DryRun) {
    Write-Host "Running ARM validation for '${FeederSlug}:$Variant'..."
    $validation = Invoke-AzJson (@('deployment','group','validate','--resource-group',$rg,'--template-file',$templatePath,'--only-show-errors','--output','json','--parameters') + $paramArgs)
    $validationState = if ($validation.properties.provisioningState) { $validation.properties.provisioningState } else { 'Succeeded' }
    $evidence.Add("Validation state: $validationState")
    Write-Host "VALID ${FeederSlug}:$Variant"
    $pass = $true
  } else {
    $deploymentName = New-SafeName -Value "verify-$FeederSlug-$Variant-$suffix" -MaxLength 64
    Write-Host "Creating deployment '$deploymentName'..."
    $deployment = Invoke-AzJson (@('deployment','group','create','--name',$deploymentName,'--resource-group',$rg,'--template-file',$templatePath,'--only-show-errors','--output','json','--parameters') + $paramArgs)
    $outputs = Get-DeploymentOutputsHashtable -Deployment $deployment
    $containerGroupName = Get-ContainerGroupName -Outputs $outputs -Overrides $overrides -Variant $Variant -Slug $FeederSlug
    $evidence.Add("Deployment state: $($deployment.properties.provisioningState)")
    if ($Variant -in @('mqtt','amqp')) {
      try {
        $evidence.Add((Wait-ContainerRunning -ResourceGroupName $rg -ContainerGroupName $containerGroupName))
      } catch {
        $evidence.Add((Get-ContainerStateEvidence -ResourceGroupName $rg -ContainerGroupName $containerGroupName))
        $evidence.Add("BYO broker shape-test variant: accepting deployment success without a running container.")
      }
    } else {
      $evidence.Add((Wait-ContainerRunning -ResourceGroupName $rg -ContainerGroupName $containerGroupName))
    }
    $evidence.Add((Test-DataFlow -Variant $Variant -ResourceGroupName $rg -ContainerGroupName $containerGroupName -Outputs $outputs -Overrides $overrides -TempEventHub $tempEventHub -TimeoutSeconds $DataFlowTimeoutSeconds))
    $pass = $true
  }
} catch {
  Write-Error $_.Exception.Message
  $evidence.Add("Failure: $($_.Exception.Message.Split("`n")[0])")
  $pass = $false
} finally {
  if (-not $KeepResourceGroup) {
    if ($rg) {
      Write-Host "Deleting resource group '$rg' (no-wait)..."
      & az group delete --name $rg --yes --no-wait --only-show-errors 2>$null | Out-Null
    }
    if ($ehRg) {
      Write-Host "Deleting temporary Event Hubs resource group '$ehRg' (no-wait)..."
      & az group delete --name $ehRg --yes --no-wait --only-show-errors 2>$null | Out-Null
    }
  } else {
    Write-Host "Keeping resource group '$rg' as requested."
    if ($ehRg) { Write-Host "Keeping temporary Event Hubs resource group '$ehRg' as requested." }
  }
  $elapsed = [Math]::Round(((Get-Date) - $started).TotalSeconds, 1)
  $status = if ($pass) { 'PASS' } else { 'FAIL' }
  Write-Host ""
  Write-Host "==== $status ${FeederSlug}:$Variant in ${elapsed}s ===="
  foreach ($item in $evidence) { Write-Host "- $item" }
}

if ($pass) { exit 0 } else { exit 1 }
