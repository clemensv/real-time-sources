$ErrorActionPreference = 'Stop'

$producerDir = Join-Path $PSScriptRoot "waterinfo_vmm" "waterinfo_vmm_producer"

Get-ChildItem -Path $producerDir -Recurse -Filter "*.py" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match 'from be\.') {
        $content = $content -replace 'from be\.', 'from waterinfo_vmm.waterinfo_vmm_producer.be.'
        Set-Content -Path $_.FullName -Value $content -NoNewline
        Write-Host "Fixed imports in $($_.Name)"
    }
}
