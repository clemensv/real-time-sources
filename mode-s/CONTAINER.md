# Mode-S/ADS-B Aircraft Telemetry Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between a local [dump1090](https://github.com/flightaware/dump1090) ADS-B receiver and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge connects to your dump1090 instance via the BEAST protocol, decodes raw Mode-S/ADS-B messages from aircraft broadcasting on 1090 MHz, and forwards structured aircraft telemetry to the configured Kafka endpoint.

## Mode-S/ADS-B Data

ADS-B (Automatic Dependent Surveillance-Broadcast) is a surveillance technology where aircraft broadcast their position, altitude, speed, and identification. You receive these signals with an inexpensive RTL-SDR USB dongle and an antenna, decoded by [dump1090](https://github.com/flightaware/dump1090). The easiest way to get started is [PiAware](https://flightaware.com/adsb/piaware/install) on a Raspberry Pi.

The bridge reads from dump1090's BEAST output (TCP port 30005 by default), decodes the raw messages, and bundles them into batches flushed every second or after 1,000 records.

## Functionality

The bridge connects to a dump1090 instance via the BEAST binary protocol, decodes aircraft telemetry (position, altitude, speed, heading, callsign, vertical rate), and writes batched messages to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-mode-s:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e DUMP1090_HOST='<dump1090-host-ip>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-mode-s:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e DUMP1090_HOST='<dump1090-host-ip>' \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-mode-s:latest
```

### With Antenna Reference Position

Provide your antenna's coordinates for accurate distance and bearing calculations:

```shell
$ docker run --rm \
    -e DUMP1090_HOST='<dump1090-host-ip>' \
    -e REF_LAT='52.3676' \
    -e REF_LON='4.9041' \
    -e STATIONID='amsterdam-01' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-mode-s:latest
```

## Environment Variables

### `DUMP1090_HOST`

Host or IP address of the dump1090 instance. Default: `localhost`.

### `DUMP1090_PORT`

TCP port for the BEAST binary output of dump1090. Default: `30005`.

### `REF_LAT`

Latitude of the receiving antenna, used for position calculations. Default: `0`.

### `REF_LON`

Longitude of the receiving antenna, used for position calculations. Default: `0`.

### `STATIONID`

Identifier for this receiving station, used as the CloudEvent source. Default: `station1`.

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

Polling interval in seconds. Default: `60`.

