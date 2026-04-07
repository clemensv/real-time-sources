$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptPath/../tools/require-xrcg.ps1"
xrcg generate --style kafkaproducer --language py --definitions "$scriptPath/xreg/singapore_nea.xreg.json" --projectname singapore_nea_producer --output "$scriptPath/singapore_nea_producer"
