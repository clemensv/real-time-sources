# HKO Hong Kong Weather Observation Bridge

This bridge fetches real-time weather observations from the
[Hong Kong Observatory (HKO)](https://www.hko.gov.hk/en/abouthko/opendata_intro.htm)
and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

## Data Model

The bridge emits two event types into the `hko-hong-kong` topic, keyed by
`{place_id}` (a URL-safe slug of the English place name):

| Event Type | Description |
|---|---|
| `HK.Gov.HKO.Weather.Station` | Reference data for each place (emitted at startup) |
| `HK.Gov.HKO.Weather.WeatherObservation` | Current observations: temperature, rainfall, humidity, UV index |

## Upstream API

- **Base URL**: `https://data.weather.gov.hk/weatherAPI/opendata/weather.php`
- **Auth**: None (fully open, HK Open Government Data License)
- **Rate limit**: Fair use — the bridge polls every 10 minutes by default
- **Coverage**: 27 temperature stations, 18 rainfall districts, 1 humidity station (HKO HQ), 1 UV station (King's Park)
- **Endpoint**: `?dataType=rhrread&lang=en` — Regional Weather in Hong Kong

## Source Files

| File | Description |
|---|---|
| [xreg/hko_hong_kong.xreg.json](xreg/hko_hong_kong.xreg.json) | xRegistry manifest |
| [hko_hong_kong/hko_hong_kong.py](hko_hong_kong/hko_hong_kong.py) | Runtime bridge |
| [hko_hong_kong_producer/](hko_hong_kong_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |

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

### Option 3: Fabric notebook hosting

Run this feeder as a scheduled Microsoft Fabric notebook (no container required) via
[`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1),
which uploads [`notebook/hko-hong-kong-feed.ipynb`](notebook/hko-hong-kong-feed.ipynb) and binds it to a Lakehouse, KQL database, and Event Stream in your Fabric workspace.

## MQTT and AMQP companion transports

This source now ships Kafka plus dedicated MQTT and AMQP companion containers. MQTT publishes binary-mode CloudEvents into the source-specific UNS topic tree declared in `xreg/`; AMQP publishes the same CloudEvents to the configured queue or topic address (`hko-hong-kong`). Docker E2E mock mode is available through `HKO_HONG_KONG_MOCK=true`.

- MQTT image: `ghcr.io/clemensv/real-time-sources/hko-hong-kong-mqtt`
- AMQP image: `ghcr.io/clemensv/real-time-sources/hko-hong-kong-amqp`
- MQTT templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`
- AMQP templates: `azure-template-amqp.json`, `azure-template-with-servicebus.json`
