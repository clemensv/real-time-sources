# NASA TEMPO (Tropospheric Emissions Monitoring of POllution) Hourly Air Quality

- **Country/Region**: North America (Mexico City to central Canada, Atlantic to Pacific)
- **Endpoint**: `https://data.gesdisc.eosdis.nasa.gov/data/TEMPO/` (GES DISC)
- **Protocol**: HTTPS file download (NetCDF-4)
- **Auth**: Earthdata Login (free registration)
- **Format**: NetCDF-4
- **Freshness**: ~2 hours from observation
- **Docs**: https://tempo.si.edu/data.html, https://disc.gsfc.nasa.gov/datasets?project=TEMPO
- **Score**: 14/18

## Overview

NASA's Tropospheric Emissions: Monitoring of POllution (TEMPO) instrument, launched in 2023 aboard a geostationary satellite, is the first space-based instrument to monitor hourly air quality over North America from sunrise to sunset. TEMPO measures atmospheric concentrations of nitrogen dioxide (NO₂), ozone (O₃), formaldehyde (HCHO), sulfur dioxide (SO₂), and aerosols with ~10 km × 10 km spatial resolution.

Unlike polar-orbiting satellites (which pass over each location once or twice daily), TEMPO's geostationary orbit enables continuous monitoring — providing hourly snapshots of air pollution across the entire North American field of regard. This hourly cadence captures diurnal cycles (rush-hour traffic peaks, industrial emissions, wildfire smoke transport) and enables rapid-update air quality forecasts.

Data products include Level 2 (swath data, individual scans) and Level 3 (gridded hourly averages). NRT Level 2 products are available within ~2 hours of observation. TEMPO data is used by EPA Air Now, NOAA air quality forecasts, and state environmental agencies for public health alerts.

## Endpoint Analysis

**GES DISC data directory:**
```
https://data.gesdisc.eosdis.nasa.gov/data/TEMPO/TEMPO_NO2_L2.002/
```

Files follow naming convention:
```
TEMPO_NO2_L2_V03_20240115T183000Z_S012G01.nc
       ^    ^           ^           ^
      gas  L2        timestamp    scan/granule
```

**Product codes:**
- `TEMPO_NO2_L2` — Nitrogen Dioxide (tropospheric column), Level 2
- `TEMPO_O3TOT_L2` — Total Column Ozone, Level 2
- `TEMPO_O3TROP_L2` — Tropospheric Ozone, Level 2
- `TEMPO_HCHO_L2` — Formaldehyde, Level 2
- `TEMPO_CLOUD_L2` — Cloud parameters
- `TEMPO_NO2_L3` — Hourly gridded NO₂

**Sample NetCDF structure (TEMPO_NO2_L2):**
- `geolocation/latitude`, `geolocation/longitude` — pixel centers (swath geometry)
- `product/vertical_column_troposphere` — NO₂ column density (molecules/cm²)
- `product/vertical_column_troposphere_uncertainty` — retrieval uncertainty
- `product/processing_quality_flags` — QA flags (0=good, >0=suspect/fail)
- Metadata: observation time, solar zenith angle, cloud fraction

**Earthdata Login auth:**
```bash
curl -n -c cookies.txt -b cookies.txt \
  "https://data.gesdisc.eosdis.nasa.gov/data/TEMPO/TEMPO_NO2_L2.002/2024/015/TEMPO_NO2_L2_V03_20240115T183000Z_S012G01.nc"
```

**Coverage:**
- Longitude: ~140°W to ~40°W (Pacific to Atlantic)
- Latitude: ~20°N to ~60°N (Mexico City to Edmonton/Winnipeg)
- Temporal: Hourly from sunrise to sunset local time (~12–14 scans per day depending on latitude and season)
- Spatial resolution: ~10 km × 10 km at nadir

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | ~2 hour latency from observation — excellent for satellite products |
| Openness | 2 | Free Earthdata Login required, instant registration |
| Stability | 2 | New mission (2023 launch), operational but data formats may evolve |
| Structure | 3 | NetCDF-4 with CF conventions, well-documented variables |
| Identifiers | 2 | Pixel lat/lon + timestamp; gridded L3 products use fixed grid |
| Richness | 2 | Trace gas columns + uncertainty + QA flags; no surface concentration (column-integrated) |

**TEMPO is a breakthrough for air quality monitoring.** The hourly North American coverage is unprecedented. Previous satellite air quality products (OMI, TROPOMI) provided daily snapshots; TEMPO captures morning rush hour, midday photochemical production, and evening emissions separately. The ~2 hour latency is fast enough for same-day air quality forecasts.

**Strong operational value:** EPA, NOAA, and state agencies incorporate TEMPO data into Air Quality Index (AQI) forecasts and public health advisories. The data complements ground-based EPA AirNow stations (which measure surface concentration) by showing transport, dispersion, and spatial extent of pollution plumes.

**Gridded L3 products are bridge-friendly.** Hourly averaged grids at fixed lat/lon resolution enable stable keying (grid cell ID). L2 swath data has more spatial detail but variable geometry (each scan has slightly different pixel locations).

## Limitations

- **Earthdata Login required.** Free but adds auth complexity (OAuth/cookie handling).
- **File-based delivery (NetCDF).** Each hourly scan is a ~50 MB file. Bridge must poll directory, download, parse NetCDF, extract grid cells. Heavier than JSON REST APIs.
- **Column density, not surface concentration.** TEMPO measures the vertical column of trace gases from ground to space (molecules/cm²), not the concentration you'd breathe at ground level (ppb or µg/m³). Surface-level estimates require conversion models that account for mixing layer height.
- **Daytime-only coverage.** Geostationary IR/visible sensors cannot retrieve tropospheric NO₂/O₃ at night. Hourly data is available only from sunrise to sunset (~12–16 scans per day, varies by season and latitude).
- **North America only.** Field of regard is ~40°W to ~140°W, ~20°N to ~60°N. No Europe, Asia, South America.
- **New mission, evolving data products.** TEMPO launched in 2023; L2/L3 product definitions are stabilizing but may see version updates. Early adopters should expect data format changes.
- **Grid-cell volume.** North America at 10 km resolution is ~100,000 grid cells. Emitting all cells every hour is high volume; filtering to populated areas or pollution hotspots is recommended.

**No breaking limitations for NRT bridging.** The Earthdata Login and NetCDF file handling are standard for NASA EOSDIS products. The daytime-only constraint is inherent to the measurement technique.

## Final Verdict

**Verdict**: ✅ **Build**

TEMPO is NASA's flagship air quality mission with unique hourly North American coverage and ~2 hour NRT latency. The data fills a critical gap for same-day air quality forecasting and public health advisories. While file-based NetCDF delivery and Earthdata Login add complexity, the operational value is high.

**Recommended approach:**
- Regional bridge (e.g., "US Eastern Corridor," "California Central Valley," "Great Lakes") or major metro areas (NYC, LA, Chicago, Houston)
- Use Level 3 hourly gridded products (fixed grid cells) for stable keying
- Poll hourly for new granules during daylight hours
- Keying by grid cell (lat/lon at 10 km resolution or coarser aggregation)
- Emit only high-quality pixels (processing_quality_flags == 0)

**Bridge type:** Poller (HTTPS file listing + NetCDF download/parse, hourly interval during daytime)

**Keying:** Grid cell (lat/lon at 10 km) OR metropolitan area aggregate

**Reference data:** Fixed grid metadata (lat/lon bounds, cell IDs) — static, embedded in NetCDF or L3 product docs

**Pairs well with:** EPA AirNow ground stations (surface concentration), NOAA HRRR smoke forecasts (wildfire plumes), NASA FIRMS (fire sources)

**Similar NASA products to consider:**
- **OMI (Ozone Monitoring Instrument)** — daily global O₃/NO₂/SO₂, 13×24 km, on Aura satellite (2004–present)
- **TROPOMI (Sentinel-5P)** — daily global trace gases, 7×7 km, European mission with NASA involvement
- Both have ~1 day latency and global coverage but lack TEMPO's hourly North America cadence
