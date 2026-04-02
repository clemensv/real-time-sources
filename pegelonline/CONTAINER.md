# WSV Pegelonline API Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the WSV Pegelonline API and
Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge reads
real-time water level data from the WSV Pegelonline API and writes it to a Kafka
topic.

## WSV Pegelonline API

The WSV Pegelonline API is a service provided by the Federal Waterways and
Shipping Administration of Germany (Wasserstraßen- und Schifffahrtsverwaltung
des Bundes, WSV). It offers real-time water level data for German rivers and
waterways, essential for navigation, flood prediction, and environmental
monitoring.

## Functionality

The bridge fetches water level data from the WSV Pegelonline API and writes the
data to a Kafka topic as structured JSON [CloudEvents](https://cloudevents.io/)
in a JSON format documented in [EVENTS.md](EVENTS.md). You can configure the
bridge to handle multiple stations by supplying their identifiers in the
configuration.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

## Using the Container Image

The container image defines a single command that starts the bridge. It reads
data from the WSV Pegelonline API and writes it to a Kafka topic, Azure Event
Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e STATIONS='<station-ids>' \
    ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the
connection string from the Azure portal, Azure CLI, or the "custom endpoint" of
a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e STATIONS='<station-ids>' \
    ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to establish a connection to
Azure Event Hubs or Fabric Event Streams. This replaces the need for
`KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with
TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication. Ensure your Kafka brokers support SASL
PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

## Deploying into Azure Container Instances

You can deploy the Pegelonline bridge as a container directly to Azure Container
Instances. Just click the button below and go.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template.json)
