# BOM Australia Weather Observations

Real-time weather observations from the [Australian Bureau of Meteorology](http://www.bom.gov.au/) (BOM).

## Data Model

The bridge emits two event types:

- **Station** (reference) — station metadata including WMO ID, name, state, coordinates.
- **WeatherObservation** (telemetry) — half-hourly surface observations covering temperature, wind, pressure, humidity, rainfall, cloud cover, visibility, and sea state.

Observations are keyed by WMO station number (`station_wmo`).

## Upstream API

BOM publishes 72-hour observation products per station as anonymous JSON:

```
http://reg.bom.gov.au/fwo/{product_id}/{product_id}.{wmo_id}.json
```

Product IDs follow the pattern `ID{state_letter}60901` for capital city observations. Each response contains ~48 half-hourly records with approximately 30 meteorological parameters per observation.

No authentication required. Data is Crown Copyright, free for non-commercial use.

## Default Station Coverage

The bridge ships with a default catalog covering all Australian state/territory capital airports:

| Station | WMO | State |
|---------|-----|-------|
| Sydney Airport | 94767 | NSW |
| Melbourne Airport | 94866 | VIC |
| Brisbane Airport | 94576 | QLD |
| Perth Airport | 94610 | WA |
| Adelaide (West Terrace) | 94648 | SA |
| Hobart Airport | 94970 | TAS |
| Darwin Airport | 94120 | NT |
| Canberra Airport | 94926 | ACT |

Additional stations can be configured via the `BOM_STATIONS` environment variable using `product_id:wmo_id` pairs.

## Links

- [BOM Data Feeds](http://www.bom.gov.au/catalogue/data-feeds.shtml)
- [72-hour Observation Products User Guide](https://www.bom.gov.au/catalogue/72_hr_historical_obs.pdf)

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template-with-eventhub.json)
