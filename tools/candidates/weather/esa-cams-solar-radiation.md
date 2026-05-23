# Copernicus CAMS Solar Radiation Service

- **Country/Region**: Europe, Africa, Middle East, parts of Asia
- **Endpoint**: https://ads.atmosphere.copernicus.eu/datasets/cams-solar-radiation-timeseries
- **Protocol**: CDS API
- **Auth**: Free ADS account
- **Format**: CSV, NetCDF
- **Freshness**: Historical (2004–present) + near-real-time (1–2 day lag)
- **Score**: 9/18

## Overview

CAMS Solar Radiation Service provides **global/direct/diffuse solar irradiance** for solar
energy applications:

- **GHI** (Global Horizontal Irradiance)
- **BHI** (Beam Horizontal Irradiance)
- **DHI** (Diffuse Horizontal Irradiance)
- **BNI** (Beam Normal Irradiance)
- **Time-series or gridded** (0.05° ~5 km resolution)
- **1–2 day lag** for near-real-time

Derived from Meteosat satellite imagery (clear-sky model + cloud detection).

## Verdict

❌ **Skip** — 1–2 day lag is too slow for real-time solar forecasting. CDS API is bulk-download.
**Better alternatives**: national meteorological services provide **hourly solar radiation**
observations from ground stations (DWD, Met Office, KNMI) with <1 hour latency.

| Criterion | Score |
|-----------|-------|
| Value | 2 (solar energy, but lag reduces operational utility) |
| Freshness | 1 (1–2 day lag) |
| Openness | 2 |
| Schema | 3 |
| Machine-readability | 1 |
| Repo fit | 0 (grid data or time-series, lag) |

**Total: 9/18** — **Skip**.
