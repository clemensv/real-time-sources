# NDW Road Traffic Container

## Overview

Docker container that bridges Dutch NDW (Nationaal Dataportaal Wegverkeer) open road traffic data to Apache Kafka as CloudEvents. Polls gzip-compressed DATEX II XML files from [https://opendata.ndw.nu/](https://opendata.ndw.nu/) and emits structured events for traffic speed, travel time, DRIP signs, MSI lane signals, and situation data (roadworks, bridge openings, closures, speed limits, safety messages).

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONNECTION_STRING` | Yes | — | Kafka connection string. Either `BootstrapServer=host:port;EntityPath=topic` (plain) or Azure Event Hubs format `Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...` |
| `KAFKA_TOPIC` | No | `ndw-road-traffic` | Kafka topic for all event types |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plain (non-TLS) connections |
| `POLLING_INTERVAL` | No | `60` | Telemetry poll interval in seconds |
| `STATE_FILE` | No | `~/.ndw_road_traffic_state.json` | Path to state file for deduplication |

## Docker Pull and Run

```bash
docker pull ghcr.io/clemensv/real-time-sources-ndw-road-traffic:latest

# Plain Kafka (local)
docker run -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=ndw-road-traffic" \
           -e KAFKA_ENABLE_TLS=false \
           ghcr.io/clemensv/real-time-sources-ndw-road-traffic:latest

# Azure Event Hubs
docker run -e CONNECTION_STRING="Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<key>;EntityPath=ndw-road-traffic" \
           ghcr.io/clemensv/real-time-sources-ndw-road-traffic:latest
```

## Event Types

All events are emitted as CloudEvents (structured JSON) to a single Kafka topic. The Kafka key format varies by message group:

| Group | Kafka Key Pattern | Event Types |
|-------|------------------|-------------|
| NL.NDW.AVG | `measurement-sites/{measurement_site_id}` | PointMeasurementSite, RouteMeasurementSite, TrafficObservation, TravelTimeObservation |
| NL.NDW.DRIP | `drips/{vms_controller_id}/{vms_index}` | DripSign, DripDisplayState |
| NL.NDW.MSI | `msi-signs/{sign_id}` | MsiSign, MsiDisplayState |
| NL.NDW.Situations | `situations/{situation_record_id}` | Roadwork, BridgeOpening, TemporaryClosure, TemporarySpeedLimit, SafetyRelatedMessage |

## Behavior

- **Reference data first**: At startup (and every hour), the bridge emits reference events for measurement sites, DRIP signs, and MSI signs before telemetry.
- **Telemetry polling**: Traffic speed, travel time, DRIP display states, and MSI display states are polled every `POLLING_INTERVAL` seconds.
- **Situations polling**: All 5 situation feeds are polled every 5 minutes.
- **Deduplication**: Events are deduplicated by site/sign ID and publication timestamp using a local state file.
- **Fault isolation**: A failure in one feed does not prevent other feeds from being processed.
