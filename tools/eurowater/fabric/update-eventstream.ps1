param(
    [Parameter(Mandatory=$true)]
    [string]$WorkspaceId,
    [Parameter(Mandatory=$true)]
    [string]$EventstreamId,
    [Parameter(Mandatory=$true)]
    [string]$DatabaseId
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Read SQL files
$stationsSQL = Get-Content "$scriptDir\normalize_stations.sql" -Raw
$measurementsSQL = Get-Content "$scriptDir\normalize_measurements.sql" -Raw

# Remove SQL comments (lines starting with --)
$stationsSQL = ($stationsSQL -split "`n" | Where-Object { $_ -notmatch '^\s*--' }) -join "`r`n"
$measurementsSQL = ($measurementsSQL -split "`n" | Where-Object { $_ -notmatch '^\s*--' }) -join "`r`n"

# Replace EventInput with [eurowater-ingest-stream]
$stationsSQL = $stationsSQL -replace 'FROM EventInput', 'FROM [eurowater-ingest-stream]'
$measurementsSQL = $measurementsSQL -replace 'FROM EventInput', 'FROM [eurowater-ingest-stream]'

# Remove blank lines
$stationsSQL = ($stationsSQL -split "`r?`n" | Where-Object { $_.Trim() -ne '' }) -join "`r`n"
$measurementsSQL = ($measurementsSQL -split "`r?`n" | Where-Object { $_.Trim() -ne '' }) -join "`r`n"

# Combine
$combinedSQL = $stationsSQL + "`r`n" + $measurementsSQL

Write-Host "Combined SQL length: $($combinedSQL.Length)"

# Build eventstream JSON
$eventstreamObj = @{
    sources = @(
        @{
            id = "7c03b91d-b67a-4029-a34a-05766e659214"
            name = "eurowater-input"
            type = "CustomEndpoint"
            properties = @{}
        }
    )
    destinations = @(
        @{
            id = "080b1a64-fdf0-46f3-8796-72fd7eb058a8"
            name = "stations-kql"
            type = "Eventhouse"
            properties = @{
                dataIngestionMode = "ProcessedIngestion"
                workspaceId = $WorkspaceId
                itemId = $DatabaseId
                databaseName = "eurowater"
                tableName = "Stations"
                inputSerialization = @{
                    type = "Json"
                    properties = @{ encoding = "UTF8" }
                }
            }
            inputNodes = @( @{ name = "StationOutput" } )
        },
        @{
            id = "c35a72a8-a468-4420-ad4f-d8749fa56bb1"
            name = "measurements-kql"
            type = "Eventhouse"
            properties = @{
                dataIngestionMode = "ProcessedIngestion"
                workspaceId = $WorkspaceId
                itemId = $DatabaseId
                databaseName = "eurowater"
                tableName = "Measurements"
                inputSerialization = @{
                    type = "Json"
                    properties = @{ encoding = "UTF8" }
                }
            }
            inputNodes = @( @{ name = "MeasurementOutput" } )
        }
    )
    streams = @(
        @{
            id = "09c87bbf-addf-447d-bf5d-50dd244ebd75"
            name = "MeasurementOutput"
            type = "DerivedStream"
            properties = @{
                inputSerialization = @{
                    type = "Json"
                    properties = @{ encoding = "UTF8" }
                }
            }
            inputNodes = @( @{ name = "normalize" } )
        },
        @{
            id = "7d907ee2-2668-45c9-b53b-cc44a6c76901"
            name = "StationOutput"
            type = "DerivedStream"
            properties = @{
                inputSerialization = @{
                    type = "Json"
                    properties = @{ encoding = "UTF8" }
                }
            }
            inputNodes = @( @{ name = "normalize" } )
        },
        @{
            id = "db56b96f-424a-4274-8f46-f0395cfe918a"
            name = "eurowater-ingest-stream"
            type = "DefaultStream"
            properties = @{}
            inputNodes = @( @{ name = "eurowater-input" } )
        }
    )
    operators = @(
        @{
            name = "normalize"
            type = "SQL"
            inputNodes = @( @{ name = "eurowater-ingest-stream" } )
            properties = @{
                query = $combinedSQL
                advancedSettings = $null
            }
        }
    )
    compatibilityLevel = "1.1"
}

$eventstreamJson = $eventstreamObj | ConvertTo-Json -Depth 10 -Compress
$eventstreamBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($eventstreamJson))

$definitionPayload = @{
    definition = @{
        parts = @(
            @{
                path = "eventstream.json"
                payload = $eventstreamBase64
                payloadType = "InlineBase64"
            },
            @{
                path = "eventstreamProperties.json"
                payload = "ew0KICAicmV0ZW50aW9uVGltZUluRGF5cyI6IDEsDQogICJldmVudFRocm91Z2hwdXRMZXZlbCI6ICJMb3ciDQp9"
                payloadType = "InlineBase64"
            },
            @{
                path = ".platform"
                payload = "ewogICIkc2NoZW1hIjogImh0dHBzOi8vZGV2ZWxvcGVyLm1pY3Jvc29mdC5jb20vanNvbi1zY2hlbWFzL2ZhYnJpYy9naXRJbnRlZ3JhdGlvbi9wbGF0Zm9ybVByb3BlcnRpZXMvMi4wLjAvc2NoZW1hLmpzb24iLAogICJtZXRhZGF0YSI6IHsKICAgICJ0eXBlIjogIkV2ZW50c3RyZWFtIiwKICAgICJkaXNwbGF5TmFtZSI6ICJldXJvd2F0ZXItaW5nZXN0IgogIH0sCiAgImNvbmZpZyI6IHsKICAgICJ2ZXJzaW9uIjogIjIuMCIsCiAgICAibG9naWNhbElkIjogIjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIKICB9Cn0="
                payloadType = "InlineBase64"
            }
        )
    }
} | ConvertTo-Json -Depth 10 -Compress

Write-Host "Definition payload size: $($definitionPayload.Length) bytes"

# Get token
$token = (az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv)

# Call updateDefinition
$uri = "https://api.fabric.microsoft.com/v1/workspaces/$WorkspaceId/eventstreams/$EventstreamId/updateDefinition"
Write-Host "POST $uri"

$response = Invoke-WebRequest -Uri $uri -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body $definitionPayload -UseBasicParsing

Write-Host "Status: $($response.StatusCode)"
Write-Host "Headers:"
$response.Headers | Format-List
if ($response.Content) {
    Write-Host "Body: $($response.Content)"
}
