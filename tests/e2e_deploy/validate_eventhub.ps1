<#
.SYNOPSIS
    Consumes messages from an Event Hub and validates CloudEvents Kafka headers.
    Returns the message count.
#>
param(
    [Parameter(Mandatory)][string]$ConnectionString,
    [Parameter(Mandatory)][string]$EventHubName,
    [Parameter(Mandatory)][string]$SessionDir,
    [Parameter(Mandatory)][string]$Source,
    [int]$TimeoutSeconds = 600,
    [int]$MinMessages = 1
)

$consumerScript = @"
import sys, json, time
from azure.eventhub import EventHubConsumerClient

conn_str = sys.argv[1]
eh_name = sys.argv[2]
timeout = int(sys.argv[3])
min_msgs = int(sys.argv[4])

messages = []
start = time.time()

def on_event(partition_context, event):
    if event:
        props = {}
        if event.properties:
            props = {k.decode() if isinstance(k, bytes) else str(k): v.decode() if isinstance(v, bytes) else str(v)
                     for k, v in event.properties.items()}
        body = event.body_as_str()
        messages.append({
            "partition": partition_context.partition_id,
            "offset": event.offset,
            "properties": props,
            "body_preview": body[:200] if body else "",
            "body_size": len(body) if body else 0
        })
        partition_context.update_checkpoint(event)

client = EventHubConsumerClient.from_connection_string(conn_str, consumer_group="\$Default", eventhub_name=eh_name)
try:
    with client:
        while len(messages) < min_msgs and (time.time() - start) < timeout:
            client.receive(on_event=on_event, starting_position="-1", max_wait_time=30)
            if len(messages) >= min_msgs:
                break
except Exception as e:
    print(json.dumps({"error": str(e), "messages": messages}))
    sys.exit(1)

# Validate CloudEvents Kafka headers
errors = []
for i, msg in enumerate(messages):
    p = msg["properties"]
    for hdr in ["ce_type", "ce_source", "ce_subject"]:
        if hdr not in p:
            errors.append(f"Message {i}: missing {hdr}")

print(json.dumps({"messages": messages, "count": len(messages), "validation_errors": errors}))
"@

$scriptPath = Join-Path $SessionDir "$Source-eh-consumer.py"
$consumerScript | Set-Content $scriptPath -Encoding utf8

$pyResult = python $scriptPath $ConnectionString $EventHubName $TimeoutSeconds $MinMessages 2>&1 | Out-String
Remove-Item $scriptPath -ErrorAction SilentlyContinue

$parsed = $pyResult.Trim() | ConvertFrom-Json
if ($parsed.error) {
    throw "Event Hub consumer error: $($parsed.error)"
}
if ($parsed.validation_errors -and $parsed.validation_errors.Count -gt 0) {
    Write-Warning "CloudEvents validation errors: $($parsed.validation_errors -join '; ')"
}

return $parsed.count
