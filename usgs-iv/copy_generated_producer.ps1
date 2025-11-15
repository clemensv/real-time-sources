# Copy generated producer files to usgs_iv/usgs_iv_producer

Write-Host "Copying generated producer files..." -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceDir = Join-Path $scriptDir "usgs_iv_producer" "usgs-iv-producer_kafka_producer" "src" "usgs-iv-producer_kafka_producer"
$dataSourceDir = Join-Path $scriptDir "usgs_iv_producer" "usgs-iv-producer_data" "src" "usgs-iv-producer_data"
$targetDir = Join-Path $scriptDir "usgs_iv" "usgs_iv_producer"

# Ensure target directory exists
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

# Copy producer.py as producer_client.py
$producerFile = Join-Path $sourceDir "producer.py"
$targetProducerFile = Join-Path $targetDir "producer_client.py"
if (Test-Path $producerFile) {
    Copy-Item -Path $producerFile -Destination $targetProducerFile -Force
    Write-Host "  ✓ Producer client copied" -ForegroundColor Green
}

# Copy data models (all directories under data source)
if (Test-Path $dataSourceDir) {
    $dataDirs = Get-ChildItem -Path $dataSourceDir -Directory
    foreach ($dir in $dataDirs) {
        $targetDataDir = Join-Path $targetDir $dir.Name
        Copy-Item -Path $dir.FullName -Destination $targetDataDir -Recurse -Force
        Write-Host "  ✓ Data models copied: $($dir.Name)" -ForegroundColor Green
    }
}

# Copy __init__.py
$initFile = Join-Path $sourceDir "__init__.py"
$targetInitFile = Join-Path $targetDir "__init__.py"
if (Test-Path $initFile) {
    Copy-Item -Path $initFile -Destination $targetInitFile -Force
    Write-Host "  ✓ __init__.py copied" -ForegroundColor Green
}

Write-Host "`n✓ Producer files copied successfully" -ForegroundColor Green
Write-Host "Target directory: $targetDir" -ForegroundColor Gray
