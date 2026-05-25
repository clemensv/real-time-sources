# EPA UV Bridge

## Overview

**EPA UV Bridge** polls the official US EPA Envirofacts UV Index web services and emits hourly and daily UV forecast events to Kafka, MQTT 5.0, and AMQP 1.0 as CloudEvents.

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

## Fabric notebook hosting

- This bridge can also be hosted as a scheduled Microsoft Fabric notebook. See `tools/deploy-fabric/deploy-feeder-notebook.ps1` and `epa-uv/notebook/epa-uv-feed.ipynb`.

## Upstream Links

- Docs: https://www.epa.gov/enviro/web-services
- Hourly city/state endpoint pattern: `https://data.epa.gov/dmapservice/getEnvirofactsUVHOURLY/CITY/{City}/STATE/{State}/JSON`
- Daily city/state endpoint pattern: `https://data.epa.gov/dmapservice/getEnvirofactsUVDAILY/CITY/{City}/STATE/{State}/JSON`

## Transports

This source now ships separate Kafka and MQTT containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-epa-uv-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variants for EPA UV Index forecasts. Topics are retained QoS-1 UV forecast leaves under uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/..., where {state} is lowercase US state, {city_slug} is lowercase kebab-case city, and {location_id} preserves the existing Kafka/CloudEvents entity id intentionally for subject/key compatibility even though it is derivable from state+city. Hourly slots use topic-safe {forecast_hour}=YYYYMMDDTHH; daily slots use {forecast_date}=YYYY-MM-DD. Message expiry bounds retained forecast slots so stale forecasts age out.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/epa_uv.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/hourly/{forecast_hour}` | `US.EPA.UVIndex.HourlyForecast` | QoS 1, retain=true, expiry=172800s |
| `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/daily/{forecast_date}` | `US.EPA.UVIndex.DailyForecast` | QoS 1, retain=true, expiry=1209600s |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.

## AMQP 1.0 companion feeder

This source now ships Kafka, MQTT, and AMQP 1.0 transport variants. The AMQP container (`ghcr.io/clemensv/real-time-sources-epa-uv-amqp:latest`) publishes the same CloudEvents payloads as the Kafka and MQTT feeders to a single broker address named `epa-uv` by default, using binary-mode AMQP 1.0 for generic brokers or Azure Service Bus.

Run locally against an AMQP 1.0 broker:

```bash
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=epa-uv \
  -e AMQP_USERNAME=admin \
  -e AMQP_PASSWORD=admin \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-epa-uv-amqp:latest
```

Deploy to Azure Service Bus with `azure-template-with-servicebus.json` (also mirrored at `infra/azure-template-amqp.json`). The template provisions a Service Bus queue, storage-backed state share, a user-assigned managed identity, and an Azure Container Instance configured for AMQP CBS / Entra ID authentication.

