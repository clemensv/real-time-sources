# Generate NASA FIRMS Kafka producer from xRegistry definitions

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

Write-Host "Generating NASA FIRMS producer from xRegistry definitions..." -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "nasa_firms.xreg.json"
$outputDir = Join-Path $scriptDir "nasa_firms_producer"

if (-not (Test-Path $xregFile)) {
    Write-Host "Error: xRegistry file not found: $xregFile" -ForegroundColor Red
    exit 1
}
if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}
xrcg generate --style kafkaproducer --language py --projectname nasa-firms-producer --definitions $xregFile --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Producer generation completed" -ForegroundColor Green

