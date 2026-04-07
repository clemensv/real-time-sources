$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptPath/../tools/require-xrcg.ps1"
xrcg generate --style kafkaproducer --language py --definitions "$scriptPath/xreg/environment_canada.xreg.json" --projectname environment_canada_producer --output "$scriptPath/environment_canada_producer"
