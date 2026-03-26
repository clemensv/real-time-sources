# Generate ARM template for UK EA Flood Monitoring container deployment
# This script generates the azure-template.json file

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Generating Azure template for UK EA Flood Monitoring..." -ForegroundColor Cyan

$template = @{
    '$schema' = 'https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#'
    contentVersion = '1.0.0.0'
    parameters = @{
        appName = @{
            type = 'string'
            defaultValue = '[resourceGroup().name]'
            maxLength = 64
            metadata = @{
                description = 'The name of the container instance.'
            }
        }
        connectionStringSecret = @{
            type = 'securestring'
            metadata = @{
                description = 'The Microsoft Fabric Event Stream custom input endpoint connection string.'
            }
        }
        imageName = @{
            type = 'string'
            defaultValue = 'ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring:latest'
            metadata = @{
                description = 'The name of the container image.'
            }
        }
    }
    resources = @(
        @{
            type = 'Microsoft.ContainerInstance/containerGroups'
            apiVersion = '2021-09-01'
            name = "[parameters('appName')]"
            location = "[resourceGroup().location]"
            properties = @{
                containers = @(
                    @{
                        name = "[parameters('appName')]"
                        properties = @{
                            image = "[parameters('imageName')]"
                            resources = @{
                                requests = @{
                                    cpu = 0.5
                                    memoryInGB = 1
                                }
                            }
                            environmentVariables = @(
                                @{
                                    name = 'CONNECTION_STRING'
                                    secureValue = "[parameters('connectionStringSecret')]"
                                }
                            )
                        }
                    }
                )
                restartPolicy = 'Always'
                osType = 'Linux'
            }
        }
    )
}

$templateJson = $template | ConvertTo-Json -Depth 10
$templatePath = Join-Path $scriptDir "azure-template.json"
Set-Content -Path $templatePath -Value $templateJson

Write-Host "✓ Azure template generated: $templatePath" -ForegroundColor Green
