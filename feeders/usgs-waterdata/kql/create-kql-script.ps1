$ErrorActionPreference = 'Stop'
$source = Split-Path $PSScriptRoot -Parent
$oldTemp = $env:TEMP
$oldTmp = $env:TMP
$work = Join-Path $source '.kql-work'
New-Item -ItemType Directory -Force $work | Out-Null
try {
    $env:TEMP = $work
    $env:TMP = $work
    # Keep ISO-8601 durations as source text; Kusto timespan is not a calendar duration.
    $document = Get-Content (Join-Path $source 'xreg\usgs-waterdata.xreg.json') -Raw -Encoding UTF8 |
        ConvertFrom-Json -Depth 100
    $schemas = $document.schemagroups.'USGS.WaterData.jstruct'.schemas
    $duration = $schemas.'USGS.WaterData.TimeSeries'.versions.'1'.schema.definitions.USGS.WaterData.TimeSeries.properties.data_gap_interval
    $duration.type = @('string', 'null')
    $duration.description += ' Kusto stores the original ISO-8601 text, including calendar durations, without timespan conversion.'
    $inputContract = Join-Path $work 'kql.xreg.json'
    $document | ConvertTo-Json -Depth 100 | Set-Content $inputContract -Encoding UTF8
    & (Join-Path $source '..\..\tools\generate-kql-from-xreg.ps1') `
        -XregPath $inputContract `
        -OutputPath (Join-Path $PSScriptRoot 'usgs-waterdata.kql') `
        -Qualified -Namespace 'USGS.WaterData'
} finally {
    $env:TEMP = $oldTemp
    $env:TMP = $oldTmp
    Remove-Item -Recurse -Force $work
}
