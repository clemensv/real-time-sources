$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptPath/../tools/require-xrcg.ps1"
xrcg generate --style kafkaproducer --language py --definitions "$scriptPath/xreg/hko_hong_kong.xreg.json" --projectname hko_hong_kong_producer --output "$scriptPath/hko_hong_kong_producer"
