# EUMETSAT CM SAF Radiation and Cloud Products

- **Country/Region**: Europe, Africa, Atlantic (MSG disk), Global (AVHRR)
- **Endpoint**: FTP, THREDDS, WMS (https://wui.cmsaf.eu)
- **Protocol**: FTP, NetCDF download, WMS, THREDDS/OPeNDAP
- **Auth**: Free registration
- **Format**: NetCDF-4
- **Freshness**: Hourly (surface radiation), daily (cloud properties), monthly (climate records)
- **Docs**: https://www.cmsaf.eu
- **Score**: 10/18

## Overview

The Climate Monitoring SAF (CM SAF), operated by DWD (Germany), produces **climate data records** from geostationary and polar satellites. While most products are **archival** (Climate Data Records for long-term trends), some have **near-real-time** versions:

| Product | Description | Cadence | Coverage |
|---------|-------------|---------|----------|
| **SIS** | Surface incoming shortwave radiation | Hourly | MSG disk |
| **SID** | Direct solar radiation | Hourly | MSG disk |
| **DNI** | Direct normal irradiance | Hourly | MSG disk |
| **CTX** | Cloud top parameters (temp, pressure, height) | Hourly | MSG disk |

**Why radiation matters**:
- **Solar energy**: PV power output forecasting
- **Agriculture**: Photosynthetically active radiation (crop growth)
- **Climate monitoring**: Radiation budget (Earth energy balance)

## Why Weak

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 2 | Hourly (some products), daily (most) |
| **Openness** | 2 | Free registration |
| **Stability** | 3 | Operational CM SAF, DWD backing |
| **Structure** | 3 | NetCDF-4 |
| **Identifiers** | 0 | Gridded field |
| **Additive value** | 0 | Climate records (long-term), not real-time hazard |

## Verdict

**SKIP** (10/18) — CM SAF focuses on **climate data records** (CDRs) for long-term monitoring, not operational NRT products. Hourly solar radiation is the fastest product, but it's a gridded field (not point events).

**Better alternatives** for solar radiation:
- Ground pyranometer networks (real-time, point observations)
- NWP model outputs (ECMWF, NOAA) for solar forecast

**Status**: Low priority. CM SAF is valuable for climate, but not for event streaming.
