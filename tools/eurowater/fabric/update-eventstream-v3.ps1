$ErrorActionPreference = "Stop"

# Get current definition
$token = (az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv)
$wsId = "c98acd97-4363-4296-8323-b6ab21e53903"
$esId = "cc28e604-8cc8-4771-affb-13cb0a683c8f"

Write-Host "Fetching current definition..."
$defResp = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/getDefinition" -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body "{}"

$esPart = $defResp.definition.parts | Where-Object { $_.path -eq "eventstream.json" }
$esJsonRaw = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($esPart.payload))
Write-Host "Original JSON length: $($esJsonRaw.Length)"

# Find the query value boundaries in the raw JSON
# The JSON has: "query": "SELECT\r\n..."
$queryKeyIdx = $esJsonRaw.IndexOf('"query"')
Write-Host "query key at index: $queryKeyIdx"

# Find the opening quote of the value
$valueStartIdx = $esJsonRaw.IndexOf('"', $queryKeyIdx + 7) # skip "query" and colon/spaces
$valueStartIdx++ # move past the opening quote

# Find the closing quote - need to handle escaped quotes
$i = $valueStartIdx
$depth = 0
while ($i -lt $esJsonRaw.Length) {
    if ($esJsonRaw[$i] -eq '\' -and $i + 1 -lt $esJsonRaw.Length) {
        $i += 2 # skip escaped character
        continue
    }
    if ($esJsonRaw[$i] -eq '"') {
        break # found unescaped closing quote
    }
    $i++
}
$valueEndIdx = $i
$currentValueEscaped = $esJsonRaw.Substring($valueStartIdx, $valueEndIdx - $valueStartIdx)
Write-Host "Current query value (escaped) length: $($currentValueEscaped.Length)"

# Build new SQL
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$stationsSQL = Get-Content "$scriptDir\normalize_stations.sql" -Raw
$measurementsSQL = Get-Content "$scriptDir\normalize_measurements.sql" -Raw

# Remove SQL comments
$stationsSQL = ($stationsSQL -split "`n" | Where-Object { $_ -notmatch '^\s*--' }) -join "`r`n"
$measurementsSQL = ($measurementsSQL -split "`n" | Where-Object { $_ -notmatch '^\s*--' }) -join "`r`n"

# Replace EventInput -> [eurowater-ingest-stream]
$stationsSQL = $stationsSQL -replace 'FROM EventInput', 'FROM [eurowater-ingest-stream]'
$measurementsSQL = $measurementsSQL -replace 'FROM EventInput', 'FROM [eurowater-ingest-stream]'

# Remove blank lines
$stationsSQL = ($stationsSQL -split "`r?`n" | Where-Object { $_.Trim() -ne '' }) -join "`r`n"
$measurementsSQL = ($measurementsSQL -split "`r?`n" | Where-Object { $_.Trim() -ne '' }) -join "`r`n"

$newSQL = $stationsSQL + "`r`n" + $measurementsSQL
Write-Host "New SQL length: $($newSQL.Length)"

# JSON-escape the new SQL to match the format in the raw JSON
# newlines -> \r\n, tabs -> \t, etc.
$newValueEscaped = $newSQL -replace '\\', '\\' -replace '"', '\"' -replace "`r`n", '\r\n' -replace "`n", '\n' -replace "`r", '\r' -replace "`t", '\t'
Write-Host "New query value (escaped) length: $($newValueEscaped.Length)"

# Replace in the raw JSON
$newJsonRaw = $esJsonRaw.Substring(0, $valueStartIdx) + $newValueEscaped + $esJsonRaw.Substring($valueEndIdx)
Write-Host "New JSON length: $($newJsonRaw.Length)"

# Verify JSON is valid
try {
    $parsed = $newJsonRaw | ConvertFrom-Json
    $newQueryLen = $parsed.operators[0].properties.query.Length
    Write-Host "Parsed OK. New query in parsed JSON: $newQueryLen chars"
    if ($parsed.operators[0].properties.query -match 'NO.NVE') {
        Write-Host "Contains NO.NVE: YES"
    } else {
        Write-Host "Contains NO.NVE: NO"
    }
} catch {
    Write-Host "ERROR: Invalid JSON: $_"
    exit 1
}

# Base64 encode
$newBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($newJsonRaw))

# Build update payload using the original parts for other files
$otherParts = $defResp.definition.parts | Where-Object { $_.path -ne "eventstream.json" }

$partsArray = @()
$partsArray += @{ path = "eventstream.json"; payload = $newBase64; payloadType = "InlineBase64" }
foreach ($p in $otherParts) {
    $partsArray += @{ path = $p.path; payload = $p.payload; payloadType = $p.payloadType }
}

$payload = @{
    definition = @{
        parts = $partsArray
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Host "Update payload size: $($payload.Length)"

# Push the update
$uri = "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/updateDefinition"
Write-Host "POST $uri"
$response = Invoke-WebRequest -Uri $uri -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body $payload -UseBasicParsing
Write-Host "Status: $($response.StatusCode)"
