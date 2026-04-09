# EPA UV Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container polls the official US EPA Envirofacts UV Index web services and emits hourly and daily UV forecast events to Kafka-compatible endpoints as CloudEvents JSON.

## Upstream

- **Publisher:** United States Environmental Protection Agency
- **Docs:** https://www.epa.gov/enviro/web-services
- **Products:** Hourly UV forecast and daily UV forecast/alert
- **Auth:** None
- **License:** US Government public data

## Behavior

The bridge polls the hourly and daily city/state UV forecast endpoints for one or more configured locations and deduplicates by `location_id + forecast time/date`. There is no separate upstream reference-data feed for locations, so the bridge emits forecast events only.

## Running the Container

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=epa-uv" \
  -e EPA_UV_LOCATIONS="Seattle,WA" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-epa-uv:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=epa-uv" \
  -e EPA_UV_LOCATIONS="Seattle,WA" \
  ghcr.io/clemensv/real-time-sources-epa-uv:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka/Event Hubs/Fabric connection string |
| `EPA_UV_LOCATIONS` | No | Semicolon-separated `CITY,STATE` pairs; default `Seattle,WA` |
| `KAFKA_ENABLE_TLS` | No | Set `false` for plain Kafka in local and Docker E2E runs |
| `EPA_UV_STATE_FILE` | No | Path to dedupe state; default `/mnt/fileshare/epa_uv_state.json` |
