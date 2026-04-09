# Nepal BIPAD Portal River Monitoring Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Nepal BIPAD Portal
river-stations API and Apache Kafka, Azure Event Hubs, and Fabric Event
Streams. The bridge reads real-time water level data from Nepal's Himalayan
river monitoring stations and writes it to a Kafka topic.

## Nepal BIPAD Portal

The [BIPAD Portal](https://bipadportal.gov.np/) (Building Information Platform
Against Disaster) is operated by the Government of Nepal. It provides real-time
river monitoring data from stations across Nepal's major river basins including
Bagmati, Narayani, Koshi, Karnali, Mahakali, and Babai. Data originates from
the Nepal Department of Hydrology and Meteorology (hydrology.gov.np).

## Functionality

The bridge fetches river station data from the BIPAD Portal API and writes it
to a Kafka topic as structured JSON [CloudEvents](https://cloudevents.io/) in
a format documented in [EVENTS.md](EVENTS.md).

The bridge emits two event types:
- **RiverStation** — Reference data for each monitoring station (location,
  basin, thresholds, administrative codes). Emitted at startup and refreshed
  every 6 hours.
- **WaterLevelReading** — Telemetry with current water level, alert status
  (BELOW WARNING LEVEL / WARNING / DANGER), and trend (STEADY / RISING /
  FALLING). Emitted every polling cycle with deduplication by station and
  timestamp.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-nepal-bipad-hydrology:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-nepal-bipad-hydrology:latest
```

## Using the Container Image

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-nepal-bipad-hydrology:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-nepal-bipad-hydrology:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to establish a connection to
Azure Event Hubs or Fabric Event Streams. This replaces the need for
`KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `POLLING_INTERVAL`

Polling interval in seconds (default: 900 = 15 minutes).

### `KAFKA_ENABLE_TLS`

Set to `false` to disable TLS for the Kafka connection (default: `true`).

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template-with-eventhub.json)
