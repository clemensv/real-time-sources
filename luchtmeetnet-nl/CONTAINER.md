# Luchtmeetnet Netherlands Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container bridges the public Dutch Luchtmeetnet air-quality API into a
Kafka-compatible topic. It emits structured JSON CloudEvents for station
metadata, component definitions, hourly measurements, and hourly Dutch
Luchtkwaliteitsindex values. The payload contract is documented in
[EVENTS.md](EVENTS.md).

## Upstream Source

Luchtmeetnet is the Dutch national air-quality monitoring platform. The public
API exposes:

- station metadata
- a component catalog
- hourly measurements for monitored formulas
- hourly LKI values

The upstream is public, unauthenticated, and updated hourly.

## Pulling the Image

```shell
docker pull ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl:latest
```

## Running with Kafka

```shell
docker run --rm ^
  -e KAFKA_BOOTSTRAP_SERVERS=localhost:9092 ^
  -e KAFKA_TOPIC=luchtmeetnet-nl ^
  -e KAFKA_ENABLE_TLS=false ^
  -e POLLING_INTERVAL=3600 ^
  ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl:latest
```

## Running with Azure Event Hubs or Fabric Event Streams

```shell
docker run --rm ^
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=luchtmeetnet-nl" ^
  -e POLLING_INTERVAL=3600 ^
  ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl:latest
```

## Environment Variables

### Required connection settings

- `CONNECTION_STRING` — Event Hubs or Fabric custom-endpoint connection string.
  When this is set, it overrides the explicit Kafka connection parameters.
- `KAFKA_BOOTSTRAP_SERVERS` — Comma-separated Kafka broker list.
- `KAFKA_TOPIC` — Target Kafka topic.
- `SASL_USERNAME` — SASL/PLAIN username for Kafka.
- `SASL_PASSWORD` — SASL/PLAIN password for Kafka.
- `KAFKA_ENABLE_TLS` — Enables TLS when set to `true` (default). Set to
  `false` for plain local Kafka in Docker E2E and local development.

### Polling and state settings

- `POLLING_INTERVAL` — Seconds between telemetry polls. Default: `3600`.
- `STATE_FILE` — JSON file used to persist last-seen timestamps across restarts.
- `STATION_REFRESH_INTERVAL` — Number of telemetry polls between station
  metadata refreshes. Default: `24`.
- `STATION_LIMIT` — Optional limit on the number of stations to poll. This is
  mainly useful for testing or when you want to stay well below the upstream
  fair-use threshold while experimenting.

## Event Hubs Connection String Format

```text
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<event-hub-name>
```

The bridge derives:

- Kafka bootstrap servers from `Endpoint`
- the Kafka topic from `EntityPath`
- SASL username as `$ConnectionString`
- SASL password as the full connection string

## Azure Container Instances

You can run the image directly in Azure Container Instances by supplying either
the Kafka settings or a single Event Hubs connection string as environment
variables. The image has no persistent state requirement beyond the optional
`STATE_FILE`, so it is a good fit for stateless container deployment.

## Analytics Follow-On

If you want to land these events into a database or analytics engine, the
repo-wide guidance in [DATABASE.md](../DATABASE.md) applies here as well.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fluchtmeetnet-nl%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fluchtmeetnet-nl%2Fazure-template-with-eventhub.json)
