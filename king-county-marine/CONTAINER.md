# King County Marine Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container polls current King County marine buoy and mooring raw-data datasets and emits station reference events plus normalized water-quality readings as CloudEvents JSON.

## Upstream

- **Publisher:** King County Water and Land Resources Division
- **Platform:** Socrata datasets on `data.kingcounty.gov`
- **Cadence:** 15-minute telemetry for current buoy/mooring datasets
- **Auth:** None
- **License:** Public Domain

## Behavior

At startup the bridge discovers active raw buoy/mooring datasets from the King County Socrata catalog, fetches dataset metadata, and emits station reference events. It then polls the current datasets and emits normalized water-quality readings keyed by `station_id`.

Historical-only raw-output datasets and periodic non-buoy monitoring programs are intentionally excluded from this source.

## Running the Container

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=king-county-marine" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-king-county-marine:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=king-county-marine" \
  ghcr.io/clemensv/real-time-sources-king-county-marine:latest
```

### MQTT/UNS image

```bash
docker build -f Dockerfile.mqtt -t king-county-marine-mqtt .
docker run --rm \
  -e MQTT_BROKER_URL="mqtt://host.docker.internal:1883" \
  ghcr.io/clemensv/real-time-sources/king-county-marine-mqtt:latest
```

The MQTT image publishes retained QoS 1 binary CloudEvents under
`maritime/us/wa/king-county/king-county-marine/{station_id}/{event}`. Mount
`/var/lib/king-county-marine` to persist de-duplication state across restarts.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka/Event Hubs/Fabric connection string |
| `KAFKA_ENABLE_TLS` | No | Set `false` for plain Kafka in local and Docker E2E runs |
| `KING_COUNTY_MARINE_STATE_FILE` | No | Path to dedupe state; default `/mnt/fileshare/king_county_marine_state.json` for Kafka and `/var/lib/king-county-marine/state.json` for MQTT |
| `MQTT_BROKER_URL` | MQTT only | MQTT broker URL such as `mqtt://broker:1883` or `mqtts://broker:8883` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | MQTT only | Optional MQTT credentials |
| `MQTT_CONTENT_MODE` | MQTT only | CloudEvents MQTT content mode (`binary`, default, or `structured`) |
| `KING_COUNTY_MARINE_SAMPLE_MODE` | MQTT test only | Publish one deterministic sample station and reading instead of polling live Socrata feeds |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-with-eventhub.json)


## AMQP 1.0 companion feeder

Pull and run the AMQP image:

```bash
docker pull ghcr.io/clemensv/real-time-sources-king-county-marine-amqp:latest
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=king-county-marine \
  -e AMQP_USERNAME=user \
  -e AMQP_PASSWORD=secret \
  -e AMQP_AUTH_MODE=password \
  -e KING_COUNTY_MARINE_SAMPLE_MODE=true \
  ghcr.io/clemensv/real-time-sources-king-county-marine-amqp:latest
```

For Azure Service Bus, set `AMQP_AUTH_MODE=entra`, `AMQP_HOST=<namespace>.servicebus.windows.net`, `AMQP_PORT=5671`, `AMQP_TLS=true`, and optionally `AMQP_ENTRA_CLIENT_ID` for a user-assigned managed identity. For the Service Bus emulator or SAS-only namespaces, use `AMQP_AUTH_MODE=sas` with `AMQP_SAS_KEY_NAME` and `AMQP_SAS_KEY`.

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Optional full AMQP URL; path overrides `AMQP_ADDRESS`. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port. | localhost / 5672 |
| `AMQP_ADDRESS` | Queue/topic/event-hub name. | `king-county-marine` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | empty |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_TLS` | Enable TLS for AMQP. | false (`entra` implies TLS) |
| `AMQP_CONTENT_MODE` | CloudEvents content mode. | `binary` |
| `AMQP_ENTRA_AUDIENCE` | Token audience for CBS. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | User-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials. | empty |

Deploy a new Service Bus queue plus managed identity with [`azure-template-with-servicebus.json`](azure-template-with-servicebus.json) or [`infra/azure-template-amqp.json`](infra/azure-template-amqp.json).
