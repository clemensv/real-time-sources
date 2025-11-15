# Generate USGS IV producer from xRegistry definitions

Write-Host "Generating USGS IV producer from xRegistry definitions..." -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg" "usgs_iv.xreg.json"
$outputDir = Join-Path $scriptDir "usgs_iv_producer"

Write-Host "xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "Output directory: $outputDir" -ForegroundColor Gray

# Check if xreg file exists
if (-not (Test-Path $xregFile)) {
    Write-Host "Error: xRegistry file not found: $xregFile" -ForegroundColor Red
    exit 1
}

# Remove old output if it exists
if (Test-Path $outputDir) {
    Write-Host "Removing existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

# Generate producer code
Write-Host "Generating Kafka producer code..." -ForegroundColor Cyan
xregistry generate --style kafkaproducer --language py --projectname usgs-iv-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Producer generation completed successfully" -ForegroundColor Green
} else {
    Write-Host "`n✗ Producer generation failed" -ForegroundColor Red
    exit $LASTEXITCODE
}
