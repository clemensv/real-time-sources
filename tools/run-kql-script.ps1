<#
.SYNOPSIS
    Executes a Kusto Query Language (KQL) script against a specified Azure Data Explorer cluster and database.

.DESCRIPTION
    This script checks for the presence of the Kusto CLI tool. If it is not found, it calls an installation script. 
    Once the Kusto CLI is available, it executes the provided KQL script against the specified cluster and database.

.PARAMETER clusterUri
    The URI of the Azure Data Explorer cluster to connect to. This parameter is mandatory.

.PARAMETER database
    The name of the database within the Azure Data Explorer cluster where the KQL script will be executed. This parameter is mandatory.

.PARAMETER script
    The path to the KQL script file that will be executed. This parameter is mandatory.

.EXAMPLE
    .\run-kql-script.ps1 -clusterUri "https://mycluster.kusto.windows.net" -database "mydatabase" -script "C:\path\to\script.kql"

.NOTES
    Author: [Your Name]
    Date: [Date]
#>

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
