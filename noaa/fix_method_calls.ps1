# Fix method calls in noaa.py to match generated producer client

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$noaaFile = Join-Path $scriptDir "noaa" "noaa.py"

Write-Host "Fixing producer method calls in noaa.py..." -ForegroundColor Cyan

$content = Get-Content -Path $noaaFile -Raw

# Map old method names to new method names
$methodMappings = @{
    'send_microsoft_opendata_us_noaa_station' = 'send_microsoft_open_data_us_noaa_station'
    'send_microsoft_opendata_us_noaa_waterlevel' = 'send_microsoft_open_data_us_noaa_water_level'
    'send_microsoft_opendata_us_noaa_predictions' = 'send_microsoft_open_data_us_noaa_predictions'
    'send_microsoft_opendata_us_noaa_airtemperature' = 'send_microsoft_open_data_us_noaa_air_temperature'
    'send_microsoft_opendata_us_noaa_wind' = 'send_microsoft_open_data_us_noaa_wind'
    'send_microsoft_opendata_us_noaa_airpressure' = 'send_microsoft_open_data_us_noaa_air_pressure'
    'send_microsoft_opendata_us_noaa_watertemperature' = 'send_microsoft_open_data_us_noaa_water_temperature'
    'send_microsoft_opendata_us_noaa_conductivity' = 'send_microsoft_open_data_us_noaa_conductivity'
    'send_microsoft_opendata_us_noaa_visibility' = 'send_microsoft_open_data_us_noaa_visibility'
    'send_microsoft_opendata_us_noaa_humidity' = 'send_microsoft_open_data_us_noaa_humidity'
    'send_microsoft_opendata_us_noaa_salinity' = 'send_microsoft_open_data_us_noaa_salinity'
}

$fixCount = 0
foreach ($old in $methodMappings.Keys) {
    $new = $methodMappings[$old]
    if ($content -match $old) {
        $content = $content -replace $old, $new
        Write-Host "  Fixed: $old -> $new" -ForegroundColor Gray
        $fixCount++
    }
}

Set-Content -Path $noaaFile -Value $content -NoNewline

Write-Host ""
Write-Host "✓ Fixed $fixCount method calls" -ForegroundColor Green
