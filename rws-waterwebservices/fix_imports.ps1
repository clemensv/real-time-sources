$ErrorActionPreference = 'Stop'

$producerDir = Join-Path $PSScriptRoot "rws_waterwebservices" "rws_waterwebservices_producer"

Get-ChildItem -Path $producerDir -Recurse -Filter "*.py" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match 'from nl\.') {
        $content = $content -replace 'from nl\.', 'from rws_waterwebservices.rws_waterwebservices_producer.nl.'
        Set-Content -Path $_.FullName -Value $content -NoNewline
        Write-Host "Fixed imports in $($_.Name)"
    }
}
