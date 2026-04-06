$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "autobahn.xreg.json"
$outputDir = Join-Path $scriptDir "autobahn_producer"

Write-Host "Generating Autobahn producer from $xregFile"

if (-not (Test-Path $xregFile)) {
    throw "xRegistry file not found: $xregFile"
}

if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate `
    --style kafkaproducer `
    --language py `
    --projectname autobahn-producer `
    --definitions $xregFile `
    --output $outputDir

if ($LASTEXITCODE -ne 0) {
    throw "Producer generation failed"
}

Write-Host "Generation complete. Output in $outputDir" -ForegroundColor Green