$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$catalog = Get-Content (Join-Path $PSScriptRoot 'arm-catalog.json') -Raw | ConvertFrom-Json -AsHashtable
$original = $catalog.feeders[0]
$feeders = foreach ($template in $original.emptyTemplates) {
    $entry = $original | ConvertTo-Json -Depth 30 | ConvertFrom-Json -AsHashtable
    $entry.emptyTemplates = @($template)
    $entry.envVars += @{
        name='STATE_FILE'; armParamName='stateFile'; default='/mnt/bridge-state/usgs-waterdata.json'
        isRequired=$false; isSecret=$false
    }
    if ($template -eq 'feeders\usgs-waterdata\azure-template.json') {
        $settings = @(
            @('CONNECTION_STRING', 'connectionString', '', $true),
            @('KAFKA_BOOTSTRAP_SERVERS', 'kafkaBootstrapServers', 'localhost:9092', $false),
            @('KAFKA_TOPIC', 'kafkaTopic', 'usgs-waterdata', $false),
            @('KAFKA_ENABLE_TLS', 'kafkaEnableTls', 'true', $false),
            @('SASL_USERNAME', 'saslUsername', '', $false),
            @('SASL_PASSWORD', 'saslPassword', '', $true),
            @('SASL_MECHANISM', 'saslMechanism', 'PLAIN', $false)
        )
    } elseif ($template -eq 'feeders\usgs-waterdata\azure-template-mqtt.json') {
        $settings = @(
            @('MQTT_AUTH_MODE', 'mqttAuthMode', '', $false),
            @('MQTT_ENABLE_TLS', 'mqttEnableTls', 'true', $false),
            @('MQTT_CA_FILE', 'mqttCaFile', '', $false),
            @('MQTT_CLIENT_CERT', 'mqttClientCert', '', $false),
            @('MQTT_CLIENT_KEY', 'mqttClientKey', '', $false)
        )
    } else {
        $settings = @()
    }
    foreach ($setting in $settings) {
        $entry.envVars += @{
            name=$setting[0]; armParamName=$setting[1]; default=$setting[2]
            isRequired=$false; isSecret=$setting[3]
        }
    }
    $entry
}
$generatedCatalog = Join-Path $PSScriptRoot '.arm-catalog.generated.json'
try {
    @{feeders=@($feeders)} | ConvertTo-Json -Depth 30 | Set-Content $generatedCatalog -Encoding utf8NoBOM
    & python (Join-Path $repoRoot 'tools\generate-arm-templates.py') --repo-root $repoRoot `
        --catalog $generatedCatalog --filter usgs-waterdata
    if ($LASTEXITCODE -ne 0) { throw 'USGS Water Data ARM template generation failed' }
    $reference = Get-Content (Join-Path $PSScriptRoot 'azure-template-with-eventhub.json') -Raw |
        ConvertFrom-Json -AsHashtable
    $referenceContainer = $reference.resources | Where-Object type -eq 'Microsoft.ContainerInstance/containerGroups'
    foreach ($path in $original.emptyTemplates) {
        $target = Join-Path $repoRoot $path
        $document = Get-Content $target -Raw | ConvertFrom-Json -AsHashtable
        if ($document.resources.type -notcontains 'Microsoft.Storage/storageAccounts') {
            $document.variables.storageAccountName = $reference.variables.storageAccountName
            if (-not $document.parameters.ContainsKey('containerGroupName')) {
                $document.variables.storageAccountName = $document.variables.storageAccountName.Replace(
                    "parameters('containerGroupName')", "variables('containerGroupName')")
            }
            $document.variables.fileShareName = $reference.variables.fileShareName
            $storage = @($reference.resources | Where-Object type -like 'Microsoft.Storage/*')
            $document.resources = $storage + $document.resources
            foreach ($container in @($document.resources | Where-Object type -eq 'Microsoft.ContainerInstance/containerGroups')) {
                $container.dependsOn += "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', variables('storageAccountName'), 'default', variables('fileShareName'))]"
                $container.properties.volumes = $referenceContainer.properties.volumes
                foreach ($application in $container.properties.containers) {
                    $application.properties.volumeMounts = $referenceContainer.properties.containers[0].properties.volumeMounts
                }
            }
        }
        if ($path -eq 'feeders\usgs-waterdata\azure-template-mqtt.json') {
            $document.parameters.mqttAuthMode.allowedValues = @('', 'anonymous', 'userpass', 'password', 'tls-cert')
            $document.parameters.mqttAuthMode.metadata.description =
                'MQTT authentication mode; empty selects userpass when brokerUsername is supplied, otherwise anonymous. Use the Event Grid template for managed-identity Entra authentication.'
            foreach ($container in @($document.resources | Where-Object type -eq 'Microsoft.ContainerInstance/containerGroups')) {
                foreach ($application in $container.properties.containers) {
                    $mode = $application.properties.environmentVariables | Where-Object name -eq 'MQTT_AUTH_MODE'
                    $mode.value = "[if(empty(parameters('mqttAuthMode')), if(empty(parameters('brokerUsername')), 'anonymous', 'userpass'), parameters('mqttAuthMode'))]"
                }
            }
        }
        $document | ConvertTo-Json -Depth 100 | Set-Content $target -Encoding utf8NoBOM
    }
} finally {
    Remove-Item $generatedCatalog -ErrorAction SilentlyContinue
}
