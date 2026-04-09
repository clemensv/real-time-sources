$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "french_road_traffic.xreg.json"
$outputDir = Join-Path $scriptDir "french_road_traffic_producer"

Write-Host "Generating French Road Traffic producer from $xregFile"

if (-not (Test-Path $xregFile)) {
    throw "xRegistry file not found: $xregFile"
}

if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate `
    --style kafkaproducer `
    --language py `
    --projectname french-road-traffic-producer `
    --definitions $xregFile `
    --output $outputDir

if ($LASTEXITCODE -ne 0) {
    throw "Producer generation failed"
}

Write-Host "Producer generated successfully in $outputDir"
