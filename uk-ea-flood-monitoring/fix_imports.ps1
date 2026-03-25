# Fix imports in generated producer files
# Replace 'uk-ea-flood-monitoring-producer_data' with proper Python package imports

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = Join-Path $scriptDir "uk_ea_flood_monitoring\uk_ea_flood_monitoring_producer"

Write-Host "Fixing imports in generated files..." -ForegroundColor Cyan

$files = Get-ChildItem -Path $targetDir -Filter "*.py" -Recurse

$fixedCount = 0
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content

    # Replace dotted import patterns
    $content = $content -replace 'from uk-ea-flood-monitoring-producer_data\.', 'from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.'
    $content = $content -replace 'import uk-ea-flood-monitoring-producer_data\.', 'import uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.'
    # Replace single-name import patterns
    $content = [regex]::Replace($content, 'from uk-ea-flood-monitoring-producer_data import (\w+)', {
        param($m)
        $className = $m.Groups[1].Value
        $moduleName = $className.ToLower()
        "from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.uk.gov.environment.ea.floodmonitoring.$moduleName import $className"
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
