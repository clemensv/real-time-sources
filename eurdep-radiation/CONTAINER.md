# EURDEP Radiation Container

## Overview

This container bridges the EURDEP (European Radiological Data Exchange
Platform) ambient gamma dose rate monitoring network to Apache Kafka
endpoints. It polls the IMIS WFS data interface hourly, emitting station
metadata as reference events and dose rate readings as telemetry events
in CloudEvents format.

EURDEP aggregates data from approximately 5,500 stationary gamma dose rate
monitoring stations across 39 European countries. Each station reports
hourly averaged ambient dose rates in microsieverts per hour (µSv/h).

For the full event catalog, see [EVENTS.md](EVENTS.md).

## Container Image

```bash
docker pull ghcr.io/clemensv/real-time-sources/eurdep-radiation:latest
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
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=eurdep-radiation" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/eurdep-radiation:latest
```

## Running with Azure Event Hubs

```bash
docker run -d \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=eurdep-radiation" \
  ghcr.io/clemensv/real-time-sources/eurdep-radiation:latest
```

## Running with Fabric Event Streams

Use the Kafka connection string from your Fabric Event Stream custom
endpoint. The format is the same as Azure Event Hubs.

## Behavior

1. At startup, fetches all EURDEP features and emits `eu.jrc.eurdep.Station`
   events for each unique station.
2. Enters a polling loop, fetching the latest measurements every
   `POLLING_INTERVAL` seconds (default: 3600 = 1 hour).
3. Deduplicates readings by tracking the last `end_measure` timestamp
   per station. Only new readings are emitted.
4. For each station, only the shortest `analyzed_range_in_h` reading is
   emitted to avoid duplicate measurements at different analysis windows.
5. Station reference data is refreshed every 6 hours.
6. All events are keyed by the station identifier (e.g. `AT0001`), enabling
   per-station partitioning.

## Upstream Source

- EURDEP: https://eurdep.jrc.ec.europa.eu/
- Data interface: https://www.imis.bfs.de/ogc/opendata/ows (WFS 1.1.0)
- License: EU open data
