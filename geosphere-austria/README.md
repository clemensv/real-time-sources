# GeoSphere Austria — TAWES Weather Observations

This bridge polls 10-minute weather observations from the
[GeoSphere Austria](https://geosphere.at) TAWES (Teilautomatische
Wetterstationen) automatic station network and emits them as CloudEvents
into Apache Kafka.

## Data Source

- **Provider:** GeoSphere Austria (formerly ZAMG)
- **API:** `https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min`
- **Protocol:** REST JSON (GeoJSON output)
- **Authentication:** None (open data, CC BY 4.0)
- **Update frequency:** Every 10 minutes
- **Coverage:** ~270 active TAWES stations across Austria

## Event Types

| Type | Description |
|---|---|
| `at.geosphere.tawes.WeatherStation` | Station reference data (location, elevation, state) |
| `at.geosphere.tawes.WeatherObservation` | 10-minute observation (temperature, humidity, wind, etc.) |

See [EVENTS.md](EVENTS.md) for the full schema documentation.

## Parameters

The bridge fetches these TAWES parameters:

| API Param | Field | Unit | Description |
|---|---|---|---|
| TL | temperature | °C | Air temperature |
| RF | humidity | % | Relative humidity |
| RR | precipitation | mm | 10-minute precipitation |
| DD | wind_direction | ° | Wind direction |
| FF | wind_speed | m/s | Wind speed |
| P | pressure | hPa | Atmospheric pressure |
| SO | sunshine_duration | s | Sunshine duration |
| GLOW | global_radiation | W/m² | Global radiation |

## Quick Start

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=geosphere-austria-tawes" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/geosphere-austria:latest
```

See [CONTAINER.md](CONTAINER.md) for full deployment instructions.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template-with-eventhub.json)
