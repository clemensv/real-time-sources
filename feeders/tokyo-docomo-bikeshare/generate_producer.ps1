$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\tokyo-docomo-bikeshare.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname tokyo_docomo_bikeshare_producer --output (Join-Path $scriptDir 'tokyo_docomo_bikeshare_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'JP.ODPT.DocomoBikeshare.Mqtt' --projectname tokyo_docomo_bikeshare_mqtt_producer --output (Join-Path $scriptDir 'tokyo_docomo_bikeshare_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'JP.ODPT.DocomoBikeshare.Amqp' --projectname tokyo_docomo_bikeshare_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'tokyo_docomo_bikeshare_amqp_producer')

Convert-GeneratedPyprojects
