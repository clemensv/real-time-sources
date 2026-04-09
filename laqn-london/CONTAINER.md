# LAQN London Air Quality Network Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container bridges the public LAQN London Air Quality Network API operated
by King's College London into Kafka-compatible endpoints. It emits structured
JSON CloudEvents for monitoring sites, pollutant species, hourly measurements,
and Daily Air Quality Index bulletin records.

The upstream is HTTP-only at `http://api.erg.ic.ac.uk/AirQuality/`. That is the
published upstream interface and therefore what this bridge uses.

## Functionality

At startup, the container fetches all site metadata and all pollutant species
definitions and emits them as reference events. It then polls:

- hourly site measurement data for all active sites, covering yesterday plus
  today
- the latest London-wide Daily AQI bulletin

Reference data is re-emitted every 24 polls so downstream consumers can keep a
temporally consistent local copy of the site and species catalogs.

If LAQN leaves a site's decimal latitude or longitude blank, the bridge emits
that coordinate as `null` in the site reference event and continues with the
rest of the feed.

## Installing the Container Image

```shell
docker pull ghcr.io/clemensv/real-time-sources-laqn-london:latest
```

## Using the Container Image

### With a Kafka Broker

```shell
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<broker:9092>' \
  -e KAFKA_TOPIC='laqn-london' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-laqn-london:latest
```

For local Kafka without TLS:

```shell
docker run --rm \
  -e CONNECTION_STRING='BootstrapServer=host.docker.internal:9092;EntityPath=laqn-london' \
  -e KAFKA_ENABLE_TLS='false' \
  ghcr.io/clemensv/real-time-sources-laqn-london:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
docker run --rm \
  -e CONNECTION_STRING='Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=laqn-london' \
  ghcr.io/clemensv/real-time-sources-laqn-london:latest
```

## Environment Variables

### `CONNECTION_STRING`

Azure Event Hubs or Fabric Event Streams connection string. When set, it
overrides the explicit Kafka bootstrap server and SASL settings.

### `KAFKA_BOOTSTRAP_SERVERS`

Kafka bootstrap servers as a comma-separated `host:port` list.

### `KAFKA_TOPIC`

Kafka topic name for the emitted CloudEvents.

### `SASL_USERNAME`

Username for SASL/PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL/PLAIN authentication.

### `KAFKA_ENABLE_TLS`

Set to `false` when targeting a plain local Kafka broker. The default is `true`.

### `POLLING_INTERVAL`

Polling interval in seconds. The default is `3600`.

### `STATE_FILE`

Optional path for the persisted dedupe state file. The default is
`~/.laqn_london_state.json`.

## Output Contract

The emitted CloudEvents are documented in [EVENTS.md](EVENTS.md). Site,
measurement, and Daily AQI events are keyed by `site_code`. Species reference
events are keyed by `species_code`. All event types share the same Kafka topic.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-with-eventhub.json)
