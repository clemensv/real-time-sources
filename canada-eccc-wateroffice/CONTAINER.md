# Canada ECCC Water Office Hydrometric Bridge — Container

## Source

Environment and Climate Change Canada (ECCC) Water Survey of Canada real-time hydrometric data via the OGC API Features service at `https://api.weather.gc.ca`.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes (feed mode) | Kafka or Azure Event Hubs connection string |
| `KAFKA_TOPIC` | No | Kafka topic name (default: `canada-eccc-wateroffice`) |
| `KAFKA_BROKER` | Alt to CONNECTION_STRING | Plain bootstrap server, e.g. `localhost:9092` |
| `KAFKA_ENABLE_TLS` | No | Set to `false` to disable TLS (default: `true`) |
| `POLLING_INTERVAL` | No | Observation polling interval in seconds (default: `300`) |

## Docker Pull & Run

```bash
docker pull ghcr.io/clemensv/real-time-sources/canada-eccc-wateroffice:latest

# Plain Kafka
docker run --rm \
  -e KAFKA_BROKER=broker:9092 \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/canada-eccc-wateroffice:latest

# Azure Event Hubs
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<key>;EntityPath=canada-eccc-wateroffice" \
  ghcr.io/clemensv/real-time-sources/canada-eccc-wateroffice:latest
```

## Kafka Output

| Property | Value |
|---|---|
| Default topic | `canada-eccc-wateroffice` |
| Kafka key format | `stations/{station_number}` |
| Content type | `application/cloudevents+json` |

## Event Types

| `CA.Gov.ECCC.Hydro.Station` | Station reference metadata |
| `CA.Gov.ECCC.Hydro.Observation` | Real-time water level / discharge |
