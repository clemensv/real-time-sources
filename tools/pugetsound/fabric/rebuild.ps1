$feeders = @(
    "feeders\seattle-911\kql\seattle-911.kql",
    "feeders\seattle-street-closures\kql\seattle-street-closures.kql",
    "feeders\king-county-marine\kql\king_county_marine.kql",
    "feeders\epa-uv\kql\epa_uv.kql",
    "feeders\nws-forecasts\kql\nws-forecasts.kql",
    "feeders\wsdot\kql\wsdot.kql",
    "feeders\noaa\kql\noaa.kql"
)

$out = [System.Collections.Generic.List[string]]::new()
$first = $true

foreach ($f in $feeders) {
    $lines = [System.IO.File]::ReadAllLines((Join-Path $pwd $f))
    if ($first) {
        $out.AddRange([string[]]$lines)
        $out.Add("")
        $first = $false
        continue
    }
    $skip = $true
    $fenceCount = 0
    foreach ($line in $lines) {
        if ($skip) {
                if ($line.Trim() -match '^```$') { $fenceCount++ }
                if ($fenceCount -ge 2) { $skip = $false; continue }
            continue
        }
        $out.Add($line)
    }
    $out.Add("")
}

$combined = [string]::Join("`n", $out)
[System.IO.File]::WriteAllText((Join-Path $pwd "tools\pugetsound\fabric\pugetsound.kql"), $combined, (New-Object System.Text.UTF8Encoding($false)))
$cnt = ([regex]::Matches($combined, "\.create-merge table \[_cloudevents_dispatch\]")).Count
$tc  = ([regex]::Matches($combined, "\.create-merge table \[")).Count + ([regex]::Matches($combined, "\.create-merge table \['")).Count
Write-Host "DONE dispatch=$cnt total_create_merge=$tc"
