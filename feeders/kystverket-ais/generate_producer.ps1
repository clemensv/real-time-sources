# Generate the Kystverket AIS data producer using xrcg

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\kystverket-ais.xreg.json"
$outputDir = Join-Path $projectRoot "kystverket_ais_producer"

Write-Host "Generating Kystverket AIS producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

# Ensure the output directory exists
if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

# Generate the Kafka producer code
Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate --style kafkaproducer --language py --projectname kystverket_ais-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Review the generated code in: $outputDir" -ForegroundColor Gray
    Write-Host "  2. Install dependencies: poetry install" -ForegroundColor Gray
    Write-Host "  3. Run the producer: poetry run python -m kystverket_ais" -ForegroundColor Gray
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
}


xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\kystverket-ais.xreg.json `
    --endpoint NO.Kystverket.AIS.Amqp `
    --projectname kystverket_ais_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output kystverket_ais_amqp_producer

Convert-GeneratedPyprojects
