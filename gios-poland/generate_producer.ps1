. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\gios_poland.xreg.json"
$outputDir = Join-Path $projectRoot "gios_poland_producer"

Write-Host "Generating GIOS Poland producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate --style kafkaproducer --language py --projectname gios-poland-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run copy_generated_producer.ps1 to copy files into the main package" -ForegroundColor Gray
    Write-Host "  2. Run fix_imports.ps1 to fix generated import paths" -ForegroundColor Gray
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}
