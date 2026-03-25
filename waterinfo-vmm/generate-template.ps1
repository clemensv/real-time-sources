$ErrorActionPreference = 'Stop'

$templateFile = Join-Path $PSScriptRoot "azure-template.json"
Write-Host "Azure template: $templateFile"
Write-Host "Deploy with:"
Write-Host "  az deployment group create --resource-group <rg> --template-file $templateFile --parameters eventHubConnectionString='<connection-string>'"
