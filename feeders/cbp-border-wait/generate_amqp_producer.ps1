$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Get-ChildItem (Join-Path $scriptDir "xreg") -Filter "*.xreg.json" | Select-Object -First 1 -ExpandProperty FullName
$outputDir = Join-Path $scriptDir "cbp_border_wait_amqp_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint gov.cbp.borderwait.Amqp `
    --projectname cbp_border_wait_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output $outputDir
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }
