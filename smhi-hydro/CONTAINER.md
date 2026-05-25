# SMHI Hydrological Data Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the SMHI hydrological open data
portal and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge
reads real-time discharge data from the SMHI open data API and writes it to a
Kafka topic.

## SMHI API

SMHI (Sveriges meteorologiska och hydrologiska institut) provides real-time
hydrological data for Swedish rivers and waterways. The API provides 15-minute
discharge (flow rate) measurements for hundreds of stations across Sweden via a
bulk endpoint that returns all stations in a single request.

## Functionality

The bridge fetches hydrological data from the SMHI open data API and writes the
data to a Kafka topic as structured JSON [CloudEvents](https://cloudevents.io/)
in a JSON format documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

## Using the Container Image

The container image defines a single command that starts the bridge. It reads
data from the SMHI open data API and writes it to a Kafka topic, Azure Event
Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BROKER='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='smhi-hydro' \
    ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the
connection string from the Azure portal, Azure CLI, or the "custom endpoint" of
a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e KAFKA_TOPIC='smhi-hydro' \
    ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

### Preserving State Between Restarts

To preserve the state between restarts and avoid reprocessing observations,
mount a volume to the container and set the `STATE_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/smhi_hydro_state.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for `KAFKA_BROKER`.

### `KAFKA_BROKER`

The address of the Kafka broker (e.g., `broker1:9092`). The client communicates
with TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `POLLING_INTERVAL`

The polling interval in seconds. Default: `900` (15 minutes).

### `STATE_FILE`

The file path where the bridge stores the state of processed observations. This
helps in resuming data fetching without duplication after restarts. Default:
`~/.smhi_hydro_state.json`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template-with-eventhub.json)

## MQTT/UNS image

A sibling container image, ghcr.io/clemensv/real-time-sources-smhi-hydro-mqtt, is built from
`Dockerfile.mqtt` and publishes the same station-catalog and discharge
events as **MQTT 5.0 binary-mode CloudEvents** into a Unified-Namespace
topic tree:

```
hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/info          # station reference
hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/discharge     # latest discharge observation
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
    ghcr.io/clemensv/real-time-sources-smhi-hydro-mqtt:latest
```

Set `MQTT_TLS=true` or use the `mqtts://`/`ssl://` URL scheme to
enable TLS. `MQTT_CLIENT_ID` is optional but recommended on shared
brokers. `POLLING_INTERVAL` (seconds) controls how often the upstream
HTTP service is re-polled (default 900 s).

### Subscription patterns

```
# Everything from this source
hydro/se/smhi/smhi-hydro/#

# All discharge telemetry for one catchment
hydro/se/smhi/smhi-hydro/<catchment_name>/+/discharge

# Reference data for every station
hydro/se/smhi/smhi-hydro/+/+/info
```

## AMQP 1.0 image

Image: `ghcr.io/clemensv/real-time-sources-smhi-hydro-amqp:latest`

The AMQP image publishes the same reference and telemetry CloudEvents as the Kafka and MQTT variants, but targets queue-oriented AMQP 1.0 consumers such as ActiveMQ Artemis, RabbitMQ AMQP 1.0, Qpid Dispatch, Azure Service Bus, and Azure Event Hubs.

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL=amqp://user:password@broker:5672/smhi-hydro \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-smhi-hydro-amqp:latest
```

### Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST=<namespace>.servicebus.windows.net \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS=smhi-hydro \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default \
  ghcr.io/clemensv/real-time-sources-smhi-hydro-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm \
  -e AMQP_HOST=servicebus-emulator \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=smhi-hydro \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey \
  -e AMQP_SAS_KEY=<emulator-key> \
  ghcr.io/clemensv/real-time-sources-smhi-hydro-amqp:latest
```

### AMQP environment variables

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Full AMQP URL; path becomes the address when present. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when not using `AMQP_BROKER_URL`. | `localhost` / `5672` or `5671` with TLS |
| `AMQP_ADDRESS` | Queue, topic, or event hub name. | `smhi-hydro` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | empty |
| `AMQP_TLS` | Enable TLS for AMQP. | `false` (`true` for Entra deployments) |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` | Token audience for CBS Entra auth. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS policy and key for CBS SAS auth / emulator. | empty |
| `AMQP_CONTENT_MODE` | CloudEvents content mode. | `binary` |
| `MOCK_MODE` | Emit deterministic reference + telemetry mock events and exit; used by Docker E2E. | `false` |

Deploy to Azure with `azure-template-with-servicebus.json` (mirrored at `infra/azure-template-amqp.json`). The template provisions a Service Bus namespace and queue, user-assigned managed identity, Data Sender role assignment, ACI container group, Log Analytics workspace, and Azure Files state share.

