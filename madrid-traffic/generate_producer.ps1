$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "madrid_traffic.xreg.json"
$outputDir = Join-Path $scriptDir "madrid_traffic_producer"

Write-Host "Generating Madrid Traffic producer from $xregFile"

if (-not (Test-Path $xregFile)) {
    throw "xRegistry file not found: $xregFile"
}

if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate `
    --style kafkaproducer `
    --language py `
    --projectname madrid-traffic-producer `
    --definitions $xregFile `
    --output $outputDir

if ($LASTEXITCODE -ne 0) {
    throw "Producer generation failed"
}

Write-Host "Producer generated successfully in $outputDir"
