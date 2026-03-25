# Fix imports in generated producer files
# Replace 'noaa-producer_data' with proper Python package imports

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = Join-Path $scriptDir "noaa\noaa_producer"

Write-Host "Fixing imports in generated files..." -ForegroundColor Cyan

$files = Get-ChildItem -Path $targetDir -Filter "*.py" -Recurse

$fixedCount = 0
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content
    
    # Replace the bad import pattern
    $content = $content -replace 'from noaa-producer_data\.', 'from noaa.noaa_producer.'
    $content = $content -replace 'import noaa-producer_data\.', 'import noaa.noaa_producer.'
    $content = [regex]::Replace($content, 'from noaa-producer_data import (\w+)', {
        param($m)
        $className = $m.Groups[1].Value
        $moduleName = $className.ToLower()
        "from noaa.noaa_producer.microsoft.opendata.us.noaa.$moduleName import $className"
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
