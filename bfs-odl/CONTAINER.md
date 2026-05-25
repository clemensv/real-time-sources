# BfS ODL Container

## Overview

This container bridges the German Federal Office for Radiation Protection
(BfS) ODL ambient gamma dose rate monitoring network to Apache Kafka
endpoints. It polls the BfS WFS data interface hourly, emitting station
metadata as reference events and dose rate measurements as telemetry events
in CloudEvents format.

The BfS operates approximately 1,700 stationary gamma dose rate probes
across Germany. Each probe reports hourly averaged ambient dose rates in
microsieverts per hour (µSv/h), optionally decomposed into cosmic and
terrestrial components.

For the full event catalog, see [EVENTS.md](EVENTS.md).

## Container Image

```bash
docker pull ghcr.io/clemensv/real-time-sources/bfs-odl:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka connection string (see below) |
| `POLLING_INTERVAL` | No | `3600` | Polling interval in seconds |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plain Kafka without TLS |
| `STATE_FILE` | No | — | Path to state persistence file for deduplication |

## Running with Plain Kafka

```bash
docker run -d \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=bfs-odl" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/bfs-odl:latest
```

## Running with Azure Event Hubs

```bash
docker run -d \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=bfs-odl" \
  ghcr.io/clemensv/real-time-sources/bfs-odl:latest
```

## Running with Fabric Event Streams

Use the Kafka connection string from your Fabric Event Stream custom
endpoint. The format is the same as Azure Event Hubs.

## Behavior

1. At startup, fetches all station metadata and emits `de.bfs.odl.Station`
   events for each station.
2. Enters a polling loop, fetching the latest 1-hour measurements every
   `POLLING_INTERVAL` seconds (default: 3600 = 1 hour).
3. Deduplicates measurements by tracking the last `end_measure` timestamp
   per station. Only new or updated readings are emitted.
4. All events are keyed by the 9-digit station identifier (`kenn`), enabling
   per-station partitioning.

## Upstream Source

- BfS ODL Info: https://odlinfo.bfs.de/
- Data interface: https://odlinfo.bfs.de/ODL/EN/service/data-interface/data-interface_node.html
- License: Open data, see https://www.imis.bfs.de/geoportal/resources/sitepolicy.html

## MQTT / Unified Namespace

A separate container image publishes the same data as MQTT 5.0 binary-mode
CloudEvents into a Unified Namespace topic tree:

```
radiation/de/bfs/bfs-odl/{state}/{station_id}/info
radiation/de/bfs/bfs-odl/{state}/{station_id}/dose-rate
```

All messages are published with **QoS 1** and **retain = true**.

### Subscription wildcards

| Pattern | Description |
|---|---|
| `radiation/de/bfs/bfs-odl/#` | All BfS ODL events |
| `radiation/de/bfs/bfs-odl/bayern/+/dose-rate` | Dose rate for all Bayern stations |
| `radiation/de/bfs/bfs-odl/+/+/info` | Station info for all states |

### Running the MQTT container

```bash
docker pull ghcr.io/clemensv/real-time-sources/bfs-odl-mqtt:latest

docker run -d \
  -e MQTT_BROKER_URL="mqtt://broker:1883" \
  -e POLLING_INTERVAL=3600 \
  ghcr.io/clemensv/real-time-sources/bfs-odl-mqtt:latest
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `MQTT_BROKER_URL` | Yes | — | MQTT broker URL (mqtt:// or mqtts://) |
| `POLLING_INTERVAL` | No | `3600` | Polling interval in seconds |
| `ONCE_MODE` | No | `false` | Exit after one cycle |
| `MQTT_CLIENT_ID` | No | — | MQTT client identifier |
| `MQTT_CONTENT_MODE` | No | `binary` | CloudEvents content mode (`binary` or `structured`) |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-with-eventhub.json)


## MQTT and AMQP companion feeders

This source now ships separate Kafka, MQTT, and AMQP containers. The MQTT companion publishes binary-mode CloudEvents to `radiation/ch/bfs/bfs-odl/{canton}/{station_id}/{event}` (`info`, `dose-rate`) with retained QoS 1 messages for last-known-value consumers. The AMQP companion publishes the same CloudEvents to AMQP 1.0 brokers or Azure Service Bus using the station subject and a `canton` application property for filtering.

Images: `ghcr.io/clemensv/real-time-sources-bfs-odl-mqtt:latest`, `ghcr.io/clemensv/real-time-sources-bfs-odl-amqp:latest`. Deployment templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-with-servicebus.json`, and `infra/azure-template-amqp.json`.
