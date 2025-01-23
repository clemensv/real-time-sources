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
        "appName" = @{
            "type"        = "string"
            "defaultValue" = "[if(empty(resourceGroup().name), 'mode-s', resourceGroup().name)]"
            "metadata"    = @{
                "description" = "The name of the container instance."
            }
            "maxLength"   = 64
        }
        "imageName" = @{
            "type"        = "string"
            "defaultValue" = "ghcr.io/clemensv/real-time-sources-mode-s:latest"
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
        "dump1090Host" = @{
            "type"        = "string"
            "defaultValue" = "localhost"
            "metadata"    = @{
                "description" = "Hostname or IP address of dump1090."
            }
        }
        "dump1090Port" = @{
            "type"        = "string"
            "defaultValue" = "30005"
            "metadata"    = @{
                "description" = "TCP port dump1090 listens on."
            }
        }
        "refLat" = @{
            "type"        = "string"
            "defaultValue" = "0"
            "metadata"    = @{
                "description" = "Latitude of the receiving antenna."
            }
        }
        "refLon" = @{
            "type"        = "string"
            "defaultValue" = "0"
            "metadata"    = @{
                "description" = "Longitude of the receiving antenna."
            }
        }
        "stationId" = @{
            "type"        = "string"
            "defaultValue" = "station1"
            "metadata"    = @{
                "description" = "Station ID for event source attribution."
            }
        }
        "kafkaBootstrapServers" = @{
            "type"        = "string"
            "defaultValue" = ""
            "metadata"    = @{
                "description" = "Kafka bootstrap servers."
            }
        }
        "kafkaTopic" = @{
            "type"        = "string"
            "defaultValue" = ""
            "metadata"    = @{
                "description" = "Kafka topic to publish messages."
            }
        }
        "saslUsername" = @{
            "type"        = "string"
            "defaultValue" = ""
            "metadata"    = @{
                "description" = "Username for SASL authentication."
            }
        }
        "saslPassword" = @{
            "type"        = "securestring"
            "metadata"    = @{
                "description" = "Password for SASL authentication."
            }
        }
        "pollingInterval" = @{
            "type"        = "string"
            "defaultValue" = "60"
            "metadata"    = @{
                "description" = "Polling interval in seconds."
            }
        }
        "logLevel" = @{
            "type"        = "string"
            "defaultValue" = "INFO"
            "metadata"    = @{
                "description" = "Logging level."
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
                                "name"  = "DUMP1090_HOST"
                                "value" = "[parameters('dump1090Host')]"
                            },
                            @{
                                "name"  = "DUMP1090_PORT"
                                "value" = "[parameters('dump1090Port')]"
                            },
                            @{
                                "name"  = "REF_LAT"
                                "value" = "[parameters('refLat')]"
                            },
                            @{
                                "name"  = "REF_LON"
                                "value" = "[parameters('refLon')]"
                            },
                            @{
                                "name"  = "STATIONID"
                                "value" = "[parameters('stationId')]"
                            },
                            @{
                                "name"        = "CONNECTION_STRING"
                                "secureValue" = "[parameters('connectionStringSecret')]"
                            },
                            @{
                                "name"  = "KAFKA_BOOTSTRAP_SERVERS"
                                "value" = "[parameters('kafkaBootstrapServers')]"
                            },
                            @{
                                "name"  = "KAFKA_TOPIC"
                                "value" = "[parameters('kafkaTopic')]"
                            },
                            @{
                                "name"  = "SASL_USERNAME"
                                "value" = "[parameters('saslUsername')]"
                            },
                            @{
                                "name"        = "SASL_PASSWORD"
                                "secureValue" = "[parameters('saslPassword')]"
                            },
                            @{
                                "name"  = "POLLING_INTERVAL"
                                "value" = "[parameters('pollingInterval')]"
                            },
                            @{
                                "name"  = "LOG_LEVEL"
                                "value" = "[parameters('logLevel')]"
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
