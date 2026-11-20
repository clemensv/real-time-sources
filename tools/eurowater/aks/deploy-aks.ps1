<#
.SYNOPSIS
    Deploys the 12-container Eurowater fleet to an existing AKS cluster.

.DESCRIPTION
    Gets AKS credentials through the isolated Microsoft Azure CLI profile,
    validates the existing Kubernetes Secret and PVC, optionally scales the
    node pool, validates the manifest, applies it, and waits for rollout.

    This script never creates or reads secret values. The eurowater-secret
    Secret must already contain the connection settings required by the
    feeders and NVE_API_KEY.
#>

[CmdletBinding()]
param(
    [string]$ResourceGroupName = "rg-rts-feeders-aks",
    [string]$ClusterName = "aks-rts-feeders",
    [string]$NodePoolName = "nodepool1",
    [ValidateRange(0, 100)]
    [int]$NodeCount = 0,
    [ValidateRange(60, 1800)]
    [int]$RolloutTimeoutSeconds = 600
)

$ErrorActionPreference = "Stop"
$Namespace = "feeders"

if (-not (Get-Command az_m -ErrorAction SilentlyContinue)) {
    throw "az_m was not found. Use the Microsoft-tenant Azure CLI profile shim."
}
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    throw "kubectl was not found."
}

$manifest = Join-Path $PSScriptRoot "deployment.yaml"

Write-Host "Connecting kubectl to $ClusterName..."
& az_m aks get-credentials `
    --resource-group $ResourceGroupName `
    --name $ClusterName `
    --overwrite-existing `
    --output none
if ($LASTEXITCODE -ne 0) {
    throw "Failed to get AKS credentials."
}

foreach ($dependency in @(
    @{ Kind = "secret"; Name = "eurowater-secret" },
    @{ Kind = "pvc"; Name = "eurowater-pvc" }
)) {
    & kubectl get $dependency.Kind $dependency.Name --namespace $Namespace --output name | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Missing required $($dependency.Kind) '$($dependency.Name)' in namespace '$Namespace'."
    }
}

Write-Host "Validating manifest..."
& kubectl apply --dry-run=client --filename $manifest | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Client-side manifest validation failed."
}
& kubectl apply --dry-run=server --filename $manifest | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Server-side manifest validation failed."
}

if ($NodeCount -gt 0) {
    Write-Host "Scaling node pool $NodePoolName to $NodeCount nodes..."
    & az_m aks nodepool scale `
        --resource-group $ResourceGroupName `
        --cluster-name $ClusterName `
        --name $NodePoolName `
        --node-count $NodeCount `
        --output none
    if ($LASTEXITCODE -ne 0) {
        throw "Node-pool scale failed."
    }
}

Write-Host "Applying Eurowater deployment..."
& kubectl apply --filename $manifest
if ($LASTEXITCODE -ne 0) {
    throw "Deployment apply failed."
}

& kubectl rollout status deployment/eurowater `
    --namespace $Namespace `
    --timeout "$($RolloutTimeoutSeconds)s"
if ($LASTEXITCODE -ne 0) {
    throw "Eurowater rollout did not complete within $RolloutTimeoutSeconds seconds."
}

& kubectl get pods `
    --namespace $Namespace `
    --selector app=eurowater `
    --output wide
