# Generate the Hub'Eau Hydrometrie producer using xrcg

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\hubeau_hydrometrie.xreg.json"
$outputDir = Join-Path $scriptDir "hubeau_hydrometrie_producer"

Write-Host "Generating Hub'Eau Hydrometrie producer from xRegistry definitions..." -ForegroundColor Cyan

if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate --style kafkaproducer --language py --projectname hubeau-hydrometrie-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
