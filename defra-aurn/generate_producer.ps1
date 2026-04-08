. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\defra_aurn.xreg.json --projectname defra_aurn_producer --output defra_aurn_producer
