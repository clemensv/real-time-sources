# Environment Canada Weather Bridge — Container Deployment

## Upstream Source

The [Environment and Climate Change Canada (ECCC) GeoMet API](https://api.weather.gc.ca/)
provides free access to SWOB (Surface Weather Observation) data from ~963
stations across Canada via OGC API - Features. Data is published under the
Open Government Licence - Canada and refreshed hourly. The bridge fetches
station metadata from `swob-stations` and observations from `swob-realtime`,
extracts core weather parameters, and emits CloudEvents into Kafka.

## Docker Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources/environment-canada:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | `environment-canada` | Target Kafka topic |
| `POLLING_INTERVAL` | No | `900` | Seconds between polling cycles |
| `STATE_FILE` | No | `~/.environment_canada_state.json` | Deduplication state file path |
| `STATION_LIMIT` | No | `500` | Page size for station queries |
| `OBS_LIMIT` | No | `500` | Page size for observation queries |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |

## Docker Run (Plain Kafka)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=environment-canada" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/environment-canada:latest
```

## Docker Run (Azure Event Hubs)

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=environment-canada" \
  ghcr.io/clemensv/real-time-sources/environment-canada:latest
```

## Kafka Topics and Keys

| Topic | Key | Event Types |
|---|---|---|
| `environment-canada` | `{msc_id}` | `CA.Gov.ECCC.Weather.Station`, `CA.Gov.ECCC.Weather.WeatherObservation` |

## Azure Container Instance

```bash
az container create \
  --resource-group <rg> \
  --name environment-canada \
  --image ghcr.io/clemensv/real-time-sources/environment-canada:latest \
  --environment-variables \
    CONNECTION_STRING="<connection-string>" \
  --restart-policy Always
```
