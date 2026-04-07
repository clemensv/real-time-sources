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
