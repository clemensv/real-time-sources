#requires -Version 7.0
<#
.SYNOPSIS
  Static auditor for `feeders/<slug>/azure-template*.json` files.

.DESCRIPTION
  This is the static counterpart to `tools/verify-arm-template.ps1` (which does
  a live Azure deploy). It catches the silent regressions that the deploy gate
  would miss either because they parse but misbehave, or because the reviewer
  did not run a live deploy for every variant the PR touches.

  Checks performed PER variant template:

    1. Non-empty `resources` array. An "empty placeholder" template is the
       single most common silent regression in this repo because the deploy
       button "succeeds" and creates an empty resource group.
    2. Container image suffix matches the transport family:
         azure-template.json                        -> base image (no suffix)
         azure-template-with-eventhub.json          -> base image
         azure-template-with-servicebus.json        -> -amqp:latest
         azure-template-amqp.json                   -> -amqp:latest
         azure-template-mqtt.json                   -> -mqtt:latest
         azure-template-with-eventgrid-mqtt.json    -> -mqtt:latest
    3. Storage account + file share present for stateful variants
       (kafka / eventhub / servicebus). MQTT variants do not require state.
    4. Every parameter has a non-stub `metadata.description`.
       Stub phrases: empty, "<NAME> configuration value.",
       "Core configuration for this image variant.", or shorter than 25 chars.
    5. Every feeder env var the bridge reads (matched by the `<SLUG_UPPER>_`
       prefix in the bridge .py) is either exposed as an ARM parameter and
       wired into the container `environmentVariables` array, OR hardcoded as
       a literal `value` on the container. Otherwise the var is "missing" and
       the user has no way to set it.

.PARAMETER FeederSlug
  Audit only this feeder. Default: every feeder under `feeders/`.

.PARAMETER RepoRoot
  Repo root (default: parent of this script's directory).

.PARAMETER OutJson
  If supplied, write a machine-readable report to this path.

.EXAMPLE
  pwsh tools/validate-arm-templates.ps1 -FeederSlug canada-aqhi

.EXAMPLE
  pwsh tools/validate-arm-templates.ps1 -RepoRoot . -OutJson arm-audit.json

.NOTES
  Exit codes:
    0 = no blockers across audited templates (warnings allowed)
    1 = one or more blockers found
    2 = invalid invocation (missing repo, etc.)
#>
[CmdletBinding()]
param(
    [string]$FeederSlug,
    [string]$RepoRoot,
    [string]$OutJson
)

if (-not $RepoRoot) {
    $RepoRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
}
$RepoRoot = (Resolve-Path $RepoRoot).Path
$feedersRoot = Join-Path $RepoRoot 'feeders'
if (-not (Test-Path $feedersRoot)) {
    Write-Error "No feeders/ directory at $RepoRoot"
    exit 2
}

$VARIANT_RULES = @{
    'azure-template.json'                       = @{ family = 'kafka';          imageSuffix = '';            stateful = $true  }
    'azure-template-with-eventhub.json'         = @{ family = 'eventhub';       imageSuffix = '';            stateful = $true  }
    'azure-template-with-servicebus.json'       = @{ family = 'servicebus';     imageSuffix = '-amqp';       stateful = $true  }
    'azure-template-amqp.json'                  = @{ family = 'amqp';           imageSuffix = '-amqp';       stateful = $false }
    'azure-template-mqtt.json'                  = @{ family = 'mqtt';           imageSuffix = '-mqtt';       stateful = $false }
    'azure-template-with-eventgrid-mqtt.json'   = @{ family = 'eventgrid-mqtt'; imageSuffix = '-mqtt';       stateful = $false }
}

$STUB_DESCRIPTIONS = @(
    '',
    'Core configuration for this image variant.'
)

function Test-StubDescription {
    param([string]$desc, [string]$paramName)
    if ([string]::IsNullOrWhiteSpace($desc)) { return $true }
    if ($STUB_DESCRIPTIONS -contains $desc.Trim()) { return $true }
    if ($desc -match "^$([regex]::Escape($paramName))\s+configuration value\.?$") { return $true }
    if ($desc.Length -lt 25) { return $true }
    return $false
}

function Get-FeederEnvVars {
    param([string]$bridgeDir, [string]$slugUpper)
    if (-not (Test-Path $bridgeDir)) { return @() }
    $pyFiles = Get-ChildItem -Path $bridgeDir -Filter '*.py' -Recurse -ErrorAction SilentlyContinue
    $vars = New-Object System.Collections.Generic.HashSet[string]
    foreach ($py in $pyFiles) {
        $text = Get-Content $py.FullName -Raw
        if ($null -eq $text) { continue }
        # os.getenv("X"...) and os.environ["X"] and os.environ.get("X"...)
        $matches = [regex]::Matches($text, '(?:os\.getenv|os\.environ(?:\.get)?)\s*[\[(]\s*["'']([A-Z][A-Z0-9_]*)["'']')
        foreach ($m in $matches) {
            $name = $m.Groups[1].Value
            if ($name.StartsWith("$slugUpper`_")) { [void]$vars.Add($name) }
        }
    }
    return @($vars)
}

function Get-TemplateTransport {
    param([string]$templatePath)
    $name = [IO.Path]::GetFileName($templatePath).ToLowerInvariant()
    if ($name -match 'mqtt') { return 'mqtt' }
    if ($name -match 'amqp|servicebus') { return 'amqp' }
    return 'kafka'
}

function Get-TemplateFeederEnvVars {
    param(
        [string]$feederDir,
        [string]$slug,
        [string]$slugUpper,
        [string]$templatePath
    )
    $slugUnderscore = $slug -replace '-', '_'
    $transport = Get-TemplateTransport -templatePath $templatePath
    $bridgeDirName = switch ($transport) {
        'mqtt' { "${slugUnderscore}_mqtt" }
        'amqp' { "${slugUnderscore}_amqp" }
        default { $slugUnderscore }
    }
    $bridgeDir = Join-Path $feederDir $bridgeDirName
    if (Test-Path $bridgeDir) {
        return Get-FeederEnvVars -bridgeDir $bridgeDir -slugUpper $slugUpper
    }
    if ($transport -ne 'kafka') {
        $fallbackDir = Join-Path $feederDir $slugUnderscore
        if (Test-Path $fallbackDir) {
            return Get-FeederEnvVars -bridgeDir $fallbackDir -slugUpper $slugUpper
        }
    }
    return @()
}

function Get-TemplateEnvVars {
    param($template)
    $cg = $template.resources | Where-Object { $_.type -eq 'Microsoft.ContainerInstance/containerGroups' } | Select-Object -First 1
    if (-not $cg) { return @() }
    $container = $cg.properties.containers | Select-Object -First 1
    if (-not $container) { return @() }
    return @($container.properties.environmentVariables | ForEach-Object { $_.name })
}

function Test-TemplateEnvCoverage {
    param(
        [string]$envVar,
        [string[]]$templateEnvNames
    )
    if ($templateEnvNames -contains $envVar) { return $true }
    if ($envVar -match '(_STATE_FILE|LAST_POLLED_FILE)$' -and $templateEnvNames -contains 'STATE_FILE') { return $true }
    return $false
}

function Get-ContainerMdEnvVars {
    param([string]$containerMdPath)
    if (-not (Test-Path $containerMdPath)) { return @() }
    $text = Get-Content $containerMdPath -Raw
    $vars = New-Object System.Collections.Generic.HashSet[string]
    # match leading-pipe markdown table cells beginning with an env-var token, e.g.
    # | `FOO_BAR` | description |
    # | FOO_BAR | description |
    foreach ($m in [regex]::Matches($text, '(?m)^\|\s*`?([A-Z][A-Z0-9_]{2,})`?\s*\|')) {
        $name = $m.Groups[1].Value
        # filter heading rows and separator markers
        if ($name -in @('NAME','VARIABLE','KEY','VAR','ENV','PARAMETER')) { continue }
        [void]$vars.Add($name)
    }
    return @($vars)
}

function Audit-Template {
    param(
        [string]$path,
        [string]$slug,
        [string]$slugUpper,
        [string[]]$feederEnvVars,
        [string[]]$containerMdVars
    )
    $variantName = Split-Path $path -Leaf
    $rules = $VARIANT_RULES[$variantName]
    if (-not $rules) { return $null }

    $issues = New-Object System.Collections.Generic.List[hashtable]
    $addIssue = {
        param($severity, $code, $message)
        $issues.Add(@{ severity = $severity; code = $code; message = $message })
    }

    try {
        $template = Get-Content $path -Raw | ConvertFrom-Json -ErrorAction Stop
    } catch {
        & $addIssue 'blocker' 'parse-error' "JSON parse failed: $($_.Exception.Message)"
        return @{ path = $path; variant = $variantName; family = $rules.family; issues = $issues }
    }

    # Check 1: non-empty resources
    if (-not $template.resources -or $template.resources.Count -eq 0) {
        & $addIssue 'blocker' 'empty-resources' "resources array is empty; deploy will create an empty resource group"
        return @{ path = $path; variant = $variantName; family = $rules.family; issues = $issues }
    }

    # Check 2: image suffix. The expression may be:
    #   "[concat(parameters('imageName'), '-amqp:latest')]"  (suffix in expression)
    #   "[parameters('imageName')]"                          (suffix in parameter default)
    #   "[variables('imageName')]"                           (suffix in variables block)
    $cg = $template.resources | Where-Object { $_.type -eq 'Microsoft.ContainerInstance/containerGroups' } | Select-Object -First 1
    if (-not $cg) {
        & $addIssue 'blocker' 'no-container-group' "no Microsoft.ContainerInstance/containerGroups resource"
    } else {
        $container = $cg.properties.containers | Select-Object -First 1
        $imageExpr = if ($container) { $container.properties.image } else { '' }
        $imageResolved = $imageExpr
        if ($imageExpr -match "^\[parameters\('([^']+)'\)\]$") {
            $pn = $Matches[1]
            $p = $template.parameters.$pn
            if ($p -and $p.defaultValue) { $imageResolved = $p.defaultValue }
        } elseif ($imageExpr -match "^\[variables\('([^']+)'\)\]$") {
            $vn = $Matches[1]
            if ($template.variables -and $template.variables.$vn) { $imageResolved = $template.variables.$vn }
        }
        $expectedSuffix = $rules.imageSuffix
        if ($expectedSuffix -eq '') {
            if ($imageResolved -match "-amqp:|-mqtt:") {
                & $addIssue 'blocker' 'wrong-image-suffix' "image resolves to '$imageResolved' (expr: $imageExpr) but variant $variantName expects base image (no transport suffix)"
            }
        } else {
            if ($imageResolved -notmatch [regex]::Escape($expectedSuffix + ':')) {
                & $addIssue 'blocker' 'wrong-image-suffix' "image resolves to '$imageResolved' (expr: $imageExpr) missing expected suffix '$expectedSuffix' for variant $variantName"
            }
        }
    }

    # Check 3: storage + file share for stateful variants.
    # Only block when the bridge actually reads a *_STATE_FILE env var.
    if ($rules.stateful) {
        $needsState = $feederEnvVars | Where-Object { $_ -match '(_STATE_FILE|LAST_POLLED_FILE)$' }
        $hasStorage = $template.resources | Where-Object { $_.type -eq 'Microsoft.Storage/storageAccounts' }
        $hasShare   = $template.resources | Where-Object { $_.type -eq 'Microsoft.Storage/storageAccounts/fileServices/shares' }
        if ($needsState) {
            if (-not $hasStorage) { & $addIssue 'blocker' 'missing-storage'    "stateful variant ($($rules.family)) needs state file but template has no Microsoft.Storage/storageAccounts" }
            if (-not $hasShare)   { & $addIssue 'warning' 'missing-file-share' "stateful variant ($($rules.family)) missing fileServices/shares; state will not persist across container restarts" }
        } else {
            if (-not $hasStorage) { & $addIssue 'info'    'no-state-share'     "variant ($($rules.family)) ships without a state share — confirm the bridge is genuinely stateless (no *_STATE_FILE env var detected)" }
        }
    }

    # Check 4: metadata.description quality
    $parameters = $template.parameters
    if ($parameters) {
        $paramNames = $parameters | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
        foreach ($pn in $paramNames) {
            $param = $parameters.$pn
            $desc = $null
            if ($param.metadata -and $param.metadata.description) { $desc = $param.metadata.description }
            if (Test-StubDescription -desc $desc -paramName $pn) {
                & $addIssue 'warning' 'stub-description' "parameter '$pn' has stub or missing metadata.description"
            }
        }
    }

    # Check 5: feeder env var coverage
    if ($feederEnvVars.Count -gt 0) {
        $templateEnvNames = Get-TemplateEnvVars -template $template
        foreach ($v in $feederEnvVars) {
            if (-not (Test-TemplateEnvCoverage -envVar $v -templateEnvNames $templateEnvNames)) {
                & $addIssue 'warning' 'env-var-missing' "feeder reads `$env:$v but it is not declared in this template's container environmentVariables"
            }
        }
    }

    # Check 6: CONTAINER.md ↔ ARM environmentVariables symmetry.
    # Every feeder-prefixed env var the template exposes must also appear in
    # CONTAINER.md so portal/Cloud-Shell users see the parameter documented.
    if ($containerMdVars -and $containerMdVars.Count -gt 0) {
        $templateEnvNames = Get-TemplateEnvVars -template $template
        foreach ($v in $templateEnvNames) {
            if (-not $v.StartsWith("$slugUpper`_")) { continue }
            if ($containerMdVars -notcontains $v) {
                & $addIssue 'warning' 'container-md-drift' "template exposes env var '$v' but CONTAINER.md does not document it"
            }
        }
    }

    return @{ path = $path; variant = $variantName; family = $rules.family; issues = $issues }
}

# ── Driver ──

$slugs = if ($FeederSlug) { ,$FeederSlug } else {
    Get-ChildItem $feedersRoot -Directory | Select-Object -ExpandProperty Name | Sort-Object
}

$allResults = New-Object System.Collections.Generic.List[hashtable]
$totalBlockers = 0
$totalWarnings = 0
$totalTemplates = 0

foreach ($slug in $slugs) {
    $feederDir = Join-Path $feedersRoot $slug
    if (-not (Test-Path $feederDir)) {
        Write-Warning "feeder '$slug' not found"
        continue
    }
    $slugUpper = $slug.ToUpper() -replace '-', '_'
    $containerMdVars = Get-ContainerMdEnvVars -containerMdPath (Join-Path $feederDir 'CONTAINER.md')

    # find all azure-template*.json (root + infra/)
    $templates = @()
    $templates += Get-ChildItem $feederDir -Filter 'azure-template*.json' -File -ErrorAction SilentlyContinue
    $infraDir = Join-Path $feederDir 'infra'
    if (Test-Path $infraDir) {
        $templates += Get-ChildItem $infraDir -Filter 'azure-template*.json' -File -ErrorAction SilentlyContinue
    }

    foreach ($t in $templates) {
        $feederEnvVars = Get-TemplateFeederEnvVars -feederDir $feederDir -slug $slug -slugUpper $slugUpper -templatePath $t.FullName
        $result = Audit-Template -path $t.FullName -slug $slug -slugUpper $slugUpper -feederEnvVars $feederEnvVars -containerMdVars $containerMdVars
        if ($null -eq $result) { continue }
        $result.slug = $slug
        $allResults.Add($result)
        $totalTemplates++
        foreach ($i in $result.issues) {
            if ($i.severity -eq 'blocker') { $totalBlockers++ } else { $totalWarnings++ }
        }
    }
}

# ── Report ──

Write-Host ""
Write-Host "ARM template static audit" -ForegroundColor Cyan
Write-Host "  RepoRoot:        $RepoRoot"
Write-Host "  Feeders scanned: $($slugs.Count)"
Write-Host "  Templates:       $totalTemplates"
Write-Host "  Blockers:        $totalBlockers" -ForegroundColor (@{$true='Red'; $false='Green'}[$totalBlockers -gt 0])
Write-Host "  Warnings:        $totalWarnings" -ForegroundColor (@{$true='Yellow'; $false='Green'}[$totalWarnings -gt 0])
Write-Host ""

$bySlug = $allResults | Group-Object slug
foreach ($g in $bySlug) {
    $slugBlockers = ($g.Group | ForEach-Object { $_.issues } | Where-Object severity -eq 'blocker').Count
    $slugWarnings = ($g.Group | ForEach-Object { $_.issues } | Where-Object severity -eq 'warning').Count
    if (($slugBlockers + $slugWarnings) -eq 0) { continue }
    Write-Host "[$($g.Name)] blockers=$slugBlockers warnings=$slugWarnings" -ForegroundColor (@{$true='Red'; $false='Yellow'}[$slugBlockers -gt 0])
    foreach ($r in $g.Group) {
        if ($r.issues.Count -eq 0) { continue }
        Write-Host "  $($r.variant)"
        foreach ($i in $r.issues) {
            $color = if ($i.severity -eq 'blocker') { 'Red' } else { 'Yellow' }
            Write-Host "    [$($i.severity.ToUpper())] $($i.code): $($i.message)" -ForegroundColor $color
        }
    }
}

if ($totalBlockers -eq 0 -and $totalWarnings -eq 0) {
    Write-Host "PASS: all $totalTemplates templates pass static audit." -ForegroundColor Green
} elseif ($totalBlockers -eq 0) {
    Write-Host "PASS (with $totalWarnings warning(s))." -ForegroundColor Yellow
} else {
    Write-Host "FAIL: $totalBlockers blocker(s) across $totalTemplates template(s)." -ForegroundColor Red
}

if ($OutJson) {
    $report = @{
        repoRoot       = $RepoRoot
        feedersScanned = $slugs.Count
        templatesScanned = $totalTemplates
        totalBlockers  = $totalBlockers
        totalWarnings  = $totalWarnings
        results        = $allResults
    }
    $report | ConvertTo-Json -Depth 10 | Set-Content -Path $OutJson -Encoding UTF8
    Write-Host "Report written to $OutJson"
}

exit (@{$true=1; $false=0}[$totalBlockers -gt 0])
