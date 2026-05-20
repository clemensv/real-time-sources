# NWS Forecast Zones Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container polls NWS forecast-zone products and emits zone reference data plus current land and marine forecast snapshots as CloudEvents.

## What it does

- fetches configured zone metadata from `api.weather.gov`
- fetches land-zone forecasts for public forecast zones
- fetches marine bulletin text for marine zones
- emits all events with Kafka key and CloudEvent subject equal to `zone_id`

## Container image

```shell
docker pull ghcr.io/clemensv/real-time-sources-nws-forecasts:latest
```

## Environment variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric connection string or `BootstrapServer=...;EntityPath=...` string |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers when not using `CONNECTION_STRING` |
| `KAFKA_TOPIC` | Kafka topic when not using `EntityPath` |
| `KAFKA_ENABLE_TLS` | `true` by default; set `false` for plain local Kafka |
| `SASL_USERNAME` | Optional SASL username for Kafka |
| `SASL_PASSWORD` | Optional SASL password for Kafka |
| `NWS_FORECAST_ZONES` | Comma-separated zone IDs |
| `NWS_FORECAST_STATE_FILE` | Persistent forecast dedupe state path |
| `NWS_FORECAST_POLL_INTERVAL_SECONDS` | Forecast polling interval |
| `NWS_FORECAST_REFERENCE_REFRESH_SECONDS` | Zone metadata refresh interval |

## Run with local Kafka

```shell
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=nws-forecasts" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-nws-forecasts:latest
```

## Run with Fabric Event Streams or Event Hubs

```shell
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-nws-forecasts:latest
```

## Persisting state

```shell
docker run --rm \
  -v /path/to/state:/mnt/fileshare \
  -e NWS_FORECAST_STATE_FILE=/mnt/fileshare/nws_forecasts_state.json \
  -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=nws-forecasts" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-nws-forecasts:latest
```
