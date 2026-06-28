$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\usgs_nwis_wq.xreg.json"
$kqlFile = Join-Path $scriptDir "usgs_nwis_wq.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace 'gov.usgs.waterservices.wq'
