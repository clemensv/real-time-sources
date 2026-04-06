# Digitraffic Road bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image bridges the Finnish national road sensor network operated
by Fintraffic via the Digitraffic MQTT service at `wss://tie.digitraffic.fi/mqtt`
to Apache Kafka, Azure Event Hubs, and Fabric Event Streams. It streams real-time
TMS (Traffic Measurement System) sensor data and road weather station data as
CloudEvents documented in [EVENTS.md](EVENTS.md).

## Functionality

The bridge connects to the Digitraffic MQTT WebSocket endpoint and subscribes
to TMS sensor topics (`tms-v2/#`) and road weather sensor topics
(`weather-v2/#`). Each MQTT message carries a single sensor reading identified
by station and sensor ID extracted from the topic path. The bridge enriches the
payload with the station and sensor identifiers and emits structured CloudEvents
to Kafka.

TMS stations (500+) measure vehicle counts and average speeds. Road weather
stations (350+) measure air and road surface temperatures, wind speeds,
humidity, dew point, and precipitation. Data updates every minute via REST but
arrives in real time via MQTT.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

## Using the Container Image

Run the bridge against a Kafka broker:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='broker:9092' \
    -e KAFKA_TOPIC='digitraffic-road' \
    -e KAFKA_ENABLE_TLS='false' \
    ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

Or use an Event Hubs or Fabric Event Streams connection string:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

## Environment Variables

- `CONNECTION_STRING`: Event Hubs or Fabric Event Streams connection string.
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers.
- `KAFKA_TOPIC`: Kafka topic. Defaults to `digitraffic-road`.
- `SASL_USERNAME`: SASL/PLAIN username.
- `SASL_PASSWORD`: SASL/PLAIN password.
- `KAFKA_ENABLE_TLS`: When no SASL credentials are supplied, use `true` for
  TLS or `false` for plain Kafka.
- `DIGITRAFFIC_ROAD_SUBSCRIBE`: Comma-separated data types to subscribe to.
  Defaults to `tms,weather`.
- `DIGITRAFFIC_ROAD_STATION_FILTER`: Comma-separated station IDs to include.
  Defaults to all stations.
- `DIGITRAFFIC_ROAD_FLUSH_INTERVAL`: Flush Kafka producer every N events.
  Defaults to `1000`.
