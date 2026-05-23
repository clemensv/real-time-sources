# Copernicus CAMS UV Index Forecast

- **Country/Region**: Global
- **Endpoint**: https://ads.atmosphere.copernicus.eu/ (part of CAMS atmospheric composition)
- **Protocol**: CDS API
- **Auth**: Free ADS account
- **Format**: GRIB / NetCDF
- **Freshness**: Twice daily (5-day forecast)
- **Score**: 10/18

## Overview

CAMS forecasts **UV Index** (0–11+ scale) based on atmospheric ozone, aerosols, and clouds:

- **Clear-sky and all-sky UV index**
- **5-day forecast**, twice daily (00Z, 12Z)
- **0.4° resolution** (~40 km)
- **Erythemal dose** (skin-burning UV)

Used for: public health warnings, skin cancer prevention, outdoor activity planning.

## Verdict

⚠️ **Maybe** — Daily UV index forecast grid. Could extract for major cities and emit daily
forecast events. CDS async API. **National weather services** already publish UV index
forecasts (DWD, Met Office, NOAA) with better accessibility (REST APIs, RSS feeds).

| Criterion | Score |
|-----------|-------|
| Value | 2 (health-relevant but widely available elsewhere) |
| Freshness | 2 (twice daily forecast) |
| Openness | 2 |
| Schema | 3 |
| Machine-readability | 1 |
| Repo fit | 0 (grid, extract cities) |

**Total: 10/18** — **Skip**. National met services provide better UV index APIs.
