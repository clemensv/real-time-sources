# ČHMÚ Hydrological Data Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the ČHMÚ hydrological open data
portal and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge
reads real-time water level data from the ČHMÚ open data API and writes it to a
Kafka topic.

## ČHMÚ API

The ČHMÚ (Český hydrometeorologický ústav) open data portal provides real-time
hydrological data for Czech rivers and waterways. It provides water level,
discharge, and water temperature data for hundreds of stations across the Czech
Republic, updated every 10 minutes.

## Functionality

The bridge fetches hydrological data from the ČHMÚ open data API and writes the
data to a Kafka topic as structured JSON [CloudEvents](https://cloudevents.io/)
in a JSON format documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-chmi-hydro:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-chmi-hydro:latest
```

## Using the Container Image

The container image defines a single command that starts the bridge. It reads
data from the ČHMÚ open data API and writes it to a Kafka topic, Azure Event
Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BROKER='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='chmi-hydro' \
    ghcr.io/clemensv/real-time-sources-chmi-hydro:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the
connection string from the Azure portal, Azure CLI, or the "custom endpoint" of
a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e KAFKA_TOPIC='chmi-hydro' \
    ghcr.io/clemensv/real-time-sources-chmi-hydro:latest
```

### Preserving State Between Restarts

To preserve the state between restarts and avoid reprocessing observations,
mount a volume to the container and set the `STATE_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/chmi_hydro_state.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-chmi-hydro:latest
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

The polling interval in seconds. Default: `600` (10 minutes).

### `STATE_FILE`

The file path where the bridge stores the state of processed observations. This
helps in resuming data fetching without duplication after restarts. Default:
`~/.chmi_hydro_state.json`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template-with-eventhub.json)
## MQTT/UNS image

A sibling container image, ghcr.io/clemensv/real-time-sources-chmi-hydro-mqtt, is built from
`Dockerfile.mqtt` and publishes the same station-catalog and water-level
events as **MQTT 5.0 binary-mode CloudEvents** into a Unified-Namespace
topic tree:

```
hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/info          # station reference
hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/water-level   # latest water level / discharge / temperature
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
    ghcr.io/clemensv/real-time-sources-chmi-hydro-mqtt:latest
```

Set `MQTT_TLS=true` or use the `mqtts://`/`ssl://` URL scheme to
enable TLS. `MQTT_CLIENT_ID` is optional but recommended on shared
brokers. `POLLING_INTERVAL` (seconds) controls how often the upstream
HTTP service is re-polled (default 600 s).

### Subscription patterns

```
# Everything from this source
hydro/cz/chmi/chmi-hydro/#

# All telemetry for one stream_name
hydro/cz/chmi/chmi-hydro/<stream_name>/+/water-level

# Reference data for every station
hydro/cz/chmi/chmi-hydro/+/+/info
```

