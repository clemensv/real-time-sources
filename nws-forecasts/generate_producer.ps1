. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\nws_forecasts.xreg.json"
$outputDir = Join-Path $projectRoot "nws_forecasts_producer"

Write-Host "Generating NWS Forecasts producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname nws_forecasts_producer --output $outputDir

if ($LASTEXITCODE -ne 0) {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Producer generation completed successfully." -ForegroundColor Green
