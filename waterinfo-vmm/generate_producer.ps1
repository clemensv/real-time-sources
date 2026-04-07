$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$XREG_ROOT = Join-Path $PSScriptRoot "xreg"
$SCHEMA_FILE = Join-Path $XREG_ROOT "waterinfo_vmm.xreg.json"
$OUTPUT_DIR = Join-Path $PSScriptRoot "waterinfo_vmm_producer"

Write-Host "Generating producer from $SCHEMA_FILE"
xrcg generate `
    --style kafkaproducer `
    --language py `
    --projectname waterinfo_vmm_producer `
    --definitions $SCHEMA_FILE `
    --output $OUTPUT_DIR

Write-Host "Generation complete. Output in $OUTPUT_DIR"
