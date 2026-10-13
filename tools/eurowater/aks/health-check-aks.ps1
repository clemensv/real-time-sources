<#
.SYNOPSIS
    Checks the deployed Eurowater AKS pod and its shared state files.

.DESCRIPTION
    Verifies that one Eurowater pod exists, all 12 containers are ready, no
    container has restarted, and the shared state directory is accessible.
    It does not display environment variables, Secret contents, or tokens.
#>

[CmdletBinding()]
param(
    [string]$Namespace = "feeders",
    [ValidateRange(1, 1440)]
    [int]$StateFreshnessMinutes = 120
)

$ErrorActionPreference = "Stop"
$expectedContainers = @(
    "pegelonline",
    "chmi-hydro",
    "imgw-hydro",
    "smhi-hydro",
    "hubeau-hydrometrie",
    "uk-ea-flood-monitoring",
    "rws-waterwebservices",
    "waterinfo-vmm",
    "nve-hydro",
    "syke-hydro",
    "bafu-hydro",
    "german-waters"
)
$expectedStateFiles = @(
    "pegelonline_state.json",
    "chmi_hydro_state.json",
    "imgw_hydro_state.json",
    "smhi_hydro_state.json",
    "hubeau_hydrometrie_state.json",
    "uk_ea_flood_monitoring_state.json",
    "rws_waterwebservices_state.json",
    "waterinfo_vmm_state.json",
    "nve_hydro_state.json",
    "syke_hydro_state.json",
    "bafu_hydro_state.json",
    "german_waters_state.json"
)

$podJson = & kubectl get pods `
    --namespace $Namespace `
    --selector app=eurowater `
    --output json
if ($LASTEXITCODE -ne 0) {
    throw "Failed to query Eurowater pods."
}

$podList = $podJson | ConvertFrom-Json
if ($podList.items.Count -ne 1) {
    throw "Expected one Eurowater pod, found $($podList.items.Count)."
}

$pod = $podList.items[0]
$statuses = @($pod.status.containerStatuses)
$actualNames = @($statuses.name | Sort-Object)
$missing = @($expectedContainers | Where-Object { $_ -notin $actualNames })
if ($missing.Count -gt 0) {
    throw "Missing containers: $($missing -join ', ')."
}

$notReady = @($statuses | Where-Object { -not $_.ready })
$restarted = @($statuses | Where-Object { $_.restartCount -ne 0 })

$statuses |
    Sort-Object name |
    Select-Object name, ready, restartCount,
        @{ Name = "image"; Expression = { $_.image } } |
    Format-Table -AutoSize

if ($notReady.Count -gt 0) {
    throw "Containers not ready: $($notReady.name -join ', ')."
}
if ($restarted.Count -gt 0) {
    throw "Containers with restarts: $($restarted.name -join ', ')."
}

$podName = $pod.metadata.name
$freshnessCommand = @'
now=$(date +%s)
limit=__LIMIT_SECONDS__
failed=0
for name in __EXPECTED_STATE_FILES__; do
  file="/mnt/fileshare/$name"
  if [ ! -e "$file" ]; then
    printf "%-55s MISSING\n" "$name"
    failed=1
    continue
  fi
  modified=$(stat -c %Y "$file")
  age=$((now - modified))
  printf "%-55s %8ss old\n" "$name" "$age"
  if [ "$age" -gt "$limit" ]; then
    failed=1
  fi
done
exit "$failed"
'@
$freshnessCommand = $freshnessCommand.Replace(
    "__LIMIT_SECONDS__",
    [string]($StateFreshnessMinutes * 60)
).Replace(
    "__EXPECTED_STATE_FILES__",
    ($expectedStateFiles -join " ")
).Replace("`r`n", "`n")
$encodedFreshnessCommand = [Convert]::ToBase64String(
    [Text.Encoding]::UTF8.GetBytes($freshnessCommand)
)
$freshnessRunner = "printf '%s' '$encodedFreshnessCommand' | base64 -d | sh"

Write-Host "Shared state-file freshness:"
& kubectl exec `
    --namespace $Namespace `
    $podName `
    --container pegelonline `
    -- sh -c $freshnessRunner
if ($LASTEXITCODE -ne 0) {
    throw "One or more expected state files are missing or older than $StateFreshnessMinutes minutes."
}

Write-Host "Eurowater health check passed for pod $podName."
