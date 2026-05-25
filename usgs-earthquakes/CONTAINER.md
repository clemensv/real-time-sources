# USGS Earthquake Hazards Program bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [USGS Earthquake Hazards
Program](https://earthquake.usgs.gov/) real-time GeoJSON feeds and Apache Kafka,
Azure Event Hubs, and Fabric Event Streams. The bridge fetches earthquake events
and forwards them to the configured Kafka endpoints.

## USGS Earthquake Hazards Program

The [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/) provides
real-time earthquake data via GeoJSON feeds. The feeds include data on
earthquakes worldwide for the past hour, day, week, and month, updated every
minute. The data includes location, magnitude, depth, felt reports, and
alert levels.

## Functionality

The bridge polls the USGS Earthquake GeoJSON feeds at regular intervals and
writes earthquake events to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading earthquake data
from the USGS feeds and writing it to Kafka, Azure Event Hubs, or Fabric Event
Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string from Azure Event Hubs or Microsoft Fabric Event
Streams:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

### Deploy to Azure

You can deploy the container to Azure Container Instances using the provided ARM
template:

[![Deploy to
Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template.json)

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`,
`SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with
TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `LOG_LEVEL`

The logging level. Default: `INFO`.

### `USGS_EQ_LAST_POLLED_FILE`

The file path where the bridge stores the IDs of previously processed events to
avoid duplication after restarts. Default:
`~/.usgs_earthquakes_last_polled.json`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-with-eventhub.json)

## MQTT/Unified Namespace image

A sibling MQTT container image, `ghcr.io/clemensv/real-time-sources-usgs-earthquakes-mqtt:latest`, publishes the same source events as MQTT 5.0 binary-mode CloudEvents. It uses the xRegistry MQTT messagegroup `USGS.Earthquakes.mqtt` and the source-specific Unified Namespace topic tree described in [EVENTS.md](EVENTS.md).

### Run against a generic MQTT 5 broker

```shell
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-usgs-earthquakes-mqtt:latest
```

### MQTT environment variables

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL including host, port, and TLS scheme, for example `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional username/password credentials for brokers that require user authentication. Leave unset for anonymous brokers. |
| `MQTT_CLIENT_ID` | Optional MQTT client identifier. Set it explicitly on shared brokers and Event Grid namespaces. |
| `MQTT_CONTENT_MODE` | CloudEvents content mode, `binary` by default. Keep `binary` for MQTT 5 user-property metadata. |
| `POLLING_INTERVAL` | Source polling interval in seconds, when supported by the feeder. |
| `STATE_FILE` | Optional path for source dedupe/checkpoint state, when the feeder maintains local state. |
| topic prefix | Fixed by the xRegistry contract, not an environment variable. Root: `seismic/intl/usgs/usgs-earthquakes`. |
| retain default | Per message in xRegistry; see the topic table below. |
| QoS default | Per message in xRegistry; MQTT messages in this source use QoS 1 unless noted otherwise. |

### MQTT topic patterns

| Topic pattern | Message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `seismic/intl/usgs/usgs-earthquakes/{net}/{magnitude_bucket}/{code}/quake` | `USGS.Earthquakes.Event` | `false` | `1` | `` |

### Subscription patterns

```text
# Everything from this source
seismic/intl/usgs/usgs-earthquakes/#
```

### MQTT Azure deployment

Deploy the MQTT container against an existing MQTT 5 broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-mqtt.json)

Deploy the MQTT container with a new Azure Event Grid namespace MQTT broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP 1.0 container

The AMQP companion image publishes the same `Usgs Earthquakes` CloudEvents to a generic AMQP 1.0 broker, Azure Service Bus with Entra ID CBS, or a SAS-token Service Bus-compatible endpoint.

```bash
docker pull ghcr.io/clemensv/real-time-sources-usgs-earthquakes-amqp:latest
```

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=usgs-earthquakes   ghcr.io/clemensv/real-time-sources-usgs-earthquakes-amqp:latest
```

### Azure Service Bus (Entra ID)

```bash
docker run --rm   -e AMQP_HOST=<namespace>.servicebus.windows.net   -e AMQP_PORT=5671   -e AMQP_TLS=true   -e AMQP_ADDRESS=usgs-earthquakes   -e AMQP_AUTH_MODE=entra   -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default   ghcr.io/clemensv/real-time-sources-usgs-earthquakes-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm   -e AMQP_HOST=servicebus-emulator   -e AMQP_PORT=5672   -e AMQP_ADDRESS=usgs-earthquakes   -e AMQP_AUTH_MODE=sas   -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey   -e AMQP_SAS_KEY=<base64-key>   ghcr.io/clemensv/real-time-sources-usgs-earthquakes-amqp:latest
```

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Optional AMQP URI for generic brokers. | unset |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when no URI is supplied. | `localhost` / `5672` |
| `AMQP_ADDRESS` | Queue/topic/address to publish to. | `usgs-earthquakes` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | unset |
| `AMQP_TLS` | Use TLS (`true`, `1`, or `yes`). | `false` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra token scope and optional managed identity client ID. | Service Bus scope / unset |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials. | unset |
| `AMQP_CONTENT_MODE` | CloudEvents content mode: `binary` or `structured`. | `binary` |

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-amqp.json)

