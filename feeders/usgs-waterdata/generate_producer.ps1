$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    . (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
    Assert-XrcgVersion
    foreach ($transport in @(
        @{ Style='kafkaproducer'; Endpoint='Kafka'; Project='usgs_waterdata_producer' },
        @{ Style='mqttclient'; Endpoint='Mqtt'; Project='usgs_waterdata_mqtt_producer' },
        @{ Style='amqpproducer'; Endpoint='Amqp'; Project='usgs_waterdata_amqp_producer' }
    )) {
        $arguments = @('generate', '--style', $transport.Style, '--language', 'py',
            '--definitions', 'xreg\usgs-waterdata.xreg.json', '--endpoint', "USGS.WaterData.$($transport.Endpoint)",
            '--projectname', $transport.Project, '--output', $transport.Project)
        if ($transport.Style -eq 'amqpproducer') { $arguments += @('--template-args', 'azure_cbs_target=servicebus') }
        if (Test-Path $transport.Project) { Remove-Item -Recurse -Force $transport.Project }
        & xrcg @arguments
        if ($LASTEXITCODE -ne 0) { throw "Producer generation failed: $($transport.Style)" }
        $package = Get-ChildItem (Join-Path $transport.Project '*\src\*\*.py') -ErrorAction SilentlyContinue
        if (-not $package) { throw "Generator returned no Python package: $($transport.Style)" }
    }
    Convert-GeneratedPyprojects
} finally {
    Pop-Location
}
