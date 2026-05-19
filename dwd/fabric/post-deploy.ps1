<#
.SYNOPSIS
    dwd-specific post-deploy hook: wires the 8 ICON-D2 Kusto-backed layers
    into an existing Fabric Map item.

.DESCRIPTION
    Auto-invoked by tools/deploy-fabric/deploy-fabric.ps1 (and the notebook
    variant) at the end of a generic deployment via the well-known path
    `<source>/fabric/post-deploy.ps1`. Can also be run standalone for
    re-wiring after a layer/colour change.

    When invoked as a hook, the generic deployer passes a -Context
    hashtable containing the IDs created by the bootstrap. The Fabric Map
    item itself is *not* created by the generic deployer (the Fabric REST
    surface doesn't yet expose Map-item creation), so this hook needs the
    map item id, which it reads from the DWD_FABRIC_MAP_ID environment
    variable. If that variable is missing the hook prints instructions and
    exits successfully (so it doesn't fail the bootstrap when no map item
    has been prepared yet).

.PARAMETER Context
    Hashtable provided by the generic deployer. Required keys consumed:
        WorkspaceId, DatabaseId, EventhouseClusterUri
    Ignored keys: everything else.

.PARAMETER WorkspaceId
    Standalone-mode override. GUID of the Fabric workspace.

.PARAMETER MapId
    Standalone-mode override. GUID of the Fabric Map item. Defaults to
    $env:DWD_FABRIC_MAP_ID.

.PARAMETER KqlDatabaseId
    Standalone-mode override. GUID of the KQL database with IconD2Points.

.PARAMETER KustoUri
    Standalone-mode override. Full https URI of the Kusto cluster.

.PARAMETER KustoDatabase
    KQL database name (default: dwd).

.EXAMPLE
    # Auto-invoked: the user does not run this directly.
    ../../tools/deploy-fabric/deploy-fabric.ps1 -Source dwd `
        -ResourceGroup rg-dwd -Workspace <ws>

.EXAMPLE
    # Standalone re-wire after a layer tweak:
    $env:DWD_FABRIC_MAP_ID = "39abf7e3-1df6-4cbf-ab92-93d6d4cf07e5"
    ./post-deploy.ps1 `
        -WorkspaceId   "a26c1440-1c4a-4774-b944-fd62f7380d62" `
        -KqlDatabaseId "8c202901-5346-4faf-88a6-9c15d737a91b" `
        -KustoUri      "https://trd-xxxxxxxx.z1.kusto.fabric.microsoft.com"
#>
[CmdletBinding()]
param(
    [hashtable] $Context,
    [string]    $WorkspaceId,
    [string]    $MapId          = $env:DWD_FABRIC_MAP_ID,
    [string]    $KqlDatabaseId,
    [string]    $KustoUri,
    [string]    $KustoDatabase  = "dwd"
)

$ErrorActionPreference = "Stop"

# Merge Context (hook invocation) with explicit params (standalone).
if ($Context) {
    if (-not $WorkspaceId   -and $Context.ContainsKey('WorkspaceId'))          { $WorkspaceId   = $Context.WorkspaceId }
    if (-not $KqlDatabaseId -and $Context.ContainsKey('DatabaseId'))           { $KqlDatabaseId = $Context.DatabaseId }
    if (-not $KustoUri      -and $Context.ContainsKey('EventhouseClusterUri')) { $KustoUri      = $Context.EventhouseClusterUri }
    if (-not $KustoDatabase -and $Context.ContainsKey('DatabaseName'))         { $KustoDatabase = $Context.DatabaseName }
}

if (-not $MapId) {
    Write-Host "  [dwd post-deploy] DWD_FABRIC_MAP_ID not set; skipping map wiring." -ForegroundColor DarkYellow
    Write-Host "  Create a blank Fabric Map item in the workspace and re-run with:" -ForegroundColor DarkYellow
    Write-Host "    `$env:DWD_FABRIC_MAP_ID = '<map-item-guid>'" -ForegroundColor DarkYellow
    Write-Host "    pwsh dwd/fabric/post-deploy.ps1 -Context <ctx>" -ForegroundColor DarkYellow
    exit 0
}

foreach ($pair in @(
    @('WorkspaceId',   $WorkspaceId),
    @('KqlDatabaseId', $KqlDatabaseId),
    @('KustoUri',      $KustoUri)
)) {
    if (-not $pair[1]) { throw "Missing required value: $($pair[0])" }
}

# Acquire tokens via az CLI if not provided in the environment.
if (-not $env:FABRIC_TOKEN) {
    Write-Host "  [dwd post-deploy] Acquiring Fabric token via az CLI..."
    $env:FABRIC_TOKEN = (az account get-access-token `
        --resource "https://api.fabric.microsoft.com" `
        --query accessToken -o tsv)
}
if (-not $env:KUSTO_TOKEN) {
    # The Kusto audience must be the specific cluster URI: the generic
    # https://kusto.fabric.microsoft.com is not a registered AAD resource
    # principal in some tenants (e.g. Microsoft corp).
    Write-Host "  [dwd post-deploy] Acquiring Kusto token via az CLI..."
    $env:KUSTO_TOKEN = (az account get-access-token `
        --resource $KustoUri `
        --query accessToken -o tsv)
}

$py = if ($env:PYTHON) { $env:PYTHON } else { "python" }
$script = Join-Path $PSScriptRoot "wire_icond2_map.py"

& $py $script `
    --workspace-id $WorkspaceId `
    --map-id       $MapId `
    --kql-db-id    $KqlDatabaseId `
    --kusto-uri    $KustoUri `
    --kusto-db     $KustoDatabase
if ($LASTEXITCODE -ne 0) { throw "wire_icond2_map.py exited with $LASTEXITCODE" }
