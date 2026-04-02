$ErrorActionPreference = "Stop"

# Get current definition (has stations-only changes)
$token = (az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv)
$wsId = $args[0]
$esId = $args[1]
if (-not $wsId -or -not $esId) { throw "Usage: .\update-eventstream-add-measurements.ps1 <workspace-id> <eventstream-id>" }

Write-Host "Fetching current definition..."
$defResp = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/getDefinition" -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body "{}"

$esPart = $defResp.definition.parts | Where-Object { $_.path -eq "eventstream.json" }
$esJsonRaw = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($esPart.payload))
Write-Host "Current JSON length: $($esJsonRaw.Length)"

# Find SQL query boundaries
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

# Add measurement UNION ALL blocks for all 3 countries
# Append before the final semicolon of the measurements query
# The current SQL ends with: ...WHERE type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading';\r
# We need to add UNION ALL blocks before the semicolon

$newMeasurements = @"
\r\nUNION ALL\r\nSELECT\r\n    CONCAT('no-', data.station_id)            AS station_id,\r\n    'no'                                       AS country_code,\r\n    data.water_level_timestamp                 AS [timestamp],\r\n    'water_level'                              AS parameter,\r\n    data.water_level                           AS value,\r\n    data.water_level_unit                      AS unit,\r\n    NULL                                       AS quality,\r\n    'nve-hydro'                                AS source_system,\r\n    'EU.Eurowater.Measurement'                 AS [__ce_type]\r\nFROM [eurowater-ingest-stream]\r\nWHERE type = 'NO.NVE.Hydrology.WaterLevelObservation'\r\n    AND data.water_level_timestamp IS NOT NULL\r\n    AND data.water_level_timestamp <> ''\r\nUNION ALL\r\nSELECT\r\n    CONCAT('no-', data.station_id)            AS station_id,\r\n    'no'                                       AS country_code,\r\n    data.discharge_timestamp                   AS [timestamp],\r\n    'discharge'                                AS parameter,\r\n    data.discharge                             AS value,\r\n    data.discharge_unit                        AS unit,\r\n    NULL                                       AS quality,\r\n    'nve-hydro'                                AS source_system,\r\n    'EU.Eurowater.Measurement'                 AS [__ce_type]\r\nFROM [eurowater-ingest-stream]\r\nWHERE type = 'NO.NVE.Hydrology.WaterLevelObservation'\r\n    AND data.discharge_timestamp IS NOT NULL\r\n    AND data.discharge_timestamp <> ''\r\nUNION ALL\r\nSELECT\r\n    CONCAT('fi-', data.station_id)            AS station_id,\r\n    'fi'                                       AS country_code,\r\n    data.water_level_timestamp                 AS [timestamp],\r\n    'water_level'                              AS parameter,\r\n    data.water_level                           AS value,\r\n    data.water_level_unit                      AS unit,\r\n    NULL                                       AS quality,\r\n    'syke-hydro'                               AS source_system,\r\n    'EU.Eurowater.Measurement'                 AS [__ce_type]\r\nFROM [eurowater-ingest-stream]\r\nWHERE type = 'FI.SYKE.Hydrology.WaterLevelObservation'\r\n    AND data.water_level_timestamp IS NOT NULL\r\n    AND data.water_level_timestamp <> ''\r\nUNION ALL\r\nSELECT\r\n    CONCAT('fi-', data.station_id)            AS station_id,\r\n    'fi'                                       AS country_code,\r\n    data.discharge_timestamp                   AS [timestamp],\r\n    'discharge'                                AS parameter,\r\n    data.discharge                             AS value,\r\n    data.discharge_unit                        AS unit,\r\n    NULL                                       AS quality,\r\n    'syke-hydro'                               AS source_system,\r\n    'EU.Eurowater.Measurement'                 AS [__ce_type]\r\nFROM [eurowater-ingest-stream]\r\nWHERE type = 'FI.SYKE.Hydrology.WaterLevelObservation'\r\n    AND data.discharge_timestamp IS NOT NULL\r\n    AND data.discharge_timestamp <> ''\r\nUNION ALL\r\nSELECT\r\n    CONCAT('ch-', data.station_id)            AS station_id,\r\n    'ch'                                       AS country_code,\r\n    data.water_level_timestamp                 AS [timestamp],\r\n    'water_level'                              AS parameter,\r\n    data.water_level                           AS value,\r\n    data.water_level_unit                      AS unit,\r\n    NULL                                       AS quality,\r\n    'bafu-hydro'                               AS source_system,\r\n    'EU.Eurowater.Measurement'                 AS [__ce_type]\r\nFROM [eurowater-ingest-stream]\r\nWHERE type = 'CH.BAFU.Hydrology.WaterLevelObservation'\r\n    AND data.water_level_timestamp IS NOT NULL\r\n    AND data.water_level_timestamp <> ''\r\nUNION ALL\r\nSELECT\r\n    CONCAT('ch-', data.station_id)            AS station_id,\r\n    'ch'                                       AS country_code,\r\n    data.discharge_timestamp                   AS [timestamp],\r\n    'discharge'                                AS parameter,\r\n    data.discharge                             AS value,\r\n    data.discharge_unit                        AS unit,\r\n    NULL                                       AS quality,\r\n    'bafu-hydro'                               AS source_system,\r\n    'EU.Eurowater.Measurement'                 AS [__ce_type]\r\nFROM [eurowater-ingest-stream]\r\nWHERE type = 'CH.BAFU.Hydrology.WaterLevelObservation'\r\n    AND data.discharge_timestamp IS NOT NULL\r\n    AND data.discharge_timestamp <> ''\r\nUNION ALL\r\nSELECT\r\n    CONCAT('ch-', data.station_id)            AS station_id,\r\n    'ch'                                       AS country_code,\r\n    data.water_temperature_timestamp           AS [timestamp],\r\n    'water_temperature'                        AS parameter,\r\n    data.water_temperature                     AS value,\r\n    data.water_temperature_unit                AS unit,\r\n    NULL                                       AS quality,\r\n    'bafu-hydro'                               AS source_system,\r\n    'EU.Eurowater.Measurement'                 AS [__ce_type]\r\nFROM [eurowater-ingest-stream]\r\nWHERE type = 'CH.BAFU.Hydrology.WaterLevelObservation'\r\n    AND data.water_temperature_timestamp IS NOT NULL\r\n    AND data.water_temperature_timestamp <> ''
"@

# Insert before the final semicolon
$currentEscapedSQL = $currentEscapedSQL.Replace(
    "WHERE type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading';\r",
    "WHERE type = 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading'" + $newMeasurements + ";\r"
)

Write-Host "New escaped SQL length: $($currentEscapedSQL.Length)"

# Put back in JSON
$newJsonRaw = $esJsonRaw.Substring(0, $valueStartIdx) + $currentEscapedSQL + $esJsonRaw.Substring($valueEndIdx)

# Verify
try {
    $parsed = $newJsonRaw | ConvertFrom-Json
    $qLen = $parsed.operators[0].properties.query.Length
    Write-Host "JSON valid. SQL length: $qLen"
    Write-Host "Has NO.NVE.Hydrology.WaterLevelObservation: $($parsed.operators[0].properties.query -match 'NO.NVE.Hydrology.WaterLevelObservation')"
    Write-Host "Has CH.BAFU.Hydrology.WaterLevelObservation: $($parsed.operators[0].properties.query -match 'CH.BAFU.Hydrology.WaterLevelObservation')"
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
$uri = "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/updateDefinition"
Write-Host "POST $uri"
$response = Invoke-WebRequest -Uri $uri -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body $payload -UseBasicParsing
Write-Host "Status: $($response.StatusCode)"
