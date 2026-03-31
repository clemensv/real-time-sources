$ErrorActionPreference = "Stop"

# Get current (original) definition
$token = (az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv)
$wsId = "<your-workspace-id>"
$esId = "<your-eventstream-id>"

Write-Host "Fetching current definition..."
$defResp = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/getDefinition" -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body "{}"

$esPart = $defResp.definition.parts | Where-Object { $_.path -eq "eventstream.json" }
$esJsonRaw = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($esPart.payload))
Write-Host "Original JSON length: $($esJsonRaw.Length)"

# Find and extract the current SQL query value from the raw JSON
$queryKeyIdx = $esJsonRaw.IndexOf('"query"')
$valueStartIdx = $esJsonRaw.IndexOf('"', $queryKeyIdx + 7) + 1
$i = $valueStartIdx
while ($i -lt $esJsonRaw.Length) {
    if ($esJsonRaw[$i] -eq '\' -and $i + 1 -lt $esJsonRaw.Length) { $i += 2; continue }
    if ($esJsonRaw[$i] -eq '"') { break }
    $i++
}
$valueEndIdx = $i
$currentEscapedSQL = $esJsonRaw.Substring($valueStartIdx, $valueEndIdx - $valueStartIdx)
Write-Host "Current escaped SQL length: $($currentEscapedSQL.Length)"

# Add ONLY station support for NO, FI, CH - minimal change
# In the stations query, add WHEN clauses before ELSE NULL and types to WHERE IN

# station_id CASE: add before "ELSE NULL\r\n    END AS station_id"
$currentEscapedSQL = $currentEscapedSQL.Replace(
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station'\r\n            THEN CONCAT('be-', data.station_no)\r\n        ELSE NULL\r\n    END AS station_id",
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station'\r\n            THEN CONCAT('be-', data.station_no)\r\n        WHEN type = 'NO.NVE.Hydrology.Station'\r\n            THEN CONCAT('no-', data.station_id)\r\n        WHEN type = 'FI.SYKE.Hydrology.Station'\r\n            THEN CONCAT('fi-', data.station_id)\r\n        WHEN type = 'CH.BAFU.Hydrology.Station'\r\n            THEN CONCAT('ch-', data.station_id)\r\n        ELSE NULL\r\n    END AS station_id"
)

# country_code CASE: add before ELSE NULL
$currentEscapedSQL = $currentEscapedSQL.Replace(
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN 'be'\r\n        ELSE NULL\r\n    END AS country_code",
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN 'be'\r\n        WHEN type = 'NO.NVE.Hydrology.Station' THEN 'no'\r\n        WHEN type = 'FI.SYKE.Hydrology.Station' THEN 'fi'\r\n        WHEN type = 'CH.BAFU.Hydrology.Station' THEN 'ch'\r\n        ELSE NULL\r\n    END AS country_code"
)

# source_station_id CASE
$currentEscapedSQL = $currentEscapedSQL.Replace(
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.station_no\r\n        ELSE NULL\r\n    END AS source_station_id",
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.station_no\r\n        WHEN type = 'NO.NVE.Hydrology.Station' THEN data.station_id\r\n        WHEN type = 'FI.SYKE.Hydrology.Station' THEN data.station_id\r\n        WHEN type = 'CH.BAFU.Hydrology.Station' THEN data.station_id\r\n        ELSE NULL\r\n    END AS source_station_id"
)

# station_name CASE
$currentEscapedSQL = $currentEscapedSQL.Replace(
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.station_name\r\n        ELSE NULL\r\n    END AS station_name",
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.station_name\r\n        WHEN type = 'NO.NVE.Hydrology.Station' THEN data.station_name\r\n        WHEN type = 'FI.SYKE.Hydrology.Station' THEN data.name\r\n        WHEN type = 'CH.BAFU.Hydrology.Station' THEN data.name\r\n        ELSE NULL\r\n    END AS station_name"
)

# river_name CASE
$currentEscapedSQL = $currentEscapedSQL.Replace(
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.river_name\r\n        ELSE NULL\r\n    END AS river_name",
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN data.river_name\r\n        WHEN type = 'NO.NVE.Hydrology.Station' THEN data.river_name\r\n        WHEN type = 'FI.SYKE.Hydrology.Station' THEN data.river_name\r\n        WHEN type = 'CH.BAFU.Hydrology.Station' THEN data.water_body_name\r\n        ELSE NULL\r\n    END AS river_name"
)

# source_system CASE
$currentEscapedSQL = $currentEscapedSQL.Replace(
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN 'waterinfo-vmm'\r\n        ELSE NULL\r\n    END AS source_system",
    "WHEN type = 'BE.Vlaanderen.Waterinfo.VMM.Station' THEN 'waterinfo-vmm'\r\n        WHEN type = 'NO.NVE.Hydrology.Station' THEN 'nve-hydro'\r\n        WHEN type = 'FI.SYKE.Hydrology.Station' THEN 'syke-hydro'\r\n        WHEN type = 'CH.BAFU.Hydrology.Station' THEN 'bafu-hydro'\r\n        ELSE NULL\r\n    END AS source_system"
)

# WHERE IN list: add the 3 new types
$currentEscapedSQL = $currentEscapedSQL.Replace(
    "'BE.Vlaanderen.Waterinfo.VMM.Station'\r\n)",
    "'BE.Vlaanderen.Waterinfo.VMM.Station',\r\n    'NO.NVE.Hydrology.Station',\r\n    'FI.SYKE.Hydrology.Station',\r\n    'CH.BAFU.Hydrology.Station'\r\n)"
)

Write-Host "New escaped SQL length: $($currentEscapedSQL.Length)"

# Put back in the JSON
$newJsonRaw = $esJsonRaw.Substring(0, $valueStartIdx) + $currentEscapedSQL + $esJsonRaw.Substring($valueEndIdx)

# Verify
try {
    $parsed = $newJsonRaw | ConvertFrom-Json
    Write-Host "JSON valid. SQL length: $($parsed.operators[0].properties.query.Length)"
    Write-Host "Has NO.NVE: $($parsed.operators[0].properties.query -match 'NO.NVE')"
} catch {
    Write-Host "ERROR: Invalid JSON: $_"
    exit 1
}

# Base64 encode and build payload
$newBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($newJsonRaw))
$otherParts = $defResp.definition.parts | Where-Object { $_.path -ne "eventstream.json" }
$partsArray = @(@{ path = "eventstream.json"; payload = $newBase64; payloadType = "InlineBase64" })
foreach ($p in $otherParts) { $partsArray += @{ path = $p.path; payload = $p.payload; payloadType = $p.payloadType } }
$payload = @{ definition = @{ parts = $partsArray } } | ConvertTo-Json -Depth 5 -Compress

Write-Host "Payload size: $($payload.Length)"

# Push
$uri = "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/updateDefinition"
Write-Host "POST $uri"
$response = Invoke-WebRequest -Uri $uri -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body $payload -UseBasicParsing
Write-Host "Status: $($response.StatusCode)"
