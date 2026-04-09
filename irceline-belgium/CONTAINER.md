# Container contract for IRCELINE Belgium

This container polls the public IRCELINE Belgium SOS Timeseries API and emits CloudEvents to Kafka in structured mode with `application/cloudevents+json`.

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | No | empty | Kafka/Event Hubs connection string. Supports Event Hubs `Endpoint=...;EntityPath=...` and plain Kafka `BootstrapServer=host:port;EntityPath=topic` styles. |
| `KAFKA_BOOTSTRAP_SERVERS` | No | unset | Plain Kafka bootstrap servers. Overrides `BootstrapServer` from `CONNECTION_STRING` when set. |
| `KAFKA_TOPIC` | No | `irceline-belgium` | Kafka topic for all station, timeseries, and observation events. |
| `SASL_USERNAME` | No | unset | SASL username for plain Kafka clusters that require authentication. |
| `SASL_PASSWORD` | No | unset | SASL password for plain Kafka clusters that require authentication. |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for local Docker Kafka brokers that use PLAINTEXT. |
| `POLLING_INTERVAL` | No | `3600` | Poll interval in seconds. The bridge fetches the last two hours for every timeseries on each cycle. |
| `STATE_FILE` | No | `~/.irceline_belgium_state.json` | Local file used to persist the newest emitted timestamp per timeseries. |

## Docker example for plain Kafka

```powershell
docker run --rm `
  -e KAFKA_BOOTSTRAP_SERVERS=host.docker.internal:9092 `
  -e KAFKA_TOPIC=irceline-belgium `
  -e KAFKA_ENABLE_TLS=false `
  irceline-belgium:latest
```

## Docker example for Event Hubs

```powershell
docker run --rm `
  -e CONNECTION_STRING="Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=...;EntityPath=irceline-belgium" `
  irceline-belgium:latest
```

## Behavior

- Emits station reference data first at startup
- Emits expanded timeseries reference data next
- Polls recent observations hourly by default
- Re-emits reference data every 24 hours to keep downstream state temporally consistent
- Continues past per-timeseries fetch errors and retries on the next cycle

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template-with-eventhub.json)
