# RWS Waterwebservices Bridge to Apache Kafka, Azure Event Hubs, Fabric Event Streams, and MQTT

This container image provides a bridge between the Rijkswaterstaat (RWS) Waterwebservices API and Apache Kafka, Azure Event Hubs, Fabric Event Streams, and MQTT. The bridge polls real-time water level observations from approximately 785 monitoring stations across the Netherlands and forwards them to the configured endpoint.

## RWS Waterwebservices API

Rijkswaterstaat is the executive agency of the Dutch Ministry of Infrastructure and Water Management. The Waterwebservices API provides free, unauthenticated access to real-time water level measurements (WATHTE) from surface water stations across the Netherlands, updated every 10 minutes. The data produces approximately 113,000 readings per day.

## Functionality

The bridge fetches water level data from the RWS API and writes it to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Station reference data is emitted at startup, followed by continuous water level observations. Previously seen readings are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-rws-waterwebservices:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-rws-waterwebservices:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-rws-waterwebservices:latest
```

### Preserving State Between Restarts

Mount a volume and set the `STATE_FILE` environment variable to persist deduplication state:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e STATE_FILE='/mnt/fileshare/rws_state.json' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-rws-waterwebservices:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `POLLING_INTERVAL`

Polling interval in seconds. Default: `600` (10 minutes).

### `STATE_FILE`

Path to the deduplication state file. Default: `~/.rws_waterwebservices_state.json`.

## Azure Deployment

Deploy using the provided ARM template:

```shell
$ az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters connectionStringSecret='<connection-string>'
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template-with-eventhub.json)

## MQTT/UNS Container Image

A separate container image publishes the same data as MQTT 5.0 binary-mode
CloudEvents into a Unified Namespace topic tree:

```
hydro/nl/rws/rws-waterwebservices/{station_code}/info
hydro/nl/rws/rws-waterwebservices/{station_code}/water-level
```

### Installing

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-rws-waterwebservices-mqtt:latest
```

### Running

```shell
$ docker run --rm \
    -e MQTT_BROKER_URL='mqtt://your-broker:1883' \
    ghcr.io/clemensv/real-time-sources-rws-waterwebservices-mqtt:latest
```

### MQTT Wildcard Examples

Subscribe to all events from all stations:

```
hydro/nl/rws/rws-waterwebservices/#
```

Subscribe to all water-level observations:

```
hydro/nl/rws/rws-waterwebservices/+/+/water-level
```

Subscribe to all events from a specific water body (e.g. Hoek van Holland):

```
hydro/nl/rws/rws-waterwebservices/{station_code}/#
```

### MQTT Environment Variables

#### `MQTT_BROKER_URL`

Full MQTT broker URL (e.g. `mqtt://host:1883` or `mqtts://host:8883`).

#### `MQTT_HOST`

MQTT broker hostname (alternative to `MQTT_BROKER_URL`).

#### `MQTT_PORT`

MQTT broker port. Default: `1883` (or `8883` if TLS).

#### `MQTT_USERNAME`

Username for MQTT broker authentication.

#### `MQTT_PASSWORD`

Password for MQTT broker authentication.

#### `MQTT_TLS`

Enable TLS. Set to `1`, `true`, or `yes`.

#### `MQTT_CLIENT_ID`

MQTT client ID. Default: auto-generated.

#### `MQTT_CONTENT_MODE`

CloudEvents content mode: `binary` (default) or `structured`.

#### `POLLING_INTERVAL`

Polling interval in seconds. Default: `600` (10 minutes).

#### `ONCE_MODE`

Exit after one polling cycle. Set to `1`, `true`, or `yes`.

#### `STATE_FILE`

Path to the deduplication state file. Default: `~/.rws_waterwebservices_mqtt_state.json`.

## AMQP 1.0 image

Image: `ghcr.io/clemensv/real-time-sources-rws-waterwebservices-amqp:latest`

The AMQP image publishes the same reference and telemetry CloudEvents as the Kafka and MQTT variants, but targets queue-oriented AMQP 1.0 consumers such as ActiveMQ Artemis, RabbitMQ AMQP 1.0, Qpid Dispatch, Azure Service Bus, and Azure Event Hubs.

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL=amqp://user:password@broker:5672/rws-waterwebservices \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-rws-waterwebservices-amqp:latest
```

### Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST=<namespace>.servicebus.windows.net \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS=rws-waterwebservices \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default \
  ghcr.io/clemensv/real-time-sources-rws-waterwebservices-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm \
  -e AMQP_HOST=servicebus-emulator \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=rws-waterwebservices \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey \
  -e AMQP_SAS_KEY=<emulator-key> \
  ghcr.io/clemensv/real-time-sources-rws-waterwebservices-amqp:latest
```

### AMQP environment variables

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Full AMQP URL; path becomes the address when present. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when not using `AMQP_BROKER_URL`. | `localhost` / `5672` or `5671` with TLS |
| `AMQP_ADDRESS` | Queue, topic, or event hub name. | `rws-waterwebservices` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | empty |
| `AMQP_TLS` | Enable TLS for AMQP. | `false` (`true` for Entra deployments) |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` | Token audience for CBS Entra auth. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS policy and key for CBS SAS auth / emulator. | empty |
| `AMQP_CONTENT_MODE` | CloudEvents content mode. | `binary` |
| `MOCK_MODE` | Emit deterministic reference + telemetry mock events and exit; used by Docker E2E. | `false` |

Deploy to Azure with `azure-template-with-servicebus.json` (mirrored at `infra/azure-template-amqp.json`). The template provisions a Service Bus namespace and queue, user-assigned managed identity, Data Sender role assignment, ACI container group, Log Analytics workspace, and Azure Files state share.

