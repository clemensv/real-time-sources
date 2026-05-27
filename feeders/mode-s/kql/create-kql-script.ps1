$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\mode_s.xreg.json"
$recordFile = Join-Path $scriptDir "..\xreg\mode_s_adsb_record.avsc"
$kqlFile = Join-Path $scriptDir "mode_s.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"
$updatePolicyFile = Join-Path $scriptDir "update_policy.kql"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile
Add-Content -Path $kqlFile -Value ""
& avrotize a2k $recordFile | Add-Content -Path $kqlFile
Add-Content -Path $kqlFile -Value ""
Get-Content $updatePolicyFile | Add-Content -Path $kqlFile
