# EUMETSAT H SAF Snow Cover and Snow Water Equivalent

- **Country/Region**: Northern Hemisphere (Europe, North America, Asia)
- **Endpoint**: FTP: `ftphsaf.meteoam.it`, THREDDS
- **Protocol**: FTP, NetCDF/GRIB download
- **Auth**: Free H SAF registration
- **Format**: GRIB2, NetCDF-4
- **Freshness**: Daily
- **Docs**: http://hsaf.meteoam.it/snow.php
- **Score**: 8/18

## Overview

H SAF produces daily snow products:
- **H10/H11/H12**: Snow cover extent (binary: snow/no snow)
- **H13**: Fractional snow cover
- **H34**: Snow water equivalent (SWE, mm)

Snow monitoring supports:
- **Water resource management**: Snowpack = spring/summer water supply
- **Flood forecasting**: Rapid snowmelt causes flooding
- **Avalanche risk**: Snow depth and layering
- **Ski resorts**: Snow coverage for tourism

## Why Weak

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 0 | Daily (T+1 latency) — **not NRT** |
| **Openness** | 2 | Free registration |
| **Stability** | 3 | Operational H SAF |
| **Structure** | 3 | GRIB2/NetCDF |
| **Identifiers** | 0 | Gridded field |
| **Additive value** | 0 | Daily cadence too slow |

## Verdict

**SKIP** (8/18) — Daily cadence, not near-real-time. Snow cover changes slowly (days to weeks), so daily is appropriate scientifically, but not for this repo's streaming focus.
