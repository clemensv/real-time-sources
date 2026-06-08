. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\entur-norway.xreg.json --projectname entur_norway_producer --output entur_norway_producer

& (Join-Path $PSScriptRoot "generate_amqp_producer.ps1")

Convert-GeneratedPyprojects
