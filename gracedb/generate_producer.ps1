# Generate GraceDB producer from xRegistry definitions

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

Write-Host "Generating GraceDB producer from xRegistry definitions..." -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "gracedb.xreg.json"
$outputDir = Join-Path $scriptDir "gracedb_producer"

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
xrcg generate --style kafkaproducer --language py --projectname gracedb-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nProducer generation completed successfully" -ForegroundColor Green
} else {
    Write-Host "`nProducer generation failed" -ForegroundColor Red
    exit $LASTEXITCODE
}
