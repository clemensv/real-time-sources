. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\irceline_belgium.xreg.json --projectname irceline_belgium_producer --output irceline_belgium_producer
