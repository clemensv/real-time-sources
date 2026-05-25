# Hong Kong EPD AQHI — Kafka, MQTT, and AMQP Container Deployment

## Upstream Source

The Hong Kong Environmental Protection Department publishes a public XML feed
with the past 24 hours of AQHI observations for 18 monitoring stations. This
bridge emits station reference data at startup and then publishes the latest
AQHI reading per station on each polling cycle.

## Docker Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources/hongkong-epd:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | `hongkong-epd-aqhi` | Target Kafka topic |
| `POLLING_INTERVAL` | No | `3600` | Seconds between polling cycles |
| `STATE_FILE` | No | `~/.hongkong_epd_state.json` | Deduplication state file path |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |

## Docker Run (Plain Kafka)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=hongkong-epd-aqhi" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/hongkong-epd:latest
```

## Docker Run (Azure Event Hubs)

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=hongkong-epd-aqhi" \
  ghcr.io/clemensv/real-time-sources/hongkong-epd:latest
```

## Kafka Topic and Keys

| Topic | Key | Event Types |
|---|---|---|
| `hongkong-epd-aqhi` | `{station_id}` | `HK.Gov.EPD.AQHI.Station`, `HK.Gov.EPD.AQHI.AQHIReading` |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template-with-eventhub.json)

## MQTT/UNS image

A sibling container image, ghcr.io/clemensv/real-time-sources-hongkong-epd-mqtt, is built from
`Dockerfile.mqtt` and publishes the same station-catalog and AQHI reading
events as **MQTT 5.0 binary-mode CloudEvents** into a Unified-Namespace
topic tree:

```
air-quality/hk/epd/hongkong-epd/{district}/{station_id}/info   # station reference
air-quality/hk/epd/hongkong-epd/{district}/{station_id}/aqhi   # latest AQHI reading
```

Every leaf is published with QoS 1 and `retain=true` so any subscriber
sees the most recent value as soon as it subscribes. The full CloudEvents
binding (`id`, `source`, `type`, `subject`, `time`,
`specversion`) is carried as MQTT 5 user properties; the payload is the
`application/json` body of the same JsonStructure schema used by the
Kafka image.

### Run against a generic MQTT 5 broker

```
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-hongkong-epd-mqtt:latest
```

Set `MQTT_TLS=true` or use the `mqtts://`/`ssl://` URL scheme to
enable TLS. `MQTT_CLIENT_ID` is optional but recommended on shared
brokers. `POLLING_INTERVAL` (seconds) controls how often the upstream
HTTP service is re-polled (default 3600 s).

### Subscription patterns

```
# Everything from this source
air-quality/hk/epd/hongkong-epd/#

# All AQHI readings for stations in the Central & Western district
air-quality/hk/epd/hongkong-epd/central-and-western/+/aqhi

# Reference data for every station
air-quality/hk/epd/hongkong-epd/+/+/info
```

## AMQP 1.0 container variant

Image: `ghcr.io/clemensv/real-time-sources-hongkong-epd-amqp:latest`

The AMQP companion publishes Hong Kong EPD AQHI CloudEvents to generic AMQP 1.0 brokers with SASL PLAIN, Azure Service Bus with Entra ID CBS, or Service Bus-compatible SAS CBS. It uses the same event schemas as the Kafka and MQTT variants.

### Generic AMQP broker

```bash
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=hongkong-epd \
  -e AMQP_USERNAME=admin \
  -e AMQP_PASSWORD=admin \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-hongkong-epd-amqp:latest
```

### Azure Service Bus with Entra ID

```bash
docker run --rm \
  -e AMQP_HOST=<namespace>.servicebus.windows.net \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS=hongkong-epd \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default \
  -e AMQP_ENTRA_CLIENT_ID=<managed-identity-client-id> \
  ghcr.io/clemensv/real-time-sources-hongkong-epd-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm \
  -e AMQP_HOST=servicebus-emulator \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=hongkong-epd \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey \
  -e AMQP_SAS_KEY=<key> \
  ghcr.io/clemensv/real-time-sources-hongkong-epd-amqp:latest
```

| Variable | Description | Default |
| --- | --- | --- |
| `AMQP_BROKER_URL` | Optional `amqp://` or `amqps://` URL; path overrides `AMQP_ADDRESS`. | empty |
| `AMQP_HOST` / `AMQP_PORT` | AMQP broker host and port when no broker URL is supplied. | `localhost` / `5672` (`5671` with TLS) |
| `AMQP_ADDRESS` | Queue, topic, or link target address. | `hongkong-epd` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | empty |
| `AMQP_TLS` | Enable TLS; automatically true for Entra auth. | `false` |
| `AMQP_ENTRA_AUDIENCE` | Token scope for CBS put-token. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials for Service Bus-compatible brokers. | empty |
| `AMQP_CONTENT_MODE` | CloudEvents AMQP content mode. | `binary` |
| `POLLING_INTERVAL` | Poll interval in seconds. | source-specific |
| `STATE_FILE` | Persistent dedupe state file path. | source-specific |
| `HONGKONG_EPD_MOCK` | Emit built-in sample events for Docker E2E and offline validation. | `false` |

Use `azure-template-with-servicebus.json` or `infra/azure-template-amqp.json` for one-click Azure Service Bus deployment. The templates create a queue, Azure Files state share, ACI, user-assigned managed identity, and `Azure Service Bus Data Sender` role assignment scoped to the queue.

