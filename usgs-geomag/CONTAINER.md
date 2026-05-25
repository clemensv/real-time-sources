# USGS Geomagnetism Program Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the USGS Geomagnetism Program real-time geomagnetic field data and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches 1-minute variation data from 14 US magnetic observatories and forwards them to the configured Kafka endpoints.

## USGS Geomagnetism API

The USGS Geomagnetism Program operates 14 magnetic observatories across the United States and territories. Each observatory continuously records geomagnetic field variations (H, D, Z, F components) at 1-minute cadence. The data is publicly available through an INTERMAGNET-compatible web-service. No authentication is required.

## Functionality

The bridge polls the USGS Geomagnetism data API at `https://geomag.usgs.gov/ws/data/` for each observatory and writes new 1-minute magnetic field readings to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Observatory reference data is emitted at startup from `https://geomag.usgs.gov/ws/observatories/`. Previously seen reading timestamps per observatory are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-usgs-geomag:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-usgs-geomag:latest
```

## Using the Container Image

The container starts the bridge, polling the USGS Geomagnetism API and writing magnetic field readings to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-usgs-geomag:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-usgs-geomag:latest
```

### Preserving State Between Restarts

To preserve the last seen timestamps between restarts and avoid reprocessing readings, mount a volume and set the `GEOMAG_LAST_POLLED_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e GEOMAG_LAST_POLLED_FILE='/mnt/fileshare/usgs_geomag_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-usgs-geomag:latest
```

### Selecting Specific Observatories

To poll only specific observatories, set the `GEOMAG_OBSERVATORIES` environment variable:

```shell
$ docker run --rm \
    -e GEOMAG_OBSERVATORIES='BOU,FRN,HON' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-usgs-geomag:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic to send messages to.

### `SASL_USERNAME`

The username for SASL PLAIN authentication with the Kafka broker.

### `SASL_PASSWORD`

The password for SASL PLAIN authentication with the Kafka broker.

### `GEOMAG_LAST_POLLED_FILE`

The file path for storing last seen timestamps per observatory for deduplication. Defaults to `/mnt/fileshare/usgs_geomag_last_polled.json` inside the container.

### `GEOMAG_OBSERVATORIES`

Comma-separated list of IAGA observatory codes to poll. Defaults to all 14 USGS observatories: BOU, BRW, BSL, CMO, DED, FRD, FRN, GUA, HON, NEW, SHU, SIT, SJG, TUC.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-with-eventhub.json)

## MQTT/Unified Namespace image

A sibling MQTT container image, `ghcr.io/clemensv/real-time-sources-usgs-geomag-mqtt:latest`, publishes the same source events as MQTT 5.0 binary-mode CloudEvents. It uses the xRegistry MQTT messagegroup `gov.usgs.geomag.mqtt` and the source-specific Unified Namespace topic tree described in [EVENTS.md](EVENTS.md).

### Run against a generic MQTT 5 broker

```shell
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-usgs-geomag-mqtt:latest
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
| topic prefix | Fixed by the xRegistry contract, not an environment variable. Root: `space-weather/us/usgs/usgs-geomag`. |
| retain default | Per message in xRegistry; see the topic table below. |
| QoS default | Per message in xRegistry; MQTT messages in this source use QoS 1 unless noted otherwise. |

### MQTT topic patterns

| Topic pattern | Message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `space-weather/us/usgs/usgs-geomag/{iaga_code}/info` | `gov.usgs.geomag.Observatory` | `true` | `1` | `` |
| `space-weather/us/usgs/usgs-geomag/{iaga_code}/reading` | `gov.usgs.geomag.MagneticFieldReading` | `true` | `1` | `7200` |

### Subscription patterns

```text
# Everything from this source
space-weather/us/usgs/usgs-geomag/#
```

### MQTT Azure deployment

Deploy the MQTT container against an existing MQTT 5 broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-mqtt.json)

Deploy the MQTT container with a new Azure Event Grid namespace MQTT broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP 1.0 container

The AMQP companion image publishes the same `Usgs Geomag` CloudEvents to a generic AMQP 1.0 broker, Azure Service Bus with Entra ID CBS, or a SAS-token Service Bus-compatible endpoint.

```bash
docker pull ghcr.io/clemensv/real-time-sources-usgs-geomag-amqp:latest
```

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=usgs-geomag   ghcr.io/clemensv/real-time-sources-usgs-geomag-amqp:latest
```

### Azure Service Bus (Entra ID)

```bash
docker run --rm   -e AMQP_HOST=<namespace>.servicebus.windows.net   -e AMQP_PORT=5671   -e AMQP_TLS=true   -e AMQP_ADDRESS=usgs-geomag   -e AMQP_AUTH_MODE=entra   -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default   ghcr.io/clemensv/real-time-sources-usgs-geomag-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm   -e AMQP_HOST=servicebus-emulator   -e AMQP_PORT=5672   -e AMQP_ADDRESS=usgs-geomag   -e AMQP_AUTH_MODE=sas   -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey   -e AMQP_SAS_KEY=<base64-key>   ghcr.io/clemensv/real-time-sources-usgs-geomag-amqp:latest
```

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Optional AMQP URI for generic brokers. | unset |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when no URI is supplied. | `localhost` / `5672` |
| `AMQP_ADDRESS` | Queue/topic/address to publish to. | `usgs-geomag` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | unset |
| `AMQP_TLS` | Use TLS (`true`, `1`, or `yes`). | `false` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra token scope and optional managed identity client ID. | Service Bus scope / unset |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials. | unset |
| `AMQP_CONTENT_MODE` | CloudEvents content mode: `binary` or `structured`. | `binary` |

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-amqp.json)

