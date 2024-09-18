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
    # Call the install script
    $installScriptPath = Join-Path -Path (Split-Path -Path $MyInvocation.MyCommand.Path -Parent) -ChildPath "install-kusto-cli.ps1"
    & $installScriptPath
}

kusto.cli "${clusterUri}/${database};fed=true" -script:${script} -linemode:false -keeprunning:false
