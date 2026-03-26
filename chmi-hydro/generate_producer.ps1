$ErrorActionPreference = 'Stop'

$XREG_ROOT = Join-Path $PSScriptRoot "xreg"
$SCHEMA_FILE = Join-Path $XREG_ROOT "chmi_hydro.xreg.json"
$OUTPUT_DIR = Join-Path $PSScriptRoot "chmi_hydro_producer_tmp"

Write-Host "Generating producer from $SCHEMA_FILE"
xregistry generate `
    --style kafkaproducer `
    --language py `
    --projectname chmi_hydro_producer `
    --definitions $SCHEMA_FILE `
    --output $OUTPUT_DIR

Write-Host "Generation complete. Output in $OUTPUT_DIR"