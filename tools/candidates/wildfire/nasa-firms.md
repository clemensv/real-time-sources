# NASA FIRMS (Fire Information for Resource Management System)

**Country/Region**: Global
**Publisher**: NASA EOSDIS / LANCE (Land, Atmosphere Near real-time Capability for EOS)
**API Endpoint**: `https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{AREA_COORDINATES}/{DAY_RANGE}`
**Documentation**: https://firms.modaps.eosdis.nasa.gov/api/
**Protocol**: REST
**Auth**: Free API key (MAP_KEY) — self-service registration
**Data Format**: CSV, JSON, KML
**Update Frequency**: Near Real-Time (NRT ~3h), Real-Time (~60 min), Ultra Real-Time (<60 seconds for US/Canada)
**License**: NASA Open Data Policy (free, unrestricted)

## What It Provides

Global active fire / thermal anomaly detections from multiple satellite instruments:
- **MODIS** (Aqua/Terra) — 1km resolution, NRT and Standard Processing
- **VIIRS** (Suomi-NPP, NOAA-20, NOAA-21) — 375m resolution, NRT and SP
- **LANDSAT** (US/Canada only) — 30m resolution, NRT

Each hotspot record includes: latitude, longitude, brightness temperature, fire radiative power (FRP), confidence level, satellite/instrument, acquisition datetime, and scan/track pixel size.

## API Details

The API provides several endpoints:

- `/api/area/` — Fire hotspots by bounding box, sensor, date range. Supports CSV output. Max 5 days per query.
- `/api/country/` — Fire hotspots by country code (currently unavailable).
- `/api/data_availability/` — Check product date availability per sensor.
- `/api/kml_fire_footprints/` — KML fire detection footprints.
- `/api/missing_data/` — Dates with missing satellite data.

Example request:
```
GET https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_NOAA20_NRT/-125,25,-66,50/1
```

Sources available:
- `MODIS_NRT`, `MODIS_SP`
- `VIIRS_SNPP_NRT`, `VIIRS_SNPP_SP`
- `VIIRS_NOAA20_NRT`, `VIIRS_NOAA20_SP`
- `VIIRS_NOAA21_NRT`
- `LANDSAT_NRT` (US/Canada only)

Area can be bounding box (west,south,east,north) or `world`.

## Freshness Assessment

Excellent. URT data available in <60 seconds of satellite overpass for US/Canada. NRT data within ~3 hours globally. Multiple satellite passes per day provide frequent coverage. RT and URT data automatically replaced when NRT processing completes or after 6 hours.

## Entity Model

Each fire detection is a point feature with:
- `latitude`, `longitude` — detection location
- `brightness` / `bright_ti4`, `bright_ti5` — brightness temperatures (K)
- `scan`, `track` — pixel dimensions
- `acq_date`, `acq_time` — acquisition timestamp
- `satellite` — satellite name
- `instrument` — MODIS / VIIRS
- `confidence` — detection confidence (low/nominal/high for VIIRS, 0-100 for MODIS)
- `version` — processing version
- `frp` — Fire Radiative Power (MW)
- `daynight` — D/N flag
- `type` — fire type (VIIRS: 0=vegetation, 1=active volcano, 2=other static, 3=offshore)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | URT <60s (US/CA), NRT ~3h global |
| Openness | 3 | Free API key, NASA open data |
| Stability | 3 | Long-running NASA program, well-maintained |
| Structure | 3 | Clean CSV/JSON, consistent schema |
| Identifiers | 2 | No persistent fire ID — point detections only |
| Additive Value | 3 | Global coverage, multi-sensor, high resolution |
| **Total** | **17/18** | |

## Notes

- The MAP_KEY is free and rate-limited (default: 10 requests/minute, can be increased).
- No persistent fire identifiers — each row is an independent thermal detection. Clustering into "fires" must be done downstream.
- FIRMS is the gold standard for satellite-based global fire detection. Widely used by fire agencies worldwide.
- The `country` endpoint is currently unavailable due to ongoing issues.
- Consider using the WFS endpoint at `https://firms.modaps.eosdis.nasa.gov/geoserver/` for GeoJSON output.
