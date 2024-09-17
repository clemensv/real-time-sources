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
        "agencyId" = @{
            "type" = "string"
            "metadata" = @{
                "description" = "The GTFS agency identifier."
            }
            "maxLength" = 64
        }
        "gtfs_urls" = @{
            "type" = "string"
            "metadata" = @{
                "description" = "Comma-separated list of GTFS URLs."
            }
            "maxLength" = 2048
        }
        "gtfs_rt_urls" = @{
            "type" = "string"
            "metadata" = @{
                "description" = "Comma-separated list of GTFS-RT URLs."
            }
            "maxLength" = 2048
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
            "defaultValue" = "ghcr.io/clemensv/real-time-sources-gtfs:latest"
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
        "type" = "Microsoft.ContainerInstance/containerGroups"
        "apiVersion" = "2021-09-01"
        "name" = "[parameters('appName')]"
        "location" = "[resourceGroup().location]"
        "dependsOn" = @(
            "[resourceId('Microsoft.Storage/storageAccounts/', variables('storageAccountName'))]"
            "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', variables('storageAccountName'), 'default', variables('fileShareName'))]"
        )
        "properties" = @{
            "containers" = @(
                @{
                    "name" = "[parameters('appName')]"
                    "properties" = @{
                        "image" = "[parameters('imageName')]"
                        "resources" = @{
                            "requests" = @{
                                "cpu" = 1
                                "memoryInGB" = 2
                            }
                        }
                        "environmentVariables" = @(
                            @{
                                "name" = "CONNECTION_STRING"
                                "secureValue" = "[parameters('connectionStringSecret')]"
                            },
                            @{
                                "name" = "CACHE_DIR"
                                "value" = "/mnt/fileshare/cache"
                            },
                            @{
                                "name" = "GTFS_URLS"
                                "value" = "[parameters('gtfs_urls')]"
                            },
                            @{
                                "name" = "GTFS_RT_URLS"
                                "value" = "[parameters('gtfs_rt_urls')]"
                            },
                            @{
                                "name" = "AGENCY"
                                "value" = "[parameters('agencyId')]"
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
            "osType" = "Linux"
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
