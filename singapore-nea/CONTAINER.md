# Singapore NEA Weather — Container Deployment

## Upstream Source

The [data.gov.sg environment API](https://data.gov.sg/datasets?topics=environment)
provides free real-time weather data from Singapore's NEA station network.
Temperature updates every minute, rainfall every 5 minutes. Data is published
under the Singapore Open Data License.

## Docker Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources/singapore-nea:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | `singapore-nea` | Target Kafka topic |
| `POLLING_INTERVAL` | No | `300` | Seconds between polling cycles |
| `STATE_FILE` | No | `~/.singapore_nea_state.json` | Deduplication state file path |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |

## Docker Run (Plain Kafka)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=singapore-nea" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/singapore-nea:latest
```

## Docker Run (Azure Event Hubs)

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=singapore-nea" \
  ghcr.io/clemensv/real-time-sources/singapore-nea:latest
```

## Kafka Topics and Keys

| Topic | Key | Event Types |
|---|---|---|
| `singapore-nea` | `{station_id}` | `SG.Gov.NEA.Weather.Station`, `SG.Gov.NEA.Weather.WeatherObservation` |
