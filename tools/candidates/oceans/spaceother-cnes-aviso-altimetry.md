# AVISO+ Satellite Altimetry Data Center (CNES)

- **Country/Region**: Global oceans
- **Endpoint**: `https://www.aviso.altimetry.fr/en/data.html` (data portal), FTP/HTTPS download
- **Protocol**: FTP, HTTPS, OpenDAP (THREDDS), Copernicus Marine Service API
- **Auth**: User registration required (free)
- **Format**: NetCDF, GeoTIFF, ASCII
- **Freshness**: Near-real-time (~3-6 hours for NRT products), delayed-mode (~15-30 days for reprocessed)
- **Docs**: https://www.aviso.altimetry.fr/, https://www.aviso.altimetry.fr/en/data/data-access.html
- **Score**: 13/18

## Overview

AVISO+ (Archiving, Validation and Interpretation of Satellite Oceanographic data) is the **French space agency (CNES) data center** for satellite ocean altimetry. It distributes sea surface height (SSH), significant wave height (SWH), wind speed, and ocean current data from **10+ altimetry missions**: Jason-3, Sentinel-3A/B, Sentinel-6 Michael Freilich, SARAL/AltiKa, Cryosat-2, and historical missions (TOPEX/Poseidon, Jason-1/2, Envisat, ERS-1/2).

The platform provides **multi-mission gridded products** (Level-3/4) that merge data from all active altimeters into consistent daily/weekly global ocean maps. These are used for ocean forecasting, climate monitoring, fisheries management, and maritime operations.

**Key products**:
- **SSH (Sea Surface Height)** — Daily global grids at 0.25° resolution, NRT and delayed-mode
- **SLA (Sea Level Anomaly)** — Deviation from mean sea level, critical for eddy detection and ocean circulation
- **SWH (Significant Wave Height)** — Wave field observations, used for maritime safety and offshore operations
- **Ocean currents (geostrophic velocities)** — Derived from SSH gradients
- **Along-track vs. gridded** — Along-track (L2) is raw satellite passes, gridded (L3/L4) is interpolated 2D maps

**NRT products** (3-6 hour latency):
- **DUACS NRT** — Multi-mission gridded SSH/SLA, updated daily
- **SSALTO/DUACS** — Along-track altimetry from Jason-3, Sentinel-3A/B, Sentinel-6

## Endpoint Analysis

**AVISO+ data portal verified** — Registration required for download access.

Data access methods:
1. **FTP server** — `ftp://ftp-access.aviso.altimetry.fr/` (requires login)
2. **HTTPS** — `https://tds.aviso.altimetry.fr/thredds/` (THREDDS catalog)
3. **OpenDAP** — Subset and download via OPeNDAP protocol
4. **Copernicus Marine Service** — AVISO products are also distributed via Copernicus (https://data.marine.copernicus.eu/)
5. **Python client** — `aviso+` Python package for programmatic access

**Registration**:
1. Create account at https://www.aviso.altimetry.fr/en/my-aviso-plus.html
2. Verify email and accept data policy
3. Receive FTP/HTTPS credentials

**Example: NRT gridded SSH (DUACS)**
- Product: `SEALEVEL_GLO_PHY_L4_NRT_008_046` (Copernicus ID)
- Resolution: 0.25° × 0.25° (~ 25km at equator)
- Cadence: Daily updates
- Latency: 3-6 hours after satellite overpass
- Format: NetCDF (CF-compliant)
- Variables: `adt` (absolute dynamic topography), `sla` (sea level anomaly), `ugos`/`vgos` (geostrophic currents), `err` (error estimates)

**Example: Along-track Jason-3 (L2)**
- Product: `JASON-3 GDR` (Geophysical Data Records)
- Cadence: Orbital repeat (9.9 days for full global coverage)
- Latency: NRT products ~3 hours, GDR (delayed-mode) ~15-30 days
- Format: NetCDF
- Variables: `ssh`, `swh`, `wind_speed`, `sigma0` (radar backscatter), `range_ku` (distance to sea surface)

**THREDDS catalog tested**:
```
GET https://tds.aviso.altimetry.fr/thredds/catalog.html
```

Returns HTML catalog browser with:
- DUACS multimission gridded products (daily, weekly, monthly)
- Along-track products by mission (Jason-3, Sentinel-3A/B, Sentinel-6, SARAL, Cryosat-2)
- Delayed-mode reprocessed products
- Geostrophic current products
- Wave height climatologies

**OpenDAP access**:
```
https://tds.aviso.altimetry.fr/thredds/dodsC/dataset-duacs-nrt-global-merged-allsat-phy-l4
```

Enables subset queries (time range, bbox, variable selection) without downloading full files.

## Schema/Sample

**NetCDF structure** (DUACS NRT gridded SSH):
```
dimensions:
  time = UNLIMITED (daily)
  latitude = 720 (0.25° grid, -89.875 to 89.875)
  longitude = 1440 (0.25° grid, -179.875 to 179.875)

variables:
  float adt(time, latitude, longitude)
    long_name = "Absolute Dynamic Topography"
    units = "m"
    standard_name = "sea_surface_height_above_geoid"
  
  float sla(time, latitude, longitude)
    long_name = "Sea Level Anomaly"
    units = "m"
    standard_name = "sea_surface_height_above_mean_sea_level"
  
  float ugos(time, latitude, longitude)
    long_name = "Absolute geostrophic velocity (zonal)"
    units = "m/s"
  
  float vgos(time, latitude, longitude)
    long_name = "Absolute geostrophic velocity (meridional)"
    units = "m/s"
  
  float err(time, latitude, longitude)
    long_name = "Error estimate of sea level anomaly"
    units = "m"

global attributes:
  title = "DT merged all satellites Global Ocean Gridded SSALTO/DUACS Sea Surface Height L4 product"
  source = "Jason-3, Sentinel-3A, Sentinel-3B, Sentinel-6A, HY-2B, Cryosat-2, SARAL/AltiKa"
  institution = "CLS, CNES"
  Conventions = "CF-1.6"
  time_coverage_start = "2024-01-15T00:00:00Z"
  time_coverage_end = "2024-01-15T23:59:59Z"
  geospatial_lat_min = -90.0
  geospatial_lat_max = 90.0
  geospatial_lon_min = -180.0
  geospatial_lon_max = 180.0
  processing_level = "4"
  product_version = "2.1"
```

**Stable identifiers**:
- **Gridded products** — keyed by `{date}` (e.g., `2024-01-15`)
- **Along-track products** — keyed by `{mission}/{cycle}/{pass}` (e.g., `jason-3/450/123`)

Both are suitable for Kafka keys.

## Why Strong

1. **Multi-mission fusion** — AVISO merges data from 5+ active altimeters (Jason-3, Sentinel-3A/B, Sentinel-6, Cryosat-2, SARAL) into **consistent daily global grids**. Single integration point for all ocean altimetry.
2. **NRT latency** — 3-6 hour delay is excellent for operational oceanography (ocean forecasting, eddy tracking, fisheries).
3. **Operational quality** — DUACS products are used by **Copernicus Marine Service**, weather agencies (ECMWF, NOAA), and navies worldwide. Battle-tested.
4. **Free for research/ops** — Registration is free. Data policy allows scientific, operational, and commercial use with attribution.
5. **Standard formats** — NetCDF CF-compliant, OpenDAP-accessible. Excellent for time-series analysis and geospatial tooling.

## Limitations

- **Registration required** — Not fully open (must create account and accept data policy). Barrier for automated deployments.
- **Grid resolution** — 0.25° (~25km) is coarse for coastal applications. Along-track data is higher resolution but sparse.
- **No STAC** — NetCDF files are CF-compliant but not STAC-indexed. Discovery requires THREDDS catalog parsing or Copernicus API.
- **FTP/THREDDS** — Not a modern REST API. Bridge must use FTP polling or OpenDAP (less friendly than STAC/JSON).
- **Delayed-mode lag** — Highest-quality reprocessed products (GDR) have 15-30 day latency. NRT products have larger error bars.
- **No raw L1 data** — AVISO distributes L2 (geophysical retrievals) and L3/L4 (gridded products). Raw altimeter waveforms (L1) are not available.

## Integration Notes

**Recommended bridge pattern**: **Daily NetCDF poller**

1. **Authentication** — Bridge requires AVISO+ credentials (`AVISO_USERNAME`, `AVISO_PASSWORD`).
2. **THREDDS catalog polling** — Query `https://tds.aviso.altimetry.fr/thredds/catalog.xml` daily to discover new DUACS NRT files.
3. **Delta detection** — Track latest `time_coverage_start` in persistent state (SQLite or Kafka compacted topic). Emit only new dates.
4. **NetCDF download** — Fetch files via HTTPS or OpenDAP subset (bbox filtering if only regional coverage needed).
5. **Message groups** — One group per product type:
   - `aviso_ssh_gridded` — keyed by `{date}` (e.g., `2024-01-15`)
   - Subject: `aviso/ssh-gridded/{date}`
   - Payload: NetCDF global attributes + OpenDAP URL + summary statistics (global mean SSH, SLA range, etc.)
6. **Reference data** — Emit mission metadata (Jason-3, Sentinel-3A/B, etc.) at startup (orbit parameters, sensor specs, data coverage).

**Why not emit full NetCDF grids?** Files are **large** (50-200MB per day). Kafka topics should carry **metadata + URLs**, not raw grids. Downstream consumers fetch NetCDF subsets via OpenDAP.

**Alternative**: For **Copernicus Marine integration**, use their MOTU/OPeNDAP API instead of AVISO FTP. Same data, but Copernicus has better API tooling (`copernicusmarine` Python package).

## Verdict

**STRONG ACCEPT** — This is a **Tier-1 ocean altimetry source** with **NRT latency** (3-6 hours), **multi-mission fusion** (Jason-3 + Sentinel-3A/B/6 + Cryosat-2 + SARAL), and **operational quality** (used by Copernicus Marine, weather agencies, navies). The **registration barrier** is minor (free account), and the **NetCDF/OpenDAP formats** are standard.

Recommended as the **primary ocean altimetry source** for the repo. Integrates 5+ altimetry missions in one bridge, avoiding the need for separate Jason-3, Sentinel-3, Sentinel-6 integrations.

Alternative: If **no registration** is acceptable, use **Copernicus Marine Service** (https://data.marine.copernicus.eu/) which redistributes AVISO products via a different portal (also requires free registration, but more API-friendly).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Multi-mission SSH/SLA/currents/waves, global daily grids |
| Freshness | 3 | NRT products 3-6h latency, delayed-mode 15-30d |
| Openness | 2 | Free registration required, data policy allows research/ops/commercial |
| Schema clarity | 3 | NetCDF CF-compliant, well-documented variables and metadata |
| Machine-readability | 2 | NetCDF, OpenDAP (not STAC/JSON, but standard geospatial formats) |
| Repo fit | 0 | FTP/THREDDS polling required (not REST/STAC), but excellent data |
