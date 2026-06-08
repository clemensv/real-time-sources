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
import sys, json, time, re
from confluent_kafka import Consumer, KafkaError

conn_str = sys.argv[1]
eh_name  = sys.argv[2]
timeout  = int(sys.argv[3])
min_msgs = int(sys.argv[4])

# Parse EH AMQP connection string into Kafka bootstrap / SASL config
ns_match  = re.search(r'Endpoint=sb://([^/]+\.servicebus\.windows\.net)/', conn_str)
namespace = ns_match.group(1) if ns_match else ''

conf = {
    'bootstrap.servers':   f'{namespace}:9093',
    'security.protocol':   'SASL_SSL',
    'sasl.mechanism':      'PLAIN',
    'sasl.username':       '`$ConnectionString',
    'sasl.password':       conn_str,
    'group.id':            f'e2e-test-{int(time.time())}',
    'auto.offset.reset':   'earliest',
    'enable.auto.commit':  False,
    'session.timeout.ms':  10000,
}

consumer = Consumer(conf)
consumer.subscribe([eh_name])

messages    = []
error_items = []
start       = time.time()

try:
    while len(messages) < min_msgs and (time.time() - start) < timeout:
        msg = consumer.poll(timeout=5.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                error_items.append(str(msg.error()))
            continue
        props = {}
        if msg.headers():
            for k, v in msg.headers():
                props[k] = v.decode('utf-8') if isinstance(v, bytes) else str(v)
        body = msg.value() or b''
        try:
            body_str = body.decode('utf-8')
        except Exception:
            body_str = ''
        messages.append({
            'partition': msg.partition(),
            'offset':    msg.offset(),
            'properties': props,
            'body_preview': body_str[:200],
            'body_size': len(body),
        })
except Exception as e:
    error_items.append(str(e))
finally:
    consumer.close()

for i, m in enumerate(messages):
    p = m['properties']
    for hdr in ['ce_type', 'ce_source', 'ce_subject']:
        if hdr not in p:
            error_items.append(f'Message {i}: missing Kafka header {hdr}')

print(json.dumps({'messages': messages, 'count': len(messages), 'validation_errors': error_items}))
"@

$scriptPath = Join-Path $SessionDir "$Source-eh-consumer.py"
$consumerScript | Set-Content $scriptPath -Encoding utf8

$stderrFile = [System.IO.Path]::GetTempFileName()
$pyResult = python $scriptPath $ConnectionString $EventHubName $TimeoutSeconds $MinMessages 2>$stderrFile | Out-String
$stderrContent = (Get-Content $stderrFile -Raw -ErrorAction SilentlyContinue).Trim()
Remove-Item $stderrFile -ErrorAction SilentlyContinue
Remove-Item $scriptPath -ErrorAction SilentlyContinue

# Extract the JSON line (last line starting with '{') in case there are non-JSON warnings
$jsonLine = ($pyResult -split "`n" | Where-Object { $_ -ne $null -and $_.Trim().StartsWith('{') } | Select-Object -Last 1)
if (-not $jsonLine) { throw "No JSON output from Event Hub consumer. Stderr: $stderrContent. Stdout: $pyResult" }
$parsed = $jsonLine.Trim() | ConvertFrom-Json
if ($parsed.error) {
    throw "Event Hub consumer error: $($parsed.error)"
}
if ($parsed.validation_errors -and $parsed.validation_errors.Count -gt 0) {
    Write-Warning "CloudEvents validation errors: $($parsed.validation_errors -join '; ')"
}

return $parsed.count
