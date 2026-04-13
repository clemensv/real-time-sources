# Digitraffic Marine Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between Finland's Digitraffic Marine open data services and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The image supports two runtime modes:

- `stream` connects to the Digitraffic MQTT WebSocket and forwards AIS vessel positions and metadata.
- `port-calls` polls the Portnet-backed REST APIs and forwards vessel details, port locations, and port call visit updates.

## Digitraffic Marine Data

Digitraffic Marine is an open data service from [Fintraffic](https://www.fintraffic.fi) providing real-time AIS data for the Finnish coastal zone and Baltic Sea. No API key or registration is required. The data is licensed under Creative Commons 4.0 BY.

> Source: Fintraffic / digitraffic.fi, license CC 4.0 BY

## Functionality

Both delivery modes write [CloudEvents](https://cloudevents.io/) in JSON format to the configured Kafka endpoint. The emitted event families are documented in [EVENTS.md](EVENTS.md).

### `stream` mode

The default container command is `python -m digitraffic_maritime stream`. It connects to the Digitraffic MQTT endpoint at `wss://meri.digitraffic.fi:443/mqtt`, subscribes to vessel location and metadata topics, and continuously forwards AIS updates.

### `port-calls` mode

The container can also run `python -m digitraffic_maritime port-calls`. In this mode it polls these Digitraffic REST endpoints:

- `https://meri.digitraffic.fi/api/port-call/v1/vessel-details`
- `https://meri.digitraffic.fi/api/port-call/v1/ports`
- `https://meri.digitraffic.fi/api/port-call/v1/port-calls`

Each cycle emits reference data first (`VesselDetails`, `PortLocation`) and then visit telemetry (`PortCall`). The bridge persists last-seen timestamps in a JSON state file to suppress duplicates between polls.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

This uses the default `stream` mode:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### With a Kafka Broker

This uses the default `stream` mode:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### Position Updates Only

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e DIGITRAFFIC_SUBSCRIBE='location' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### Track Specific Vessels

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e DIGITRAFFIC_FILTER_MMSI='230629000,219598000' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### Port Calls and Reference Data

Run the image with an explicit command override to enable `port-calls` mode:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest \
    python -m digitraffic_maritime port-calls
```

### Port Calls with Direct Kafka Parameters

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e DIGITRAFFIC_PORTCALL_POLL_INTERVAL='300' \
    -e DIGITRAFFIC_PORTCALL_STATE_FILE='/state/portcalls.json' \
    -v digitraffic-portcalls-state:/state \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest \
    python -m digitraffic_maritime port-calls
```

## Environment Variables

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

### `DIGITRAFFIC_SUBSCRIBE`

Comma-separated list of message types to subscribe to: `location`, `metadata`, or both. Default: `location,metadata`.

### `DIGITRAFFIC_FILTER_MMSI`

Comma-separated list of MMSI numbers to include. When set, the bridge subscribes to specific vessel topics rather than wildcard topics. Default: all vessels.

### `DIGITRAFFIC_FLUSH_INTERVAL`

Number of events to buffer before flushing the Kafka producer. Default: `1000`.

### `DIGITRAFFIC_PORTCALL_POLL_INTERVAL`

Polling interval in seconds for the `port-calls` command. Default: `300`.

### `DIGITRAFFIC_PORTCALL_STATE_FILE`

JSON file used by the `port-calls` command to persist last-seen timestamps for `VesselDetails`, `PortLocation`, and `PortCall` records. Default: `~/.digitraffic_portcalls_state.json` inside the container unless overridden.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-eventhub.json)
