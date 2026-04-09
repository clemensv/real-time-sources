# Seattle Street Closures Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container polls the City of Seattle's official **Street Closures** dataset and emits closure events to Kafka-compatible endpoints as CloudEvents JSON.

## Upstream

- **Publisher:** Seattle Department of Transportation
- **Dataset:** Street Closures
- **Dataset page:** https://data.seattle.gov/Built-Environment/Street-Closures/ium9-iqtc
- **API endpoint:** `https://data.seattle.gov/resource/ium9-iqtc.json`
- **Cadence:** Daily
- **Auth:** None
- **License:** Public Domain

## Behavior

The bridge fetches the full current snapshot of closure rows, derives a stable `closure_id` from permit and segment fields, and re-emits rows when their content changes. The upstream does not expose row-level update timestamps, so the bridge uses snapshot comparison instead of a cursor.

## Running the Container

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=seattle-street-closures" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-seattle-street-closures:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=seattle-street-closures" \
  ghcr.io/clemensv/real-time-sources-seattle-street-closures:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka/Event Hubs/Fabric connection string |
| `KAFKA_ENABLE_TLS` | No | Set `false` for plain Kafka in local and Docker E2E runs |
| `SEATTLE_STREET_CLOSURES_STATE_FILE` | No | Path to persisted snapshot state; default `/mnt/fileshare/seattle_street_closures_state.json` |
