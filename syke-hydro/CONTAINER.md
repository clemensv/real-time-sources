# SYKE Hydrology Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Finnish Environment
Institute's (SYKE) hydrological monitoring network and Apache Kafka, Azure Event
Hubs, and Fabric Event Streams. The bridge polls the
[SYKE Hydrology OData API](https://rajapinnat.ymparisto.fi/api/Hydrologiarajapinta/1.1/odata)
for water level and discharge readings from Finnish gauging stations and forwards
new observations as [CloudEvents](https://cloudevents.io/) in JSON format.

> **Note:** The upstream data source requires no authentication or API key. The
> bridge can start fetching data immediately with no additional registration.

## Functionality

The bridge retrieves hydrological data from the SYKE Hydrology OData API —
provided by the Finnish Environment Institute — and writes entries to a Kafka
topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

On startup, the bridge emits `FI.SYKE.Hydrology.Station` events for all active
monitoring stations (reference data). It then enters a polling loop, emitting
`FI.SYKE.Hydrology.WaterLevelObservation` events only for new or changed
readings (delta emission).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-syke-hydro:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-syke-hydro:latest
```

## Using the Container Image

The container starts the bridge in feed mode, reading data from the SYKE
Hydrology OData API and writing it to Kafka, Azure Event Hubs, or Fabric Event
Streams.

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-syke-hydro:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BROKER='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    ghcr.io/clemensv/real-time-sources-syke-hydro:latest
```

### Preserving State Between Restarts

To preserve the de-duplication state between container restarts and avoid
re-sending observations, mount a volume and set the `STATE_FILE` environment
variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/syke_hydro_state.json' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-syke-hydro:latest
```

### Adjusting the Polling Interval

The default polling interval is 3600 seconds (1 hour), matching the upstream
data update cadence. You can adjust it:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e POLLING_INTERVAL='1800' \
    ghcr.io/clemensv/real-time-sources-syke-hydro:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for separate `KAFKA_BROKER` and
topic configuration, since the bootstrap server and topic are extracted from the
connection string.

### `KAFKA_BROKER`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced. Default: `syke-hydro`.

### `POLLING_INTERVAL`

The interval in seconds between polling cycles. Default: `3600` (1 hour).

### `STATE_FILE`

The file path where the bridge stores the de-duplication state. This tracks
which readings have already been forwarded, allowing the bridge to resume without
duplicating events after restarts. Default: `~/.syke_hydro_state.json`.

### `KAFKA_ENABLE_TLS`

Whether to use TLS for the Kafka connection. Default: `true`. Set to `false` for
plaintext connections to local brokers.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template-with-eventhub.json)
