# GeoSphere Austria TAWES Weather Bridge — Container

This container bridges 10-minute weather observations from the
[GeoSphere Austria](https://geosphere.at) TAWES automatic station network
into Apache Kafka as CloudEvents.

## What It Does

The bridge polls the GeoSphere Austria TAWES v1 10-minute current dataset API
every 10 minutes (configurable) and emits two event types:

- **WeatherStation** — reference data for each active TAWES station (emitted
  at startup and refreshed daily)
- **WeatherObservation** — 10-minute telemetry: temperature, humidity,
  precipitation, wind direction, wind speed, pressure, sunshine duration,
  and global radiation

Events are [CloudEvents](https://cloudevents.io/) in structured JSON mode.
See [EVENTS.md](EVENTS.md) for the full event catalog.

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | **Yes** | — | Kafka or Event Hubs connection string |
| `POLLING_INTERVAL` | No | `600` | Seconds between observation polls |
| `STATION_REFRESH_INTERVAL` | No | `86400` | Seconds between station metadata refreshes |
| `STATE_FILE` | No | `geosphere_austria_state.json` | Path for dedup state file |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plain Kafka brokers |
| `KAFKA_TOPIC` | No | `geosphere-austria-tawes` | Kafka topic override |

## Docker Pull and Run

```bash
docker pull ghcr.io/clemensv/real-time-sources/geosphere-austria:latest
```

### Plain Kafka Broker

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=geosphere-austria-tawes" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/geosphere-austria:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=...;EntityPath=geosphere-austria-tawes" \
  ghcr.io/clemensv/real-time-sources/geosphere-austria:latest
```

### Microsoft Fabric Event Streams

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://....servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=..." \
  ghcr.io/clemensv/real-time-sources/geosphere-austria:latest
```

### State Persistence

Mount a volume to persist dedup state across container restarts:

```bash
docker run --rm \
  -v geosphere-state:/app/state \
  -e STATE_FILE=/app/state/geosphere_austria_state.json \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=geosphere-austria-tawes" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/geosphere-austria:latest
```

## Azure Container Instance

Use the provided `azure-template.json` to deploy as an Azure Container Instance.
