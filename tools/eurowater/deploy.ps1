<#
.SYNOPSIS
    Deploys the European Water container group to Azure Container Instances.

.DESCRIPTION
    Deploys all 11 European waterway information services as sidecars in a
    single ACI container group, sharing one Kafka/Event Hub connection string.

    Services included:
      - Pegelonline (Germany)
      - CHMI Hydro (Czech Republic)
      - IMGW Hydro (Poland)
      - SMHI Hydro (Sweden)
      - Hub'Eau Hydrometrie (France)
      - UK EA Flood Monitoring (England)
      - RWS Waterwebservices (Netherlands)
      - Waterinfo VMM (Belgium/Flanders)
      - NVE Hydro (Norway)
      - SYKE Hydro (Finland)
      - BAFU Hydro (Switzerland)

.PARAMETER ResourceGroupName
    The Azure resource group to deploy into (will be created if it doesn't exist).

.PARAMETER ConnectionString
    The Kafka/Event Hub connection string for all containers.

.PARAMETER Location
    Azure region. Defaults to westeurope.

.EXAMPLE
    ./deploy.ps1 -ResourceGroupName eurowater-rg -ConnectionString "Endpoint=sb://..."
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,

    [Parameter(Mandatory=$true)]
    [string]$ConnectionString,

    [string]$NveApiKey = "",

    [string]$Location = "westeurope"
)

$ErrorActionPreference = "Stop"

# Ensure the resource group exists
$rg = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
if (-not $rg) {
    Write-Host "Creating resource group '$ResourceGroupName' in '$Location'..."
    New-AzResourceGroup -Name $ResourceGroupName -Location $Location | Out-Null
}

# Deploy the ARM template
$templateFile = Join-Path $PSScriptRoot "azure-template.json"

Write-Host "Deploying European Water container group..."
$deployParams = @{
    ResourceGroupName = $ResourceGroupName
    TemplateFile      = $templateFile
    connectionStringSecret = (ConvertTo-SecureString $ConnectionString -AsPlainText -Force)
}
if ($NveApiKey) {
    $deployParams['nveApiKeySecret'] = (ConvertTo-SecureString $NveApiKey -AsPlainText -Force)
}
New-AzResourceGroupDeployment @deployParams -Verbose

Write-Host "Deployment complete."
