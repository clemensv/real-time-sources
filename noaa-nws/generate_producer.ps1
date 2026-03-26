# Generate the NOAA NWS Weather Alerts producer using xrcg

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\noaa_nws.xreg.json"
$outputDir = Join-Path $projectRoot "noaa_nws_producer"

Write-Host "Generating NOAA NWS producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

# Ensure the output directory exists
if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

# Generate the Kafka producer code
Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate --style kafkaproducer --language py --projectname noaa-nws-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run copy_generated_producer.ps1 to copy files into the main package" -ForegroundColor Gray
    Write-Host "  2. Run fix_imports.ps1 to fix generated import paths" -ForegroundColor Gray
    Write-Host "  3. Install dependencies: pip install ." -ForegroundColor Gray
    Write-Host "  4. Run the poller: python -m noaa_nws" -ForegroundColor Gray
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
