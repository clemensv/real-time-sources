# Carbon Intensity UK Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the National Grid ESO Carbon Intensity API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches GB electricity carbon intensity data, generation fuel mix, and 17 DNO regional breakdowns, and forwards them to the configured Kafka endpoints.

## Carbon Intensity API

The [Carbon Intensity API](https://api.carbonintensity.org.uk/) is developed by National Grid ESO in partnership with the Environmental Defense Fund Europe, the University of Oxford, and WWF. It provides half-hourly (every 30 minutes) data including:

- **National carbon intensity** — forecast and actual gCO2/kWh with a qualitative index (very low / low / moderate / high / very high)
- **Generation fuel mix** — percentage breakdown by fuel type (biomass, coal, gas, hydro, imports, nuclear, oil, other, solar, wind)
- **Regional intensity** — carbon intensity and generation mix for all 17 GB Distribution Network Operator (DNO) regions

Data is published under a CC-BY 4.0 licence and requires no authentication.

## Functionality

The bridge polls the Carbon Intensity API every 30 minutes and writes new data to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). The bridge tracks the last polled settlement period in a state file to avoid sending duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-carbon-intensity:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-carbon-intensity:latest
```

## Using the Container Image

The container starts the bridge, polling the Carbon Intensity API and writing events to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-carbon-intensity:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-carbon-intensity:latest
```

### Preserving State Between Restarts

To preserve the last seen settlement period between restarts and avoid reprocessing, mount a volume and set the `CARBON_INTENSITY_LAST_POLLED_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e CARBON_INTENSITY_LAST_POLLED_FILE='/mnt/fileshare/carbon_intensity_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-carbon-intensity:latest
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

### `CARBON_INTENSITY_LAST_POLLED_FILE`

The file path for storing the last polled settlement period for deduplication. Defaults to `/mnt/fileshare/carbon_intensity_last_polled.json` inside the container.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template-with-eventhub.json)
