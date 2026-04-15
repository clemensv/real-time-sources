$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$XREG_ROOT = Join-Path $PSScriptRoot "xreg"
$SCHEMA_FILE = Join-Path $XREG_ROOT "canada-eccc-wateroffice.xreg.json"
$OUTPUT_DIR = Join-Path $PSScriptRoot "canada_eccc_wateroffice_producer"

Write-Host "Generating producer from $SCHEMA_FILE"
xrcg generate `
    --style kafkaproducer `
    --language py `
    --projectname canada_eccc_wateroffice_producer `
    --definitions $SCHEMA_FILE `
    --output $OUTPUT_DIR

Write-Host "Generation complete. Output in $OUTPUT_DIR"
