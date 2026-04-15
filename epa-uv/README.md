# EPA UV Bridge

## Overview

**EPA UV Bridge** polls the official US EPA Envirofacts UV Index web services and emits hourly and daily UV forecast events to Kafka as CloudEvents.

The upstream exposes four parameterized endpoints: hourly-by-city/state, hourly-by-ZIP, daily-by-city/state, and daily-by-ZIP. This bridge models the city/state family because the ZIP endpoints are duplicate parameterizations of the same products rather than distinct event families.

## Upstream Audit

| Family | Transport | Identity | Keep/Drop | Why |
|---|---|---|---|---|
| Hourly UV by city/state | REST JSON | `location_id + forecast_datetime` | Keep | Official hourly forecast product. |
| Daily UV by city/state | REST JSON | `location_id + forecast_date` | Keep | Official daily forecast product with alert flag. |
| Hourly UV by ZIP | REST JSON | same logical product | Drop | Duplicate presentation of hourly data. |
| Daily UV by ZIP | REST JSON | same logical product | Drop | Duplicate presentation of daily data. |
| UV widget pages/docs | HTML | n/a | Drop | Documentation/UI only. |

The API does not expose a separate location catalog or reference metadata feed, so this source emits forecast events only.

## Event Model

- **HourlyForecast** — one hourly UV forecast value for a configured city/state
- **DailyForecast** — one daily UV index and alert value for a configured city/state

## Configuration

The bridge is location-scoped. Configure one or more `CITY,STATE` pairs with `EPA_UV_LOCATIONS`.

Example:

```bash
EPA_UV_LOCATIONS="Seattle,WA;Portland,OR"
```

If no locations are provided, the bridge defaults to `Seattle,WA` so the container emits data out of the box.

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Kafka/Event Hubs/Fabric connection string |
| `EPA_UV_LOCATIONS` | Semicolon-separated `CITY,STATE` pairs |
| `EPA_UV_STATE_FILE` | State file path for dedupe |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fepa-uv%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fepa-uv%2Fazure-template-with-eventhub.json)

## Upstream Links

- Docs: https://www.epa.gov/enviro/web-services
- Hourly city/state endpoint pattern: `https://data.epa.gov/dmapservice/getEnvirofactsUVHOURLY/CITY/{City}/STATE/{State}/JSON`
- Daily city/state endpoint pattern: `https://data.epa.gov/dmapservice/getEnvirofactsUVDAILY/CITY/{City}/STATE/{State}/JSON`
