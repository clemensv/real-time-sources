# Copernicus Global Flood Awareness System (GloFAS)

- **Country/Region**: Global
- **Endpoint**: https://global-flood.emergency.copernicus.eu/
- **Protocol**: WMS, NetCDF (restricted FTP/API)
- **Auth**: Free registration required
- **Format**: NetCDF, WMS raster
- **Freshness**: Twice daily (00Z, 12Z forecast runs)
- **Docs**: https://global-flood.emergency.copernicus.eu/, https://confluence.ecmwf.int/display/GLOFAS
- **Score**: 11/18

## Overview

GloFAS (Global Flood Awareness System) extends EFAS capabilities to **worldwide coverage**,
providing 30-day probabilistic flood forecasts for all continents. Like EFAS, it runs the
LISFLOOD hydrological model forced by ECMWF weather forecasts.

GloFAS delivers:
- **30-day ensemble forecasts** (51 members, twice daily)
- **~5,000 reporting points** on major rivers globally
- **5 km gridded discharge** for all river pixels
- **Flood early warning thresholds** (2-year, 5-year, 20-year return periods)
- **Reforecasts** (hindcast climatology for threshold calibration)

Used by: UNOCHA, WFP, Red Cross, WMO, national hydrological services in 100+ countries.

**Key difference from EFAS**: Global vs. European coverage, 30-day vs. 10-day horizon.

## Endpoint Analysis

**Similar access restrictions to EFAS**:

- WMS visualization service (public): `https://global-flood.emergency.copernicus.eu/geoserver/wms`
- Data API (restricted): requires registration, EULA acceptance, possible FTP credentials
- No public REST API for forecast data as of Jan 2026

**WMS layers** (public, PNG tiles only):

```
GetMap request:
  layers=glofas:forecast_discharge_mean
  bbox=-180,-90,180,90
  width=800&height=400
  srs=EPSG:4326
  format=image/png
```

Returns raster map, **not machine-readable data**.

**Hypothetical REST endpoint** (if institutional access granted):

```
GET /api/v1/forecast?
  point_id=G12345&
  issue_time=2026-01-15T00:00:00Z
```

Returns ensemble discharge forecast for next 30 days at 6-hour intervals.

## Why Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Value** | 3 | **Global** flood forecasting for 100+ countries. Critical for humanitarian early action, especially in data-sparse regions (Africa, South Asia, South America). |
| **Freshness** | 2 | Twice daily (00Z, 12Z), 30-day forecast. Good for medium-range planning but not real-time. |
| **Openness** | 1 | **Restricted access** — requires registration, EULA, and likely institutional approval for API/FTP. |
| **Schema clarity** | 3 | NetCDF with CF conventions, reporting point metadata (river name, basin, thresholds). |
| **Machine-readability** | 1 | **No public API** — WMS provides images only. Forecast data requires FTP/API with credentials. |
| **Repo fit** | 1 | Ensemble forecasts (51 members × 5,000 points × 120 timesteps) are bulk data. Better as notification + S3 storage than Kafka streaming. |

**Total: 11/18** — High humanitarian value but **access restrictions** prevent open bridging.

## Limitations

- Identical to EFAS (restricted access, FTP-based, institutional approval)
- 5,000 global reporting points = ~1 point per 1,000 km² catchment, very sparse in small basins
- Calibration challenges in ungauged basins (Africa, Asia)

## Verdict

⏭️ **Reference** — Same verdict as EFAS. Requires institutional data-sharing agreement.
**Skip** unless formal arrangement with ECMWF/JRC is established.

**Alternative**: National hydrological services with open APIs (USGS, BOM Australia, etc.)
provide ground-truth discharge measurements instead of model forecasts.
