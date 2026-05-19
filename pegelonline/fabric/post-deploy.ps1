<#
.SYNOPSIS
    pegelonline-specific post-deploy hook: wires the 6 Kusto-backed point
    layers into an existing Fabric Map item.

.DESCRIPTION
    Auto-invoked by tools/deploy-fabric/deploy-fabric.ps1 (and the notebook
    variant) at the end of a generic deployment via the well-known path
    `<source>/fabric/post-deploy.ps1`. Can also be run standalone for
    re-wiring after a layer/colour/KQL change.

    When invoked as a hook, the generic deployer passes a -Context hashtable
    containing the IDs created by the bootstrap. The Fabric Map item itself
    is NOT created by the generic deployer (the Fabric REST surface doesn't
    yet expose Map-item creation), so this hook needs the map item id, which
    it reads from the PEGELONLINE_FABRIC_MAP_ID environment variable. If
    that variable is missing the hook prints instructions and exits
    successfully (so it doesn't fail the bootstrap when no map item has
    been prepared yet).

.PARAMETER Context
    Hashtable provided by the generic deployer. Required keys consumed:
        WorkspaceId, DatabaseId, EventhouseClusterUri
    Ignored keys: everything else.
#>
[CmdletBinding()]
param(
    [hashtable] $Context,
    [string]    $WorkspaceId,
    [string]    $MapId          = $env:PEGELONLINE_FABRIC_MAP_ID,
    [string]    $KqlDatabaseId,
    [string]    $KustoUri,
    [string]    $KustoDatabase  = "pegelonline"
)

$ErrorActionPreference = "Stop"

if ($Context) {
    if (-not $WorkspaceId   -and $Context.ContainsKey('WorkspaceId'))          { $WorkspaceId   = $Context.WorkspaceId }
    if (-not $KqlDatabaseId -and $Context.ContainsKey('DatabaseId'))           { $KqlDatabaseId = $Context.DatabaseId }
    if (-not $KustoUri      -and $Context.ContainsKey('EventhouseClusterUri')) { $KustoUri      = $Context.EventhouseClusterUri }
    if (-not $KustoDatabase -and $Context.ContainsKey('DatabaseName'))         { $KustoDatabase = $Context.DatabaseName }
}

if (-not $MapId) {
    Write-Host "  [pegelonline post-deploy] PEGELONLINE_FABRIC_MAP_ID not set; skipping map wiring." -ForegroundColor DarkYellow
    Write-Host "  Create a blank Fabric Map item in the workspace and re-run with:" -ForegroundColor DarkYellow
    Write-Host "    `$env:PEGELONLINE_FABRIC_MAP_ID = '<map-item-guid>'" -ForegroundColor DarkYellow
    Write-Host "    pwsh pegelonline/fabric/post-deploy.ps1 -Context <ctx>" -ForegroundColor DarkYellow
    exit 0
}

foreach ($pair in @(
    @('WorkspaceId',   $WorkspaceId),
    @('KqlDatabaseId', $KqlDatabaseId),
    @('KustoUri',      $KustoUri)
)) {
    if (-not $pair[1]) { throw "Missing required value: $($pair[0])" }
}

if (-not $env:FABRIC_TOKEN) {
    Write-Host "  [pegelonline post-deploy] Acquiring Fabric token via az CLI..."
    $env:FABRIC_TOKEN = (az account get-access-token `
        --resource "https://api.fabric.microsoft.com" `
        --query accessToken -o tsv)
}
if (-not $env:KUSTO_TOKEN) {
    # The Kusto audience must be the specific cluster URI: the generic
    # https://kusto.fabric.microsoft.com is not a registered AAD resource
    # principal in some tenants (e.g. Microsoft corp).
    Write-Host "  [pegelonline post-deploy] Acquiring Kusto token via az CLI..."
    $env:KUSTO_TOKEN = (az account get-access-token `
        --resource $KustoUri `
        --query accessToken -o tsv)
}

$py = if ($env:PYTHON) { $env:PYTHON } else { "python" }
$script = Join-Path $PSScriptRoot "wire_pegelonline_map.py"

& $py $script `
    --workspace-id $WorkspaceId `
    --map-id       $MapId `
    --kql-db-id    $KqlDatabaseId `
    --kusto-uri    $KustoUri `
    --kusto-db     $KustoDatabase
if ($LASTEXITCODE -ne 0) { throw "wire_pegelonline_map.py exited with $LASTEXITCODE" }
