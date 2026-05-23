# Copernicus CAMS Greenhouse Gas Forecast (CO2, CH4)

- **Country/Region**: Global
- **Endpoint**: https://ads.atmosphere.copernicus.eu/datasets/cams-global-greenhouse-gas-forecasts
- **Protocol**: CDS API
- **Auth**: Free ADS account
- **Format**: GRIB / NetCDF
- **Freshness**: Daily (5-day forecast)
- **Score**: 10/18

## Overview

CAMS produces **daily CO₂ and CH₄ forecasts**:

- **CO₂** concentration (ppm) — column-mean and 3D vertical profile
- **CH₄** concentration (ppb) — column-mean and 3D vertical profile
- **5-day forecast**, updated daily at 00Z
- **0.4° resolution** (~40 km)

Assimilates satellite observations (GOSAT, TROPOMI, IASI) and surface flask measurements.

## Verdict

⚠️ **Maybe** — Greenhouse gas forecasts are **slow-changing** (daily updates, GHG lifetime
= years). Not real-time. CDS async API is bulk-download model. Better for **climatology**
than real-time streaming.

| Criterion | Score |
|-----------|-------|
| Value | 2 (climate science, policy-relevant but slow dynamics) |
| Freshness | 1 (daily, GHG is slow-changing) |
| Openness | 2 |
| Schema | 3 |
| Machine-readability | 1 |
| Repo fit | 1 (grid data) |

**Total: 10/18** — **Skip**. Prefer **ground station networks** (NOAA GML, ICOS) for actual
CO₂/CH₄ measurements instead of model forecasts.
