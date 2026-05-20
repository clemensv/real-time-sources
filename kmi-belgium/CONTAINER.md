# KMI Belgium Weather Observation Bridge — Container Deployment

## Upstream Source

The [KMI/RMI open data AWS service](https://opendata.meteo.be/service/aws/ows) provides free ten-minute automatic weather station observations for Belgium through an OGC WFS 2.0 endpoint. The bridge polls the `aws:aws_10min` feature type, extracts active stations from the latest observations, and emits CloudEvents into Kafka.

## Docker Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources/kmi-belgium:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | `kmi-belgium` | Target Kafka topic |
| `POLLING_INTERVAL` | No | `600` | Seconds between polling cycles |
| `STATE_FILE` | No | `~/.kmi_belgium_state.json` | Deduplication state file path |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |

## Docker Run (Plain Kafka)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=kmi-belgium" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/kmi-belgium:latest
```

## Docker Run (Azure Event Hubs)

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=kmi-belgium" \
  ghcr.io/clemensv/real-time-sources/kmi-belgium:latest
```

## Kafka Topics and Keys

| Topic | Key | Event Types |
|---|---|---|
| `kmi-belgium` | `{station_code}` | `BE.Gov.KMI.Weather.Station`, `BE.Gov.KMI.Weather.WeatherObservation` |

## Azure Container Instance

Deploy using the Azure CLI:

```bash
az container create \
  --resource-group <rg> \
  --name kmi-belgium \
  --image ghcr.io/clemensv/real-time-sources/kmi-belgium:latest \
  --environment-variables \
    CONNECTION_STRING="<connection-string>" \
  --restart-policy Always
```
