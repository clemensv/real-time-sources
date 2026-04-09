# VATSIM Live Data Feed Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the VATSIM virtual aviation
network live data feed and Apache Kafka, Azure Event Hubs, and Fabric Event
Streams. The bridge polls pilot positions, controller positions, and network
status and writes them to a Kafka topic.

## VATSIM Data Feed

VATSIM (Virtual Air Traffic Simulation Network) is a free online network where
virtual pilots and air traffic controllers connect to simulate real-world
aviation. The data feed at `https://data.vatsim.net/v3/vatsim-data.json`
provides a JSON snapshot of all connected clients, updated every ~15 seconds.
No authentication is required.

## Functionality

The bridge polls the VATSIM data feed and writes pilot positions, controller
positions, and network status to a Kafka topic as structured JSON
[CloudEvents](https://cloudevents.io/). Events are described in
[EVENTS.md](EVENTS.md). The bridge deduplicates by callsign so only changed
positions are emitted.

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-vatsim:latest
```

## Using the Container Image

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-vatsim:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-vatsim:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to establish a connection.

### `KAFKA_BOOTSTRAP_SERVERS`

Comma-separated list of Kafka bootstrap servers.

### `KAFKA_TOPIC`

Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `POLLING_INTERVAL`

Polling interval in seconds (default: 60).
