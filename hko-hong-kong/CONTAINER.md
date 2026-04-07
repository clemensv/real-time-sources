# HKO Hong Kong Weather — Container Deployment

## Upstream Source

The [HKO Open Data API](https://www.hko.gov.hk/en/abouthko/opendata_intro.htm)
provides free real-time weather data from Hong Kong. The bridge polls the
`rhrread` endpoint for temperature (27 stations), rainfall (18 districts),
humidity (HKO HQ), and UV index (King's Park). Data is published under the
Hong Kong Open Government Data License.

## Docker Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources/hko-hong-kong:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | `hko-hong-kong` | Target Kafka topic |
| `POLLING_INTERVAL` | No | `600` | Seconds between polling cycles |
| `STATE_FILE` | No | `~/.hko_hong_kong_state.json` | Deduplication state file path |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |

## Docker Run (Plain Kafka)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=hko-hong-kong" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/hko-hong-kong:latest
```

## Docker Run (Azure Event Hubs)

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=hko-hong-kong" \
  ghcr.io/clemensv/real-time-sources/hko-hong-kong:latest
```

## Kafka Topics and Keys

| Topic | Key | Event Types |
|---|---|---|
| `hko-hong-kong` | `{place_id}` | `HK.Gov.HKO.Weather.Station`, `HK.Gov.HKO.Weather.WeatherObservation` |
