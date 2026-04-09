# Canada AQHI Bridge

This source bridges the Canadian Air Quality Health Index (AQHI) program from
Environment and Climate Change Canada into Kafka as structured JSON
[CloudEvents](https://cloudevents.io/).

## What it emits

The bridge emits three event types on one Kafka topic:

- `ca.gc.weather.aqhi.Community` reference events for AQHI reporting communities
- `ca.gc.weather.aqhi.Observation` events for current AQHI observations
- `ca.gc.weather.aqhi.Forecast` events for the four standard public forecast periods

The event contract is documented in [EVENTS.md](EVENTS.md).

## Upstream review and source choice

The AQHI program exposes several real-time and near-real-time channels:

| Family | Transport | Identity | Decision |
|---|---|---|---|
| Current observations by community | XML `.../observation/realtime/xml/AQ_OBS_<CGNDB>_CURRENT.xml` | CGNDB community code | Keep |
| Public forecasts by community | XML `.../forecast/realtime/xml/AQ_FCST_<CGNDB>_CURRENT.xml` | CGNDB community code | Keep |
| Community reference catalog | `aqhi_community.geojson` | CGNDB community code | Keep |
| Station/feed catalog | `aqhi_station.geojson` | CGNDB community code | Keep |
| Region-wide observation CSV matrices | Datamart CSV | Region + CGNDB columns | Drop as duplicate presentation |
| Region-wide model forecast CSV matrices | Datamart CSV | Region + CGNDB rows | Drop as duplicate presentation for this contract |
| GeoJSON observation items | OGC API / HPFX GeoJSON | Community code | Drop as duplicate presentation |
| GeoJSON forecast items | OGC API / HPFX GeoJSON | Community code | Drop as duplicate presentation |

I picked the XML current feeds plus the official GeoJSON reference catalogs
because they are community-keyed already, which keeps the bridge and the event
contract simple. The richer CSV and OGC variants are useful, but they are
alternate presentations of the same AQHI communities and forecast content for
this source.

## Stable identity model

The upstream stable identifier is the five-character CGNDB community code. The
current repo contract still keys the stream by `{province}/{community_name}`, so
the payload carries both that public community identity and the upstream
`cgndb_code` used to join back to the official AQHI metadata.

## Runtime behavior

- Fetches reference data from the official AQHI community and station GeoJSON feeds
- Uses AQHI feed-region partitions to avoid irrelevant province lookups when the
  run is scoped to a subset such as `PROVINCES=ON`
- Rewrites catalog XML feed links onto the live `https://dd.weather.gc.ca/today/air_quality/aqhi/...`
  base before polling, because the GeoJSON catalog still publishes legacy `http://.../air_quality/...`
  paths that return 404
- Resolves ambiguous multi-province regions through Natural Resources Canada’s
  geolocation service and caches the result in the state file
- Emits community reference data first
- Polls current AQHI observations and public forecasts every hour by default
- Deduplicates observations by community and observation timestamp
- Deduplicates forecasts by community, publication time, and forecast period
- Refreshes reference data every 24 hours by default

## Installation

```powershell
cd C:\git\real-time-sources\canada-aqhi
pip install .\canada_aqhi_producer\canada_aqhi_producer_data
pip install .\canada_aqhi_producer\canada_aqhi_producer_kafka_producer
pip install -e .
```

## Usage

List communities:

```powershell
python -m canada_aqhi list --provinces NL,NS,ON
```

Start the bridge:

```powershell
python -m canada_aqhi feed --connection-string "BootstrapServer=localhost:9092;EntityPath=canada-aqhi" --polling-interval 3600
```

## Environment variables

- `CONNECTION_STRING`
- `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_TOPIC`
- `SASL_USERNAME`
- `SASL_PASSWORD`
- `KAFKA_ENABLE_TLS`
- `POLLING_INTERVAL`
- `REFERENCE_REFRESH_INTERVAL`
- `STATE_FILE`
- `PROVINCES`

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
