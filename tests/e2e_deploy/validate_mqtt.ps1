<#
.SYNOPSIS
    Subscribes to an Event Grid MQTT namespace with a freshly-registered client
    certificate and validates CloudEvents MQTT user properties. Returns the
    message count.

.DESCRIPTION
    Event Grid MQTT namespaces do NOT accept an external subscriber that merely
    holds an Entra "EventGrid TopicSpaces Subscriber" RBAC role on the topic
    space — the user token's `sub` claim does not match the `oid` the broker
    authorizes, and username/password is the wrong transport for the JWT anyway.
    The working approach (verified live) is:

      1. Register a self-signed client certificate as a namespace Client
         (ThumbprintMatch) with a Subscriber permission binding on the topic
         space — via tools/Register-EventGridMqttTestClient.ps1.
      2. Subscribe to the topic space's actual `topicTemplates` (which end in
         `/#`), NOT a bare `#`. A bare `#` is broader than the topic-space
         template and the broker returns SUBACK reason code 135 (Not
         authorized); the template itself is granted (reason code 1) and
         receives every published message regardless of topic depth.

    This was the root cause of the long-standing "issue #840" WARNs: the
    validator subscribed to bare `#`, was silently rejected (no on_subscribe
    SUBACK check), and reported 0 messages. Subscribing to the topic-space
    template fixes it.

    Return contract:
      >= 1  : that many CloudEvents messages were received and validated.
       0    : connected + SUBACK granted, but the feeder published nothing in
              the window (legitimately quiet source — caller treats as WARN
              no-data, NOT a failure).
      -1    : genuine block — cert registration failed, CONNACK rejected, or
              SUBACK rejected (reason code >= 128). Caller treats as WARN
              blocked.

    The Source parameter locates the feeder folder for logging only; the
    subscribe filters come from the live topic space, not from xreg.
#>
param(
    [Parameter(Mandatory)][string]$Hostname,
    [Parameter(Mandatory)][string]$ResourceGroup,
    [Parameter(Mandatory)][string]$Subscription,
    [Parameter(Mandatory)][string]$SessionDir,
    [Parameter(Mandatory)][string]$Source,
    [string]$TopicPattern = "",   # optional explicit override; otherwise live topic templates are used
    [int]$TimeoutSeconds = 600,
    [int]$MinMessages = 1
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path "$PSScriptRoot/../..").Path

# 1. Resolve the Event Grid namespace and its first topic space.
$egNs = az eventgrid namespace list --resource-group $ResourceGroup --subscription $Subscription `
    --query "[0]" -o json 2>$null | ConvertFrom-Json
if (-not $egNs) {
    Write-Warning "No Event Grid namespace found in resource group '$ResourceGroup'."
    return -1
}
$nsName  = $egNs.name
$mqttHost = if ($Hostname) { $Hostname } else { $egNs.topicSpacesConfiguration.hostname }

$topicSpaces = az eventgrid namespace topic-space list --resource-group $ResourceGroup `
    --namespace-name $nsName --subscription $Subscription -o json 2>$null | ConvertFrom-Json
if (-not $topicSpaces -or @($topicSpaces).Count -eq 0) {
    Write-Warning "No topic space found on namespace '$nsName'."
    return -1
}
$ts      = @($topicSpaces)[0]
$tsName  = $ts.name
$templates = @($ts.topicTemplates)
if ($TopicPattern) { $templates = @($TopicPattern) }
if (-not $templates -or $templates.Count -eq 0) { $templates = @('#') }
Write-Host "  Topic space: $tsName  templates: $($templates -join ', ')"

# 2. Register a cert-based subscriber client + Subscriber permission binding.
$certDir = Join-Path $SessionDir "mqtt-certs-$Source"
if (Test-Path $certDir) { Remove-Item $certDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $certDir | Out-Null
$clientName = ("e2e-reader-$Source" -replace '[^-a-zA-Z0-9]', '-')
if ($clientName.Length -gt 60) { $clientName = $clientName.Substring(0, 60) }
$registerLog = Join-Path $certDir 'register.log'
Write-Host "  Registering cert subscriber client '$clientName' on topic space '$tsName'..."
& "$repoRoot\tools\Register-EventGridMqttTestClient.ps1" `
    -ResourceGroup $ResourceGroup `
    -NamespaceName $nsName `
    -SubscriptionId $Subscription `
    -ClientName $clientName `
    -ClientGroupName "e2e-readers" `
    -TopicSpaceName $tsName `
    -OutputDirectory $certDir `
    -CertValidityDays 1 *> $registerLog
$certFile = Join-Path $certDir "$clientName.crt"
$keyFile  = Join-Path $certDir "$clientName.key"
$caFile   = Join-Path $certDir "$clientName-ca.crt"
if (-not (Test-Path $certFile) -or -not (Test-Path $keyFile)) {
    Write-Warning "Cert registration failed; see $registerLog (tail):"
    Get-Content $registerLog -Tail 20 -ErrorAction SilentlyContinue | ForEach-Object { Write-Warning "    $_" }
    return -1
}
# Cert + permission binding propagation.
Start-Sleep -Seconds 30

# 3. Subscribe with the cert, SUBACK-checked, against the topic-space templates.
$consumerScript = @'
import sys, json, time, threading, os
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

hostname, certfile, keyfile, cafile, client_id, templates_arg, timeout, minmsgs = (
    sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
    sys.argv[6], int(sys.argv[7]), int(sys.argv[8])
)
templates = [t for t in templates_arg.split(';') if t]

messages = []
connected = threading.Event()
suback = {}
mid_to_topic = {}
auth_rejected = []
connack = {"rc": None}


def on_connect(c, u, f, rc, props=None):
    rc2 = rc if isinstance(rc, int) else rc.value
    connack["rc"] = rc2
    if rc2 == 0:
        for t in templates:
            res, mid = c.subscribe(t, qos=1)
            mid_to_topic[mid] = t
        connected.set()
    else:
        auth_rejected.append("CONNACK rc=%d" % rc2)
        connected.set()


def on_subscribe(c, u, mid, reason_codes, props=None):
    vals = [(rc if isinstance(rc, int) else rc.value) for rc in reason_codes]
    suback[mid_to_topic.get(mid, "?")] = vals
    for v in vals:
        if v >= 128:
            auth_rejected.append("SUBACK %s rc=%d" % (mid_to_topic.get(mid, "?"), v))


def on_message(c, u, msg):
    up = {}
    p2 = getattr(msg, "properties", None)
    if p2 and getattr(p2, "UserProperty", None):
        up = {str(k): str(v) for k, v in p2.UserProperty}
    messages.append({"topic": msg.topic, "user_properties": up, "payload_size": len(msg.payload)})


c = mqtt.Client(client_id=client_id, callback_api_version=CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
if cafile and os.path.exists(cafile):
    c.tls_set(ca_certs=cafile, certfile=certfile, keyfile=keyfile)
else:
    c.tls_set(certfile=certfile, keyfile=keyfile)
c.username_pw_set(client_id)
c.on_connect = on_connect
c.on_subscribe = on_subscribe
c.on_message = on_message
c.connect(hostname, 8883, keepalive=60)
c.loop_start()

if not connected.wait(30):
    print(json.dumps({"error": "connect-timeout", "messages": [], "count": 0}))
    sys.exit(1)
if connack["rc"] not in (0, None):
    print(json.dumps({"error": "connack:" + ";".join(auth_rejected), "messages": [], "count": 0}))
    sys.exit(1)

# Give SUBACKs a moment, then bail early if every subscription was rejected.
time.sleep(3)
if auth_rejected and len(messages) == 0:
    print(json.dumps({"error": "suback-rejected:" + ";".join(auth_rejected),
                      "suback": suback, "messages": [], "count": 0}))
    sys.exit(1)

deadline = time.time() + timeout
while time.time() < deadline and len(messages) < minmsgs:
    time.sleep(1)
c.loop_stop()
c.disconnect()

# CloudEvents MQTT user-property validation (bare names per CE MQTT binding;
# accept ce- prefixed too, both observed in practice).
verr = []
for i, m in enumerate(messages[:50]):
    up = m["user_properties"]
    for bare, pref in [("type", "ce-type"), ("source", "ce-source"), ("subject", "ce-subject")]:
        if bare not in up and pref not in up:
            verr.append("msg%d missing %s" % (i, bare))

print(json.dumps({"messages": messages[:10], "count": len(messages),
                  "suback": suback, "auth_rejected": auth_rejected,
                  "validation_errors": verr}))
'@

$scriptPath = Join-Path $certDir "subscriber.py"
$consumerScript | Set-Content $scriptPath -Encoding utf8
$templatesArg = ($templates -join ';')
$stderrFile = Join-Path $certDir 'sub-err.log'
$pyResult = & python $scriptPath $mqttHost $certFile $keyFile $caFile $clientName $templatesArg $TimeoutSeconds $MinMessages 2>$stderrFile | Out-String
$pyExit = $LASTEXITCODE
$stderrContent = ((Get-Content $stderrFile -Raw -ErrorAction SilentlyContinue) ?? "").Trim()

$jsonLine = ($pyResult -split "`n" | Where-Object { $_ -ne $null -and $_.Trim().StartsWith('{') } | Select-Object -Last 1)

# Clean up cert material (contains a private key).
Remove-Item $certDir -Recurse -Force -ErrorAction SilentlyContinue

if (-not $jsonLine) {
    Write-Warning "No JSON output from MQTT subscriber. Stderr: $stderrContent"
    return -1
}
$parsed = $jsonLine.Trim() | ConvertFrom-Json

if ($parsed.error) {
    Write-Warning "MQTT subscribe blocked: $($parsed.error)"
    if ($parsed.suback) { Write-Warning "  SUBACK reason codes: $($parsed.suback | ConvertTo-Json -Compress)" }
    return -1
}
if ($parsed.validation_errors -and $parsed.validation_errors.Count -gt 0) {
    Write-Warning "MQTT CloudEvents validation errors: $($parsed.validation_errors -join '; ')"
}
Write-Host "  SUBACK reason codes: $($parsed.suback | ConvertTo-Json -Compress)"
Write-Host "  Received $($parsed.count) MQTT message(s) via cert subscriber"
return [int]$parsed.count
