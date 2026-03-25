# Copy generated producer files to the main uk_ea_flood_monitoring package

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$generatedProducerSrc = Join-Path $scriptDir "uk_ea_flood_monitoring_producer\uk-ea-flood-monitoring-producer_kafka_producer\src\uk-ea-flood-monitoring-producer_kafka_producer"
$generatedDataSrc = Join-Path $scriptDir "uk_ea_flood_monitoring_producer\uk-ea-flood-monitoring-producer_data\src\uk-ea-flood-monitoring-producer_data"
$targetProducerDir = Join-Path $scriptDir "uk_ea_flood_monitoring\uk_ea_flood_monitoring_producer"

Write-Host "Copying generated producer files..." -ForegroundColor Cyan

# Copy the producer client
$producerFile = Join-Path $generatedProducerSrc "producer.py"
$targetProducerFile = Join-Path $targetProducerDir "producer_client.py"

if (Test-Path $producerFile) {
    Write-Host "  Copying producer_client.py..." -ForegroundColor Gray
    Copy-Item -Path $producerFile -Destination $targetProducerFile -Force
    Write-Host "  ✓ Producer client copied" -ForegroundColor Green
} else {
    Write-Host "  ✗ Producer file not found: $producerFile" -ForegroundColor Red
}

# Copy the data models (uk/ directory structure)
$generatedUkDir = Join-Path $generatedDataSrc "uk"
$targetUkDir = Join-Path $targetProducerDir "uk"

if (Test-Path $generatedUkDir) {
    Write-Host "  Copying data models..." -ForegroundColor Gray

    # Remove existing uk directory
    if (Test-Path $targetUkDir) {
        Remove-Item -Path $targetUkDir -Recurse -Force
    }

    # Copy the new one
    Copy-Item -Path $generatedUkDir -Destination $targetUkDir -Recurse -Force
    Write-Host "  ✓ Data models copied" -ForegroundColor Green
} else {
    Write-Host "  ✗ UK directory not found: $generatedUkDir" -ForegroundColor Red
}

# Copy __init__.py from generated data
$generatedDataInit = Join-Path $generatedDataSrc "__init__.py"
$targetProducerInit = Join-Path $targetProducerDir "__init__.py"

if (Test-Path $generatedDataInit) {
    Write-Host "  Copying __init__.py..." -ForegroundColor Gray
    Copy-Item -Path $generatedDataInit -Destination $targetProducerInit -Force
    Write-Host "  ✓ __init__.py copied" -ForegroundColor Green
}

Write-Host ""
Write-Host "✓ Producer files copied successfully" -ForegroundColor Green
Write-Host ""
Write-Host "Generated files location: $targetProducerDir" -ForegroundColor Cyan
