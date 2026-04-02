# Waterinfo.be (VMM) Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Waterinfo.be KIWIS API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge polls real-time water level observations from approximately 1,785 monitoring stations across Flanders (Belgium) and forwards them to the configured Kafka endpoint.

## Waterinfo.be / VMM API

Waterinfo.be is an open data platform operated by the Flanders Environment Agency (VMM — Vlaamse Milieumaatschappij). The API provides free access to real-time water level measurements from monitoring stations across Flanders, updated every 15 minutes. The data produces approximately 106,000 readings per day. No authentication is required.

## Functionality

The bridge fetches water level data from the KIWIS API and writes it to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Station reference data is emitted at startup, followed by continuous water level readings. Previously seen readings are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-waterinfo-vmm:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-waterinfo-vmm:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-waterinfo-vmm:latest
```

### Preserving State Between Restarts

Mount a volume and set the `STATE_FILE` environment variable to persist deduplication state:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e STATE_FILE='/mnt/fileshare/waterinfo_vmm_state.json' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-waterinfo-vmm:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `POLLING_INTERVAL`

Polling interval in seconds. Default: `900` (15 minutes).

### `STATE_FILE`

Path to the deduplication state file. Default: `~/.waterinfo_vmm_state.json`.

## Azure Deployment

Deploy using the provided ARM template:

```shell
$ az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters connectionStringSecret='<connection-string>'
```

