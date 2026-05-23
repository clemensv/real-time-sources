# NOAA Coral Reef Watch 5km Daily SST

- **Country/Region**: Global (coral reef regions)
- **Endpoint**: `https://www.star.nesdis.noaa.gov/pub/sod/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst/{YYYY}/`
- **Protocol**: HTTP file listing + direct NetCDF download
- **Auth**: None
- **Format**: NetCDF4
- **Freshness**: Daily (1-2 day latency)
- **Docs**: https://coralreefwatch.noaa.gov/product/5km/index.php
- **Score**: 9/18

## Overview

NOAA Coral Reef Watch (CRW) produces daily global 5km sea surface temperature (SST) and coral bleaching thermal stress products using satellite data from **VIIRS** (Suomi-NPP, NOAA-20, NOAA-21), **GOES-16/18** (ABI), and **Himawari-8/9** (AHI). CRW products are designed to monitor coral reef health and predict mass bleaching events.

Key products:
- **SST**: Daily analyzed sea surface temperature (°C)
- **SST Anomaly**: Difference from climatological mean
- **Coral Bleaching HotSpot**: Positive SST anomaly above bleaching threshold
- **Degree Heating Week (DHW)**: Accumulated thermal stress over 12 weeks (bleaching predictor)

CRW products are used for:
- **Coral bleaching alerts**: Early warning for reef managers
- **Marine protected area management**: Thermal stress monitoring
- **Climate impact assessment**: Long-term warming trends
- **Fisheries**: Reef ecosystem health indicators

## Endpoint Analysis

**File directory structure:**

```
https://www.star.nesdis.noaa.gov/pub/sod/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst/{YYYY}/
```

Example file:
```
coraltemp_v3.1_20260522.nc
```

File naming:
- `coraltemp_v3.1_YYYYMMDD.nc`
- Published daily with 1-2 day latency

**Data format**: NetCDF4 (CF-compliant), **not JSON**.

Variables (per file):
- `analysed_sst`: SST (°C), global 5km grid (~7,200 × 3,600 pixels)
- `sea_surface_temperature_anomaly`: SST anomaly (°C)
- `mask`: Land/ice mask
- `sst_trend_7d`: 7-day SST trend (°C/week)

**File size**: ~200-300 MB per daily global file.

**Volume**: 1 file/day, ~7 files/week, ~30 files/month.

**Key model**: Gridded raster (no entity key). Each file is a global daily snapshot.

## Schema / Sample

NetCDF4 structure (simplified):
```
dimensions:
    lat = 3600;
    lon = 7200;
    time = 1;

variables:
    float analysed_sst(time, lat, lon);
        units = "degree_Celsius";
        long_name = "Analysed sea surface temperature";
    
    float sea_surface_temperature_anomaly(time, lat, lon);
        units = "degree_Celsius";
    
    byte mask(time, lat, lon);
        valid_range = 1, 5;  // 1=ocean, 2=land, 3=lake, 4=ice, 5=fill
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | **Critical for coral reef conservation** and bleaching alerts |
| Freshness | 1/3 | Daily updates with 1-2 day latency (not near-real-time) |
| Openness | 3/3 | No auth, NOAA open data, stable archive |
| Schema Clarity | 2/3 | NetCDF4 CF-compliant, well-documented |
| Machine-Readability | 1/3 | NetCDF4 (not JSON) — requires xarray/netCDF4 |
| Repo Fit | -1/3 | **Gridded raster** (25M cells, 200-300 MB/file) — poor fit for entity-keyed events |

**Total: 9/18**

- Coral bleaching is politically and ecologically significant
- Multi-satellite blended product (VIIRS + GOES + Himawari)
- DHW product is the **gold standard** for bleaching prediction
- **However**: Daily cadence with 1-2 day latency disqualifies as "real-time"
- Gridded data model doesn't align with entity-keyed event streams
- 200-300 MB NetCDF4 files are incompatible with HTTP polling

## Limitations

- **Daily cadence with 1-2 day latency** — not near-real-time
- **Binary NetCDF4 format** — not JSON
- **Massive file sizes** (200-300 MB for global daily grid)
- **Gridded data model** — no natural reef/station entity key
- Interpretation requires climatological baseline (MMM, maximum monthly mean)
- Coverage is global, but only meaningful for coral reef latitudes (30°N - 30°S)

## Verdict

**SKIP** — While Coral Reef Watch products are scientifically and ecologically important, they are disqualified by **daily cadence with 1-2 day latency** (not near-real-time) and the **NetCDF4 gridded raster model** (200-300 MB files, 25M grid cells). This repo targets sub-hourly event streams with stable entity keys. CRW data is better suited to scientific data archives and pull-based workflows. **Defer** unless NOAA publishes a **JSON point-based API** (e.g., "DHW for these 500 named reef sites").
