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

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template-with-eventhub.json)
