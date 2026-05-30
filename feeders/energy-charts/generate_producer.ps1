# Regenerate Kafka, MQTT, and AMQP producers from the source xRegistry manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\energy_charts.xreg.json"

function Repair-KafkaInfoExport {
  # WORKAROUND(xregistry/codegen#364): xrcg 0.10.7 generates the Kafka Info
  # dataclass but omits it from the producer_data package exports.
  $dataRoot = Join-Path $scriptDir "energy_charts_producer\energy_charts_producer_data\src\energy_charts_producer_data"
  $topLevelInfoModule = Join-Path $dataRoot "info.py"
  $infoPackageDir = Join-Path $dataRoot "info"
  if (-not (Test-Path $topLevelInfoModule)) {
    throw "Expected Kafka Info dataclass at '$topLevelInfoModule' after generation."
  }
  if (-not (Test-Path $infoPackageDir)) {
    throw "Expected Kafka info package at '$infoPackageDir' after generation."
  }

  [System.IO.File]::Copy($topLevelInfoModule, (Join-Path $infoPackageDir "info.py"), $true)

  $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
  $rootContent = @"
from .info import PublicPower, Info, SpotPrice, GridSignal

__all__ = ["PublicPower", "Info", "SpotPrice", "GridSignal"]
"@
  $infoPackageContent = @"
from .energy_charts import PublicPower, GridSignal, SpotPrice
from .info import Info

__all__ = ["PublicPower", "Info", "GridSignal", "SpotPrice"]
"@
  [System.IO.File]::WriteAllText((Join-Path $dataRoot "__init__.py"), ($rootContent.TrimStart("`r", "`n") + "`n"), $utf8NoBom)
  [System.IO.File]::WriteAllText((Join-Path $dataRoot "info\__init__.py"), ($infoPackageContent.TrimStart("`r", "`n") + "`n"), $utf8NoBom)
}

foreach ($output in @("energy_charts_producer", "energy_charts_mqtt_producer", "energy_charts_amqp_producer")) {
  $outputDir = Join-Path $scriptDir $output
  if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
}
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname energy_charts_producer --output (Join-Path $scriptDir "energy_charts_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }
Repair-KafkaInfoExport
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint info.energy_charts.Mqtt --projectname energy_charts_mqtt_producer --output (Join-Path $scriptDir "energy_charts_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint info.energy_charts.Amqp --projectname energy_charts_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir "energy_charts_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }
