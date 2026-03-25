$ErrorActionPreference = 'Stop'

$SRC = Join-Path $PSScriptRoot "waterinfo_vmm_producer_tmp"
$DST = Join-Path $PSScriptRoot "waterinfo_vmm" "waterinfo_vmm_producer"

if (Test-Path $SRC) {
    Copy-Item -Path "$SRC\*" -Destination $DST -Recurse -Force
    Write-Host "Copied generated producer to $DST"
} else {
    Write-Host "Source directory not found: $SRC"
}
