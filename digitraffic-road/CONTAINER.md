# Digitraffic Road bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image bridges the Finnish national road traffic network operated
by Fintraffic via the Digitraffic MQTT service at `wss://tie.digitraffic.fi/mqtt`
to Apache Kafka, Azure Event Hubs, and Fabric Event Streams. It streams real-time
TMS sensor data, road weather sensor data, traffic messages (announcements,
road works, weight restrictions, exempted transports), and maintenance vehicle
tracking as CloudEvents documented in [EVENTS.md](EVENTS.md).

## Functionality

The bridge connects to the Digitraffic MQTT WebSocket endpoint and subscribes
to four data families:

- **TMS sensor topics** (`tms-v2/#`): Vehicle counts and average speeds from 500+ stations.
- **Road weather sensor topics** (`weather-v2/#`): Temperature, wind, humidity, and precipitation from 350+ stations.
- **Traffic message topics** (`traffic-message-v3/simple/#`): Incidents, road works, weight restrictions, and exempted transports. MQTT payloads are gzip-compressed and base64-encoded Simple JSON.
- **Maintenance tracking topics** (`maintenance-v2/routes/#`): Position and task reports from road maintenance vehicles.

Events are emitted to three separate Kafka topics with distinct key models:

| Kafka topic | Key | Data families |
|---|---|---|
| `digitraffic-road-sensors` | `{station_id}/{sensor_id}` | TMS + weather sensor readings |
| `digitraffic-road-messages` | `{situation_id}` | Traffic messages |
| `digitraffic-road-maintenance` | `{domain}` | Maintenance tracking |

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
    -e KAFKA_TOPIC_SENSORS='digitraffic-road-sensors' \
    -e KAFKA_TOPIC_MESSAGES='digitraffic-road-messages' \
    -e KAFKA_TOPIC_MAINTENANCE='digitraffic-road-maintenance' \
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

- `CONNECTION_STRING`: Event Hubs or Fabric Event Streams connection string (provides bootstrap servers and SASL credentials).
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers.
- `KAFKA_TOPIC_SENSORS`: Kafka topic for sensor data. Defaults to `digitraffic-road-sensors`.
- `KAFKA_TOPIC_MESSAGES`: Kafka topic for traffic messages. Defaults to `digitraffic-road-messages`.
- `KAFKA_TOPIC_MAINTENANCE`: Kafka topic for maintenance tracking. Defaults to `digitraffic-road-maintenance`.
- `SASL_USERNAME`: SASL/PLAIN username.
- `SASL_PASSWORD`: SASL/PLAIN password.
- `KAFKA_ENABLE_TLS`: When no SASL credentials are supplied, use `true` for
  TLS or `false` for plain Kafka.
- `DIGITRAFFIC_ROAD_SUBSCRIBE`: Comma-separated data families to subscribe to.
  Defaults to `tms,weather,traffic-messages,maintenance`.
- `DIGITRAFFIC_ROAD_STATION_FILTER`: Comma-separated station IDs to include
  (sensors only). Defaults to all stations.
- `DIGITRAFFIC_ROAD_FLUSH_INTERVAL`: Flush Kafka producer every N events.
  Defaults to `1000`.
