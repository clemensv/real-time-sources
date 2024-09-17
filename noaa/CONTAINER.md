# NOAA Tides and Currents API Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the NOAA Tides and Currents API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches real-time data from NOAA endpoints and forwards it to the configured Kafka endpoints.

## NOAA Tides and Currents API

The National Oceanic and Atmospheric Administration (NOAA) Tides and Currents API offers real-time and historical data on tides, water levels, currents, and other oceanographic and meteorological parameters. This information is vital for navigation, coastal management, engineering, and environmental monitoring.

## Functionality

The bridge retrieves data from the NOAA Tides and Currents API and writes it to a Kafka topic as [CloudEvents](https://cloudevents.io/) in a JSON format, which is documented in [EVENTS.md](EVENTS.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-noaa:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-noaa:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading data from the NOAA Tides and Currents API and writing it to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-noaa:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-noaa:latest
```

### Preserving State Between Restarts

To preserve the last polled timestamps between restarts and avoid reprocessing data, mount a volume to the container and set the `NOAA_LAST_POLLED_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e NOAA_LAST_POLLED_FILE='/mnt/fileshare/noaa_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-noaa:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication. Ensure your Kafka brokers support SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `NOAA_LAST_POLLED_FILE`

The file path where the bridge stores the last polled timestamps. This helps in resuming data fetching without duplication after restarts. Default is `/mnt/fileshare/noaa_last_polled.json`.


## Deploying into Azure Container Instances

You can deploy the RSS/Atom bridge as a container directly to Azure Container
Instances providing the information explained above. Just click the button below and go.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa%2Fazure-template.json)


## Additional Information

- **Source Code**: [GitHub Repository](https://github.com/clemensv/real-time-sources/tree/main/noaa)
- **Documentation**: Refer to [EVENTS.md](EVENTS.md) for the JSON event format.
- **License**: MIT

## Example

To run the bridge and send data to an Azure Event Hub:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...' \
    -e NOAA_LAST_POLLED_FILE='/mnt/fileshare/noaa_last_polled.json' \
    -v /path/to/state:/mnt/fileshare \
    ghcr.io/clemensv/real-time-sources-noaa:latest
```

An exemplary CloudEvent produced by the bridge looks as follows:

```json
{
    "specversion": "1.0",
    "type": "Microsoft.OpenData.US.NOAA.WaterLevel",
    "source": "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/8652587.json",
    "id": "7bf3c89c-0d21-4815-a882-ce7a2c1e9637",
    "time": "2024-09-17T15:59:18.831393Z",
    "data": {
        "station_id": "8652587",
        "timestamp": "2024-09-16T16:06:00.0000000Z",
        "value": 0.295,
        "stddev": 0.005,
        "outside_sigma_band": false,
        "flat_tolerance_limit": false,
        "rate_of_change_limit": false,
        "max_min_expected_height": false,
        "quality": 0
    }
}
```

This setup allows you to integrate real-time oceanographic data into your data processing pipelines, aiding in navigation safety, coastal planning, and environmental monitoring.

## Notes

- Ensure that you have network connectivity to the NOAA Tides and Currents API endpoints.
- The bridge efficiently handles data fetching and forwarding, but monitor resource usage if you are fetching data at a high frequency.
- Customize the application according to your data freshness requirements and system capabilities.

