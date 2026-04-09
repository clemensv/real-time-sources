# iRail Container

## Overview

This container bridges the iRail Belgian railway API to Apache Kafka
endpoints. It polls the iRail liveboard API for approximately 600
NMBS/SNCB railway stations, emitting station metadata as reference events
and real-time departure boards as telemetry events in CloudEvents format.

The iRail API provides real-time information about train departures across
the Belgian railway network, including delays, platform assignments,
cancellation status, and crowd-sourced occupancy estimates.

For the full event catalog, see [EVENTS.md](EVENTS.md).

## Container Image

```bash
docker pull ghcr.io/clemensv/real-time-sources/irail:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka connection string (see below) |
| `POLLING_INTERVAL` | No | `300` | Polling interval in seconds |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plain Kafka without TLS |
| `STATION_FILTER` | No | — | Comma-separated station IDs to poll (default: all) |

## Running with Plain Kafka

```bash
docker run -d \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=irail" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/irail:latest
```

## Running with Azure Event Hubs

```bash
docker run -d \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=irail" \
  ghcr.io/clemensv/real-time-sources/irail:latest
```

## Running with Fabric Event Streams

Use the Kafka connection string from your Fabric Event Stream custom
endpoint. The format is the same as Azure Event Hubs.

## Behavior

1. At startup, fetches all station metadata and emits `be.irail.Station`
   events for each station (~600 stations).
2. Enters a polling loop, fetching the current departure board for each
   station via the iRail liveboard API.
3. Respects the iRail rate limit of 3 requests/second. A full cycle through
   all stations takes approximately 3–4 minutes.
4. After completing a full cycle, waits for the remaining `POLLING_INTERVAL`
   before starting the next cycle.
5. All events are keyed by the 9-digit UIC-derived NMBS station identifier,
   enabling per-station partitioning.

## Station Filter

To reduce load and focus on specific stations, set `STATION_FILTER` to a
comma-separated list of 9-digit NMBS station codes:

```bash
docker run -d \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=irail" \
  -e KAFKA_ENABLE_TLS=false \
  -e STATION_FILTER="008814001,008821006,008892007" \
  ghcr.io/clemensv/real-time-sources/irail:latest
```

Common station codes:
- `008814001` — Brussels-South (Bruxelles-Midi / Brussel-Zuid)
- `008821006` — Antwerp-Central (Antwerpen-Centraal)
- `008892007` — Ghent-Sint-Pieters (Gent-Sint-Pieters)
- `008891009` — Bruges (Brugge)
- `008812005` — Brussels-North (Bruxelles-Nord / Brussel-Noord)

## Upstream Source

- iRail API: https://api.irail.be/
- Documentation: https://docs.irail.be/
- Status: https://status.irail.be/
- License: iRail open data

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template-with-eventhub.json)
