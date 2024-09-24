# PowerShell version: 7.1

# Define parameters for the ARM template
$templateParameters = @{
    "`$schema"       = "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#"
    "contentVersion" = "1.0.0.0"
    "parameters"     = @{
        "connectionStringSecret" = @{
            "type"     = "securestring"
            "metadata" = @{
                "description" = "The Microsoft Fabric Event Stream custom input endpoint or Azure Event Hubs connection string."
            }
        }
        "feedUrls" = @{
            "type"        = "string"
            "defaultValue" = ""
            "metadata"    = @{
                "description" = "Comma-separated list of feed URLs (RSS or OPML)"
            }
        }
        "appName" = @{
            "type"        = "string"
            "defaultValue" = "[if(empty(resourceGroup().name), 'usgs-iv', resourceGroup().name)]"
            "metadata"    = @{
                "description" = "The name of the container instance."
            }
            "maxLength"   = 64
        }
        "imageName" = @{
            "type"        = "string"
            "defaultValue" = "ghcr.io/clemensv/real-time-sources-usgs-iv:latest"
            "metadata"    = @{
                "description" = "The name of the container image."
            }
        }
        "logAnalyticsWorkspaceId" = @{
            "type"        = "string"
            "metadata"    = @{
                "description" = "The Id of the Log Analytics workspace. In the portal, you find this under Settings -> Agents -> Windows/Linux Servers -> Agent Instructions."
            }
        }
        "logAnalyticsWorkspaceKey" = @{
            "type"        = "securestring"
            "metadata"    = @{
                "description" = "The primary or secondary key of the Log Analytics workspace. In the portal, you find this under Settings -> Agents -> Windows/Linux Servers -> Agent Instructions."
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
        "type" = "Microsoft.Storage/storageAccounts"
        "apiVersion" = "2021-04-01"
        "name" = "[variables('storageAccountName')]"
        "location" = "[resourceGroup().location]"
        "sku" = @{
            "name" = "Standard_LRS"
        }
        "kind" = "StorageV2"
        "properties" = @{
            "accessTier" = "Hot"
        }
    }
    @{
        "type" = "Microsoft.Storage/storageAccounts/fileServices"
        "apiVersion" = "2021-04-01"
        "name" = "[concat(variables('storageAccountName'), '/default/')]"
        "location" = "[resourceGroup().location]"
        "dependsOn" = @("[concat('Microsoft.Storage/storageAccounts/', variables('storageAccountName'))]")
        "properties" = @{
            "protocolSettings" = @{
                "smb" = @{
                    "enabled" = $true
                }
            }
        }
    }
    @{
        "type" = "Microsoft.Storage/storageAccounts/fileServices/shares"
        "apiVersion" = "2021-04-01"
        "name" = "[concat(variables('storageAccountName'), '/default/', variables('fileShareName'))]"
        "location" = "[resourceGroup().location]"
        "dependsOn" = @("[concat('Microsoft.Storage/storageAccounts/', variables('storageAccountName'))]")
        "properties" = @{
            "shareQuota" = 5120
        }
    }
    @{
        "type"       = "Microsoft.ContainerInstance/containerGroups"
        "apiVersion" = "2021-09-01"
        "name"       = "[parameters('appName')]"
        "location"   = "[resourceGroup().location]"
        "properties" = @{
            "containers" = @(
                @{
                    "name"       = "[parameters('appName')]"
                    "properties" = @{
                        "image"                = "[parameters('imageName')]"
                        "resources"            = @{
                            "requests" = @{
                                "cpu"        = 0.5
                                "memoryInGB" = 1
                            }
                        }
                        "environmentVariables" = @(
                            @{
                                "name"        = "CONNECTION_STRING"
                                "secureValue" = "[parameters('connectionStringSecret')]"
                            }
                            @{
                                "name"  = "LOG_LEVEL"
                                "value" = "INFO"
                            }
                            @{
                                "name"  = "USGS_LAST_POLLED_FILE"
                                "value" = "/mnt/fileshare/usgs_last_polled.json"
                            }
                        )
                        "volumeMounts" = @(
                            @{
                                "name" = "azurefilevolume"
                                "mountPath" = "/mnt/fileshare"
                            }
                        )
                    }
                }
            )
            "osType"        = "Linux"
            "restartPolicy" = "Always"
            "volumes" = @(
                @{
                    "name" = "azurefilevolume"
                    "azureFile" = @{
                        "shareName" = "[variables('fileShareName')]"
                        "storageAccountName" = "[variables('storageAccountName')]"
                        "storageAccountKey" = "[listKeys(resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName')), '2019-06-01').keys[0].value]"
                    }
                }
            )
            "diagnostics"   = @{
                "logAnalytics" = @{
                    "workspaceId" = "[parameters('logAnalyticsWorkspaceId')]"
                    "workspaceKey" = "[parameters('logAnalyticsWorkspaceKey')]"
                }
            }
        }
    }
)

# Combine parameters and resources into the final template
$armTemplate = @{
    "`$schema"       = $templateParameters["`$schema"]
    "contentVersion" = $templateParameters["contentVersion"]
    "parameters"     = $templateParameters["parameters"]
    "variables"      = $templateParameters["variables"]
    "resources"      = $templateResources
}

# Convert the ARM template to JSON and emit it
$templateJson = $armTemplate | ConvertTo-Json -Depth 100
Write-Output $templateJson
