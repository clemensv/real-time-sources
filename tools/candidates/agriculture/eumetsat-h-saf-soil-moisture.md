# EUMETSAT H SAF Soil Moisture Products

- **Country/Region**: Europe, Global
- **Endpoint**: FTP: `ftphsaf.meteoam.it`, THREDDS (in development)
- **Protocol**: FTP, NetCDF/GRIB download
- **Auth**: Free H SAF registration
- **Format**: GRIB2, NetCDF-4
- **Freshness**: Daily (analysis of previous day), some products 3x daily
- **Docs**: http://hsaf.meteoam.it/soil-moisture.php
- **Score**: 9/18

## Overview

H SAF produces surface and root-zone soil moisture products from microwave radiometers and scatterometers:

| Product | Description | Cadence | Resolution | Coverage |
|---------|-------------|---------|------------|----------|
| **H25** | ASCAT surface soil moisture (SSM) | Daily | 25 km | Global |
| **H26** | ASCAT SSM (12.5 km) | Daily | 12.5 km | Global |
| **H141** | Metop ASCAT SSM (time series) | Daily | 12.5 km | Global |
| **H14** | Root zone soil moisture | 5 days | 0.25° | Europe |

Soil moisture is critical for:
- **Agricultural drought**: Crop water stress monitoring
- **Flood forecasting**: Saturated soils increase runoff (flash floods)
- **Wildfire risk**: Dry soils + dry vegetation = high fire danger
- **Numerical weather**: Soil moisture affects boundary-layer humidity and precipitation

## Endpoint Analysis

**FTP**: `ftp.hsaf.meteoam.it/products/h25/` (requires registration)

**File pattern**:
```
h25_20240615_00000000_cont.grib.gz
```

**Update cadence**:
- Daily products (H25, H26): Available ~12:00 UTC for previous day
- Time-series products (H141): Continuous append (updated daily)

**Latency**: T+1 day (not near-real-time; analysis product)

## Why Weak for This Repo

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 0 | Daily (T+1 day latency) — **not NRT** |
| **Openness** | 2 | Free registration |
| **Stability** | 3 | Operational H SAF |
| **Structure** | 3 | GRIB2/NetCDF |
| **Identifiers** | 0 | Gridded field |
| **Additive value** | 1 | Repo has no soil moisture, but daily cadence |

## Verdict

**SKIP** (9/18) — Daily cadence with T+1 latency is **not near-real-time**. Soil moisture changes slowly (days to weeks), so daily updates are scientifically appropriate, but they don't fit the repo's sub-hourly streaming focus.

Better H SAF candidates: **Precipitation** (H60/H63 — 15 minutes) is covered.

If soil moisture is needed, **SMAP** (NASA, 2-3 day revisit) or **SMOS** (ESA) are alternatives, but all have similar daily cadence.
