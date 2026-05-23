# Copernicus CLMS Global NDVI Near-Real-Time

- **Country/Region**: Global land
- **Endpoint**: https://land.copernicus.eu/global/products/ndvi
- **Protocol**: WCS, file download
- **Auth**: None
- **Format**: GeoTIFF, NetCDF
- **Freshness**: 10-day products
- **Score**: 9/18

## Overview

CLMS Global Land Service provides **Normalized Difference Vegetation Index (NDVI)** from
Sentinel-3 and Proba-V:

- **300m resolution**
- **10-day composites** (dekadal)
- **Near-real-time** (10-day lag for current dekad)
- **Global coverage**

NDVI tracks vegetation health, crop phenology, drought impacts.

## Verdict

❌ **Skip** — 10-day aggregates are too slow for real-time streaming. Better suited to
batch analysis. **CLMS NRT is not truly real-time** (10-day processing window).

| Criterion | Score |
|-----------|-------|
| Value | 2 |
| Freshness | 1 (10-day) |
| Openness | 3 |
| Schema | 2 |
| Machine-readability | 1 (bulk GeoTIFF) |
| Repo fit | 0 (10-day grid data) |

**Total: 9/18** — **Skip**.
