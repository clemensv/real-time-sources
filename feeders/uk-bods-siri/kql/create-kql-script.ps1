$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\..\siri\xreg\siri.xreg.json"
$kqlFile = Join-Path $scriptDir "uk-bods-siri.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace org.siri
