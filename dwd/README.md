# DWD Open Data Bridge Usage Guide

## Overview

**DWD Open Data Bridge** polls the [Deutscher Wetterdienst (DWD) Climate Data
Center](https://opendata.dwd.de/) open-data file server for weather
observations, station metadata, and weather alerts from ~1,450 stations across
Germany. The data is forwarded to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format.

## Key Features

- **10-Minute Observations**: Air temperature, precipitation, wind, and solar
  radiation updated every 10 minutes from the DWD "now" dataset.
- **10-Minute Extremes** (optional): Extreme wind and extreme temperature
  datasets from the DWD 10-minute "now" directories.
- **Station Metadata**: Station list with coordinates, elevation, and state for
  all reporting stations.
- **Weather Alerts**: CAP (Common Alerting Protocol) weather alerts from the DWD
  warning system.
- **Hourly Observations** (optional): Recent hourly data including cloud cover.
- **Radar Product Feed** (optional): Radar product file metadata from
  `weather/radar/composite/`.
- **ICON-D2 Forecast Feed** (optional): ICON-D2 forecast file metadata from
  `weather/nwp/icon-d2/grib/`.
- **Modular Architecture**: Enable or disable individual data modules.
- **Kafka Integration**: Send data to Apache Kafka, Azure Event Hubs, or
  Microsoft Fabric Event Streams using SASL PLAIN authentication.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can
download Python from [here](https://www.python.org/downloads/) or from the
Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=dwd
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/dwd
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `dwd` command. It supports
several subcommands.

The events sent to Kafka are formatted as CloudEvents, documented in
[EVENTS.md](EVENTS.md).

### List Available Modules

```bash
dwd list-modules
```

Output:

```
  station_metadata          ON   poll=86400s
  station_obs_10min         ON   poll=600s
  station_obs_10min_extremes OFF poll=600s
  station_obs_hourly        OFF  poll=3600s
  weather_alerts            ON   poll=300s
  radar_products            OFF  poll=300s
  icon_d2_forecast          OFF  poll=300s
```

### Start the Feed

#### Using a Connection String (Event Hubs / Fabric Event Streams)

```bash
dwd feed --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
dwd feed \
    --kafka-bootstrap-servers "<bootstrap_servers>" \
    --kafka-topic "<topic_name>" \
    --sasl-username "<username>" \
    --sasl-password "<password>"
```

### Command-Line Arguments (feed)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `-c`, `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric Event Stream connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic name |
| `--sasl-username` | `SASL_USERNAME` | SASL PLAIN username |
| `--sasl-password` | `SASL_PASSWORD` | SASL PLAIN password |
| `-i`, `--polling-interval` | `POLLING_INTERVAL` | Global poll interval override (seconds) |
| `--state-file` | `STATE_FILE` | Path to state checkpoint file (default: `~/.dwd_state.json`) |
| `--modules` | `DWD_MODULES` | Comma-separated list of modules to enable |
| `--modules-disabled` | `DWD_MODULES_DISABLED` | Comma-separated list of modules to disable |
| `--10min-params` | `DWD_10MIN_PARAMS` | Comma-separated 10-min categories (default: air_temperature,precipitation,wind,solar) |
| `--stations` | `DWD_STATIONS` | Comma-separated station IDs to include (default: all) |
| `--base-url` | `DWD_BASE_URL` | DWD server base URL (default: `https://opendata.dwd.de`) |

### Examples

#### Poll Only Weather Alerts

```bash
dwd feed -c "<conn_string>" --modules weather_alerts
```

#### Poll Only Air Temperature for Specific Stations

```bash
dwd feed -c "<conn_string>" --modules station_obs_10min --10min-params air_temperature --stations 44,73,433
```

## Modules

### station_metadata (default: ON, poll: 3600s)

Fetches station lists from the DWD CDC station description files, merges them,
and emits a `StationMetadata` event for each station when changes are detected.
Covers ~1,450 stations across all 16 German states.

### station_obs_10min (default: ON, poll: 600s)

Polls the DWD 10-minute "now" datasets. Downloads ZIP archives containing
semicolon-delimited CSV files with recent observations. Tracks the latest
timestamp per station per category to emit only new measurements.

Categories: `air_temperature`, `precipitation`, `wind`, `solar`,
`extreme_wind`, `extreme_temperature`.

### station_obs_10min_extremes (default: OFF, poll: 600s)

Polls only the 10-minute extreme datasets and emits:

- `ExtremeWind10Min` (fields from `FX_10`, `FNX_10`, `DX_10`)
- `ExtremeTemperature10Min` (fields from `TX_10`, `TN_10`)

### station_obs_hourly (default: OFF, poll: 3600s)

Polls hourly "recent" datasets. Disabled by default because the data only
updates once per day and is not truly real-time.

### weather_alerts (default: ON, poll: 300s)

Downloads the LATEST CAP alert bundle from DWD, extracts individual XML alert
files, and emits new alerts. Tracks seen alert identifiers to avoid duplicates.

### radar_products (default: OFF, poll: 300s)

Polls DWD radar composite directories and emits:

- `RadarProductCatalog` (reference metadata per radar product directory)
- `RadarFileProduct` (metadata for new/updated radar files, including URL and
  last-modified timestamp)

### icon_d2_forecast (default: OFF, poll: 300s)

Polls DWD ICON-D2 forecast GRIB directories and emits:

- `ForecastModelCatalog` (reference metadata for the `icon-d2` model)
- `IconD2ForecastFile` (metadata for new/updated forecast files, including URL
  and parsed run/lead-time when available)

## Upstream Channel Inventory and Scope Decisions

The current extension pass audited the major DWD Open Data channel families and
applies the following keep/drop decisions:

| Family | Transport / Path | Identity | Cadence | Decision | Rationale |
|---|---|---|---|---|---|
| CDC station metadata | REST file (`.../10_minutes/*/now/*_Beschreibung_Stationen.txt`) | `station_id` | low-frequency updates | Keep (implemented) | Required reference data for station telemetry. |
| CDC 10-minute observations | REST file ZIP (`.../10_minutes/{air_temperature,precipitation,wind,solar}/now/`) | `station_id` | ~10 min | Keep (implemented) | Core near-real-time weather telemetry. |
| CDC 10-minute extremes | REST file ZIP (`.../10_minutes/{extreme_wind,extreme_temperature}/now/`) | `station_id` | ~10 min | Keep (implemented in this pass) | High-value near-real-time extremes. |
| CDC hourly observations | REST file ZIP (`.../hourly/*/recent/`) | `station_id` + parameter | hourly/daily refresh | Keep (optional module) | Useful enrichment; lower freshness so disabled by default. |
| Weather alerts (CAP) | REST ZIP (`weather/alerts/cap/.../LATEST...zip`) | `identifier` | minutes | Keep (implemented) | Operational severe-weather alerts. |
| ICON-D2 forecasts | REST file products (`weather/nwp/icon-d2/grib/`) | `file_url` | rolling | Keep (implemented, optional module) | Emits forecast file metadata events keyed by the file's absolute HTTPS URL. |
| Radar products | REST file products (`weather/radar/composite/`) | `file_url` | minutes | Keep (implemented, optional module) | Emits radar file metadata events keyed by the file's absolute HTTPS URL. |
| Satellite products | REST file products (`weather/satellite/`) | product + tile/area + validity time | minutes | Keep (next phase) | Distinct image/raster model and ingestion pattern. |

## Data Source

All data originates from the [DWD Open Data Server](https://opendata.dwd.de/)
which provides free access to weather and climate data under the
[GeoNutzV](https://www.gesetze-im-internet.de/geonutzv/) license.

## Fetching Referenced Files

Events from the `radar_products` and `icon_d2_forecast` modules carry a
`file_url` field that points at a file on `https://opendata.dwd.de/`. Every
such URL is publicly fetchable with an **unauthenticated HTTPS `GET`** — no
API key, token, signed URL, referer check, or cookie is required. The server
(nginx fronting an Apache autoindex) honours `Range` and
`If-Modified-Since`/`ETag`, so handlers can do conditional or partial fetches.
A typical consumer dereferences an event by issuing a plain `GET file_url`
and decoding the payload using the format conventions below.

### File payload formats

| Channel | URL pattern | Container | Payload format | What's inside |
|---|---|---|---|---|
| 10-minute observations | `…/10_minutes/{cat}/now/10minutenwerte_*_now.zip` | ZIP (single `.txt`) | Semicolon-delimited CSV, latin-1 | One row per 10-minute slot (last ~24 h) for one station. Header: `STATIONS_ID;MESS_DATUM;QN;…;eor`. Per-category columns: `air_temperature` → `PP_10,TT_10,TM5_10,RF_10,TD_10`; `precipitation` → `RWS_DAU_10,RWS_10,RWS_IND_10`; `wind` → `FF_10,DD_10`; `solar` → `DS_10,GS_10,SD_10,LS_10`; `extreme_wind` → `FX_10,FNX_10,DX_10`; `extreme_temperature` → `TX_10,TN_10,TX5_10,TN5_10`. `MESS_DATUM` is UTC `YYYYMMDDHHMM`; `-999` denotes missing. |
| Station description | `…/10_minutes/{cat}/now/zehn_now_{tu,rr,ff,st}_Beschreibung_Stationen.txt` | Plain text, latin-1 | Fixed-width table | One row per station: `Stations_id, von_datum, bis_datum, Stationshoehe (m), geoBreite, geoLaenge, Stationsname, Bundesland, Abgabe`. ~1,450 stations across all 16 German states. |
| CAP weather alerts | `weather/alerts/cap/COMMUNEUNION_DWD_STAT/Z_CAP_C_EDZW_*_PVW_STATUS_PREMIUMDWD_COMMUNEUNION_*.zip` | ZIP of XML | CAP 1.2 (`urn:oasis:names:tc:emergency:cap:1.2`) | One XML per alert. Each carries `identifier, sender (opendata@dwd.de), sent, status, msgType, references` plus one or more `<info>` blocks with `category=Met, event (e.g. BÖEN, GEWITTER), urgency, severity, certainty, effective/onset/expires, headline, description, instruction`, DWD `eventCode` extensions (`PROFILE_VERSION, LICENSE, II, GROUP, AREA_COLOR`) and `<area>` polygons in WGS84. The `…_LATEST_…_DE.zip` is a near-empty (~22 B) sentinel when no alerts are active; rolling timestamped bundles carry the actual content when alerts exist. |
| Radar composite (HDF5) | `weather/radar/composite/{dmax,hx,hymecng,rs,rv,vii,wn}/composite_*-hd5` | ODIM-H5 (HDF5, magic `\x89HDF\r\n\x1a\n`) | Gridded reflectivity / precipitation | OPERA ODIM_H5 layout: `/what` (object, version, source, date, time), `/where` (projection, LL/UR corners, xscale/yscale, xsize/ysize ≈ 1100×900 for the national composite), `/how`, and `/datasetN/data1/{data, what}` arrays (typically scaled int16 with `gain/offset/nodata/undetect`). Read with `h5py` or `wradlib`. |
| Radar composite (BUFR) | `weather/radar/composite/pg/PAAH21EDZW*.buf` | WMO BUFR (magic `BUFR`) | Binary BUFR message | DWD point/grid radar precipitation product. Decode with `eccodes`/`pdbufr`. Typically 30–40 KB. |
| Radar composite (binary) | `weather/radar/composite/hg/HG*.bz2` | bzip2-wrapped binary | DWD RADOLAN/HG grid | Decompress with `bz2`, then parse as DWD radar grid (header + scaled values). |
| ICON-D2 forecast | `weather/nwp/icon-d2/grib/<HH>/<param>/icon-d2_germany_<grid>_<level_type>_<run>_<lead>_<level>_<param>.grib2.bz2` | bzip2-wrapped GRIB2 (magic `GRIB`) | Single GRIB2 message | One parameter × one vertical level × one forecast lead hour for the ICON-D2 domain (~2 km, Germany + surroundings, ~650×750 grid). Section 1 reports WMO centre 78 (Offenbach) and the run reference time (e.g. `2026-05-17T00:00:00Z`). The file name carries all selectors: `run=YYYYMMDDHH`, `lead=000..048`, `level_type ∈ {single-level, model-level, pressure-level, time-invariant}`, `level` (model-level index, hPa, or surface tag), `parameter` (e.g. `t`, `u`, `v`, `qv`, `clc`, `tot_prec`, `clct`, `alb_rad`). Decompress with `bz2` and decode with `eccodes`/`pygrib`/`cfgrib`. |

Per-file sizes are typically well under 1 MB except for the larger HDF5 radar
composites (a few MB up to ~10 MB) and the per-directory `content.log.bz2`
catalog logs (multi-MB, not a payload — filter out if you walk directories
yourself rather than following `file_url` from events).

## Microsoft Fabric Integration

For a recommended end-to-end flow that lands the bridge's events into a
**Fabric Lakehouse** (bronze raw bytes + silver Delta) and renders the
results as **Fabric Maps** vector and imagery layers (including Cloud
Optimized GeoTIFFs from ICON‑D2 GRIB2 and radar composites), see
[FABRIC.md](FABRIC.md). It covers the Eventstream → Spark Notebook
destination (preview) wiring, per‑channel pipelines, idempotency,
scale, and ready‑to‑use Eventhouse KQL functions for map layers.

## Data Management

The bridge maintains a state file (default `~/.dwd_state.json`) to track:
- Last-seen timestamps per station per category (for deduplication)
- Seen alert identifiers (to avoid re-emitting active alerts)
- Directory listing timestamps (to skip unchanged directories)

This ensures the bridge only emits new data on each poll cycle.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-eventhub.json)
