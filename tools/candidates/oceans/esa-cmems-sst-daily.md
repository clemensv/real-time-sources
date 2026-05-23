# Copernicus Marine Service SST Daily Analysis

- **Country/Region**: Global oceans
- **Endpoint**: https://data.marine.copernicus.eu/products
- **Protocol**: ERDDAP, OPeNDAP, S3
- **Auth**: Free account
- **Format**: NetCDF
- **Freshness**: Daily (1-day lag)
- **Score**: 11/18

## Overview

CMEMS produces **daily global Sea Surface Temperature (SST)** analysis by merging multiple satellites:

- **Product**: `GLOBAL_ANALYSISFORECAST_PHY_001_024` (0.083° ~10 km, daily)
- **Sources**: Sentinel-3 SLSTR, MODIS, VIIRS, in-situ buoys
- **Latency**: 1-day
- **Variables**: SST, SST anomaly, sea ice concentration

Used for: marine heatwave detection, fisheries, coral bleaching, hurricane forecasting.

## Verdict

⚠️ **Maybe** — Daily **gridded SST** (0.083° global = 4,320 × 2,160 cells = 9M points).
Bulk NetCDF download. Could aggregate by pre-defined ocean regions (e.g., 100 marine
protected areas, coral reef zones) and emit daily SST summary events.

| Criterion | Score |
|-----------|-------|
| Value | 3 (ocean health, climate) |
| Freshness | 1 (daily, 1-day lag) |
| Openness | 1 (account required) |
| Schema | 3 |
| Machine-readability | 2 (ERDDAP/OPeNDAP) |
| Repo fit | 1 (grid data, extract regions) |

**Total: 11/18** — **Maybe**. Build if regional aggregation pattern is adopted.
