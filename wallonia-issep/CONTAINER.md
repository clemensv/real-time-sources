# Container contract for Wallonia ISSeP

This container polls the public Wallonia ISSeP Opendatasoft air quality API and emits CloudEvents to Kafka in structured mode with `application/cloudevents+json`.

## MQTT/UNS transport

The **MQTT variant** (`Dockerfile.mqtt`) publishes retained, QoS-1,
binary-mode CloudEvents into a Unified-Namespace topic tree:

```
air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/info
air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/observation
```

### Wildcard subscriptions

| Pattern | What it captures |
|---------|-----------------|
| `air-quality/be/issep/wallonia-issep/#` | All air-quality events for Wallonia ISSeP |
| `air-quality/be/issep/wallonia-issep/+/info` | All sensor configuration info events |
| `air-quality/be/issep/wallonia-issep/+/observation` | All observation events |

### Environment variables (MQTT)

| Variable | Required | Default | Description |
|---|---|---|---|
| `MQTT_BROKER_URL` | Yes | empty | MQTT broker URL, e.g. `mqtt://broker:1883` or `mqtts://broker:8883` |
| `MQTT_HOST` | No | `localhost` | Broker host (used when `MQTT_BROKER_URL` is empty) |
| `MQTT_PORT` | No | `1883` | Broker port |
| `MQTT_USERNAME` | No | unset | MQTT username |
| `MQTT_PASSWORD` | No | unset | MQTT password |
| `MQTT_TLS` | No | `false` | Enable TLS |
| `MQTT_CLIENT_ID` | No | auto | MQTT client ID |
| `MQTT_CONTENT_MODE` | No | `binary` | CloudEvents content mode (`binary` or `structured`) |
| `POLLING_INTERVAL` | No | `600` | Poll interval in seconds |
| `STATE_FILE` | No | `~/.wallonia_issep_mqtt_state.json` | Deduplication state file |
| `ONCE_MODE` | No | `false` | Exit after first poll cycle (for testing) |

### Docker example (MQTT)

```powershell
docker run --rm `
  -e MQTT_BROKER_URL=mqtt://host.docker.internal:1883 `
  -e POLLING_INTERVAL=300 `
  wallonia-issep-mqtt:latest
```

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | No | empty | Kafka/Event Hubs connection string. Supports Event Hubs `Endpoint=...;EntityPath=...` and plain Kafka `BootstrapServer=host:port;EntityPath=topic` styles. |
| `KAFKA_BOOTSTRAP_SERVERS` | No | unset | Plain Kafka bootstrap servers. Overrides `BootstrapServer` from `CONNECTION_STRING` when set. |
| `KAFKA_TOPIC` | No | `wallonia-issep` | Kafka topic for all sensor configuration and observation events. |
| `SASL_USERNAME` | No | unset | SASL username for plain Kafka clusters that require authentication. |
| `SASL_PASSWORD` | No | unset | SASL password for plain Kafka clusters that require authentication. |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for local Docker Kafka brokers that use PLAINTEXT. |
| `POLLING_INTERVAL` | No | `600` | Poll interval in seconds. The bridge fetches the latest sensor readings on each cycle. |
| `STATE_FILE` | No | `~/.wallonia_issep_state.json` | Local file used to persist the newest emitted timestamp per configuration. |

## Docker example for plain Kafka

```powershell
docker run --rm `
  -e KAFKA_BOOTSTRAP_SERVERS=host.docker.internal:9092 `
  -e KAFKA_TOPIC=wallonia-issep `
  -e KAFKA_ENABLE_TLS=false `
  wallonia-issep:latest
```

## Docker example for Event Hubs

```powershell
docker run --rm `
  -e CONNECTION_STRING="Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=...;EntityPath=wallonia-issep" `
  wallonia-issep:latest
```

## Behavior

- Emits sensor configuration reference data at startup derived from data records
- Polls the latest sensor readings every 10 minutes by default
- Deduplicates by configuration_id and moment timestamp
- Re-emits reference data every 24 hours to keep downstream state temporally consistent
- Continues past per-record errors and retries on the next cycle

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template-with-eventhub.json)

## AMQP 1.0 image

Image: `ghcr.io/clemensv/real-time-sources-wallonia-issep-amqp:latest`

The AMQP image publishes the same reference and telemetry CloudEvents as the Kafka and MQTT variants, but targets queue-oriented AMQP 1.0 consumers such as ActiveMQ Artemis, RabbitMQ AMQP 1.0, Qpid Dispatch, Azure Service Bus, and Azure Event Hubs.

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL=amqp://user:password@broker:5672/wallonia-issep \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-wallonia-issep-amqp:latest
```

### Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST=<namespace>.servicebus.windows.net \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS=wallonia-issep \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default \
  ghcr.io/clemensv/real-time-sources-wallonia-issep-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm \
  -e AMQP_HOST=servicebus-emulator \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=wallonia-issep \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey \
  -e AMQP_SAS_KEY=<emulator-key> \
  ghcr.io/clemensv/real-time-sources-wallonia-issep-amqp:latest
```

### AMQP environment variables

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Full AMQP URL; path becomes the address when present. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when not using `AMQP_BROKER_URL`. | `localhost` / `5672` or `5671` with TLS |
| `AMQP_ADDRESS` | Queue, topic, or event hub name. | `wallonia-issep` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | empty |
| `AMQP_TLS` | Enable TLS for AMQP. | `false` (`true` for Entra deployments) |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` | Token audience for CBS Entra auth. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS policy and key for CBS SAS auth / emulator. | empty |
| `AMQP_CONTENT_MODE` | CloudEvents content mode. | `binary` |
| `MOCK_MODE` | Emit deterministic reference + telemetry mock events and exit; used by Docker E2E. | `false` |

Deploy to Azure with `azure-template-with-servicebus.json` (mirrored at `infra/azure-template-amqp.json`). The template provisions a Service Bus namespace and queue, user-assigned managed identity, Data Sender role assignment, ACI container group, Log Analytics workspace, and Azure Files state share.

