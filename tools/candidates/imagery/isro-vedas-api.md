# ISRO VEDAS API Centre (EO Data Services)

- **Country/Region**: India / National coverage
- **Endpoint**: https://vedas.sac.gov.in/vconsole (VEDAS API Centre)
- **Protocol**: WMS API (map tiles), Temporal API (NDVI time series)
- **Auth**: Registration required (API key)
- **Format**: WMS tiles (PNG/JPEG images), JSON (time series API)
- **Freshness**: Varies by product — Sentinel-2 (~5 days cloud-free composite), Resourcesat (~monthly)
- **Docs**: https://vedas.sac.gov.in/vconsole
- **Score**: 7/18

## Overview

VEDAS (Visualization of Earth Observation Data and Archival System) is ISRO's Earth observation data portal developed by the Space Applications Centre (SAC). In 2024-2025, VEDAS launched an **API Centre** (https://vedas.sac.gov.in/vconsole) providing programmatic access to select geospatial products.

**Two APIs currently available**:
1. **WMS API** — Web Map Service for satellite imagery (Sentinel-2 True Color / False Color Composite, Resourcesat AWIFS FCC)
2. **Temporal API** — NDVI time-series data for point locations or polygons

This is a **positive development** — VEDAS API Centre is ISRO's first documented public REST API for Earth observation data. However, it is **not a near-real-time satellite feed** — the data is primarily **archive and composite imagery**, not live sensor observations.

## Endpoint Analysis

**API Centre portal verified** — https://vedas.sac.gov.in/vconsole provides API documentation and registration.

**Registration**:
- Free registration required to obtain API key
- Email verification
- Approval timeline: likely faster than MOSDAC (this is a new initiative targeting developer access), but unknown

**WMS API**:
- **Sentinel-2 FCC/TCC** — False Color Composite and True Color Composite imagery
  - "View imagery for any specific date or instantaneous temporal composites over a desired timeframe"
  - **Temporal composite** — cloud-free mosaic over a date range (e.g., best available pixels over 1 month)
- **Resourcesat-2A AWIFS FCC** — False Color Composite from Indian satellite
  - 56 m resolution, 370 km swath, 5-day repeat
- **Request format**: WMS GetMap with bbox, date range, CRS

**Temporal API**:
- **NDVI time series** for point locations or polygons
- **Source**: Sentinel-2 (10 m resolution)
- Returns JSON with date-value pairs: `[{"date": "2023-05-01", "ndvi": 0.72}, ...]`
- Can calculate temporal metrics (mean, max, min) over a date range
- **Future expansion**: "More temporal datasets will be made available"

**Sample request** (hypothetical, based on description):
```
GET https://vedas.sac.gov.in/api/wms?
  service=WMS&version=1.3.0&request=GetMap&
  layers=sentinel2_fcc&
  bbox=77.0,28.0,77.5,28.5&
  width=512&height=512&
  crs=EPSG:4326&
  time=2023-05-01/2023-05-31&
  format=image/png&
  api_key=YOUR_API_KEY
```

**Freshness**:
- **Sentinel-2** — ESA mission, 5-day global revisit. VEDAS likely ingests Sentinel-2 L2A (atmospherically corrected) from ESA Copernicus Open Access Hub.
- **Temporal composites** — by definition, composites are **not real-time**. A 1-month composite has a 30-day lag.
- **Resourcesat AWIFS** — ISRO's own satellite, but VEDAS documentation does not specify update cadence. Likely monthly composites.

**No raw sensor data**: WMS returns rendered map tiles (PNG/JPEG), not raw reflectance values or spectral bands. Temporal API returns NDVI values (processed index), not raw imagery.

## Why This Scores Moderately

**Pros**:
1. **First ISRO public API** — this is a significant step forward for ISRO open data
2. **API key access** — REST API with JSON responses (Temporal API)
3. **Documented** — API Centre provides user guide and examples
4. **Sentinel-2 integration** — leverages open Copernicus data (good interoperability)
5. **NDVI time series** — useful for agriculture, vegetation monitoring

**Cons**:
1. **Not near-real-time** — temporal composites and monthly mosaics have significant lag (days to weeks)
2. **WMS tiles, not data** — WMS API returns rendered images, not raw values
3. **Limited product set** — only Sentinel-2 and Resourcesat AWIFS, no INSAT geostationary imagery
4. **Registration required** — not fully open (API key barrier)
5. **No sensor-level telemetry** — this is processed imagery/indices, not raw satellite observations

## Verdict

**⚠️ Conditional Skip** — VEDAS API Centre is a **promising development** but **not suitable for this repo's near-real-time mission**:
- Temporal composites (weeks of data) are not real-time
- WMS tiles are rendered images, not structured data
- Temporal API provides NDVI time series, which could be valuable for agriculture monitoring, but the update cadence is too slow (5-day Sentinel-2 repeat, likely weekly/monthly composite refresh)

**If VEDAS adds**:
- **Daily Resourcesat AWIFS imagery** (raw reflectance, not composites)
- **INSAT-3D/3DR near-real-time products** (SST, OLR, cloud products with <6 hour latency)
- **Oceansat-3 ocean color** (daily/weekly composites)

...then it would become a viable candidate. Monitor VEDAS API Centre for product expansion.

**Recommendation**: **Do not build a bridge now**, but **bookmark for future**. VEDAS API Centre is the most accessible ISRO data API to date. If they add NRT products, re-evaluate.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2 | Sentinel-2 composites, NDVI time series — useful but not unique (ESA Copernicus already open) |
| Freshness | 1 | Temporal composites (weeks lag), Sentinel-2 (5-day repeat) — too slow for real-time |
| Openness | 2 | Free API key required (better than MOSDAC registration), but still a barrier |
| Schema Clarity | 2 | WMS (standard but raster), Temporal API (JSON, simple schema) |
| Machine-Readability | 2 | REST API (good), but WMS tiles are images not data |
| Repo-Fit | -2 | Not near-real-time, WMS tiles (not data), limited product scope — **misfit for this repo** |

**Score: 7/18** — Promising API but not suitable for NRT satellite bridge. Revisit if ISRO adds daily/hourly products.
