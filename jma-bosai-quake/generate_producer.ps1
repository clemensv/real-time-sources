# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\jma-bosai-quake.xreg.json --projectname jma_bosai_quake_producer --output jma_bosai_quake_producer

# xrcg 0.10.1 emits invalid Python identifiers for string enum values that begin with digits.
# Keep the xreg enum values as the JMA shindo codes, but normalize generated Python member names.
$replacementMap = [ordered]@{
    'MaxIntensityenum.1' = 'MaxIntensityenum.INTENSITY_1'
    'MaxIntensityenum.2' = 'MaxIntensityenum.INTENSITY_2'
    'MaxIntensityenum.3' = 'MaxIntensityenum.INTENSITY_3'
    'MaxIntensityenum.4' = 'MaxIntensityenum.INTENSITY_4'
    'MaxIntensityenum.5-' = 'MaxIntensityenum.INTENSITY_5_MINUS'
    'MaxIntensityenum.5+' = 'MaxIntensityenum.INTENSITY_5_PLUS'
    'MaxIntensityenum.6-' = 'MaxIntensityenum.INTENSITY_6_MINUS'
    'MaxIntensityenum.6+' = 'MaxIntensityenum.INTENSITY_6_PLUS'
    'MaxIntensityenum.7' = 'MaxIntensityenum.INTENSITY_7'
}
Get-ChildItem -Path (Join-Path $PSScriptRoot 'jma_bosai_quake_producer') -Filter '*.py' -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    foreach ($entry in $replacementMap.GetEnumerator()) {
        $content = $content.Replace($entry.Key, $entry.Value)
    }
    Set-Content -Path $_.FullName -Value $content -Encoding utf8
}
$producerTestPath = Join-Path $PSScriptRoot 'jma_bosai_quake_producer\jma_bosai_quake_producer_kafka_producer\tests\test_producer.py'
$producerTestContent = Get-Content $producerTestPath -Raw
$producerTestContent = $producerTestContent.Replace('from test_jma_bosai_quake_producer_data_earthquakereport import Test_EarthquakeReport', 'from test_earthquakereport import Test_EarthquakeReport')
Set-Content -Path $producerTestPath -Value $producerTestContent -Encoding utf8

$enumPath = Join-Path $PSScriptRoot 'jma_bosai_quake_producer\jma_bosai_quake_producer_data\src\jma_bosai_quake_producer_data\maxintensityenum.py'
$enumContent = Get-Content $enumPath -Raw
$enumContent = $enumContent.Replace("    1 = '1'", "    INTENSITY_1 = '1'")
$enumContent = $enumContent.Replace("    2 = '2'", "    INTENSITY_2 = '2'")
$enumContent = $enumContent.Replace("    3 = '3'", "    INTENSITY_3 = '3'")
$enumContent = $enumContent.Replace("    4 = '4'", "    INTENSITY_4 = '4'")
$enumContent = $enumContent.Replace("    5- = '5-'", "    INTENSITY_5_MINUS = '5-'")
$enumContent = $enumContent.Replace("    5+ = '5+'", "    INTENSITY_5_PLUS = '5+'")
$enumContent = $enumContent.Replace("    6- = '6-'", "    INTENSITY_6_MINUS = '6-'")
$enumContent = $enumContent.Replace("    6+ = '6+'", "    INTENSITY_6_PLUS = '6+'")
$enumContent = $enumContent.Replace("    7 = '7'", "    INTENSITY_7 = '7'")
Set-Content -Path $enumPath -Value $enumContent -Encoding utf8
