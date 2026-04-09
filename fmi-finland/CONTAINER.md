# FMI Finland Air Quality Bridge to Kafka, Event Hubs, and Fabric

This container image runs the FMI Finland air quality bridge. The bridge polls
the Finnish Meteorological Institute OGC WFS service for hourly air quality
observations, emits station reference data first, and then emits hourly
observation events as structured JSON CloudEvents. The event contract is
documented in [EVENTS.md](EVENTS.md).

## Upstream Source

- FMI OGC WFS 2.0 open data service
- No authentication required
- Hourly air quality observations for Finnish monitoring stations
- Station metadata from the `fmi::ef::stations` stored query

## Container Image

Pull the image from GitHub Container Registry:

```powershell
docker pull ghcr.io/clemensv/real-time-sources-fmi-finland:latest
```

## Running with Kafka

```powershell
docker run --rm `
  -e KAFKA_BOOTSTRAP_SERVERS=host.docker.internal:9092 `
  -e KAFKA_TOPIC=fmi-finland-airquality `
  -e POLLING_INTERVAL=3600 `
  ghcr.io/clemensv/real-time-sources-fmi-finland:latest
```

## Running with Azure Event Hubs or Fabric Event Streams

```powershell
docker run --rm `
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<name>;SharedAccessKey=<key>;EntityPath=fmi-finland-airquality" `
  -e POLLING_INTERVAL=3600 `
  ghcr.io/clemensv/real-time-sources-fmi-finland:latest
```

## Running with the repo Docker E2E Kafka convention

```powershell
docker run --rm `
  -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=fmi-finland-airquality" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-fmi-finland:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | No | Event Hubs style or plain Kafka connection string. If `EntityPath` is present, it becomes the topic unless `KAFKA_TOPIC` is set. |
| `KAFKA_BOOTSTRAP_SERVERS` | No | Explicit Kafka bootstrap servers. Use this for a plain Kafka broker without a connection string. |
| `KAFKA_TOPIC` | No | Kafka topic name. Defaults to `fmi-finland-airquality`. |
| `SASL_USERNAME` | No | Optional SASL username for direct Kafka connections. |
| `SASL_PASSWORD` | No | Optional SASL password for direct Kafka connections. |
| `POLLING_INTERVAL` | No | Polling interval in seconds. Default `3600`. |
| `STATION_REFRESH_INTERVAL` | No | Interval in seconds for re-emitting station reference data. Default `86400`. |
| `STATE_FILE` | No | Path to the JSON state file used for observation deduplication. |

## Persisting State

If you want the bridge to survive restarts without replaying the same
observation windows, mount a volume and point `STATE_FILE` at that location:

```powershell
docker run --rm `
  -v ${PWD}\state:C:\state `
  -e KAFKA_BOOTSTRAP_SERVERS=host.docker.internal:9092 `
  -e STATE_FILE=C:\state\fmi_finland_state.json `
  ghcr.io/clemensv/real-time-sources-fmi-finland:latest
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffmi-finland%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffmi-finland%2Fazure-template-with-eventhub.json)
