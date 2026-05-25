# German Waters Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between Germany's state-level hydrological
monitoring networks and Apache Kafka, Azure Event Hubs, and Fabric Event Streams.
The bridge aggregates water level, discharge, and related readings from ~2,724
gauging stations across 12 federal states — pulling exclusively from official
government open data portals — and forwards new observations as
[CloudEvents](https://cloudevents.io/) in JSON format.

> **Note:** The upstream data sources require no authentication or API keys. The
> bridge can start fetching data immediately with no additional registration.

## Functionality

The bridge polls 12 independent state-level water data providers — each with its
own API format (JSON, HTML scraping, GeoJSON, JavaScript arrays) — normalises the
readings, and writes them to a Kafka topic as [CloudEvents](https://cloudevents.io/)
in JSON format, documented in [EVENTS.md](EVENTS.md).

On startup, the bridge emits `DE.Waters.Hydrology.Station` events for all
monitoring stations (reference data). It then enters a polling loop, emitting
`DE.Waters.Hydrology.WaterLevelObservation` events only for new or changed
readings (delta emission via a de-duplication state file).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-german-waters:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-german-waters:latest
```

## Using the Container Image

The container starts the bridge in feed mode, reading data from the German state
water data portals and writing it to Kafka, Azure Event Hubs, or Fabric Event
Streams.

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

### Preserving State Between Restarts

To preserve the de-duplication state between container restarts and avoid
re-sending observations, mount a volume and set the `STATE_FILE` environment
variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/german_waters_state.json' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

### Filtering Providers

You can include or exclude specific state providers:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e PROVIDERS='bayern_gkd,nrw_hygon' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e EXCLUDE_PROVIDERS='sh_lkn,mv_lung' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

### Adjusting the Polling Interval

The default polling interval is 900 seconds (15 minutes). You can adjust it:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e POLLING_INTERVAL='600' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for separate `KAFKA_BOOTSTRAP_SERVERS`
and topic configuration, since the bootstrap server and topic are extracted from the
connection string.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced. Must be provided via the
connection string or this variable when using a plain Kafka broker.

### `SASL_USERNAME`

Username for SASL PLAIN authentication against the Kafka broker.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication against the Kafka broker.

### `POLLING_INTERVAL`

The interval in seconds between polling cycles. Default: `900` (15 minutes).

### `STATE_FILE`

The file path where the bridge stores the de-duplication state. This tracks
which readings have already been forwarded, allowing the bridge to resume without
duplicating events after restarts. Default: `~/.german_waters_state.json`.

### `PROVIDERS`

Comma-separated list of provider keys to include. When set, only the listed
providers are polled. Available keys: `bayern_gkd`, `nrw_hygon`, `sh_lkn`,
`nds_nlwkn`, `sa_lhw`, `he_hlnug`, `sn_lfulg`, `bw_hvz`, `bb_lfu`,
`th_tlubn`, `mv_lung`, `be_senumvk`.

### `EXCLUDE_PROVIDERS`

Comma-separated list of provider keys to exclude from polling.

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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgerman-waters%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgerman-waters%2Fazure-template-with-eventhub.json)

## MQTT/UNS image

A sibling container image, ghcr.io/clemensv/real-time-sources-german-waters-mqtt, is built from
`Dockerfile.mqtt` and publishes the same station-catalog and water-level
events as **MQTT 5.0 binary-mode CloudEvents** into a Unified-Namespace
topic tree:

```
hydro/de/wsv/german-waters/{water_body}/{station_id}/info          # station reference
hydro/de/wsv/german-waters/{water_body}/{station_id}/water-level   # latest water level / discharge
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
    ghcr.io/clemensv/real-time-sources-german-waters-mqtt:latest
```

Set `MQTT_TLS=true` or use the `mqtts://`/`ssl://` URL scheme to
enable TLS. `MQTT_CLIENT_ID` is optional but recommended on shared
brokers. `POLLING_INTERVAL` (seconds) controls how often the upstream
HTTP services are re-polled (default 900 s).

### MQTT Environment Variables

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Full broker URL (e.g. `mqtt://host:1883` or `mqtts://host:8883`) |
| `MQTT_HOST` | Broker hostname (alternative to URL) |
| `MQTT_PORT` | Broker port (alternative to URL) |
| `MQTT_USERNAME` | MQTT username |
| `MQTT_PASSWORD` | MQTT password |
| `MQTT_TLS` | Enable TLS (`true`/`false`) |
| `MQTT_CLIENT_ID` | Optional MQTT client ID |
| `MQTT_CONTENT_MODE` | CloudEvents content mode (`binary` or `structured`, default: `binary`) |
| `POLLING_INTERVAL` | Polling interval in seconds (default: `900`) |
| `STATE_FILE` | De-duplication state file path (default: `~/.german_waters_mqtt_state.json`) |
| `ONCE_MODE` | Exit after first poll cycle (`true`/`false`) |
| `PROVIDERS` | Comma-separated provider keys to include |
| `EXCLUDE_PROVIDERS` | Comma-separated provider keys to exclude |

### Subscription patterns

```
# Everything from this source
hydro/de/wsv/german-waters/#

# All water-level telemetry on the Rhine
hydro/de/wsv/german-waters/rhein/+/water-level

# One station's info
hydro/de/wsv/german-waters/+/{station_id}/info
```

## AMQP 1.0 image

Image: `ghcr.io/clemensv/real-time-sources-german-waters-amqp:latest`

The AMQP image publishes the same reference and telemetry CloudEvents as the Kafka and MQTT variants, but targets queue-oriented AMQP 1.0 consumers such as ActiveMQ Artemis, RabbitMQ AMQP 1.0, Qpid Dispatch, Azure Service Bus, and Azure Event Hubs.

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL=amqp://user:password@broker:5672/german-waters \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-german-waters-amqp:latest
```

### Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST=<namespace>.servicebus.windows.net \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS=german-waters \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default \
  ghcr.io/clemensv/real-time-sources-german-waters-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm \
  -e AMQP_HOST=servicebus-emulator \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=german-waters \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey \
  -e AMQP_SAS_KEY=<emulator-key> \
  ghcr.io/clemensv/real-time-sources-german-waters-amqp:latest
```

### AMQP environment variables

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Full AMQP URL; path becomes the address when present. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when not using `AMQP_BROKER_URL`. | `localhost` / `5672` or `5671` with TLS |
| `AMQP_ADDRESS` | Queue, topic, or event hub name. | `german-waters` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | empty |
| `AMQP_TLS` | Enable TLS for AMQP. | `false` (`true` for Entra deployments) |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` | Token audience for CBS Entra auth. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS policy and key for CBS SAS auth / emulator. | empty |
| `AMQP_CONTENT_MODE` | CloudEvents content mode. | `binary` |
| `MOCK_MODE` | Emit deterministic reference + telemetry mock events and exit; used by Docker E2E. | `false` |

Deploy to Azure with `azure-template-with-servicebus.json` (mirrored at `infra/azure-template-amqp.json`). The template provisions a Service Bus namespace and queue, user-assigned managed identity, Data Sender role assignment, ACI container group, Log Analytics workspace, and Azure Files state share.

