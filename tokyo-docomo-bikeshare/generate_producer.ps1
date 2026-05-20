. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\tokyo-docomo-bikeshare.xreg.json"
$outputDir = Join-Path $projectRoot "tokyo_docomo_bikeshare_producer"

Write-Host "Generating Tokyo Docomo Bikeshare producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate --style kafkaproducer --language py --projectname tokyo-docomo-bikeshare-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}
