<#
.SYNOPSIS
    Receives messages from a Service Bus topic and validates AMQP CloudEvents properties.
    Returns the message count.
#>
param(
    [Parameter(Mandatory)][string]$ConnectionString,
    [Parameter(Mandatory)][string]$TopicName,
    [Parameter(Mandatory)][string]$SessionDir,
    [Parameter(Mandatory)][string]$Source,
    [int]$TimeoutSeconds = 600,
    [int]$MinMessages = 1
)

$consumerScript = @"
import sys, json, time
from azure.servicebus import ServiceBusClient

conn_str = sys.argv[1]
topic_name = sys.argv[2]
timeout = int(sys.argv[3])
min_msgs = int(sys.argv[4])

messages = []
errors = []
start = time.time()

client = ServiceBusClient.from_connection_string(conn_str)
# Create a temporary subscription for testing
sub_name = "e2e-test-sub"
try:
    from azure.servicebus.management import ServiceBusAdministrationClient
    admin = ServiceBusAdministrationClient.from_connection_string(conn_str)
    try:
        admin.create_subscription(topic_name, sub_name)
    except Exception:
        pass  # may already exist

    with client:
        receiver = client.get_subscription_receiver(
            topic_name=topic_name,
            subscription_name=sub_name,
            max_wait_time=30
        )
        with receiver:
            while len(messages) < min_msgs and (time.time() - start) < timeout:
                batch = receiver.receive_messages(max_message_count=10, max_wait_time=30)
                for msg in batch:
                    app_props = {str(k): str(v) for k, v in (msg.application_properties or {}).items()}
                    body = str(msg)
                    messages.append({
                        "properties": app_props,
                        "content_type": msg.content_type,
                        "body_size": len(body)
                    })
                    # Validate AMQP CloudEvents binding (cloudEvents: prefix)
                    for attr in ["cloudEvents:type", "cloudEvents:source", "cloudEvents:subject"]:
                        # Also check byte-decoded key variants
                        found = any(attr in k or attr.encode() == k for k in (msg.application_properties or {}).keys())
                        if not found:
                            errors.append(f"Message {len(messages)-1}: missing AMQP property '{attr}'")
                    receiver.complete_message(msg)

    # Cleanup subscription
    try:
        admin.delete_subscription(topic_name, sub_name)
    except Exception:
        pass

except Exception as e:
    print(json.dumps({"error": str(e), "messages": messages, "validation_errors": errors}))
    sys.exit(1)

print(json.dumps({"messages": messages, "count": len(messages), "validation_errors": errors}))
"@

$scriptPath = Join-Path $SessionDir "$Source-sb-consumer.py"
$consumerScript | Set-Content $scriptPath -Encoding utf8

$pyResult = python $scriptPath $ConnectionString $TopicName $TimeoutSeconds $MinMessages 2>&1 | Out-String
Remove-Item $scriptPath -ErrorAction SilentlyContinue

$parsed = $pyResult.Trim() | ConvertFrom-Json
if ($parsed.error) {
    throw "Service Bus consumer error: $($parsed.error)"
}
if ($parsed.validation_errors -and $parsed.validation_errors.Count -gt 0) {
    Write-Warning "AMQP CloudEvents validation errors: $($parsed.validation_errors -join '; ')"
}

return $parsed.count
