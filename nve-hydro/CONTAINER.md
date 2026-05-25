# NVE Hydrology Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Norwegian Water Resources and
Energy Directorate's (NVE) hydrological monitoring network and Apache Kafka, Azure
Event Hubs, and Fabric Event Streams. The bridge polls the
[NVE HydAPI](https://hydapi.nve.no) for water level and discharge readings from
Norwegian gauging stations and forwards new observations as
[CloudEvents](https://cloudevents.io/) in JSON format.

> **Note:** The upstream data source requires an API key. Register at
> [hydapi.nve.no](https://hydapi.nve.no/UserDocumentation/) to obtain a free
> API key, then pass it via the `NVE_API_KEY` environment variable.

## Functionality

The bridge retrieves hydrological data from the NVE HydAPI — the official REST
API for hydrological observations in Norway — and writes entries to a Kafka topic
as [CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

On startup, the bridge emits `NO.NVE.Hydrology.Station` events for all active
monitoring stations (reference data). It then enters a polling loop, emitting
`NO.NVE.Hydrology.WaterLevelObservation` events only for new or changed readings
(delta emission).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

## Using the Container Image

The container starts the bridge in feed mode, reading data from the NVE HydAPI
and writing it to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e NVE_API_KEY='<your-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e NVE_API_KEY='<your-api-key>' \
    -e KAFKA_BROKER='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

### Preserving State Between Restarts

To preserve the de-duplication state between container restarts and avoid
re-sending observations, mount a volume and set the `STATE_FILE` environment
variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/nve_hydro_state.json' \
    -e NVE_API_KEY='<your-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

### Adjusting the Polling Interval

The default polling interval is 600 seconds (10 minutes). You can adjust it:

```shell
$ docker run --rm \
    -e NVE_API_KEY='<your-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    -e POLLING_INTERVAL='300' \
    ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

## Environment Variables

### `NVE_API_KEY`

The API key for the NVE HydAPI. Required. Register at
[hydapi.nve.no](https://hydapi.nve.no/UserDocumentation/) to obtain a free key.

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for separate `KAFKA_BROKER` and
topic configuration, since the bootstrap server and topic are extracted from the
connection string.

### `KAFKA_BROKER`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced. Default: `nve-hydro`.

### `POLLING_INTERVAL`

The interval in seconds between polling cycles. Default: `600` (10 minutes).

### `STATE_FILE`

The file path where the bridge stores the de-duplication state. This tracks
which readings have already been forwarded, allowing the bridge to resume without
duplicating events after restarts. Default: `~/.nve_hydro_state.json`.

### `KAFKA_ENABLE_TLS`

Whether to use TLS for the Kafka connection. Default: `true`. Set to `false` for
plaintext connections to local brokers.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template-with-eventhub.json)

## MQTT/UNS image

A sibling container image, ghcr.io/clemensv/real-time-sources-nve-hydro-mqtt, is built from
`Dockerfile.mqtt` and publishes the same station-catalog and water-level
events as **MQTT 5.0 binary-mode CloudEvents** into a Unified-Namespace
topic tree:

```
hydro/no/nve/nve-hydro/{river_name}/{station_id}/info          # station reference
hydro/no/nve/nve-hydro/{river_name}/{station_id}/water-level   # latest water level / discharge / temperature
```

Every leaf is published with QoS 1 and `retain=true` so any subscriber
sees the most recent value as soon as it subscribes. The full CloudEvents
binding (`id`, `source`, `type`, `subject`, `time`,
`specversion`) is carried as MQTT 5 user properties; the payload is the
`application/json` body of the same JsonStructure schema used by the
Kafka image.

### Run against a generic MQTT 5 broker

```
docker run --rm \\
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \\
    -e MQTT_USERNAME='<username>' \\
    -e MQTT_PASSWORD='<password>' \\
    ghcr.io/clemensv/real-time-sources-nve-hydro-mqtt:latest
```

Set `MQTT_TLS=true` or use the `mqtts://`/`ssl://` URL scheme to
enable TLS. `MQTT_CLIENT_ID` is optional but recommended on shared
brokers. `POLLING_INTERVAL` (seconds) controls how often the upstream
HTTP service is re-polled (default 600 s).

### Subscription patterns

```
# Everything from this source
hydro/no/nve/nve-hydro/#

# All telemetry for one river_name
hydro/no/nve/nve-hydro/<river_name>/+/water-level

# Reference data for every station
hydro/no/nve/nve-hydro/+/+/info
```

## AMQP 1.0 image

Image: `ghcr.io/clemensv/real-time-sources-nve-hydro-amqp:latest`

The AMQP image publishes the same reference and telemetry CloudEvents as the Kafka and MQTT variants, but targets queue-oriented AMQP 1.0 consumers such as ActiveMQ Artemis, RabbitMQ AMQP 1.0, Qpid Dispatch, Azure Service Bus, and Azure Event Hubs.

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL=amqp://user:password@broker:5672/nve-hydro \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-nve-hydro-amqp:latest
```

### Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST=<namespace>.servicebus.windows.net \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS=nve-hydro \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default \
  ghcr.io/clemensv/real-time-sources-nve-hydro-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm \
  -e AMQP_HOST=servicebus-emulator \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=nve-hydro \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey \
  -e AMQP_SAS_KEY=<emulator-key> \
  ghcr.io/clemensv/real-time-sources-nve-hydro-amqp:latest
```

### AMQP environment variables

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Full AMQP URL; path becomes the address when present. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when not using `AMQP_BROKER_URL`. | `localhost` / `5672` or `5671` with TLS |
| `AMQP_ADDRESS` | Queue, topic, or event hub name. | `nve-hydro` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | empty |
| `AMQP_TLS` | Enable TLS for AMQP. | `false` (`true` for Entra deployments) |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` | Token audience for CBS Entra auth. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS policy and key for CBS SAS auth / emulator. | empty |
| `AMQP_CONTENT_MODE` | CloudEvents content mode. | `binary` |
| `MOCK_MODE` | Emit deterministic reference + telemetry mock events and exit; used by Docker E2E. | `false` |

Deploy to Azure with `azure-template-with-servicebus.json` (mirrored at `infra/azure-template-amqp.json`). The template provisions a Service Bus namespace and queue, user-assigned managed identity, Data Sender role assignment, ACI container group, Log Analytics workspace, and Azure Files state share.

