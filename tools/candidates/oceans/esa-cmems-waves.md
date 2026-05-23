# Copernicus CMEMS Wave Height Analysis

- **Country/Region**: Global oceans
- **Endpoint**: https://data.marine.copernicus.eu/products
- **Protocol**: ERDDAP, OPeNDAP
- **Auth**: Free account
- **Format**: NetCDF
- **Freshness**: Daily (1-day lag)
- **Score**: 10/18

## Overview

CMEMS provides global **significant wave height (Hs)** and wave period products:

- **Product**: `GLOBAL_ANALYSISFORECAST_WAV_001_027` (0.2° ~20 km)
- **Variables**: Hs (m), wave period (s), wave direction (°), swell vs. wind-sea
- **Daily analysis** + 10-day forecast
- **1-day lag** for analysis

Used for: shipping route optimization, offshore operations, coastal engineering.

## Verdict

⚠️ **Maybe** — Daily gridded waves. Could extract along **shipping corridors** (trans-Atlantic,
Suez Canal approaches, Drake Passage) and emit daily Hs summaries. Account required.

| Criterion | Score |
|-----------|-------|
| Value | 2 (maritime safety, but in-situ buoys better) |
| Freshness | 1 (daily) |
| Openness | 1 |
| Schema | 3 |
| Machine-readability | 2 |
| Repo fit | 1 (grid → extract corridors) |

**Total: 10/18** — **Maybe**. **NOAA NDBC buoys** (already in repo) provide **hourly Hs**
measurements at fixed stations with no lag — better fit than CMEMS gridded product.
