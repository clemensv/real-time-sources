$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\fienta.xreg.json"
$kqlFile = Join-Path $scriptDir "fienta.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"
& $generatorScript -XregPath $inputFile -OutputPath $kqlFile

