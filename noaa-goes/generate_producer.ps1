$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\noaa_goes.xreg.json"
$outputDir = Join-Path $projectRoot "noaa_goes_producer"

Write-Host "Generating NOAA GOES/SWPC producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xregistry generate --style kafkaproducer --language py --projectname noaa-goes-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run copy_generated_producer.ps1" -ForegroundColor Gray
    Write-Host "  2. Run fix_imports.ps1" -ForegroundColor Gray
} else {
    Write-Host "✗ Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}
