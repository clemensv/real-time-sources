# Singapore NEA Weather and Air Quality — Container Deployment

## Upstream Source

The [data.gov.sg environment API](https://data.gov.sg/datasets?topics=environment)
provides free real-time weather and air quality data from Singapore's NEA.
The bridge emits weather station reference data plus observations, and a second
air-quality stream keyed by NEA's five reporting regions. Data is published
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
| `AIRQUALITY_TOPIC` | No | `singapore-nea-airquality` | Target Kafka topic for air quality events |
| `POLLING_INTERVAL` | No | `300` | Seconds between polling cycles |
| `AIRQUALITY_POLLING_INTERVAL` | No | `3600` | Seconds between air quality polling cycles |
| `STATE_FILE` | No | `~/.singapore_nea_state.json` | Deduplication state file path |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |

## Docker Run (Plain Kafka)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=singapore-nea" \
  -e AIRQUALITY_TOPIC=singapore-nea-airquality \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/singapore-nea:latest
```

## Docker Run (Azure Event Hubs)

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=singapore-nea" \
  -e AIRQUALITY_TOPIC=singapore-nea-airquality \
  ghcr.io/clemensv/real-time-sources/singapore-nea:latest
```

## Kafka Topics and Keys

| Topic | Key | Event Types |
|---|---|---|
| `singapore-nea` | `{station_id}` | `SG.Gov.NEA.Weather.Station`, `SG.Gov.NEA.Weather.WeatherObservation` |
| `singapore-nea-airquality` | `{region}` | `SG.Gov.NEA.AirQuality.Region`, `SG.Gov.NEA.AirQuality.PSIReading`, `SG.Gov.NEA.AirQuality.PM25Reading` |
