# Copernicus Atmosphere Monitoring Service (CAMS) Global Air Quality Forecast

- **Country/Region**: Global
- **Endpoint**: `https://ads.atmosphere.copernicus.eu/api/v2`
- **Protocol**: CDS API (HTTP REST + Python client)
- **Auth**: Free API key (ADS account required)
- **Format**: GRIB2 / NetCDF
- **Freshness**: Twice daily (00Z, 12Z runs), 5-day forecast, hourly time steps
- **Docs**: https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts
- **Score**: 12/18

## Overview

CAMS (Copernicus Atmosphere Monitoring Service) Global Forecast is the world's leading
operational air quality and atmospheric composition prediction system. Operated by ECMWF,
it delivers **twice-daily** 5-day forecasts of:

- **Gases**: O₃, NO₂, SO₂, CO, HCHO, PM2.5, PM10
- **Aerosols**: dust, sea salt, organic matter, black carbon, sulfate
- **Greenhouse gases**: CO₂, CH₄ (separate product)
- **Meteorology**: temperature, wind, pressure, humidity

The forecast assimilates satellite observations (including Sentinel-5P TROPOMI) and runs
on ECMWF's Integrated Forecasting System (IFS) at ~40km global resolution (0.4° grid).
Hourly time steps from analysis time to +120 hours.

CAMS is used by:
- National meteorological services for air quality alerts
- Health agencies for pollution exposure warnings
- Aviation for volcanic ash avoidance
- Energy sector for solar power forecasting
- Climate researchers for model evaluation

Unlike raw Sentinel-5P pixels, CAMS provides gap-free global grids with vertical profiles
and multi-day forecasts.

## Endpoint Analysis

CAMS data is distributed via the **Atmosphere Data Store (ADS)**, which uses the CDS API
(Climate Data Store API client). Users must:

1. Register for a free ADS account at https://ads.atmosphere.copernicus.eu/
2. Install the Python CDS API client: `pip install cdsapi`
3. Configure `~/.cdsapirc` with API key
4. Submit data requests via Python or REST

The API is **asynchronous**: requests are queued, processed server-side, and downloaded
when ready. Typical wait time: 5–30 minutes for a single forecast time step.

**Example API request** (Python):

```python
import cdsapi

client = cdsapi.Client()

client.retrieve(
    'cams-global-atmospheric-composition-forecasts',
    {
        'date': '2026-01-15/2026-01-15',
        'time': '00:00',
        'leadtime_hour': ['0', '6', '12', '18', '24'],
        'variable': ['nitrogen_dioxide', 'ozone', 'particulate_matter_2.5um'],
        'type': 'forecast',
        'format': 'netcdf',
        'area': [60, -10, 35, 40],  # North, West, South, East (Europe)
    },
    'cams_forecast.nc'
)
```

The ADS API does **not** support live streaming or incremental polling. Each request
downloads a complete NetCDF or GRIB2 file (1–500 MB depending on spatial/temporal extent).

**Alternative: WMS for visualization** (not data extraction):
```
https://ads.atmosphere.copernicus.eu/api/wms/cams-global-atmospheric-composition-forecasts
```

WMS provides PNG map tiles but not machine-readable concentration values.

## Schema / Sample Payload

NetCDF output contains:
- **Dimensions**: `time`, `level` (pressure or model levels), `latitude`, `longitude`
- **Variables**: `no2`, `o3`, `pm2p5` (μg/m³ for PM, mol/mol for gases)
- **Attributes**: forecast reference time, valid time, model version, units

Example NetCDF structure:

```
netcdf cams_forecast {
dimensions:
    time = 5 ;
    level = 60 ;
    latitude = 451 ;
    longitude = 900 ;
variables:
    float no2(time, level, latitude, longitude) ;
        no2:units = "kg kg**-1" ;
        no2:long_name = "Nitrogen dioxide" ;
    float o3(time, level, latitude, longitude) ;
        o3:units = "kg kg**-1" ;
        o3:long_name = "Ozone" ;
    double time(time) ;
        time:units = "hours since 1900-01-01 00:00:00.0" ;
```

Surface-level (model level 60 or ~10m altitude) concentrations are most relevant for
air quality applications.

## Why Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Value** | 3 | Global air quality forecasts used operationally by health agencies, governments, and industry. Scientifically authoritative (ECMWF). |
| **Freshness** | 2 | Twice daily (00Z, 12Z), hourly forecast steps. Not sub-hourly but sufficient for air quality alerts. |
| **Openness** | 2 | Free API key with account registration. No usage fees, but quota limits (unclear enforcement). |
| **Schema clarity** | 3 | NetCDF-4 with CF conventions, GRIB2 with ECMWF parameter IDs. Fully documented. |
| **Machine-readability** | 1 | **Asynchronous download API**, not streaming. Must poll for job completion, then fetch file. Not REST-friendly for real-time bridges. |
| **Repo fit** | 1 | **Grid data**, not point observations. Each forecast is a global 451×900 grid. Modeling as CloudEvents requires either: (a) one event per grid cell per hour = millions/day, or (b) one "forecast-available" notification per run = 2 events/day. Neither fits the repo's station/stream pattern. |

**Total: 12/18** — High scientific value, but **poor API fit** for real-time streaming.

## Integration Notes

### Challenge: Asynchronous Bulk Downloads

The CDS API is designed for **batch data retrieval**, not streaming. A typical workflow:

1. Submit request (returns request ID)
2. Poll for completion (5–30 minutes)
3. Download NetCDF/GRIB2 file (1–500 MB)
4. Parse locally

This is incompatible with sub-minute polling bridges. A CAMS bridge would need to:

- Run twice daily (after 00Z and 12Z forecast completion, ~03:00 and 15:00 UTC)
- Download the latest forecast NetCDF
- Extract surface-level NO₂, O₃, PM2.5 for key grid cells or regions
- Emit one CloudEvent per region/pollutant/timestep

### Event Model Option 1: Forecast Notification

Emit one event per forecast run:

- **Subject**: `forecast/cams/global/{forecast_base_time}`
- **Kafka key**: `{forecast_base_time}` (e.g., `2026-01-15T00:00:00Z`)
- **Payload**: Metadata (run time, variables, spatial extent) + NetCDF S3 URL
- **Type**: `eu.copernicus.cams.forecast.available`

Consumers fetch and process the NetCDF themselves. This is a **data-notification pattern**,
not a data stream.

### Event Model Option 2: Regional Aggregates

Extract city-level or country-level average concentrations and emit per region:

- **Subject**: `airquality/{country_code}/{city}` (e.g., `airquality/FR/Paris`)
- **Kafka key**: `{country_code}:{city}`
- **Payload**: Hourly NO₂, O₃, PM2.5 forecast array (120 hours × 3 pollutants)
- **Type**: `eu.copernicus.cams.forecast.regional`

This requires pre-defining regions of interest (e.g., 100 European cities) and spatially
averaging the CAMS grid. More useful for downstream consumers but requires manual region
curation.

### Preferred Approach

**Hybrid**: Emit one **forecast-available** event per run with NetCDF URL, plus extract
concentrations for a curated list of ~200 global cities and emit those as time-series
events. This balances bulk-data access with direct consumability.

## Limitations

- **Asynchronous API** — not designed for real-time polling
- **Bulk downloads** — minimum viable request is 1 forecast step (10+ MB), not incremental
- **API quota** — ADS enforces undocumented rate limits; heavy polling may trigger blocks
- **Grid data** — not point observations; requires spatial interpolation or aggregation
- **Model, not obs** — CAMS is a forecast/analysis, not raw measurements. Inherits model biases.
- **Latency** — 00Z forecast available ~03:00 UTC, 12Z forecast ~15:00 UTC (3-hour delay)
- **No WebSocket/SSE** — pull-only API

## Alternative: CAMS European Air Quality

For **higher resolution** over Europe, consider:

`cams-europe-air-quality-forecasts` (0.1° / ~10km, same ADS API)

Covers Europe only but provides:
- Ensemble forecasts (11 members)
- Higher spatial detail
- Same pollution species

Same API limitations apply.

## Why It Matters

CAMS is the atmospheric component of Copernicus and the backbone of European air quality
forecasting. It powers:

- **EPA AirNow** (US) — CAMS dust forecasts for Southwest
- **Copernicus Emergency** — volcanic ash and wildfire smoke tracking
- **WHO air quality** — exposure estimates for health impact studies
- **Solar energy** — aerosol optical depth for PV output forecasting

CAMS assimilates Sentinel-5P TROPOMI, OMI, IASI, GOME-2, and ground station data into a
physically consistent 4D atmospheric state.

## Verdict

⚠️ **Maybe** — Scientifically critical and widely used, but the **asynchronous bulk-download
API** is a poor fit for real-time streaming architecture. Better suited to a **daily batch
job** that downloads forecasts and publishes to object storage (S3), with lightweight
CloudEvents notifications pointing to the NetCDF files. **Build** only if the repo adopts
a "data-available notification" pattern for large scientific datasets.

**Alternative**: If the goal is **actual air quality measurements** (not forecasts), bridge
ground station networks like **EEA AirBase** or **OpenAQ** instead. Those provide real-time
PM2.5/NO₂/O₃ observations from thousands of stations.
