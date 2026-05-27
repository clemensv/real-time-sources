# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style mqttclient --language py --definitions xreg\jma-bosai-quake.xreg.json --endpoint JP.JMA.Quake.Mqtt --projectname jma_bosai_quake_mqtt_producer --output jma_bosai_quake_mqtt_producer

# xrcg 0.10.x emits invalid Python identifiers for JMA shindo string enum values.
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
    'MaxIntensityenum.VALUE_1' = 'MaxIntensityenum.INTENSITY_1'
    'MaxIntensityenum.VALUE_2' = 'MaxIntensityenum.INTENSITY_2'
    'MaxIntensityenum.VALUE_3' = 'MaxIntensityenum.INTENSITY_3'
    'MaxIntensityenum.VALUE_4' = 'MaxIntensityenum.INTENSITY_4'
    'MaxIntensityenum.VALUE_7' = 'MaxIntensityenum.INTENSITY_7'
}
Get-ChildItem -Path (Join-Path $PSScriptRoot 'jma_bosai_quake_mqtt_producer') -Filter '*.py' -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    foreach ($entry in $replacementMap.GetEnumerator()) { $content = $content.Replace($entry.Key, $entry.Value) }
    Set-Content -Path $_.FullName -Value $content -Encoding utf8
}
$enumPath = Join-Path $PSScriptRoot 'jma_bosai_quake_mqtt_producer\jma_bosai_quake_mqtt_producer_data\src\jma_bosai_quake_mqtt_producer_data\maxintensityenum.py'
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
$enumContent = $enumContent.Replace("    VALUE_1 = '1'", "    INTENSITY_1 = '1'")
$enumContent = $enumContent.Replace("    VALUE_2 = '2'", "    INTENSITY_2 = '2'")
$enumContent = $enumContent.Replace("    VALUE_3 = '3'", "    INTENSITY_3 = '3'")
$enumContent = $enumContent.Replace("    VALUE_4 = '4'", "    INTENSITY_4 = '4'")
$enumContent = $enumContent.Replace("    VALUE_5_ = '5-'", "    INTENSITY_5_MINUS = '5-'")
$enumContent = $enumContent.Replace("    VALUE_5_ = '5+'", "    INTENSITY_5_PLUS = '5+'")
$enumContent = $enumContent.Replace("    VALUE_6_ = '6-'", "    INTENSITY_6_MINUS = '6-'")
$enumContent = $enumContent.Replace("    VALUE_6_ = '6+'", "    INTENSITY_6_PLUS = '6+'")
$enumContent = $enumContent.Replace("    VALUE_7 = '7'", "    INTENSITY_7 = '7'")
Set-Content -Path $enumPath -Value $enumContent -Encoding utf8

$enumTestPath = Join-Path $PSScriptRoot 'jma_bosai_quake_mqtt_producer\jma_bosai_quake_mqtt_producer_data\tests\test_maxintensityenum.py'
$enumTestContent = Get-Content $enumTestPath -Raw
$enumTestContent = $enumTestContent.Replace("MaxIntensityenum.VALUE_5_.value, '5-'", "MaxIntensityenum.INTENSITY_5_MINUS.value, '5-'")
$enumTestContent = $enumTestContent.Replace("MaxIntensityenum.VALUE_5_.value, '5+'", "MaxIntensityenum.INTENSITY_5_PLUS.value, '5+'").Replace("MaxIntensityenum.VALUE_6_.value, '6-'", "MaxIntensityenum.INTENSITY_6_MINUS.value, '6-'").Replace("MaxIntensityenum.VALUE_6_.value, '6+'", "MaxIntensityenum.INTENSITY_6_PLUS.value, '6+'")
Set-Content -Path $enumTestPath -Value $enumTestContent -Encoding utf8
