# UK EA Flood Monitoring API Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the UK Environment Agency Flood
Monitoring API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The
bridge reads real-time water level and flow data from approximately 4,000
monitoring stations across England and writes it to a Kafka topic.

## UK EA Flood Monitoring API

The Environment Agency's real-time flood monitoring API provides access to water
level, flow, rainfall, wind, and temperature data from monitoring stations
across England. The service is free, requires no authentication, and updates
every 15 minutes.

## Functionality

The bridge fetches water level data from the EA Flood Monitoring API and writes
the data to a Kafka topic as structured JSON [CloudEvents](https://cloudevents.io/)
in a JSON format documented in [EVENTS.md](EVENTS.md).

## Database Schemas and handling

If you want to build a full data pipeline with all events ingested into
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring:latest
```

## Using the Container Image

The container image defines a single command that starts the bridge. It reads
data from the UK EA Flood Monitoring API and writes it to a Kafka topic, Azure
Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS=<kafka-bootstrap-servers> \
    -e KAFKA_TOPIC=<kafka-topic> \
    -e SASL_USERNAME=<sasl-username> \
    -e SASL_PASSWORD=<sasl-password> \
    ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring:latest
```

### With a Connection String

```shell
$ docker run --rm \
    -e CONNECTION_STRING="Endpoint=sb://...;EntityPath=...;SharedAccessKeyName=...;SharedAccessKey=..." \
    ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring:latest
```

### Azure Container Instance Deployment

Deploy using the provided ARM template:

```shell
$ az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters connectionStringSecret=<connection-string>
```
