. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\canada-aqhi.xreg.json --projectname canada_aqhi_producer --output canada_aqhi_producer
