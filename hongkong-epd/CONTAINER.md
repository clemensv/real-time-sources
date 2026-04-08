# Hong Kong EPD AQHI — Container Deployment

## Upstream Source

The Hong Kong Environmental Protection Department publishes a public XML feed
with the past 24 hours of AQHI observations for 18 monitoring stations. This
bridge emits station reference data at startup and then publishes the latest
AQHI reading per station on each polling cycle.

## Docker Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources/hongkong-epd:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | `hongkong-epd-aqhi` | Target Kafka topic |
| `POLLING_INTERVAL` | No | `3600` | Seconds between polling cycles |
| `STATE_FILE` | No | `~/.hongkong_epd_state.json` | Deduplication state file path |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |

## Docker Run (Plain Kafka)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=hongkong-epd-aqhi" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/hongkong-epd:latest
```

## Docker Run (Azure Event Hubs)

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=hongkong-epd-aqhi" \
  ghcr.io/clemensv/real-time-sources/hongkong-epd:latest
```

## Kafka Topic and Keys

| Topic | Key | Event Types |
|---|---|---|
| `hongkong-epd-aqhi` | `{station_id}` | `HK.Gov.EPD.AQHI.Station`, `HK.Gov.EPD.AQHI.AQHIReading` |
