# Copernicus Climate Change Service (C3S) ERA5 Near-Real-Time

- **Country/Region**: Global
- **Endpoint**: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
- **Protocol**: CDS API
- **Auth**: Free CDS account
- **Format**: GRIB / NetCDF
- **Freshness**: 5-day lag (near-real-time preliminary), 3-month lag (final)
- **Score**: 8/18

## Overview

ERA5 is the world's leading **atmospheric reanalysis** — a physically consistent 4D gridded
dataset blending observations and models:

- **Hourly global data** since 1940
- **0.25° resolution** (~30 km)
- **100+ variables**: temperature, wind, pressure, precipitation, humidity, radiation, etc.
- **NRT stream**: 5-day lag preliminary data
- **Final data**: 3-month lag

ERA5 is the gold standard for climate analysis, model evaluation, and renewable energy.

## Verdict

❌ **Skip** — ERA5 is a **reanalysis** (historical/near-historical), not real-time forecasting.
5-day lag is too slow for operational use. Designed for **climate research** (multi-decadal
analysis), not real-time streaming. CDS async API is bulk-download oriented.

| Criterion | Score |
|-----------|-------|
| Value | 3 (climate benchmark) |
| Freshness | 0 (5-day lag minimum) |
| Openness | 2 |
| Schema | 3 |
| Machine-readability | 1 (async bulk API) |
| Repo fit | -1 (historical data, not NRT) |

**Total: 8/18** — **Skip**. ERA5 is for **climatology**, not real-time streams.
