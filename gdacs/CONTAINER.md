# GDACS Disaster Alert bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [Global Disaster Alert and
Coordination System (GDACS)](https://www.gdacs.org) RSS feed and Apache Kafka,
Azure Event Hubs, and Fabric Event Streams. The bridge polls GDACS for disaster
alerts worldwide and forwards them to the configured Kafka endpoints.

## GDACS

The [Global Disaster Alert and Coordination System](https://www.gdacs.org) is a
joint initiative of the United Nations and the European Commission that provides
near-real-time alerts about natural disasters around the world, including
earthquakes, tropical cyclones, floods, volcanic eruptions, forest fires, and
droughts. The RSS feed is updated within minutes of event detection.

## Functionality

The bridge polls the GDACS RSS feed at regular intervals (default: 5 minutes)
and writes disaster alert events to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

State tracking ensures only new or updated alert episodes are emitted. The
bridge persists a state file mapping each event+episode combination to its
version number, so restarts do not cause duplicate emissions.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-gdacs:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-gdacs:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading disaster alerts
from the GDACS RSS feed and writing them to Kafka, Azure Event Hubs, or Fabric
Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='gdacs' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-gdacs:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string from Azure Event Hubs or Microsoft Fabric Event
Streams:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-gdacs:latest
```

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `CONNECTION_STRING` | Azure Event Hubs or Fabric Event Stream connection string | Yes (or use `KAFKA_BOOTSTRAP_SERVERS`) |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated list of Kafka bootstrap servers | Yes (or use `CONNECTION_STRING`) |
| `KAFKA_TOPIC` | Kafka topic name (default from connection string) | No |
| `SASL_USERNAME` | SASL PLAIN username | No |
| `SASL_PASSWORD` | SASL PLAIN password | No |
| `GDACS_STATE_FILE` | Path to persist seen-event state | No |
| `LOG_LEVEL` | Logging level (default: `INFO`) | No |
| `KAFKA_ENABLE_TLS` | Enable TLS for Kafka (default: `true`) | No |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template-with-eventhub.json)
