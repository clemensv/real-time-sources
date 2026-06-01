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
    Optional Azure subscription override by name or ID. Used both for Fabric
    token acquisition and the ACI deployment.

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

.PARAMETER TemplateParameter
    Additional ARM template parameter overrides as 'name=value' strings.
    Repeatable: -TemplateParameter foo=1 -TemplateParameter bar=baz.
    Forwarded verbatim to `az deployment group create --parameters`.
    These are passed AFTER the script-managed parameters (connectionString,
    containerGroupName, location, optional ApiKeyParamName), so they can
    override the defaults baked into azure-template.json without overriding
    the connection string.

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

.EXAMPLE
    ./deploy-fabric-aci.ps1 -Source canada-aqhi `
        -ResourceGroup rg-aqhi -Location westeurope `
        -Workspace ContosoRealTime -Eventhouse contoso-eh `
        -TemplateParameter 'provinces=BC,ON' `
        -TemplateParameter 'referenceRefreshInterval=3600'
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

    [string[]]$TemplateParameter = @(),

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

function ConvertFrom-AzCliJson {
    param(
        [AllowNull()]
        [object]$InputObject,
        [string]$Context = "Azure CLI output"
    )

    if ($null -eq $InputObject) { return $null }

    $text = if ($InputObject -is [string]) {
        $InputObject
    } else {
        $InputObject | Out-String
    }

    $trimmed = $text.Trim()
    if (-not $trimmed) { return $null }

    try {
        return $trimmed | ConvertFrom-Json
    } catch {
        $jsonStarts = [regex]::Matches($trimmed, '(?m)^[\t ]*[\{\[]')
        foreach ($match in $jsonStarts) {
            $candidate = $trimmed.Substring($match.Index).Trim()
            try {
                return $candidate | ConvertFrom-Json
            } catch {
                continue
            }
        }
    }

    throw "Failed to parse JSON from $Context. Raw output:`n$trimmed"
}

function Resolve-AzSubscriptionContext {
    param([Parameter(Mandatory = $true)] [string]$Subscription)

    az account set --subscription $Subscription --only-show-errors 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to set subscription '$Subscription' (name or ID)."
    }

    $account = az account show --only-show-errors --output json 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to resolve the active Azure subscription after selecting '$Subscription': $($account | Out-String)"
    }

    $parsed = ConvertFrom-AzCliJson -InputObject $account -Context "az account show output for subscription '$Subscription'"
    return [pscustomobject]@{
        Id   = $parsed.id
        Name = $parsed.name
    }
}

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
    throw "deploy-fabric.ps1 did not produce a connection string at $csFile. Review the step-A warnings above; if the Event Stream was created successfully, fetch the Custom Endpoint connection string from the Fabric portal and use the 'Container only' tile."
}
$esConnectionString = (Get-Content -Path $csFile -Raw).Trim()
if ([string]::IsNullOrWhiteSpace($esConnectionString)) {
    throw "Connection string file $csFile was empty."
}
Write-OK "Captured Event Stream connection string ($($esConnectionString.Length) chars)"

# ── Stage B: ACI deployment ─────────────────────────────────────────────

Write-Step "B" "Deploying ACI container into resource group '$ResourceGroup'..."

if ($SubscriptionId) {
    $selectedSubscription = Resolve-AzSubscriptionContext -Subscription $SubscriptionId
    $SubscriptionId = $selectedSubscription.Id
    Write-OK "Subscription set: $($selectedSubscription.Name) ($SubscriptionId)"
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
foreach ($tp in $TemplateParameter) {
    if ([string]::IsNullOrWhiteSpace($tp)) { continue }
    if ($tp -notmatch '^[A-Za-z_][A-Za-z0-9_]*=') {
        throw "Invalid -TemplateParameter '$tp'. Expected 'name=value' (name must match ARM param naming rules)."
    }
    $paramArgs += $tp
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
