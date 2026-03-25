# Copy generated producer files to the main hubeau_hydrometrie package

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$generatedProducerSrc = Join-Path $scriptDir "hubeau_hydrometrie_producer\hubeau-hydrometrie-producer_kafka_producer\src\hubeau-hydrometrie-producer_kafka_producer"
$generatedDataSrc = Join-Path $scriptDir "hubeau_hydrometrie_producer\hubeau-hydrometrie-producer_data\src\hubeau-hydrometrie-producer_data"
$targetProducerDir = Join-Path $scriptDir "hubeau_hydrometrie\hubeau_hydrometrie_producer"

Write-Host "Copying generated producer files..." -ForegroundColor Cyan

$producerFile = Join-Path $generatedProducerSrc "producer.py"
$targetProducerFile = Join-Path $targetProducerDir "producer_client.py"
if (Test-Path $producerFile) {
    Copy-Item -Path $producerFile -Destination $targetProducerFile -Force
    Write-Host "  ✓ Producer client copied" -ForegroundColor Green
}

$generatedFrDir = Join-Path $generatedDataSrc "fr"
$targetFrDir = Join-Path $targetProducerDir "fr"
if (Test-Path $generatedFrDir) {
    if (Test-Path $targetFrDir) { Remove-Item -Path $targetFrDir -Recurse -Force }
    Copy-Item -Path $generatedFrDir -Destination $targetFrDir -Recurse -Force
    Write-Host "  ✓ Data models copied" -ForegroundColor Green
}

$generatedDataInit = Join-Path $generatedDataSrc "__init__.py"
$targetProducerInit = Join-Path $targetProducerDir "__init__.py"
if (Test-Path $generatedDataInit) {
    Copy-Item -Path $generatedDataInit -Destination $targetProducerInit -Force
}

Write-Host "✓ Producer files copied successfully" -ForegroundColor Green
