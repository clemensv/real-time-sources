$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptPath/..\tools\require-xrcg.ps1"
xrcg generate --style kafkaproducer --language py --definitions "$scriptPath\xreg\hongkong_epd.xreg.json" --projectname hongkong_epd_producer --output "$scriptPath\hongkong_epd_producer"
