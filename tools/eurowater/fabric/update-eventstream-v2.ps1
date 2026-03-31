param(
    [string]$WorkspaceId = "c98acd97-4363-4296-8323-b6ab21e53903",
    [string]$EventstreamId = "cc28e604-8cc8-4771-affb-13cb0a683c8f"
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Get current definition from Fabric  
$token = (az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv)
$defResp = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces/$WorkspaceId/eventstreams/$EventstreamId/getDefinition" -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body "{}"

# Get the eventstream.json part and decode
$esPart = $defResp.definition.parts | Where-Object { $_.path -eq "eventstream.json" }
$esJson = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($esPart.payload))
Write-Host "Original JSON length: $($esJson.Length)"

# Parse JSON
$esObj = $esJson | ConvertFrom-Json

# Get current SQL
$currentSQL = $esObj.operators[0].properties.query
Write-Host "Current SQL length: $($currentSQL.Length)"

# Read our updated SQL files
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

# Combine into new query
$newSQL = $stationsSQL + "`r`n" + $measurementsSQL
Write-Host "New SQL length: $($newSQL.Length)"

# Do a simple string replacement in the raw JSON to preserve exact structure
$newJson = $esJson.Replace($currentSQL, $newSQL)
Write-Host "New JSON length: $($newJson.Length)"

# Verify the replacement worked
if ($newJson -eq $esJson -and $currentSQL -ne $newSQL) {
    Write-Host "ERROR: JSON replacement failed!"
    exit 1
}

# Base64 encode the new JSON
$newBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($newJson))

# Build the payload using the original parts for other files
$parts = @()
foreach ($part in $defResp.definition.parts) {
    if ($part.path -eq "eventstream.json") {
        $parts += @{
            path = "eventstream.json"
            payload = $newBase64
            payloadType = "InlineBase64"
        }
    } else {
        $parts += @{
            path = $part.path
            payload = $part.payload
            payloadType = $part.payloadType
        }
    }
}

$payload = @{
    definition = @{
        parts = $parts
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Host "Payload size: $($payload.Length) bytes"

# Call updateDefinition 
$uri = "https://api.fabric.microsoft.com/v1/workspaces/$WorkspaceId/eventstreams/$EventstreamId/updateDefinition"
Write-Host "POST $uri"

$response = Invoke-WebRequest -Uri $uri -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body $payload -UseBasicParsing

Write-Host "Status: $($response.StatusCode)"
if ($response.Content) {
    Write-Host "Body: $($response.Content)"
}
