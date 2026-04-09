# CDEC California Reservoirs Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the California Data Exchange
Center (CDEC) reservoir data API and Apache Kafka, Azure Event Hubs, and Fabric
Event Streams. The bridge reads real-time reservoir storage, elevation, inflow,
and outflow data from the CDEC JSON Data Servlet and writes it to a Kafka topic.

## CDEC API

The California Data Exchange Center (CDEC) is operated by the California
Department of Water Resources. It provides real-time and near-real-time
hydrologic data for over 2,600 stations throughout California, including all
major reservoirs. The JSON Data Servlet provides programmatic access to sensor
observations at configurable time intervals.

## Functionality

The bridge polls the CDEC JSON Data Servlet for hourly reservoir readings and
writes the data to a Kafka topic as structured JSON
[CloudEvents](https://cloudevents.io/) in a format documented in
[EVENTS.md](EVENTS.md). By default, it monitors California's major reservoirs
(Shasta, Oroville, Folsom, New Melones, Don Pedro, Hetch Hetchy, Sonoma, Millerton,
Pine Flat) for storage, elevation, inflow, and outflow.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-cdec-reservoirs:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-cdec-reservoirs:latest
```

## Using the Container Image

The container image defines a single command that starts the bridge. It reads
data from the CDEC API and writes it to a Kafka topic, Azure Event Hubs, or
Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e STATIONS='SHA,ORO,FOL' \
    ghcr.io/clemensv/real-time-sources-cdec-reservoirs:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e STATIONS='SHA,ORO,FOL' \
    ghcr.io/clemensv/real-time-sources-cdec-reservoirs:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to establish a connection to
Azure Event Hubs or Fabric Event Streams. This replaces the need for
`KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `STATIONS`

Comma-separated list of CDEC station IDs to monitor (default:
`SHA,ORO,FOL,NML,DNP,HTC,SON,MIL,PNF`).

### `SENSORS`

Comma-separated list of CDEC sensor numbers (default: `15,6,76,23`). Standard
sensor numbers: 15=STORAGE, 6=ELEVATION, 76=INFLOW, 23=OUTFLOW.

### `DUR_CODE`

Duration code for the observation interval: `H` for hourly (default), `D` for
daily.

### `POLLING_INTERVAL`

Polling interval in seconds (default: 3600).

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template-with-eventhub.json)
