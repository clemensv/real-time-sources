$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\siri.xreg.json"
$kqlFile = Join-Path $scriptDir "siri.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace org.siri
