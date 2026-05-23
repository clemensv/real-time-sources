# Copernicus Marine Service Sea Ice Daily Analysis

- **Country/Region**: Arctic, Antarctic, Baltic
- **Endpoint**: https://data.marine.copernicus.eu/products
- **Protocol**: ERDDAP, OPeNDAP
- **Auth**: Free account
- **Format**: NetCDF
- **Freshness**: Daily (1-day lag)
- **Score**: 10/18

## Overview

CMEMS produces **daily sea ice concentration, extent, and thickness** products:

- **Arctic**: `ARCTIC_ANALYSISFORECAST_PHY_002_001_a` (10 km)
- **Antarctic**: `ANTARCTIC_ANALYSISFORECAST_PHY_002_011` (4 km)
- **Baltic Sea**: `BALTICSEA_ANALYSISFORECAST_PHY_003_006` (2 km)
- **Daily updates**, 1-day lag
- **Variables**: ice concentration (%), ice thickness (m), ice drift (cm/s)

Used for: shipping route planning, climate monitoring, polar research.

## Verdict

⚠️ **Maybe** — Daily **gridded ice data**. Could aggregate by shipping corridors (Northern
Sea Route, Northwest Passage) and emit daily ice concentration/thickness summaries.
Account required + bulk download model.

| Criterion | Score |
|-----------|-------|
| Value | 3 (navigation, climate) |
| Freshness | 1 (daily, 1-day lag) |
| Openness | 1 (account) |
| Schema | 3 |
| Machine-readability | 2 |
| Repo fit | 0 (grid data, extract routes) |

**Total: 10/18** — **Maybe**. Build if regional aggregation pattern adopted.
