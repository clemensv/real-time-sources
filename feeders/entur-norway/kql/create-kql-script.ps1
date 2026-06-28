$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\entur-norway.xreg.json"
$kqlFile = Join-Path $scriptDir "entur-norway.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"
& $generatorScript -XregPath $inputFile -OutputPath $kqlFile

