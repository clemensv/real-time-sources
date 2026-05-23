# TfL Road Traffic Container

This container is a bridge between the [Transport for London (TfL) Unified API](https://api.tfl.gov.uk/) road traffic data and Apache Kafka endpoints. It polls the TfL Road API and emits road corridor reference data, corridor status telemetry, and disruption telemetry as CloudEvents.

The sibling MQTT image publishes binary-mode CloudEvents into a Unified Namespace topic tree. See [EVENTS.md](EVENTS.md) for the event schemas.

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
| `uk.gov.tfl.road.RoadDisruption` | `disruptions/{road_id}/{severity}/{disruption_id}/disruption` |

## MQTT 5.0 / Unified-Namespace Feeder

The MQTT image runs `python -m tfl_road_traffic_mqtt feed` and publishes binary-mode CloudEvents under:

```text
traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/{event}
traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/{severity}/{disruption_id}/disruption
```

Road status events use QoS 1 with `retain=true` for last-known-value reads. Disruption events use QoS 1 with `retain=false`; severity is one of `serious`, `severe`, `moderate`, `minor`, `information`, or `closure`.

Run it against a broker:

```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtt://broker:1883" \
  ghcr.io/clemensv/real-time-sources/tfl-road-traffic-mqtt:latest
```

### MQTT environment variables

| Variable | Required | Default | Description |
|---|---:|---|---|
| `MQTT_BROKER_URL` | yes | — | Broker URL such as `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_ENABLE_TLS` | no | scheme/port-derived | Force TLS when set to `true`. |
| `MQTT_AUTH_MODE` | no | `anonymous` | `anonymous`, `userpass`, `tls-cert`, or `entra`. |
| `MQTT_USERNAME` | conditional | — | Username for `userpass`; Event Grid client name for `entra`. |
| `MQTT_PASSWORD` | conditional | — | Password for `userpass`. |
| `MQTT_CLIENT_CERT` | conditional | — | Client certificate PEM path for `tls-cert`. |
| `MQTT_CLIENT_KEY` | conditional | — | Client key PEM path for `tls-cert`. |
| `MQTT_CA_FILE` | no | system trust | Broker CA chain path. |
| `MQTT_CLIENT_ID` | no | `tfl-road-traffic-mqtt` | MQTT client identifier. |
| `MQTT_ENTRA_CLIENT_ID` | conditional | — | Managed identity client id for Event Grid Namespace MQTT enhanced auth. |
| `MQTT_ENTRA_AUDIENCE` | no | `https://eventgrid.azure.net/` | Entra token audience. |
| `TFL_ROAD_TRAFFIC_MQTT_EMIT_MOCK_CORPUS` | no | `false` | Emit synthetic one-shot corpus for Docker E2E tests. |

### MQTT subscription examples

- All TfL road traffic messages: `traffic/gb/tfl/tfl-road-traffic/#`
- Latest retained status for every TfL road: `traffic/gb/tfl/tfl-road-traffic/roads/+/status`
- All disruptions for A2: `traffic/gb/tfl/tfl-road-traffic/disruptions/a2/+/+/disruption`
- All severe disruptions: `traffic/gb/tfl/tfl-road-traffic/disruptions/+/severe/+/disruption`
- All closure disruptions: `traffic/gb/tfl/tfl-road-traffic/disruptions/+/closure/+/disruption`

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
