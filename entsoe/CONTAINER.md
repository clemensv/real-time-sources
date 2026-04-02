# ENTSO-E Transparency Platform Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the ENTSO-E Transparency Platform REST API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge polls for European electricity market data (generation, load, day-ahead prices) and forwards it as CloudEvents to the configured Kafka endpoints.

## ENTSO-E Transparency Platform

The European Network of Transmission System Operators for Electricity (ENTSO-E) Transparency Platform provides free access to electricity generation, consumption, transmission, and pricing data across European bidding zones. The data is published under EU Regulation 543/2013.

## Functionality

The bridge polls the ENTSO-E REST API for three data categories:
- **Actual Generation per Type** (A75) — real-time generation by production source
- **Day-Ahead Prices** (A44) — market clearing prices
- **Actual Total Load** (A65) — total electricity demand

Data is emitted as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and handling

If you want to build a full data pipeline with all events ingested into
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-entsoe:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-entsoe:latest
```

## Using the Container Image

The container starts the bridge, polling the ENTSO-E API and writing data to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e ENTSOE_SECURITY_TOKEN='<your-entsoe-api-token>' \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-entsoe:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e ENTSOE_SECURITY_TOKEN='<your-entsoe-api-token>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-entsoe:latest
```

### Preserving State Between Restarts

Mount a volume and set the `STATE_FILE` environment variable to persist checkpoints:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e STATE_FILE='/mnt/fileshare/entsoe_state.json' \
    -e ENTSOE_SECURITY_TOKEN='<your-entsoe-api-token>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-entsoe:latest
```

## Environment Variables

### `ENTSOE_SECURITY_TOKEN`

**Required.** The ENTSO-E Transparency Platform API security token. Obtain one from your account settings at [https://transparency.entsoe.eu/](https://transparency.entsoe.eu/).

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `STATE_FILE`

The file path where the bridge stores checkpoint timestamps. Default is `/mnt/fileshare/entsoe_state.json`.

### `POLLING_INTERVAL`

Seconds between poll cycles. Default is `900` (15 minutes).

### `ENTSOE_DOMAINS`

Comma-separated list of EIC bidding zone codes. Default covers DE-AT-LU, France, Netherlands, Spain, and Germany.

### `ENTSOE_DOCUMENT_TYPES`

Comma-separated list of ENTSO-E document type codes. Default is `A75,A44,A65`.

## Deploying into Azure Container Instances

You can deploy the ENTSO-E bridge as a container directly to Azure Container Instances. Just click the button below and go.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template.json)

## Additional Information

- **Source Code**: [GitHub Repository](https://github.com/clemensv/real-time-sources/tree/main/entsoe)
- **Documentation**: Refer to [EVENTS.md](EVENTS.md) for the CloudEvent schema documentation.
- **License**: MIT
