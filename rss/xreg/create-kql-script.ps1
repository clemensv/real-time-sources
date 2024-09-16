$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "feeds.xreg.json"
$outputFile = Join-Path $scriptDir "schemas.avsc"

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
avrotize a2k $outputFile --emit-cloudevents-dispatch --emit-cloudevents-columns > feeds.kql

