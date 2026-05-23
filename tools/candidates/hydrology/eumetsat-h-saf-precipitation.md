# EUMETSAT H SAF Precipitation Products

- **Country/Region**: Europe, Africa, Mediterranean, Atlantic (MSG/Metop coverage)
- **Endpoint**: FTP: `ftphsaf.meteoam.it`, THREDDS (in development)
- **Protocol**: FTP, NetCDF/GRIB download, WMS (visualization)
- **Auth**: Free registration required (username/password for FTP)
- **Format**: GRIB2, NetCDF-4, HDF5
- **Freshness**: 15-minute (MSG-based), hourly, 3-hourly, daily accumulations
- **Docs**: http://hsaf.meteoam.it
- **Score**: 14/18

## Overview

The Hydrology Satellite Application Facility (H SAF), led by Italy's AEMET, produces near-real-time precipitation estimates by blending:
- **Geostationary IR/VIS**: MSG SEVIRI (Europe/Africa disk)
- **Polar MW/IR**: AMSU-A, MHS, SSMIS (global swaths)
- **Ground radar**: European weather radar network (where available)

Key H SAF NRT precipitation products:

| Product | Description | Latency | Resolution | Coverage |
|---------|-------------|---------|------------|----------|
| **H60/H61** | Instantaneous PR rate (MSG) | 15 min | 3 km | MSG disk |
| **H63** | Accumulated PR (MSG, 1/3/6/12/24h) | 15 min | 3 km | MSG disk |
| **H64** | Blended MW/GEO PR | 1 hour | 8 km | Global |
| **H90** | PR monitoring (gauge-adjusted) | 3 hours | 16 km | Europe |

**Why precipitation matters**:
- **Flash flood warnings**: High-intensity rainfall (>50 mm/h) causes urban flooding
- **Agricultural water stress**: Cumulative rainfall vs. crop needs
- **Hydropower reservoir management**: Inflow forecasting
- **Landslide risk**: Soil saturation from multi-day precipitation

H SAF fills the gap between sparse rain gauge networks (point observations) and numerical weather models (coarse resolution). Satellite precipitation bridges spatial scales and provides coverage over oceans/mountains where gauges are absent.

## Endpoint Analysis

**FTP Server**: `ftp.hsaf.meteoam.it` (requires free registration)

**Directory structure**:
```
/products/h60/
  /h60_cur/YYYY/MM/DD/
    h60_20240615_1200_rom.grb.gz
```

**Update cadence**:
- H60/H61 (instantaneous): Every 15 minutes
- H63 (accumulation): Every 15 minutes (rolling windows)
- H64 (blended global): Every hour
- Latency: ~20-30 minutes from observation to FTP availability

**File naming** (H60 example):
```
h60_YYYYMMDD_HHMM_rom.grb.gz
```
- `h60`: Product code
- `YYYYMMDD_HHMM`: Observation time (UTC)
- `rom`: Processing center (Rome/CNMCA)
- `.grb.gz`: Gzipped GRIB2

**THREDDS** (in development): H SAF is migrating to THREDDS Data Server for OPeNDAP/WMS access. Partially operational as of 2024.

## Schema / Sample

**GRIB2 record** (H60 instantaneous precipitation rate):
```
Parameter: Total precipitation rate [kg m-2 s-1]
Level: Surface
Grid: Latitude/longitude (0.03° × 0.03° for MSG disk)
Bounding box: 60°N to 60°S, 60°W to 60°E
Time: Analysis (nowcast)
```

**Decoded to JSON** (CloudEvents bridge):
```json
{
  "type": "eumetsat.h-saf.precipitation.instantaneous",
  "source": "h-saf/h60/msg-seviri",
  "id": "h60_20240615_120000_n45p5_e012p0",
  "time": "2024-06-15T12:00:00Z",
  "subject": "precipitation/{lat_bucket}/{lon_bucket}",
  "data": {
    "product": "H60",
    "latitude": 45.52,
    "longitude": 12.01,
    "precip_rate_mm_h": 8.5,
    "precip_type": "convective",
    "quality_flag": "good",
    "sensor_source": "MSG-SEVIRI"
  }
}
```

**Event model design**:
- **Option A**: Emit entire grid as single event (~2M cells for MSG disk at 3 km) — large payload
- **Option B**: Emit only precipitating cells (PR > 0.1 mm/h) — sparse (typically 1-5% of grid during storms)
- **Option C**: Aggregate to coarser grid (0.1° or 0.25°) and emit non-zero cells

**Recommended**: **Option B** (sparse emission) — during a typical European storm, ~50,000 cells have precipitation, creating 50k events per 15-minute cycle (3.2M events/day during active weather, ~100k/day during fair weather).

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 3 | 15-minute updates (H60/H61/H63) |
| **Openness** | 2 | Free registration required, generous limits |
| **Stability** | 3 | Operational H SAF since 2005, EUMETSAT SAF |
| **Structure** | 3 | GRIB2 standard, NetCDF option, documented |
| **Identifiers** | 1 | Gridded (must create lat/lon bucket keys) |
| **Additive value** | 2 | Repo has NOAA precip; H SAF adds Europe/Africa |

**Strengths**:
- **15-minute cadence**: Fast enough for flash flood monitoring
- **High resolution**: 3 km (H60) captures convective cells
- **Operational backing**: Italian Met Service (CNMCA) + EUMETSAT
- **Multi-sensor fusion**: Combines geostationary + polar + radar
- **Critical for Europe**: Complements national radar networks (DWD, Météo-France)

**Real-world use**:
- **2021 Germany floods**: H SAF detected 150 mm/day accumulations 6 hours before catastrophic flooding
- **2023 Libya floods**: H SAF showed 200+ mm in 24h (storm Daniel), triggered humanitarian response
- **Italian civil protection**: Uses H SAF for landslide early warning in Alps/Apennines

## Limitations

1. **Registration required**: FTP access needs free H SAF account. Not anonymous like OSI SAF.

2. **Gridded format**: MSG disk = ~2M cells at 3 km. Must filter to precipitating cells only.

3. **Europe/Africa focus**: Global product (H64) exists but lower resolution (8 km) and hourly (vs. 15-min for H60).

4. **IR-based uncertainty**: Over land, IR-based precipitation estimates have ~30% error vs. rain gauges. Over ocean, error is higher (~50%). Microwave-based products (H64) are more accurate but lower temporal resolution.

5. **GRIB2 parsing**: Requires specialized libraries (`eccodes`, `pygrib`). More complex than NetCDF.

6. **Overlap with national radars**: Countries like Germany (DWD RADOLAN), France (PANTHERE), UK (NIMROD) have higher-quality national radar precipitation. H SAF adds value where radar coverage is sparse (Mediterranean, Africa, oceans).

## Verdict

**STRONG CANDIDATE** (14/18) — 15-minute precipitation at 3 km resolution fills a critical gap for European/African hydrology. **Recommended implementation**:

1. **FTP polling**: Check `/products/h60/h60_cur/` for new GRIB files every 5 minutes
2. **Parse GRIB2**: Use `eccodes` or `pygrib` to extract precip rate grid
3. **Sparse emission**: Emit events only for cells with PR ≥ 0.1 mm/h
4. **Key design**: `precipitation/{lat_0.1deg}/{lon_0.1deg}` (bucket to 0.1° for reasonable cardinality)
5. **Quality filter**: Include only cells with "good" or "acceptable" quality flags

**Volume estimate**:
- Typical European storm: ~50,000 precipitating cells
- 15-minute updates: 96 updates/day
- Fair weather (5% of storm volume): ~2,500 cells × 96 = 240k events/day
- Active weather: 50k cells × 96 = 4.8M events/day
- Average: ~1.5M events/day

**Pair with**:
- **DWD station observations** (already in repo) for ground truth
- **USGS stream gauges** (future) for rainfall → runoff correlation
- **H SAF soil moisture** (H25/H26/H141) for hydrological state

**Next steps**:
1. Register for H SAF FTP access (free, automated approval)
2. Download sample H60 GRIB2 file and test `pygrib` parsing
3. Implement sparse grid emission (precip > 0.1 mm/h)
4. Validate against DWD gauge observations

**Status**: Top-tier candidate for hydrology. Complements existing repo coverage (river gauges) with areal precipitation.
