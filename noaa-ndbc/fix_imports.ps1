# Fix imports in generated producer files
# Replace 'noaa-ndbc-producer_data' with proper Python package imports

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = Join-Path $scriptDir "noaa_ndbc\noaa_ndbc_producer"

Write-Host "Fixing imports in generated files..." -ForegroundColor Cyan

$files = Get-ChildItem -Path $targetDir -Filter "*.py" -Recurse

$fixedCount = 0
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content

    # Replace dotted import patterns
    $content = $content -replace 'from noaa-ndbc-producer_data\.', 'from noaa_ndbc.noaa_ndbc_producer.'
    $content = $content -replace 'import noaa-ndbc-producer_data\.', 'import noaa_ndbc.noaa_ndbc_producer.'
    # Replace single-name import patterns
    $content = [regex]::Replace($content, 'from noaa-ndbc-producer_data import (\w+)', {
        param($m)
        $className = $m.Groups[1].Value
        $moduleName = $className.ToLower()
        "from noaa_ndbc.noaa_ndbc_producer.microsoft.opendata.us.noaa.ndbc.$moduleName import $className"
    })

    # Fix bytes content-type header key (should be string, not bytes)
    $content = $content -replace 'message\.headers\[b"content-type"\]', 'message.headers["content-type"]'

    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "  Fixed: $($file.Name)" -ForegroundColor Gray
        $fixedCount++
    }
}

Write-Host ""
Write-Host "✓ Fixed $fixedCount files" -ForegroundColor Green
