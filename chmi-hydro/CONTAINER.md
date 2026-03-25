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

## Database Schemas and handling

If you want to build a full data pipeline with all events ingested into
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

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e KAFKA_TOPIC='chmi-hydro' \
    ghcr.io/clemensv/real-time-sources-chmi-hydro:latest
```

## Azure Deployment

You can deploy the container using the included ARM template:

```shell
az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters connectionStringSecret='<connection-string>'
```
