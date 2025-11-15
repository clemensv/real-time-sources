# Copy generated producer files to the main noaa package

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$generatedProducerSrc = Join-Path $scriptDir "noaa_producer\noaa-producer_kafka_producer\src\noaa-producer_kafka_producer"
$generatedDataSrc = Join-Path $scriptDir "noaa_producer\noaa-producer_data\src\noaa-producer_data"
$targetProducerDir = Join-Path $scriptDir "noaa\noaa_producer"

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

# Copy the data models (microsoft/ directory structure)
$generatedMicrosoftDir = Join-Path $generatedDataSrc "microsoft"
$targetMicrosoftDir = Join-Path $targetProducerDir "microsoft"

if (Test-Path $generatedMicrosoftDir) {
    Write-Host "  Copying data models..." -ForegroundColor Gray
    
    # Remove existing microsoft directory
    if (Test-Path $targetMicrosoftDir) {
        Remove-Item -Path $targetMicrosoftDir -Recurse -Force
    }
    
    # Copy the new one
    Copy-Item -Path $generatedMicrosoftDir -Destination $targetMicrosoftDir -Recurse -Force
    Write-Host "  ✓ Data models copied" -ForegroundColor Green
} else {
    Write-Host "  ✗ Microsoft directory not found: $generatedMicrosoftDir" -ForegroundColor Red
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
