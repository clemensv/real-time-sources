param(
    [Parameter(Mandatory=$true)]
    [string]$clusterUri,

    [Parameter(Mandatory=$true)]
    [string]$database,

    [Parameter(Mandatory=$true)]
    [string]$script
)

# Check if kusto.cli is in the path
if (-not (Get-Command -Name "kusto.cli" -ErrorAction SilentlyContinue)) {
    # Create a temporary directory
    $tempDir = New-Item -ItemType Directory -Path $env:TEMP -Name "kusto_cli_temp" -ErrorAction Stop

    try {
        # Download the kusto.cli zip file
        $zipFile = Join-Path -Path $tempDir.FullName -ChildPath "kusto_cli.zip"
        Invoke-WebRequest -Uri "https://www.nuget.org/api/v2/package/Microsoft.Azure.Kusto.Tools" -OutFile $zipFile -ErrorAction Stop

        # Extract the zip file
        Expand-Archive -Path $zipFile -DestinationPath $tempDir.FullName -Force -ErrorAction Stop

        # Run kusto.cli from the tools directory
        $toolsDir = Join-Path -Path $tempDir.FullName -ChildPath "tools"
        $kustoCliPath = Join-Path -Path $toolsDir -ChildPath "kusto.cli"
        & $kustoCliPath "${clusterUri}/${database};fed=true" -script:${script} -linemode:false -keeprunning:false
    }
    finally {
        # Clean up the temporary directory
        Remove-Item -Path $tempDir.FullName -Recurse -Force -ErrorAction SilentlyContinue
    }
}
else {
    # kusto.cli is already in the path, so run it directly
    & kusto.cli "${clusterUri}/${database};fed=true" -script:${script} -linemode:false -keeprunning:false
}
