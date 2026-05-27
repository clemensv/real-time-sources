$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\aviationweather.xreg.json"
$kqlFile = Join-Path $scriptDir "aviationweather.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace gov.noaa.aviationweather
