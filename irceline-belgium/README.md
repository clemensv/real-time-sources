# IRCELINE Belgium

This source bridges the IRCELINE Belgium 52°North SOS Timeseries API into Kafka as CloudEvents. It covers Belgium's interregional air-quality monitoring network and emits both reference data and hourly telemetry into a single topic.

## What it publishes

- Station reference events for the national monitoring network, currently about 137 stations in the live API
- Timeseries reference events for station × pollutant combinations, currently 678 expanded timeseries in the live API
- Observation events for hourly measurements, polled from the last two hours and deduplicated per timeseries

## Data families reviewed

| Family | Endpoint | Identity | Keep / drop | Reason |
|---|---|---|---|---|
| Stations | `GET /stations` | `station_id` | Keep | Station metadata is reference data for every observation and must be streamed, not fetched out-of-band. |
| Timeseries metadata | `GET /timeseries?expanded=true` and `GET /timeseries/{id}?expanded=true` | `timeseries_id` | Keep | This is the authoritative reference data for each emitted observation. It includes unit, station linkage, phenomenon, category, and optional `statusIntervals`. |
| Observations | `GET /timeseries/{id}/getData?timespan=...` | `timeseries_id` + observation timestamp | Keep | This is the hourly telemetry feed. |
| Phenomena catalog | `GET /phenomena` | `phenomenon.id` | Drop as standalone family | The live labels and identifiers are already present on expanded timeseries metadata. Emitting a separate catalog would duplicate the same reference data without adding new temporal context. |
| Categories catalog | `GET /categories` | `category.id` | Drop as standalone family | In the live API the categories mirror the phenomena set and are already carried on expanded timeseries metadata. |

## Upstream notes

- Base URL: `https://geo.irceline.be/sos/api/v1`
- Transport: REST over HTTPS
- Auth: none
- Update cadence: hourly observations
- Live payloads use GeoJSON coordinate order `[longitude, latitude, elevation]`; the third element is often the literal string `"NaN"` and is ignored
- Observation timestamps are Unix milliseconds and are normalized to ISO 8601 UTC strings

## BelAQI context

IRCELINE publishes optional `statusIntervals` arrays on expanded timeseries metadata. These threshold bands carry lower and upper limits, display labels, and colors. They are included on the `be.irceline.Timeseries` reference event so downstream consumers can interpret measurements in the same way the upstream service does.

## Event model

- `be.irceline.Station` — station reference data keyed by `{station_id}`
- `be.irceline.Timeseries` — timeseries reference data keyed by `{timeseries_id}`
- `be.irceline.Observation` — hourly observation telemetry keyed by `{timeseries_id}`

## Running locally

Generate the producer code first:

```powershell
.\generate_producer.ps1
pip install irceline_belgium_producer\irceline_belgium_producer_data
pip install irceline_belgium_producer\irceline_belgium_producer_kafka_producer
pip install -e .
```

Then start the bridge:

```powershell
python -m irceline_belgium feed --kafka-bootstrap-servers localhost:9092 --kafka-enable-tls false
```

## Upstream links

- API root: `https://geo.irceline.be/sos/api/v1`
- Stations: `https://geo.irceline.be/sos/api/v1/stations`
- Timeseries: `https://geo.irceline.be/sos/api/v1/timeseries`
- Phenomena: `https://geo.irceline.be/sos/api/v1/phenomena`

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template-with-eventhub.json)
