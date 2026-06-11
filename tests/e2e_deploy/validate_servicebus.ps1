<#
.SYNOPSIS
    Receives messages from a Service Bus queue or topic and validates AMQP CloudEvents properties.
    Uses DefaultAzureCredential (RBAC); caller must assign 'Azure Service Bus Data Receiver' role first.
    Returns the message count.
#>
param(
    [Parameter(Mandatory)][string]$FullyQualifiedNamespace,
    [Parameter(Mandatory)][string]$EntityName,
    [string]$EntityType = "queue",  # "queue" or "topic"
    [string]$SubscriptionName = "e2e-test-sub",
    [Parameter(Mandatory)][string]$SessionDir,
    [Parameter(Mandatory)][string]$Source,
    [int]$TimeoutSeconds = 600,
    [int]$MinMessages = 1
)

$consumerScript = @"
import sys, json, time
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient

fqns = sys.argv[1]
entity_name = sys.argv[2]
entity_type = sys.argv[3]  # "queue" or "topic"
sub_name = sys.argv[4]
timeout = int(sys.argv[5])
min_msgs = int(sys.argv[6])

messages = []
errors = []
start = time.time()

credential = DefaultAzureCredential()
client = ServiceBusClient(fully_qualified_namespace=fqns, credential=credential)

try:
    with client:
        if entity_type == "queue":
            receiver = client.get_queue_receiver(entity_name, max_wait_time=30)
        else:
            receiver = client.get_subscription_receiver(
                topic_name=entity_name,
                subscription_name=sub_name,
                max_wait_time=30
            )
        with receiver:
            while len(messages) < min_msgs and (time.time() - start) < timeout:
                batch = receiver.receive_messages(max_message_count=10, max_wait_time=30)
                for msg in batch:
                    ap = msg.application_properties or {}
                    props = {
                        (k.decode() if isinstance(k, bytes) else str(k)):
                        (v.decode() if isinstance(v, bytes) else str(v))
                        for k, v in ap.items()
                    }
                    body_bytes = b"".join(msg.body)
                    try:
                        body_obj = json.loads(body_bytes)
                    except Exception:
                        body_obj = None
                    messages.append({
                        "properties": props,
                        "content_type": msg.content_type,
                        "body_size": len(body_bytes),
                        "body_obj": body_obj
                    })
                    for attr in ["cloudEvents:type", "cloudEvents:source", "cloudEvents:subject"]:
                        if attr not in props:
                            errors.append(f"Message {len(messages)-1}: missing AMQP property '{attr}'")
                    receiver.complete_message(msg)

except Exception as e:
    print(json.dumps({"error": str(e), "messages": messages, "validation_errors": errors}))
    sys.exit(1)

print(json.dumps({"messages": messages, "count": len(messages), "validation_errors": errors}))
"@

$scriptPath = Join-Path $SessionDir "$Source-sb-consumer.py"
$consumerScript | Set-Content $scriptPath -Encoding utf8

if (-not (Test-Path $scriptPath)) {
    throw "Failed to write consumer script to '$scriptPath'. Ensure SessionDir exists: $SessionDir"
}

$stderrFile = [System.IO.Path]::GetTempFileName()
$pyResult = & python $scriptPath $FullyQualifiedNamespace $EntityName $EntityType $SubscriptionName $TimeoutSeconds $MinMessages 2>$stderrFile | Out-String
$stderrContent = ((Get-Content $stderrFile -Raw -ErrorAction SilentlyContinue) ?? "").Trim()
Remove-Item $stderrFile -ErrorAction SilentlyContinue
Remove-Item $scriptPath -ErrorAction SilentlyContinue

$jsonLine = ($pyResult -split "`n" | Where-Object { $_ -ne $null -and $_.Trim().StartsWith('{') } | Select-Object -Last 1)
if (-not $jsonLine) { throw "No JSON output from Service Bus consumer. Stderr: $stderrContent. Stdout: $pyResult" }
$parsed = $jsonLine.Trim() | ConvertFrom-Json
if ($parsed.error) {
    throw "Service Bus consumer error: $($parsed.error)"
}
if ($parsed.validation_errors -and $parsed.validation_errors.Count -gt 0) {
    Write-Warning "AMQP CloudEvents validation errors: $($parsed.validation_errors -join '; ')"
}

return $parsed.count
