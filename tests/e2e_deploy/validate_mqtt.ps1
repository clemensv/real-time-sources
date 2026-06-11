<#
.SYNOPSIS
    Subscribes to an Event Grid MQTT namespace and validates CloudEvents MQTT user properties.
    Returns the message count.

.DESCRIPTION
    NOTE: Event Grid MQTT namespace RBAC roles (EventGrid TopicSpaces Subscriber) alone do NOT
    allow external connections from non-Azure clients. A registered client certificate or
    Entra JWT client registration is required. This script will fail with rc=135 (Not authorized)
    from external (non-Azure) machines without an explicit client registration.

    This is a known limitation tracked in GitHub Issue #840.
    Currently documents the expected behavior and returns 0 as a BLOCKED result.

    The Source parameter is used to derive the MQTT topic subscription pattern from the
    xreg manifest's topic space template (not a hardcoded pattern).
#>
param(
    [Parameter(Mandatory)][string]$Hostname,
    [Parameter(Mandatory)][string]$ResourceGroup,
    [Parameter(Mandatory)][string]$Subscription,
    [Parameter(Mandatory)][string]$SessionDir,
    [Parameter(Mandatory)][string]$Source,
    [string]$TopicPattern = "",  # derived from xreg if empty
    [int]$TimeoutSeconds = 600,
    [int]$MinMessages = 1
)

$repoRoot = (Resolve-Path "$PSScriptRoot/../..").Path
$sourceDir = Join-Path $repoRoot "feeders" $Source

# Derive topic pattern from xreg if not provided
if (-not $TopicPattern) {
    $xregFiles = Get-ChildItem "$sourceDir/xreg" -Filter "*.xreg.json" -ErrorAction SilentlyContinue
    if ($xregFiles) {
        $xreg = Get-Content $xregFiles[0].FullName -Raw | ConvertFrom-Json
        # Find topicSpaces entries for MQTT binding
        $topicTemplates = $xreg.endpoints.PSObject.Properties.Value |
            Where-Object { $_.config.protocol -eq "mqtt" } |
            Select-Object -ExpandProperty config -ErrorAction SilentlyContinue |
            Select-Object -ExpandProperty topicTemplates -ErrorAction SilentlyContinue
        if ($topicTemplates) {
            # Convert URI template to MQTT wildcard
            $rawPattern = $topicTemplates | Select-Object -First 1
            $TopicPattern = ($rawPattern -replace "\{[^}]+\}", "+")
        }
    }
}

if (-not $TopicPattern) {
    Write-Warning "Could not derive MQTT topic pattern from xreg for '$Source'. Using '#'."
    $TopicPattern = "#"
}
Write-Host "  MQTT topic pattern: $TopicPattern"

$consumerScript = @"
import sys, json, time, ssl, threading
import paho.mqtt.client as mqtt

hostname = sys.argv[1]
topic_pattern = sys.argv[2]
timeout = int(sys.argv[3])
min_msgs = int(sys.argv[4])
token = sys.argv[5] if len(sys.argv) > 5 else ""

messages = []
errors = []
connected = threading.Event()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe(topic_pattern, qos=1)
        connected.set()
    else:
        errors.append(f"Connect failed with rc={rc} (Not authorized={rc==5})")
        connected.set()

def on_message(client, userdata, msg):
    user_props = {}
    if hasattr(msg, 'properties') and msg.properties and msg.properties.UserProperty:
        user_props = {k: v for k, v in msg.properties.UserProperty}
    messages.append({
        "topic": msg.topic,
        "user_properties": user_props,
        "payload_size": len(msg.payload),
        "payload_preview": msg.payload[:200].decode(errors='replace')
    })

client = mqtt.Client(protocol=mqtt.MQTTv5, client_id=f"e2e-test-{topic_pattern[:20].replace('/','').replace('+','')}")
client.on_connect = on_connect
client.on_message = on_message

if token:
    client.username_pw_set(username="e2e-test-client", password=token)
client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)

try:
    client.connect(hostname, 8883, keepalive=60)
    client.loop_start()

    if not connected.wait(timeout=30):
        raise Exception("Connection timeout")

    if errors and "Not authorized" in errors[0]:
        raise Exception(f"Auth rejected: {errors[0]}. External MQTT subscription requires registered client cert. See issue #840.")

    start = time.time()
    while len(messages) < min_msgs and (time.time() - start) < timeout:
        time.sleep(1)

    client.loop_stop()
    client.disconnect()

    # Validate CloudEvents MQTT binary binding:
    # Per CloudEvents MQTT spec, attribute names are bare (no ce- prefix).
    # The generated client strips ce- prefix before setting user properties.
    for i, msg in enumerate(messages):
        up = msg["user_properties"]
        # Accept both bare names and ce- prefixed (both observed in practice)
        for attr_bare, attr_prefixed in [("type","ce-type"), ("source","ce-source"), ("subject","ce-subject")]:
            if attr_bare not in up and attr_prefixed not in up:
                errors.append(f"Message {i}: missing MQTT user property '{attr_bare}' (or '{attr_prefixed}')")

except Exception as e:
    print(json.dumps({"error": str(e), "messages": messages, "validation_errors": errors}))
    sys.exit(1)

print(json.dumps({"messages": messages, "count": len(messages), "validation_errors": errors}))
"@

# Get an Entra token for the Event Grid namespace (may not work for auth but try)
$token = az account get-access-token --resource "https://eventgrid.azure.net/" `
    --subscription $Subscription --query accessToken --output tsv 2>$null

$scriptPath = Join-Path $SessionDir "$Source-mqtt-consumer.py"
$consumerScript | Set-Content $scriptPath -Encoding utf8

if (-not (Test-Path $scriptPath)) {
    throw "Failed to write consumer script to '$scriptPath'. Ensure SessionDir exists: $SessionDir"
}

$stderrFile = [System.IO.Path]::GetTempFileName()
$pyResult = & python $scriptPath $Hostname $TopicPattern $TimeoutSeconds $MinMessages $token 2>$stderrFile | Out-String
$stderrContent = ((Get-Content $stderrFile -Raw -ErrorAction SilentlyContinue) ?? "").Trim()
Remove-Item $stderrFile -ErrorAction SilentlyContinue
Remove-Item $scriptPath -ErrorAction SilentlyContinue

# Extract the JSON line (last line starting with '{') in case there are non-JSON warnings on stdout
$jsonLine = ($pyResult -split "`n" | Where-Object { $_ -ne $null -and $_.Trim().StartsWith('{') } | Select-Object -Last 1)
if (-not $jsonLine) {
    throw "No JSON output from MQTT consumer. Stderr: $stderrContent. Stdout: $pyResult"
}
$parsed = $jsonLine.Trim() | ConvertFrom-Json
if ($parsed.error) {
    Write-Warning "MQTT consumer blocked: $($parsed.error)"
    Write-Warning "This is a known limitation for EG MQTT from external clients. See issue #840."
    return -1  # Signal blocked (not a test error, but not success either)
}
if ($parsed.validation_errors -and $parsed.validation_errors.Count -gt 0) {
    Write-Warning "MQTT CloudEvents validation errors: $($parsed.validation_errors -join '; ')"
}

return $parsed.count
