# Energy-Charts European Electricity Data Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [Energy-Charts API](https://api.energy-charts.info/) (Fraunhofer ISE) and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge polls European electricity generation mix, day-ahead spot prices, and grid carbon signal data, then forwards them as CloudEvents.

## Energy-Charts API

The Energy-Charts API, operated by Fraunhofer ISE, provides freely available (CC BY 4.0) electricity data for 40+ European countries. Data is sourced from the ENTSO-E transparency platform and national grid operators. Generation data updates every 15 minutes for Germany, hourly for other countries.

## Functionality

The bridge polls three endpoints:
- `/public_power?country={country}` — Net electricity generation by fuel type (MW), every 15 minutes
- `/price?bzn={bidding_zone}` — Day-ahead spot prices (EUR/MWh), every hour
- `/signal?country={country}` — Grid carbon signal (traffic light 0/1/2 + renewable share %), every 15 minutes

Events are written to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Previously seen timestamps are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-energy-charts:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-energy-charts:latest
```

## Using the Container Image

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e COUNTRY='de' \
    -e BIDDING_ZONE='DE-LU' \
    ghcr.io/clemensv/real-time-sources-energy-charts:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e COUNTRY='de' \
    -e BIDDING_ZONE='DE-LU' \
    ghcr.io/clemensv/real-time-sources-energy-charts:latest
```

### Preserving State Between Restarts

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e ENERGY_CHARTS_LAST_POLLED_FILE='/mnt/fileshare/energy_charts_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-energy-charts:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic to send messages to.

### `SASL_USERNAME`

The username for SASL PLAIN authentication with the Kafka broker.

### `SASL_PASSWORD`

The password for SASL PLAIN authentication with the Kafka broker.

### `COUNTRY`

ISO 3166-1 alpha-2 country code (default: `de`). Controls which country's generation and signal data is polled.

### `BIDDING_ZONE`

ENTSO-E bidding zone identifier for price queries (default: `DE-LU`). Common zones: `DE-LU`, `FR`, `AT`, `NO1`–`NO5`, `SE1`–`SE4`.

### `ENERGY_CHARTS_LAST_POLLED_FILE`

File path for storing last seen timestamps for deduplication. Defaults to `/mnt/fileshare/energy_charts_last_polled.json`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template-with-eventhub.json)
