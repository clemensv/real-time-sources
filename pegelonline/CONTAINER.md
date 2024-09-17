# WSV Pegelonline API Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the WSV Pegelonline API and
Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge reads
real-time water level data from the WSV Pegelonline API and writes it to a Kafka
topic.

## WSV Pegelonline API

The WSV Pegelonline API is a service provided by the Federal Waterways and
Shipping Administration of Germany (Wasserstraßen- und Schifffahrtsverwaltung
des Bundes, WSV). It offers real-time water level data for German rivers and
waterways, essential for navigation, flood prediction, and environmental
monitoring.

## Functionality

The bridge fetches water level data from the WSV Pegelonline API and writes the
data to a Kafka topic as structured JSON [CloudEvents](https://cloudevents.io/)
in a JSON format documented in [EVENTS.md](EVENTS.md). You can configure the
bridge to handle multiple stations by supplying their identifiers in the
configuration.

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

## Using the Container Image

The container image defines a single command that starts the bridge. It reads
data from the WSV Pegelonline API and writes it to a Kafka topic, Azure Event
Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e STATIONS='<station-ids>' \
    ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the
connection string from the Azure portal, Azure CLI, or the "custom endpoint" of
a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e STATIONS='<station-ids>' \
    ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to establish a connection to
Azure Event Hubs or Fabric Event Streams. This replaces the need for
`KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with
TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication. Ensure your Kafka brokers support SASL
PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

## Additional Information

- **Source Code**: [GitHub Repository](https://github.com/clemensv/real-time-sources/tree/main/pegelonline)
- **Documentation**: Refer to [EVENTS.md](EVENTS.md) for the JSON event format.
- **License**: MIT

## Example

To run the bridge sending it to an Azure Event Hub:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...' \
    ghcr.io/clemensv/real-time-sources-pegelonline:latest
```

The events documented in [EVENTS.md](EVENTS.md) may look as follows:

#### Station Event

The [`de.wsv.pegelonline.Station`](EVENTS.md#message-dewsvpegelonlinestation) event provides information about a water level monitoring station. It is emitted when a new station is discovered or when the station information is updated, and during the first run of the bridge.

```JSON
{
    "specversion": "1.0",
    "type": "de.wsv.pegelonline.Station",
    "source": "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/EITZE",
    "id": "05fd3e7f-c415-4e53-986a-6480189626c0",
    "time": "2024-09-15T16:10:42.986549Z",
    "subject": "47174d8f-1b8e-4599-8a59-b580dd55bc87",
    "data": {
        "uuid": "47174d8f-1b8e-4599-8a59-b580dd55bc87",
        "number": "48900237",
        "shortname": "EITZE",
        "longname": "EITZE",
        "km": 9.56,
        "agency": "VERDEN",
        "longitude": "9.276769435375872",
        "latitude": "52.90406544743417",
        "water": {
            "shortname": "ALLER",
            "longname": "ALLER"
        }
    }
}
```	

#### Current Measurement Event

The [`de.wsv.pegelonline.CurrentMeasurement`](EVENTS.md#message-dewsvpegelonlinecurrentmeasurement) event provides the current water level measurement for a station. It is emitted at regular intervals, typically every 15 minutes.

```JSON
{
    "specversion": "1.0",
    "type": "de.wsv.pegelonline.CurrentMeasurement",
    "source": "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/47174d8f-1b8e-4599-8a59-b580dd55bc87/W/currentmeasurement.json",
    "id": "8401ce11-4538-4fb2-a53a-61ff99e7abeb",
    "time": "2024-09-17T02:46:15.822779Z",
    "subject": "47174d8f-1b8e-4599-8a59-b580dd55bc87",
    "data": {
        "station_uuid": "47174d8f-1b8e-4599-8a59-b580dd55bc87",
        "timestamp": "2024-09-17T02:45:00.0000000Z",
        "value": 262,
        "stateMnwMhw": "normal",
        "stateNswHsw": "unknown"
    }
}
```	

This setup allows you to integrate real-time water level data into your data processing pipelines, facilitating timely decision-making for navigation and environmental monitoring.
