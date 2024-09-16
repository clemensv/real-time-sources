# PowerShell version: 7.1

# Define parameters for the ARM template
$templateParameters = @{
    "`$schema"       = "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#"
    "contentVersion" = "1.0.0.0"
    "parameters"     = @{
        "connectionStringSecret" = @{
            "type"     = "securestring"
            "metadata" = @{
                "description" = "The Microsoft Fabric Event Stream custom input endpoint connection string."
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
            "defaultValue" = "[resourceGroup().name]"
            "metadata"    = @{
                "description" = "The name of the container instance."
            }
            "maxLength"   = 64
        }
        "imageName" = @{
            "type"        = "string"
            "defaultValue" = "ghcr.io/clemensv/real-time-sources-rss:latest"
            "metadata"    = @{
                "description" = "The name of the container image."
            }
        }
        # New parameter for Log Analytics workspace name
        "logAnalyticsWorkspaceId" = @{
            "type"        = "string"
            "defaultValue" = ""
            "metadata"    = @{
                "description" = "The Id of the Log Analytics workspace. Leave empty to skip log analytics configuration."
            }
        }
        "logAnalyticsWorkspaceKey" = @{
            "type"        = "securestring"
            "defaultValue" = ""
            "metadata"    = @{
                "description" = "The key of the Log Analytics workspace. Leave empty to skip log analytics configuration."
            }
        }
    }
}

# Define resources in the ARM template
$templateResources = @(
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
                                "name"  = "FEED_URLS"
                                "value" = "[parameters('feedUrls')]"
                            }
                        )
                    }
                }
            )
            "osType"        = "Linux"
            "restartPolicy" = "Always"
            # Conditional diagnostics section using here-string
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
    "resources"      = $templateResources
}

# Convert the ARM template to JSON and emit it
$templateJson = $armTemplate | ConvertTo-Json -Depth 100
Write-Output $templateJson
