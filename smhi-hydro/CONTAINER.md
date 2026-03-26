# SMHI Hydrological Data Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the SMHI hydrological open data
portal and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge
reads real-time discharge data from the SMHI open data API and writes it to a
Kafka topic.

## SMHI API

SMHI (Sveriges meteorologiska och hydrologiska institut) provides real-time
hydrological data for Swedish rivers and waterways. The API provides 15-minute
discharge (flow rate) measurements for hundreds of stations across Sweden via a
bulk endpoint that returns all stations in a single request.

## Functionality

The bridge fetches hydrological data from the SMHI open data API and writes the
data to a Kafka topic as structured JSON [CloudEvents](https://cloudevents.io/)
in a JSON format documented in [EVENTS.md](EVENTS.md).

## Database Schemas and handling

If you want to build a full data pipeline with all events ingested into
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

## Using the Container Image

The container image defines a single command that starts the bridge. It reads
data from the SMHI open data API and writes it to a Kafka topic, Azure Event
Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BROKER='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='smhi-hydro' \
    ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e KAFKA_TOPIC='smhi-hydro' \
    ghcr.io/clemensv/real-time-sources-smhi-hydro:latest
```

## Azure Deployment

You can deploy the container using the included ARM template:

```shell
az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters connectionStringSecret='<connection-string>'
```
