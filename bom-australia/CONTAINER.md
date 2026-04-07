# BOM Australia Weather Observations — Container

## Source

The [Australian Bureau of Meteorology](http://www.bom.gov.au/) publishes real-time surface weather observations
from automatic weather stations across Australia. Each station's observations are updated every 30 minutes and
include temperature, wind, pressure, humidity, rainfall, cloud cover, visibility, and sea state parameters.

This container polls configured BOM stations and emits the data as CloudEvents into Apache Kafka or Azure Event Hubs.
See [EVENTS.md](EVENTS.md) for the event catalog.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CONNECTION_STRING` | Yes | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | Override default topic `bom-australia` |
| `POLLING_INTERVAL` | No | Seconds between polls (default: 600) |
| `BOM_STATIONS` | No | Comma-separated `product_id:wmo_id` pairs |
| `KAFKA_ENABLE_TLS` | No | `false` to disable TLS (default: `true`) |

## Docker

```bash
docker pull ghcr.io/clemensv/real-time-sources/bom-australia:latest
```

### With a Kafka broker

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=kafka:9092;EntityPath=bom-australia" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/bom-australia:latest
```

### With Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=...;EntityPath=bom-australia" \
  ghcr.io/clemensv/real-time-sources/bom-australia:latest
```

### Custom station list

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=kafka:9092;EntityPath=bom-australia" \
  -e BOM_STATIONS="IDN60901:94767,IDV60901:94866,IDQ60901:94576" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/bom-australia:latest
```
