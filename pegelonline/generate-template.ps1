# PowerShell version: 7.1

# Define parameters for the ARM template
$templateParameters = @{
    "`$schema" = "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#"
    "contentVersion" = "1.0.0.0"
    "parameters" = @{
        "connectionStringSecret" = @{
            "type" = "securestring"
            "metadata" = @{
                "description" = "The Microsoft Fabric Event Stream custom input endpoint connection string."
            }
        }
        "appName" = @{
            "type" = "string"
            "defaultValue" = "[resourceGroup().name]"
            "metadata" = @{
                "description" = "The name of the container instance."
            }
            "maxLength" = 64
        }
        "imageName" = @{
            "type" = "string"
            "defaultValue" = "ghcr.io/clemensv/real-time-sources-pegelonline:latest"
            "metadata" = @{
                "description" = "The name of the container image."
            }
        }
    }
    "variables" = @{
        "storageAccountName" = "[concat(replace(parameters('appName'), '-', ''), 'stg')]"
        "fileShareName" = "fileshare"
    }
}

# Define resources in the ARM template
$templateResources = @(
    @{
        "type" = "Microsoft.ContainerInstance/containerGroups"
        "apiVersion" = "2021-09-01"
        "name" = "[parameters('appName')]"
        "location" = "[resourceGroup().location]"
        "properties" = @{
            "containers" = @(
                @{
                    "name" = "[parameters('appName')]"
                    "properties" = @{
                        "image" = "[parameters('imageName')]"
                        "resources" = @{
                            "requests" = @{
                                "cpu" = 0.5
                                "memoryInGB" = 1
                            }
                        }
                        "environmentVariables" = @(
                            @{
                                "name" = "CONNECTION_STRING"
                                "secureValue" = "[parameters('connectionStringSecret')]"
                            }
                        )
                    }
                }
            )
            "osType" = "Linux"
            "restartPolicy" = "Always"
        }
    }
)

# Combine parameters and resources into the final template
$armTemplate = @{
    "`$schema" = $templateParameters["`$schema"]
    "contentVersion" = $templateParameters["contentVersion"]
    "parameters" = $templateParameters["parameters"]
    "variables" = $templateParameters["variables"]
    "resources" = $templateResources
}

# Convert the ARM template to JSON and emit it
$templateJson = $armTemplate | ConvertTo-Json -Depth 10
Write-Output $templateJson
