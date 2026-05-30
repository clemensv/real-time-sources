# Regenerate Kafka, MQTT, and AMQP producers from the source xRegistry manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\energidataservice_dk.xreg.json"

function Repair-KafkaInfoExports {
  # WORKAROUND(xregistry/codegen#364): xrcg 0.10.7 generates the Kafka Info dataclass
  # but omits it from the producer_data __init__.py export chain.
  $dataRoot = Join-Path $scriptDir "energidataservice_dk_producer\energidataservice_dk_producer_data\src\energidataservice_dk_producer_data"
  $infoModule = Join-Path $dataRoot "dk\energinet\energidataservice\info.py"
  if (-not (Test-Path $infoModule)) {
    throw "Expected Kafka Info dataclass at '$infoModule' after generation."
  }

  $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
  $exports = @(
    @{
      Path = Join-Path $dataRoot "__init__.py"
      Content = @"
from .dk import Info, PowerSystemSnapshot, SpotPrice

__all__ = ["Info", "PowerSystemSnapshot", "SpotPrice"]
"@
    },
    @{
      Path = Join-Path $dataRoot "dk\__init__.py"
      Content = @"
from .energinet import Info, PowerSystemSnapshot, SpotPrice

__all__ = ["Info", "PowerSystemSnapshot", "SpotPrice"]
"@
    },
    @{
      Path = Join-Path $dataRoot "dk\energinet\__init__.py"
      Content = @"
from .energidataservice import Info, PowerSystemSnapshot, SpotPrice

__all__ = ["Info", "PowerSystemSnapshot", "SpotPrice"]
"@
    },
    @{
      Path = Join-Path $dataRoot "dk\energinet\energidataservice\__init__.py"
      Content = @"
from .info import Info
from .powersystemsnapshot import PowerSystemSnapshot
from .spotprice import SpotPrice

__all__ = ["Info", "PowerSystemSnapshot", "SpotPrice"]
"@
    }
  )

  foreach ($export in $exports) {
    [System.IO.File]::WriteAllText($export.Path, ($export.Content.TrimStart("`r", "`n") + "`n"), $utf8NoBom)
  }
}

function Write-InfoCompatibilityShim {
  param(
    [Parameter(Mandatory = $true)]
    [string]$DataRoot
  )

  $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
  $shimPath = Join-Path $DataRoot "info.py"
  $shimContent = @"
# Compatibility shim for the previously shipped top-level Info module path.
from .dk.energinet.energidataservice.info import Info

__all__ = ["Info"]
"@
  [System.IO.File]::WriteAllText($shimPath, ($shimContent.TrimStart("`r", "`n") + "`n"), $utf8NoBom)
}

foreach ($output in @("energidataservice_dk_producer", "energidataservice_dk_mqtt_producer", "energidataservice_dk_amqp_producer")) {
  $outputDir = Join-Path $scriptDir $output
  if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
}
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname energidataservice_dk_producer --output (Join-Path $scriptDir "energidataservice_dk_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }
Repair-KafkaInfoExports
Write-InfoCompatibilityShim -DataRoot (Join-Path $scriptDir "energidataservice_dk_producer\energidataservice_dk_producer_data\src\energidataservice_dk_producer_data")
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint dk.energinet.energidataservice.Mqtt --projectname energidataservice_dk_mqtt_producer --output (Join-Path $scriptDir "energidataservice_dk_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }
Write-InfoCompatibilityShim -DataRoot (Join-Path $scriptDir "energidataservice_dk_mqtt_producer\energidataservice_dk_mqtt_producer_data\src\energidataservice_dk_mqtt_producer_data")
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint dk.energinet.energidataservice.Amqp --projectname energidataservice_dk_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir "energidataservice_dk_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }
Write-InfoCompatibilityShim -DataRoot (Join-Path $scriptDir "energidataservice_dk_amqp_producer\energidataservice_dk_amqp_producer_data\src\energidataservice_dk_amqp_producer_data")
