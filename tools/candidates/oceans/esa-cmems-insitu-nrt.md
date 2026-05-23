# Copernicus Marine Service (CMEMS) Ocean Observations

- **Country/Region**: Global oceans
- **Endpoint**: `https://data.marine.copernicus.eu/products` (Copernicus Marine Data Store)
- **Protocol**: OPeNDAP, ERDDAP, FTP, S3
- **Auth**: Free account registration required
- **Format**: NetCDF, GRIB
- **Freshness**: Daily to hourly depending on product (NRT observations ~3-24 hours latency)
- **Docs**: https://marine.copernicus.eu/, https://help.marine.copernicus.eu/
- **Score**: 10/18

## Overview

Copernicus Marine Service (CMEMS), operated by Mercator Ocean International, provides
comprehensive ocean monitoring datasets including:

- **Sea surface temperature (SST)** — multi-satellite merged products, 0.05° resolution, daily
- **Sea level anomaly** — altimetry from Sentinel-3/6, Jason, SARAL, daily
- **Ocean color / chlorophyll-a** — Sentinel-3 OLCI, MODIS, VIIRS, daily
- **Sea ice extent/concentration** — SMOS, SSMIS, AMSR2, daily
- **Ocean currents** — surface velocities from altimetry/models, daily
- **Salinity** — SMOS, Aquarius, models
- **Wave height** — altimeter Hs, model forecasts
- **In-situ observations** — Argo floats, moorings, gliders (near-real-time)

CMEMS serves **three product types**:

1. **Near-Real-Time (NRT)** — observations within 3–24 hours, operational quality
2. **Multi-Year Product (MY)** — reprocessed historical data, scientific quality
3. **Forecasts** — 10-day ocean physics/biogeochem predictions, twice daily

The **NRT in-situ observation** products are the best fit for real-time bridging,
especially Argo floats and moored buoys.

## Endpoint Analysis

CMEMS replaced the legacy MOTU/FTP system with a new **Data Store** in 2023. Access methods:

1. **Copernicus Marine Toolbox** (Python client) — `pip install copernicusmarine`
2. **OPeNDAP** — DAP protocol for remote NetCDF access
3. **ERDDAP** — REST API with CSV/JSON output
4. **S3** — direct cloud object storage
5. **FTP** (legacy, being phased out)

The **Python toolbox** is the recommended method:

```python
import copernicusmarine

copernicusmarine.subset(
    dataset_id="cmems_obs-ins_glo_phybgcwav_mynrt_na_irr",  # Global in-situ NRT
    variables=["TEMP", "PSAL"],  # temperature, salinity
    minimum_longitude=-180,
    maximum_longitude=180,
    minimum_latitude=-90,
    maximum_latitude=90,
    start_datetime="2026-01-15T00:00:00",
    end_datetime="2026-01-15T23:59:59",
    output_filename="cmems_insitu_nrt.nc"
)
```

**ERDDAP endpoint** (for REST/JSON access):

```
https://erddap.marine.copernicus.eu/erddap/tabledap/
  cmems_obs-ins_glo_phybgcwav_mynrt_na_irr.json?
  time,latitude,longitude,TEMP,PSAL&
  time>=2026-01-15T00:00:00Z&time<=2026-01-15T23:59:59Z
```

Returns JSON array of observations from Argo floats, moorings, gliders, ships.

**Key NRT in-situ product**:

- `cmems_obs-ins_glo_phybgcwav_mynrt_na_irr` — Global NRT in-situ (irregular grid)
  - Sources: Argo floats, moored buoys, drifters, gliders, CTD casts
  - Parameters: temperature, salinity, currents, oxygen, chlorophyll, nutrients
  - Update frequency: **hourly** (Argo profiles uploaded as received)
  - Latency: 3–24 hours from observation

## Schema / Sample Payload

ERDDAP JSON output:

```json
{
  "table": {
    "columnNames": ["time", "latitude", "longitude", "depth", "TEMP", "PSAL", "platform_code"],
    "columnTypes": ["String", "float", "float", "float", "float", "float", "String"],
    "columnUnits": ["UTC", "degrees_north", "degrees_east", "meters", "degree_Celsius", "PSU", ""],
    "rows": [
      ["2026-01-15T12:34:56Z", 45.5, -30.2, 10.0, 18.3, 35.1, "6900123"],
      ["2026-01-15T12:34:56Z", 45.5, -30.2, 50.0, 17.8, 35.2, "6900123"],
      ...
    ]
  }
}
```

Fields:
- **time** — observation timestamp UTC
- **latitude, longitude** — position (degrees)
- **depth** — measurement depth (meters, positive down)
- **TEMP** — in-situ temperature (°C)
- **PSAL** — practical salinity (PSU)
- **platform_code** — unique platform ID (e.g., Argo float WMO number)

Argo floats provide vertical profiles (0–2000m depth, 10–50 measurements per profile).
Moorings provide time-series at fixed depths.

## Why Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Value** | 3 | Ocean observations are critical for climate, weather, fisheries, navigation, and marine ecosystems. CMEMS is the authoritative EU source. |
| **Freshness** | 2 | NRT products: hourly updates, 3–24 hour latency. Good for operational oceanography but not sub-hourly streaming. |
| **Openness** | 1 | **Free account required** with registration and acceptance of license terms. No usage fees but quota enforcement. |
| **Schema clarity** | 3 | NetCDF with CF conventions, ERDDAP standardized schema. Well-documented units, coordinates, QC flags. |
| **Machine-readability** | 2 | ERDDAP JSON/CSV is excellent. OPeNDAP and Python toolbox are well-supported. But no WebSocket/streaming API. |
| **Repo fit** | -1 | **Argo floats are mobile** — each float drifts 100–1000 km between profiles. WMO float ID is stable, but position changes every 10 days. Fits "vessel tracking" model (AIS) better than station model (river gauge). Moored buoys fit station model but are a small fraction of CMEMS in-situ data. |

**Total: 10/18** — Valuable dataset but **mobile platforms** (Argo) and **account requirement**
reduce fit.

## Integration Notes

### Argo Floats: Mobile Platform Model

Argo floats are autonomous drifting profilers. Each float:
- Surfaces every 10 days (configurable cycle time)
- Transmits its position + full vertical profile (T, S, sometimes O₂, pH, Chl-a)
- Drifts with currents between profiles

**Keying strategy**:
- **Subject**: `ocean/argo/{wmo_float_id}` (e.g., `ocean/argo/6900123`)
- **Kafka key**: `{wmo_float_id}` (stable 7-digit WMO identifier)
- **Payload**: Full profile (depth array + T/S/O2 arrays) + position + timestamp
- **Type**: `eu.copernicus.cmems.argo.profile`

This is analogous to **AIS vessel tracking** — stable entity ID, changing position.

### Moored Buoy: Station Model

Moored buoys (e.g., TAO/TRITON, PIRATA, RAMA tropical arrays) fit the station model:
- **Subject**: `ocean/buoy/{mooring_id}` (e.g., `ocean/buoy/TAO0N140W`)
- **Kafka key**: `{mooring_id}` (stable station code)
- **Payload**: Time-series observation (timestamp, depth, T, S)
- **Type**: `eu.copernicus.cmems.mooring.observation`

But moored buoys are a small subset (~500 globally) compared to 4,000+ Argo floats.

### Poll Strategy

Poll ERDDAP hourly for new observations:

```
time >= {last_poll_timestamp}
```

ERDDAP supports incremental queries. Filter by `platform_type` to separate Argo from moorings:

```
platform_type="drifting profiling float"  # Argo
platform_type="moored surface buoy"       # TAO/PIRATA/RAMA
```

### QC Filtering

CMEMS in-situ data includes **quality control flags**:
- `QC_FLAG = 1` — good data
- `QC_FLAG = 2` — probably good
- `QC_FLAG = 3` — bad data or missing QC
- `QC_FLAG = 4` — bad data

Emit only QC=1 or QC=2 observations to avoid sensor failures, biofouling, transmission errors.

## Limitations

- **Account required** — not open/anonymous access
- **Mobile platforms** — Argo floats drift; only moorings are fixed stations
- **Sparse coverage** — 4,000 Argo floats in global ocean = ~3° × 3° grid spacing on average
- **10-day cycle** — each Argo float profiles once per 10 days; not continuous time-series
- **No real-time streaming** — pull-based API, hourly poll at best
- **License restrictions** — CMEMS data has usage terms (attribution, non-commercial clauses in some products)
- **Bulk downloads** — NetCDF files can be 100+ MB for global daily products

## Why It Matters

CMEMS underpins:
- **Ocean forecasting** — ECMWF, Met Office, NOAA use CMEMS data assimilation
- **Climate monitoring** — Ocean heat content, sea level rise, marine heatwaves
- **Fisheries** — SST/chlorophyll for tuna, sardine, anchovy distribution
- **Shipping** — wave height, sea ice extent for route optimization
- **Oil/gas** — metocean conditions for offshore operations

Argo is the backbone of global ocean observing — 200,000+ profiles/year, sustained since 2000.

## Verdict

⚠️ **Maybe** — High scientific value but **account requirement**, **mobile platform complexity**
(Argo), and **sparse coverage** make it marginal for this repo. **Build** if:

1. Repo expands to cover **mobile platforms** (Argo = ocean analog of AIS vessels)
2. Focus on **moored buoys only** (TAO/PIRATA/RAMA = station model, but only ~500 globally)
3. Treat as **bulk-download + notification** (daily NetCDF file availability events)

**Alternative**: Bridge **national buoy networks** with open APIs instead:
- **NOAA NDBC** (already in repo) — 1,400+ buoys, no auth, REST API
- **UK Met Office marine** — moored buoys around UK
- **MeteoFrance buoys** — Mediterranean and Atlantic

These provide **fixed station IDs** and **no account requirements**, fitting the repo
pattern better than CMEMS.
