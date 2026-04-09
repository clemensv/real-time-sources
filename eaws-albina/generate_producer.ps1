# Generate the EAWS ALBINA Avalanche Bulletins producer using xrcg

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\eaws_albina.xreg.json"
$outputDir = Join-Path $projectRoot "eaws_albina_producer"

Write-Host "Generating EAWS ALBINA producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

# Ensure the output directory exists
if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

# Generate the Kafka producer code
Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate --style kafkaproducer --language py --projectname eaws-albina-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Install dependencies: pip install ." -ForegroundColor Gray
    Write-Host "  2. Run the poller: python -m eaws_albina" -ForegroundColor Gray
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
