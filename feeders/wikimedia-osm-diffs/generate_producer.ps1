# Generate the Wikimedia OSM Diffs producer using xrcg

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\wikimedia_osm_diffs.xreg.json"
$outputDir = Join-Path $projectRoot "wikimedia_osm_diffs_producer"

Write-Host "Generating Wikimedia OSM Diffs producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate --style kafkaproducer --language py --projectname wikimedia-osm-diffs-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Review the generated code in: $outputDir" -ForegroundColor Gray
    Write-Host "  2. Install dependencies: pip install ." -ForegroundColor Gray
    Write-Host "  3. Run the bridge: python -m wikimedia_osm_diffs feed" -ForegroundColor Gray
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
}
