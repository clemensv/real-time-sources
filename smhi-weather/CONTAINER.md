# SMHI Weather Observation Bridge — Container Deployment

## Upstream Source

The [SMHI Open Data Meteorological Observations API](https://opendata.smhi.se/apidocs/metobs/)
provides free real-time weather observations from ~232 stations across
Sweden. Data is published under CC BY 4.0 and refreshed hourly. The bridge
polls the latest-hour bulk endpoints for six parameters (temperature, wind
gust, dew point, pressure, humidity, precipitation), merges them per
station, and emits CloudEvents into Kafka.

## Docker Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources/smhi-weather:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | `smhi-weather` | Target Kafka topic |
| `POLLING_INTERVAL` | No | `900` | Seconds between polling cycles |
| `STATE_FILE` | No | `~/.smhi_weather_state.json` | Deduplication state file path |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |

## Docker Run (Plain Kafka)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=smhi-weather" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/smhi-weather:latest
```

## Docker Run (Azure Event Hubs)

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=smhi-weather" \
  ghcr.io/clemensv/real-time-sources/smhi-weather:latest
```

## Kafka Topics and Keys

| Topic | Key | Event Types |
|---|---|---|
| `smhi-weather` | `{station_id}` | `SE.Gov.SMHI.Weather.Station`, `SE.Gov.SMHI.Weather.WeatherObservation` |

## Azure Container Instance

Deploy using the Azure CLI:

```bash
az container create \
  --resource-group <rg> \
  --name smhi-weather \
  --image ghcr.io/clemensv/real-time-sources/smhi-weather:latest \
  --environment-variables \
    CONNECTION_STRING="<connection-string>" \
  --restart-policy Always
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template-with-eventhub.json)
