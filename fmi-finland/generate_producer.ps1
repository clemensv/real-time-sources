. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\fmi-finland.xreg.json --projectname fmi_finland_producer --output fmi_finland_producer
