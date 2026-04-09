# Canada AQHI Bridge Container

This container bridges Canada’s Air Quality Health Index (AQHI) open data into
Apache Kafka, Azure Event Hubs, and Microsoft Fabric Event Streams as
structured JSON [CloudEvents](https://cloudevents.io/). The event contract is
documented in [EVENTS.md](EVENTS.md).

## Upstream source

The bridge reads:

- AQHI community metadata from ECCC GeoJSON catalogs
- Current AQHI observations from per-community XML feeds
- Public AQHI forecasts from per-community XML feeds

Reference data is emitted before telemetry, and refreshed periodically so
downstream consumers can keep a temporally consistent view of communities and
their AQHI readings.

## Pull the image

```powershell
docker pull ghcr.io/clemensv/real-time-sources-canada-aqhi:latest
```

## Run with plain Kafka

```powershell
docker run --rm `
  -e KAFKA_BOOTSTRAP_SERVERS='localhost:9092' `
  -e KAFKA_TOPIC='canada-aqhi' `
  -e KAFKA_ENABLE_TLS='false' `
  -e PROVINCES='NL,NS,ON' `
  ghcr.io/clemensv/real-time-sources-canada-aqhi:latest
```

## Run with Azure Event Hubs or Fabric Event Streams

```powershell
docker run --rm `
  -e CONNECTION_STRING='Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=canada-aqhi' `
  -e PROVINCES='AB,BC,MB,NB,NL,NS,NT,NU,ON,PE,QC,SK,YT' `
  ghcr.io/clemensv/real-time-sources-canada-aqhi:latest
```

## Environment variables

| Name | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | No | Event Hubs-style connection string. When set, it overrides direct Kafka settings. |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes, if `CONNECTION_STRING` is not set | Kafka bootstrap server list. |
| `KAFKA_TOPIC` | No | Kafka topic name. Defaults to `canada-aqhi`. |
| `SASL_USERNAME` | No | SASL PLAIN username for Kafka brokers. |
| `SASL_PASSWORD` | No | SASL PLAIN password for Kafka brokers. |
| `KAFKA_ENABLE_TLS` | No | Set to `false` for plain Kafka. Default is `true`. |
| `POLLING_INTERVAL` | No | Polling interval in seconds. Default is `3600`. |
| `REFERENCE_REFRESH_INTERVAL` | No | Reference refresh interval in seconds. Default is `86400`. |
| `STATE_FILE` | No | Path to the JSON dedupe and province-cache state file. |
| `PROVINCES` | No | Comma-separated province or territory codes to emit. Default is all 13 codes. |

## Azure Container Instances

If you want to run the bridge in Azure Container Instances, pass the same
environment variables you would use with `docker run`. The bridge is fully
configured through environment variables; there is no interactive setup and no
mounted configuration file requirement.

When `PROVINCES` narrows the run to a subset like `ON`, the bridge uses the AQHI
feed partition names to skip irrelevant province-resolution lookups and get to
first emission faster. Ambiguous multi-province regions are still resolved and
cached through the NRCan geolocation service.

The AQHI GeoJSON catalog still advertises legacy `http://dd.weather.gc.ca/air_quality/...`
XML links. The bridge rewrites those paths onto the live
`https://dd.weather.gc.ca/today/air_quality/aqhi/...` base before polling so
current observations and forecasts keep flowing.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-with-eventhub.json)
