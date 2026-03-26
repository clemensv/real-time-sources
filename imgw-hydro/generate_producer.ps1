$ErrorActionPreference = 'Stop'

$XREG_ROOT = Join-Path $PSScriptRoot "xreg"
$SCHEMA_FILE = Join-Path $XREG_ROOT "imgw_hydro.xreg.json"
$OUTPUT_DIR = Join-Path $PSScriptRoot "imgw_hydro_producer_tmp"

Write-Host "Generating producer from $SCHEMA_FILE"
xrcg generate `
    --style kafkaproducer `
    --language py `
    --projectname imgw_hydro_producer `
    --definitions $SCHEMA_FILE `
    --output $OUTPUT_DIR

Write-Host "Generation complete. Output in $OUTPUT_DIR"