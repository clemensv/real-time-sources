# USGS NWIS Water Quality bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [USGS Water Services](https://waterservices.usgs.gov/)
Instantaneous Values Service (water quality parameters) and Apache Kafka, Azure Event Hubs, and
Fabric Event Streams. The bridge fetches continuous water quality sensor data
(dissolved oxygen, pH, temperature, turbidity, specific conductance, nitrate) and
forwards readings to the configured Kafka endpoints.

## Functionality

The bridge retrieves water quality data from the USGS Instantaneous Values Service
and writes readings to a Kafka topic as [CloudEvents](https://cloudevents.io/) in
JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database,
the integration with Fabric Eventhouse and Azure Data Explorer is described in
[DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
```

## Using the Container Image

The container starts the bridge, reading water quality data from USGS and writing
to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
```

### Preserving State Between Restarts

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e USGS_WQ_LAST_POLLED_FILE='/mnt/state/usgs_wq_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-usgs-nwis-wq:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string for Azure Event Hubs or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

Kafka broker addresses (comma-separated host:port pairs).

### `KAFKA_TOPIC`

Kafka topic for message production.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `USGS_WQ_LAST_POLLED_FILE`

File path for state persistence. Default: `/mnt/state/usgs_wq_last_polled.json`.

### `USGS_WQ_STATES`

Comma-separated state codes to poll (e.g. `MD,VA,CA`). Default: all US states and territories.

### `USGS_WQ_SITES`

Comma-separated USGS site numbers to poll (e.g. `01646500,01578310`). Overrides state-based polling.

### `USGS_WQ_PARAMETER_CODES`

Comma-separated USGS parameter codes (e.g. `00300,00010,00400`). Default: all water quality parameters.
