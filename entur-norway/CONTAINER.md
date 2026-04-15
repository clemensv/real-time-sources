# Entur Norway Container

## Overview

This container bridges the [Entur Norway](https://developer.entur.org/) SIRI
real-time feeds to Apache Kafka endpoints. It polls the SIRI 2.0 REST API for
Estimated Timetable (ET), Vehicle Monitoring (VM), and Situation Exchange (SX)
data, emitting events as CloudEvents.

The Entur API provides real-time information about Norwegian public transport
across all operators and modes (bus, tram, rail, metro, ferry). Data is sourced
from the national journey planner and covers the entire Norwegian network.

For the full event catalog, see [EVENTS.md](EVENTS.md).

## Container Image

```bash
docker pull ghcr.io/clemensv/real-time-sources/entur-norway:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka connection string (see below) |
| `POLLING_INTERVAL` | No | `30` | Polling interval in seconds |
| `MAX_SIZE` | No | `1000` | Maximum records per SIRI request |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plain Kafka without TLS |

## Running with Plain Kafka

```bash
docker run -d \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=entur-norway" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/entur-norway:latest
```

## Running with Azure Event Hubs

```bash
docker run -d \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=entur-norway" \
  ghcr.io/clemensv/real-time-sources/entur-norway:latest
```

## Running with Fabric Event Streams

Use the Kafka connection string from your Fabric Event Stream custom
endpoint. The format is the same as Azure Event Hubs.

## Behavior

1. At startup, fetches all three SIRI feeds (ET, VM, SX) without a `requestorId`
   to obtain the complete current dataset.
2. From the initial ET snapshot, emits `no.entur.DatedServiceJourney` reference
   events for each unique service journey, providing timetable context for
   downstream consumers.
3. Emits `no.entur.EstimatedVehicleJourney` events for all stop-level
   predictions from the ET feed.
4. Emits `no.entur.MonitoredVehicleJourney` events for all live vehicle
   positions from the VM feed.
5. Emits `no.entur.PtSituationElement` events for all active service disruptions
   from the SX feed.
6. Subsequent polling cycles use a persistent `requestorId` per feed to receive
   only changed data since the last request (incremental delivery).
7. Handles SIRI `MoreData: true` responses by paginating until all data is
   received.

## Kafka Topic

All events are produced to a single Kafka topic (default: `entur-norway`).

- `journeys` events use the key format `journeys/{operating_day}/{service_journey_id}`
- `situations` events use the key format `situations/{situation_number}`

## Data Source

- API: <https://api.entur.io/realtime/v1/rest/>
- Documentation: <https://developer.entur.org/pages-real-time-intro>
- License: [NLOD (Norwegian Licence for Open Government Data)](https://data.norge.no/nlod/en/2.0)
- Coverage: All Norwegian public transport operators and modes
