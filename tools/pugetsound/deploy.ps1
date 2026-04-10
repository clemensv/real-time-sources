<#
.SYNOPSIS
    Deploys the Puget Sound container group to Azure Container Instances.

.DESCRIPTION
    Deploys Seattle- and Puget Sound-focused bridges as sidecars in a single
    ACI container group, sharing one Kafka/Event Hub/Fabric Event Stream
    connection string.
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroupName,

    [Parameter(Mandatory = $true)]
    [string]$ConnectionString,

    [Parameter(Mandatory = $true)]
    [string]$WsdotAccessCode,

    [string]$Location = "westus2"
)

$ErrorActionPreference = "Stop"

$rg = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
if (-not $rg) {
    Write-Host "Creating resource group '$ResourceGroupName' in '$Location'..."
    New-AzResourceGroup -Name $ResourceGroupName -Location $Location | Out-Null
}

$templateFile = Join-Path $PSScriptRoot "azure-template.json"

Write-Host "Deploying Puget Sound container group..."
New-AzResourceGroupDeployment `
    -ResourceGroupName $ResourceGroupName `
    -TemplateFile $templateFile `
    -connectionStringSecret (ConvertTo-SecureString $ConnectionString -AsPlainText -Force) `
    -wsdotAccessCodeSecret (ConvertTo-SecureString $WsdotAccessCode -AsPlainText -Force) `
    -Verbose

Write-Host "Deployment complete."
