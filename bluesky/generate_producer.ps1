# Generate the Bluesky firehose producer using xregistry

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\bluesky.xreg.json"
$outputDir = Join-Path $projectRoot "bluesky_producer"

Write-Host "Generating Bluesky producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

# Ensure the output directory exists
if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

# Generate the Kafka producer code
Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xregistry generate --style kafkaproducer --language py --projectname bluesky-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Review the generated code in: $outputDir" -ForegroundColor Gray
    Write-Host "  2. Install dependencies: poetry install" -ForegroundColor Gray
    Write-Host "  3. Run the producer: poetry run bluesky_firehose stream" -ForegroundColor Gray
} else {
    Write-Host "✗ Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
