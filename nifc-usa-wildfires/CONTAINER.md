# NIFC USA Wildfires bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [National Interagency Fire
Center (NIFC)](https://www.nifc.gov/) ArcGIS Feature Service and Apache Kafka,
Azure Event Hubs, and Fabric Event Streams. The bridge fetches active wildfire
incident data and forwards them to the configured Kafka endpoints.

## NIFC USA Wildfires

The [NIFC](https://www.nifc.gov/) provides real-time wildfire incident data
from the Integrated Reporting of Wildland-Fire Information (IRWIN) system via
an ArcGIS Feature Service. The data includes fire location, size, containment
status, cause, personnel, and structural damage.

## Functionality

The bridge polls the NIFC ArcGIS Feature Service at regular intervals (default:
every 5 minutes) and writes wildfire incident events to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading wildfire data
from the NIFC feed and writing it to Kafka, Azure Event Hubs, or Fabric Event
Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `LOG_LEVEL`

The logging level. Default: `INFO`.

### `NIFC_LAST_POLLED_FILE`

The file path where the bridge stores the IDs of previously processed incidents
to avoid duplication after restarts. Default:
`~/.nifc_usa_wildfires_last_polled.json`.

### `KAFKA_ENABLE_TLS`

Enable TLS for Kafka connections. Default: `true`. Set to `false` for
unencrypted connections.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-with-eventhub.json)
