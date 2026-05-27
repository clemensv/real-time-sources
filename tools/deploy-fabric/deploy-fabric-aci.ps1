<#
.SYNOPSIS
    One-click ACI + Fabric deployment for a Real-Time Sources bridge.

.DESCRIPTION
    Two-stage wrapper that produces a fully wired pipeline in a single call:

      Stage A. Delegates to deploy-fabric.ps1 to provision the Fabric side
               only — Eventhouse + KQL database + Event Stream + post-deploy
               hook — and captures the Event Stream Custom Endpoint primary
               connection string.

      Stage B. Deploys the source's azure-template.json (ACI + storage +
               Log Analytics) into an Azure Resource Group, passing the
               Fabric Event Stream connection string in as the
               'connectionString' parameter. The container then feeds the
               Fabric Event Stream directly — no Event Hubs namespace is
               created.

    The result is identical to clicking the "Container + EH" tile and then
    the "Fabric" tile manually, but skips the Event Hubs namespace and
    wires the ACI to Fabric in one shot.

    This script does NOT itself deploy any Azure infrastructure beyond what
    azure-template.json declares; deploy-fabric.ps1 itself never touches
    Azure (it is Fabric-only).

.PARAMETER Source
    Source name (folder under the repo root), e.g. 'pegelonline'.

.PARAMETER ResourceGroup
    Azure resource group for the ACI container. Created on demand.

.PARAMETER Location
    Azure region for the ACI deployment. Defaults to the RG location when
    the RG already exists, or 'westeurope' when creating a new RG.

.PARAMETER SubscriptionId
    Optional Azure subscription override. Used both for Fabric token
    acquisition and the ACI deployment.

.PARAMETER Workspace
    Fabric workspace name OR GUID.

.PARAMETER Eventhouse
    Fabric Eventhouse name OR GUID. Created on demand if it doesn't exist.

.PARAMETER DatabaseName
    KQL database name. Defaults to <Source> with '-' replaced by '_'.

.PARAMETER ContainerGroupName
    Name for the Azure Container Group. Defaults to the source name.

.PARAMETER ApiKeyParamName
    For sources that require a secret (e.g. 'aisstreamApiKey',
    'nveApiKey', 'wsdotAccessCode', 'entsoeSecurityToken'), the
    azure-template.json parameter name. Pair with -ApiKey.

.PARAMETER ApiKey
    The secret value for -ApiKeyParamName.

.PARAMETER Branch
    Repo branch for fetching template URLs. Defaults to 'main'.

.PARAMETER Repo
    Repo slug. Defaults to 'clemensv/real-time-sources'.

.PARAMETER SkipPostDeployHook
    Skip the source's optional fabric/post-deploy.ps1 hook.

.EXAMPLE
    ./deploy-fabric-aci.ps1 -Source pegelonline `
        -ResourceGroup rg-streams -Location westeurope `
        -Workspace ContosoRealTime -Eventhouse ContosoRealTime-eh

.EXAMPLE
    ./deploy-fabric-aci.ps1 -Source aisstream `
        -ResourceGroup rg-streams -Location westeurope `
        -Workspace ContosoRealTime -Eventhouse ContosoRealTime-eh `
        -ApiKeyParamName aisstreamApiKey -ApiKey 'abc123…'
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,

    [string]$Location,

    [string]$SubscriptionId,

    [Parameter(Mandatory = $true)]
    [string]$Workspace,

    [string]$Eventhouse,

    [string]$DatabaseName,

    [string]$ContainerGroupName,

    [string]$ApiKeyParamName,

    [string]$ApiKey,

    [string]$Branch = "main",

    [string]$Repo = "clemensv/real-time-sources",

    [switch]$SkipPostDeployHook
)

$ErrorActionPreference = "Stop"
$RawBase = "https://raw.githubusercontent.com/$Repo/$Branch"
$TempDir = if ($env:TEMP) { $env:TEMP } elseif ($env:TMPDIR) { $env:TMPDIR } else { [System.IO.Path]::GetTempPath() }

if (-not $ContainerGroupName) { $ContainerGroupName = $Source }
if (-not $DatabaseName) { $DatabaseName = $Source -replace '-', '_' }

function Write-Step { param([string]$Step, [string]$Msg)
    Write-Host "`n[$Step] $Msg" -ForegroundColor Cyan
}
function Write-OK { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor Green }
function Write-Info { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor DarkYellow }

# ── Stage A: Fabric side (delegated to deploy-fabric.ps1) ───────────────

Write-Step "A" "Provisioning Fabric resources via deploy-fabric.ps1..."

$deployFabric = Join-Path $PSScriptRoot "deploy-fabric.ps1"
if (-not (Test-Path $deployFabric)) {
    $deployFabric = Join-Path $TempDir "deploy-fabric.ps1"
    Write-Info "Downloading deploy-fabric.ps1 from $RawBase ..."
    Invoke-WebRequest -Uri "$RawBase/tools/deploy-fabric/deploy-fabric.ps1" -OutFile $deployFabric -UseBasicParsing
}

$csFile = Join-Path $TempDir "$Source-eventstream-cs.txt"
if (Test-Path $csFile) { Remove-Item $csFile -Force }

$fwdArgs = @{
    Source     = $Source
    Workspace  = $Workspace
    OutCsFile  = $csFile
    Repo       = $Repo
    Branch     = $Branch
}
if ($Eventhouse)         { $fwdArgs['Eventhouse']         = $Eventhouse }
if ($DatabaseName)       { $fwdArgs['DatabaseName']       = $DatabaseName }
if ($SubscriptionId)     { $fwdArgs['SubscriptionId']     = $SubscriptionId }
if ($SkipPostDeployHook) { $fwdArgs['SkipPostDeployHook'] = $true }

& $deployFabric @fwdArgs
if ($LASTEXITCODE -ne 0) {
    throw "deploy-fabric.ps1 failed (exit $LASTEXITCODE); aborting ACI deploy."
}

if (-not (Test-Path $csFile)) {
    throw "deploy-fabric.ps1 did not produce a connection string at $csFile. Re-run with -SubscriptionId set to a subscription whose principal has Fabric workspace access, or fetch the CS from the portal and use the 'Container only' tile."
}
$esConnectionString = (Get-Content -Path $csFile -Raw).Trim()
if ([string]::IsNullOrWhiteSpace($esConnectionString)) {
    throw "Connection string file $csFile was empty."
}
Write-OK "Captured Event Stream connection string ($($esConnectionString.Length) chars)"

# ── Stage B: ACI deployment ─────────────────────────────────────────────

Write-Step "B" "Deploying ACI container into resource group '$ResourceGroup'..."

if ($SubscriptionId) {
    az account set --subscription $SubscriptionId 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Failed to set subscription '$SubscriptionId'" }
}

# Ensure RG exists
$rgShow = az group show --name $ResourceGroup -o json 2>$null
if ($LASTEXITCODE -ne 0 -or -not $rgShow) {
    if (-not $Location) { $Location = "westeurope" }
    Write-Info "Resource group '$ResourceGroup' not found; creating in $Location ..."
    az group create --name $ResourceGroup --location $Location -o none
    if ($LASTEXITCODE -ne 0) { throw "Failed to create resource group $ResourceGroup" }
    Write-OK "Resource group created"
} else {
    if (-not $Location) {
        $Location = ($rgShow | ConvertFrom-Json).location
    }
    Write-Info "Using existing resource group '$ResourceGroup' (location: $Location)"
}

$templateUrl = "$RawBase/feeders/$Source/azure-template.json"
Write-Info "Template: $templateUrl"

# Build the --parameters list. Use the env-var indirection (@CS_ENV) to
# avoid leaking the connection string into the shell history / process list.
$env:RTS_ACI_CS = $esConnectionString
$paramArgs = @(
    "connectionString=$esConnectionString"
    "containerGroupName=$ContainerGroupName"
    "location=$Location"
)
if ($ApiKeyParamName -and $ApiKey) {
    Write-Info "Passing $ApiKeyParamName as a secure template parameter"
    $paramArgs += "$ApiKeyParamName=$ApiKey"
}

$deploymentName = "rts-$Source-aci-$(Get-Date -Format 'yyyyMMddHHmmss')"
Write-Info "Deployment name: $deploymentName"

$armOut = az deployment group create `
    --resource-group $ResourceGroup `
    --name $deploymentName `
    --template-uri $templateUrl `
    --parameters $paramArgs `
    -o json 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host $armOut -ForegroundColor Red
    throw "ACI deployment failed."
}
Write-OK "ACI deployment complete"

Remove-Item Env:RTS_ACI_CS -ErrorAction SilentlyContinue

# ── Summary ─────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "──────────────────────────────────────────────────────────────────" -ForegroundColor Green
Write-Host " ACI + Fabric deployment complete" -ForegroundColor Green
Write-Host "──────────────────────────────────────────────────────────────────" -ForegroundColor Green
Write-Host "  Source            : $Source" -ForegroundColor Gray
Write-Host "  Resource Group    : $ResourceGroup ($Location)" -ForegroundColor Gray
Write-Host "  Container Group   : $ContainerGroupName" -ForegroundColor Gray
Write-Host "  Fabric Workspace  : $Workspace" -ForegroundColor Gray
Write-Host "  KQL Database      : $DatabaseName" -ForegroundColor Gray
Write-Host ""
Write-Host "  Tail container logs:" -ForegroundColor White
Write-Host "    az container logs -g $ResourceGroup -n $ContainerGroupName --follow" -ForegroundColor DarkGray
Write-Host ""
