# Hub'Eau Hydrométrie API Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the French Hub'Eau Hydrométrie
API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams.

## Hub'Eau Hydrométrie API

The Hub'Eau Hydrométrie API provides access to real-time water level and flow
data from approximately 6,300 hydrometric stations across France. No
authentication is required.

## Functionality

The bridge fetches hydrometric data and writes it to a Kafka topic as structured
JSON [CloudEvents](https://cloudevents.io/) documented in [EVENTS.md](EVENTS.md).

## Installing the Container Image

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-hubeau-hydrometrie:latest
```

## Using the Container Image

### With a Connection String

```shell
$ docker run --rm \
    -e CONNECTION_STRING="Endpoint=sb://...;EntityPath=...;SharedAccessKeyName=...;SharedAccessKey=..." \
    ghcr.io/clemensv/real-time-sources-hubeau-hydrometrie:latest
```

### Azure Container Instance Deployment

```shell
$ az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters connectionStringSecret=<connection-string>
```
