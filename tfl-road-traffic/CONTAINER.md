# TfL Road Traffic Container

This container is a bridge between the [Transport for London (TfL) Unified API](https://api.tfl.gov.uk/) road traffic data and Apache Kafka endpoints. It polls the TfL Road API and emits road corridor reference data, corridor status telemetry, and disruption telemetry as CloudEvents.

All events are structured CloudEvents. See [EVENTS.md](EVENTS.md) for the event schemas.

## Docker

Pull the container image:

```bash
docker pull ghcr.io/clemensv/real-time-sources/tfl-road-traffic:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka or Azure Event Hubs connection string |
| `KAFKA_ENABLE_TLS` | No | Set to `false` to disable TLS (default: `true`) |
| `POLLING_INTERVAL` | No | Seconds between telemetry poll cycles (default: `60`) |
| `REFERENCE_REFRESH_INTERVAL` | No | Seconds between reference data refreshes (default: `3600`) |

### Connection String Formats

**Plain Kafka:**
```
BootstrapServer=mybroker:9092;EntityPath=tfl-road-traffic
```

**Azure Event Hubs:**
```
Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=...;EntityPath=tfl-road-traffic
```

**Microsoft Fabric Event Stream:**
Use the Fabric-provided connection string.

## Running

### Plain Kafka (no TLS)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=mybroker:9092;EntityPath=tfl-road-traffic" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/tfl-road-traffic:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=...;EntityPath=tfl-road-traffic" \
  ghcr.io/clemensv/real-time-sources/tfl-road-traffic:latest
```

## Kafka Topics

All events are written to a single topic. The default topic name is `tfl-road-traffic` (configurable via `EntityPath` in the connection string).

### Kafka Keys

| Event Type | Key Format |
|---|---|
| `uk.gov.tfl.road.RoadCorridor` | `roads/{road_id}` |
| `uk.gov.tfl.road.RoadStatus` | `roads/{road_id}` |
| `uk.gov.tfl.road.RoadDisruption` | `disruptions/{disruption_id}` |

## Event Catalog

| Event Type | Description |
|---|---|
| `uk.gov.tfl.road.RoadCorridor` | Reference record for a TfL managed road corridor (emitted at startup and refreshed hourly) |
| `uk.gov.tfl.road.RoadStatus` | Real-time status snapshot for a TfL road corridor (emitted every polling cycle) |
| `uk.gov.tfl.road.RoadDisruption` | Real-time road disruption event (emitted when new or updated disruptions are detected) |

See [EVENTS.md](EVENTS.md) for full schema documentation.

## Data Source

Data is sourced from the [TfL Unified API](https://api.tfl.gov.uk/). The API is open and does not require authentication, though registration for an API key is recommended for production use to increase rate limits.

- `/Road` — Road corridor catalog
- `/Road/all/Status` — Current status for all corridors
- `/Road/all/Disruption` — Active disruptions on the road network
