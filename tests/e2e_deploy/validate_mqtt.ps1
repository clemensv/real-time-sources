<#
.SYNOPSIS
    Subscribes to an Event Grid MQTT namespace and validates CloudEvents MQTT user properties.
    Returns the message count.

.DESCRIPTION
    Uses Entra ID (managed identity or service principal) to authenticate to
    the Event Grid MQTT broker and subscribe to the source's topic tree.
    Validates MQTT v5 user properties for CloudEvents binding (ce- prefix).
#>
param(
    [Parameter(Mandatory)][string]$Hostname,
    [Parameter(Mandatory)][string]$ResourceGroup,
    [Parameter(Mandatory)][string]$Subscription,
    [Parameter(Mandatory)][string]$SessionDir,
    [Parameter(Mandatory)][string]$Source,
    [int]$TimeoutSeconds = 600,
    [int]$MinMessages = 1
)

$consumerScript = @"
import sys, json, time, ssl, threading
import paho.mqtt.client as mqtt

hostname = sys.argv[1]
source = sys.argv[2]
timeout = int(sys.argv[3])
min_msgs = int(sys.argv[4])
token = sys.argv[5]

messages = []
errors = []
connected = threading.Event()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        # Subscribe to source topic tree (wildcard)
        client.subscribe(f"sources/{source}/#", qos=1)
        connected.set()
    else:
        errors.append(f"Connect failed with rc={rc}")
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

client = mqtt.Client(protocol=mqtt.MQTTv5, client_id=f"e2e-test-{source}")
client.on_connect = on_connect
client.on_message = on_message

# Entra JWT auth for Event Grid MQTT
client.username_pw_set(username=f"e2e-test-{source}", password=token)
client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)

try:
    client.connect(hostname, 8883, keepalive=60)
    client.loop_start()

    if not connected.wait(timeout=30):
        raise Exception("Connection timeout")

    start = time.time()
    while len(messages) < min_msgs and (time.time() - start) < timeout:
        time.sleep(1)

    client.loop_stop()
    client.disconnect()

    # Validate CloudEvents MQTT binding (ce- prefix)
    for i, msg in enumerate(messages):
        up = msg["user_properties"]
        for attr in ["ce-type", "ce-source", "ce-subject"]:
            if attr not in up:
                errors.append(f"Message {i}: missing MQTT user property '{attr}'")

except Exception as e:
    print(json.dumps({"error": str(e), "messages": messages, "validation_errors": errors}))
    sys.exit(1)

print(json.dumps({"messages": messages, "count": len(messages), "validation_errors": errors}))
"@

# Get an Entra token for the Event Grid namespace
$token = az account get-access-token --resource "https://eventgrid.azure.net" `
    --subscription $Subscription --query accessToken --output tsv

$scriptPath = Join-Path $SessionDir "$Source-mqtt-consumer.py"
$consumerScript | Set-Content $scriptPath -Encoding utf8

$pyResult = python $scriptPath $Hostname $Source $TimeoutSeconds $MinMessages $token 2>&1 | Out-String
Remove-Item $scriptPath -ErrorAction SilentlyContinue

$parsed = $pyResult.Trim() | ConvertFrom-Json
if ($parsed.error) {
    throw "MQTT consumer error: $($parsed.error)"
}
if ($parsed.validation_errors -and $parsed.validation_errors.Count -gt 0) {
    Write-Warning "MQTT CloudEvents validation errors: $($parsed.validation_errors -join '; ')"
}

return $parsed.count
