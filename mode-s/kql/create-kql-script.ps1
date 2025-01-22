$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "../xreg/mode_s.xreg.json"
$outputFile = Join-Path $scriptDir "../xreg/schemas.avsc"
$recordFile = Join-Path $scriptDir "../xreg/mode_s_adsb_record.avsc"
$kqlFile = Join-Path $scriptDir "mode_s.kql"

# Load the JSON content
$jsonContent = Get-Content $inputFile -Raw | ConvertFrom-Json

$mergedArray = @()

# Iterate through schemagroups
foreach ($schemagroup in $jsonContent.schemagroups.psobject.Properties.value) {
    # Iterate through schemas within each schemagroup
    foreach ($schema in $schemagroup.schemas.psobject.Properties.value) {
        # Iterate through versions within each schema
        foreach ($version in $schema.versions.psobject.Properties.value) {
            # Add the 'schema' object to the merged array
            $mergedArray += $version.schema
        }
    }
}

# Output the merged array to the output file
$mergedArray | ConvertTo-Json -Depth 30 | Out-File $outputFile -Encoding UTF8
avrotize a2k $outputFile --emit-cloudevents-dispatch --emit-cloudevents-columns > $kqlFile
avrotize a2k $recordFile >> $kqlFile

type update_policy.kql >> $kqlFile