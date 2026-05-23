# EUMETSAT AC SAF Total Column Ozone and Trace Gases

- **Country/Region**: Global (polar-orbiter coverage)
- **Endpoint**: `https://acsaf.org/offline_access.php`, EUMETSAT Data Store
- **Protocol**: FTP, HTTP file download, NetCDF/HDF5
- **Auth**: Free registration for data access
- **Format**: NetCDF-4, HDF5, BUFR
- **Freshness**: Near-real-time (~3 hours from observation), daily composites
- **Docs**: https://acsaf.org
- **Score**: 12/18

## Overview

The Atmospheric Composition SAF (AC SAF), operated by FMI (Finland) and replacing the former O3M SAF, produces trace gas retrievals from UV/visible spectrometers on polar-orbiting satellites:

- **Instruments**: GOME-2 (Metop-A/B/C), TROPOMI (Sentinel-5P)
- **Products**: Total column ozone, NO2, SO2, HCHO, aerosol index, UV radiation

Key NRT products:

| Product | Parameter | Latency | Resolution | Coverage |
|---------|-----------|---------|------------|----------|
| **GOME-2 O3** | Total column ozone (DU) | 3 hours | 40×80 km | Global (14 orbits/day) |
| **GOME-2 NO2** | Tropospheric NO2 column | 3 hours | 40×80 km | Global |
| **GOME-2 SO2** | Volcanic SO2 plume | 3 hours | 40×80 km | Global |
| **TROPOMI O3/NO2** | High-res ozone/NO2 | 3 hours | 7×7 km | Global |

**Why atmospheric composition matters**:
- **Ozone hole monitoring**: Antarctic ozone depletion (Sept-Oct each year)
- **Air quality**: NO2 is a proxy for urban/industrial pollution
- **Volcanic ash**: SO2 plumes from eruptions (aviation hazard)
- **UV index**: Total column ozone determines surface UV radiation
- **Climate**: Ozone is a greenhouse gas; stratospheric trends affect climate

AC SAF products feed:
- **CAMS** (Copernicus Atmosphere Monitoring Service) for global air quality forecasts
- **WMO Global Atmosphere Watch** for ozone layer monitoring
- **Volcanic Ash Advisory Centers** (VAAC) for aviation safety

## Endpoint Analysis

**Data Access**: https://acsaf.org/offline_access.php

AC SAF uses a data request system (not open FTP):
1. Register for free account
2. Select product, date range, geographic area
3. Receive download link via email (within hours)

**Alternative: EUMETSAT Data Store**:
```
GET https://api.eumetsat.int/data/browse/collections?q=GOME-2
```

GOME-2 Level-2 products are available via Data Store with free registration.

**Update cadence**:
- NRT products: ~3 hours from observation
- Daily global composites: Available next day (~12:00 UTC)
- Each Metop satellite provides ~14 orbits/day

**File format**:
- NetCDF-4 (primary)
- HDF5 (TROPOMI)
- BUFR (WMO GTS distribution for selected products)

## Schema / Sample

**GOME-2 Total Column Ozone (NetCDF)**:
```
dimensions:
    scanline = 1024 (along-track)
    ground_pixel = 32 (across-track)

variables:
    float ozone_total_column(scanline, ground_pixel)
        units: "DU"  // Dobson Units
        long_name: "Total ozone column"
        valid_range: 100.0, 600.0
        
    float latitude(scanline, ground_pixel)
    float longitude(scanline, ground_pixel)
    
    double time(scanline)
        units: "seconds since 2000-01-01 00:00:00"
        
    int quality_flag(scanline, ground_pixel)
        flag_meanings: "good questionable bad missing"
        flag_values: 0, 1, 2, 3
```

**Event model** (CloudEvents bridge):
```json
{
  "type": "eumetsat.ac-saf.ozone.ground-pixel",
  "source": "ac-saf/gome-2/metopb",
  "id": "o3_metopb_orbit12345_scan0856_px16",
  "time": "2024-06-15T12:08:34Z",
  "subject": "atmos/{lat_bucket}/{lon_bucket}/ozone",
  "data": {
    "satellite": "metopb",
    "orbit_number": 12345,
    "scanline": 856,
    "ground_pixel": 16,
    "latitude": 45.67,
    "longitude": 12.34,
    "ozone_total_column_du": 312.5,
    "ozone_uncertainty_du": 8.2,
    "quality_flag": "good",
    "solar_zenith_angle": 42.3,
    "cloud_fraction": 0.15
  }
}
```

**Keying design**:
- Option A: `{satellite}/{orbit}/{scan}/{pixel}` (unique per observation)
- Option B: `{lat_bucket}/{lon_bucket}` (geographic, multiple passes per day)

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 2 | 3-hour latency for NRT products |
| **Openness** | 2 | Free registration, request system (not open FTP) |
| **Stability** | 3 | Operational since 2006 (GOME-2/Metop-A) |
| **Structure** | 3 | NetCDF-4, HDF5, documented schemas |
| **Identifiers** | 1 | Swath geometry (must create bucket keys) |
| **Additive value** | 1 | Repo has no atmospheric composition |

**Strengths**:
- **Scientific pedigree**: AC SAF continues 30+ year ozone monitoring record (TOMS → GOME → GOME-2 → TROPOMI)
- **Multiple satellites**: Metop-A/B/C redundancy
- **Operational importance**: Feeds CAMS, WMO GAW, VAAC
- **UV/volcanic hazard**: Ozone hole and SO2 plumes are high-impact events

**Use cases**:
- **Antarctic ozone hole**: Track size and depth (Sept-Oct peak)
- **Urban NO2**: Monitor pollution episodes (lockdown vs. normal traffic)
- **Volcanic eruptions**: Detect SO2 plumes for aviation safety
- **Wildfire smoke**: Aerosol index tracks smoke transport

## Limitations

1. **3-hour latency**: NRT products arrive ~3 hours after observation. Slower than sub-hourly weather/hydro feeds.

2. **Request system**: Not open FTP or real-time API. Must submit data requests and wait for email delivery. This is **not suitable for automated polling** unless EUMETSAT Data Store provides better access.

3. **Swath coverage**: Polar orbiter provides ~14 swaths/day, not continuous monitoring (vs. geostationary). Most locations get 1-2 overpasses per day.

4. **Large pixel size**: GOME-2 at 40×80 km cannot resolve city-scale pollution (TROPOMI at 7 km is better but still coarse vs. ground monitors).

5. **Gridded vs. point**: Products are swath grids, not station observations. Must create artificial lat/lon bucket keys.

6. **Overlap with Sentinel-5P**: TROPOMI (EU Copernicus) provides higher-resolution NO2/O3 with similar latency. AC SAF adds operational EUMETSAT provenance but Sentinel-5P may be preferred for resolution.

## Verdict

**MARGINAL** (12/18) — Strong on stability and structure, but **3-hour latency** and **request-based distribution** limit real-time utility. The data request workflow (email delivery) is **not suitable for automated polling**.

**Better alternatives**:
- **Sentinel-5P TROPOMI**: Same trace gases, higher resolution (7 km), Copernicus open data (automated API)
- **Ground monitors**: Real-time AQI from EPA/EEA station networks (sub-hourly updates)

**If pursuing AC SAF**:
- Use **EUMETSAT Data Store API** instead of request system
- Emit only **exceptional events** (ozone hole <220 DU, volcanic SO2 >10 DU, NO2 hotspots >5×10^15 molec/cm²)
- Combine with **CAMS forecasts** for forward-looking air quality

**Status**: Low priority. Consider **TROPOMI** (Sentinel-5P) or **ground AQI stations** instead for better freshness and access patterns.
