# Copernicus CAMS European Air Quality Forecast

- **Country/Region**: Europe
- **Endpoint**: https://ads.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-forecasts
- **Protocol**: CDS API
- **Auth**: Free ADS account
- **Format**: GRIB / NetCDF
- **Freshness**: Twice daily (00Z, 12Z), 4-day forecast
- **Score**: 12/18

## Overview

CAMS Regional (Europe) provides **higher-resolution** air quality forecasts than CAMS Global:

- **0.1° resolution** (~10 km) vs. 0.4° global
- **Ensemble forecast** (11 models) vs. single deterministic
- **4-day forecast** vs. 5-day global
- Species: O₃, NO₂, SO₂, CO, PM10, PM2.5, PM1, pollen (birch, olive, grass)

Updated twice daily, assimilates European ground station observations.

## Verdict

⚠️ **Maybe** — Same **CDS async API** limitations as CAMS Global. Better resolution (10km)
makes it suitable for city-level aggregates (e.g., extract Paris, Berlin, Rome O₃/PM2.5).
But still bulk-download model, not streaming.

| Criterion | Score |
|-----------|-------|
| Value | 3 (European cities, regulatory air quality) |
| Freshness | 2 (twice daily) |
| Openness | 2 (free account) |
| Schema | 3 |
| Machine-readability | 1 (async API) |
| Repo fit | 1 (grid data, extract cities manually) |

**Total: 12/18** — **Maybe**. Build if adopting regional aggregation pattern (pre-selected cities).
