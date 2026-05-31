$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\paris-bicycle-counters.xreg.json"
$kqlFile = Join-Path $scriptDir "paris-bicycle-counters.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace "FR.Paris.OpenData.Velo"
