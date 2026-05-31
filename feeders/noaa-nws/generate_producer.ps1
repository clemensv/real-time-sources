# Generate the NOAA NWS Weather Alerts producer using xrcg

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\noaa-nws.xreg.json"
$outputDir = Join-Path $projectRoot "noaa_nws_producer"

Write-Host "Generating NOAA NWS producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

# Ensure the output directory exists
if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}

# Generate the Kafka producer code
Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate --style kafkaproducer --language py --projectname noaa-nws-producer --definitions $xregFile --output $outputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run copy_generated_producer.ps1 to copy files into the main package" -ForegroundColor Gray
    Write-Host "  2. Run fix_imports.ps1 to fix generated import paths" -ForegroundColor Gray
    Write-Host "  3. Install dependencies: pip install ." -ForegroundColor Gray
    Write-Host "  4. Run the poller: python -m noaa_nws" -ForegroundColor Gray
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

& (Join-Path $PSScriptRoot "generate_mqtt_producer.ps1")
& (Join-Path $PSScriptRoot "generate_amqp_producer.ps1")

# Post-fix: expose flat schema classes (xrcg only auto-exports those it
# nests under the microsoft/ subpackage). Append any missing flat classes
# so the kafka producer's `from noaa_nws_producer_data import X` imports
# resolve.
$dataInit = Join-Path $projectRoot "noaa_nws_producer\noaa_nws_producer_data\src\noaa_nws_producer_data\__init__.py"
if (Test-Path $dataInit) {
    $content = Get-Content $dataInit -Raw
    $flatClasses = @('ObservationStation', 'WeatherObservation')
    foreach ($cls in $flatClasses) {
        $module = $cls.ToLower()
        $modPath = Join-Path $projectRoot "noaa_nws_producer\noaa_nws_producer_data\src\noaa_nws_producer_data\$module.py"
        if ((Test-Path $modPath) -and ($content -notmatch "from \.$module import $cls")) {
            $content = $content -replace '(__all__ = \[)', "from .$module import $cls`n`$1"
            $content = $content -replace '(__all__ = \[[^\]]*?)\]', "`$1, `"$cls`"]"
        }
    }
    Set-Content -Path $dataInit -Value $content -NoNewline
}
