$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\french_road_traffic.xreg.json'

function Repair-KafkaSample {
    # WORKAROUND(xregistry/codegen#365): xrcg 0.10.7 emits broken top-level model
    # imports and a malformed argparse alias in the generated Kafka sample.
    $samplePath = Join-Path $scriptDir 'french_road_traffic_producer\samples\sample.py'
    if (-not (Test-Path $samplePath)) {
        throw "Expected Kafka sample at '$samplePath' after generation."
    }

    $sample = Get-Content -Path $samplePath -Raw
    $sample = [regex]::Replace(
        $sample,
        "from french_road_traffic_producer_data\.trafficflowmeasurement import TrafficFlowMeasurement\s+from french_road_traffic_producer_data\.roadevent import RoadEvent",
        "from french_road_traffic_producer_data import TrafficFlowMeasurement, RoadEvent")
    $sample = $sample -replace "parser\.add_argument\('-c\|--connection-string',", "parser.add_argument('-c', '--connection-string',"
    [System.IO.File]::WriteAllText($samplePath, $sample, [System.Text.UTF8Encoding]::new($false))
}

function Repair-GeneratedTransportTests {
    # WORKAROUND(xregistry/codegen#366): xrcg 0.10.7 emits transport tests that
    # import data-test module names that do not exist.
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    $repairs = @(
        (Join-Path $scriptDir 'french_road_traffic_producer\french_road_traffic_producer_kafka_producer\tests\test_producer.py'),
        (Join-Path $scriptDir 'french_road_traffic_mqtt_producer\french_road_traffic_mqtt_producer_mqtt_client\tests\test_client.py'),
        (Join-Path $scriptDir 'french_road_traffic_amqp_producer\french_road_traffic_amqp_producer_amqp_producer\tests\test_producer.py')
    )

    foreach ($path in $repairs) {
        if (-not (Test-Path $path)) {
            throw "Expected generated transport test at '$path' after generation."
        }

        $content = Get-Content -Path $path -Raw
        $content = [regex]::Replace(
            $content,
            'from test_french_road_traffic(?:_mqtt|_amqp)?_producer_data_trafficflowmeasurement import Test_TrafficFlowMeasurement',
            'from test_trafficflowmeasurement import Test_TrafficFlowMeasurement')
        $content = [regex]::Replace(
            $content,
            'from test_french_road_traffic(?:_mqtt|_amqp)?_producer_data_roadevent import Test_RoadEvent',
            'from test_roadevent import Test_RoadEvent')
        [System.IO.File]::WriteAllText($path, $content, $utf8NoBom)
    }
}

foreach ($output in @('french_road_traffic_producer', 'french_road_traffic_mqtt_producer', 'french_road_traffic_amqp_producer')) {
    $outputDir = Join-Path $scriptDir $output
    if (Test-Path $outputDir) {
        Remove-Item -Path $outputDir -Recurse -Force
    }
}

xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname french_road_traffic_producer --output (Join-Path $scriptDir 'french_road_traffic_producer')
Repair-KafkaSample

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'fr.gouv.transport.bison_fute.Mqtt' --projectname french_road_traffic_mqtt_producer --output (Join-Path $scriptDir 'french_road_traffic_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'fr.gouv.transport.bison_fute.Amqp' --projectname french_road_traffic_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'french_road_traffic_amqp_producer')
Repair-GeneratedTransportTests
