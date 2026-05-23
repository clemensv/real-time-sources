# Copernicus Land Monitoring Service (CLMS) Hot Spot Monitoring

- **Country/Region**: Global
- **Endpoint**: https://land.copernicus.eu/global/products/ba (Burnt Area product)
- **Protocol**: WMS, WCS, file download (HTTP)
- **Auth**: None (free download)
- **Format**: GeoTIFF, NetCDF
- **Freshness**: Daily (10-day rolling product)
- **Docs**: https://land.copernicus.eu/global/products
- **Score**: 9/18

## Overview

CLMS Global Land Service provides **near-real-time vegetation monitoring** including:

- **Burnt Area (BA)** — global fire-affected pixels, 300m resolution, 10-day products
- **Hot Spot Monitoring** — active fire thermal anomalies
- **NDVI** — Normalized Difference Vegetation Index (10-day, monthly)
- **LAI / FAPAR** — Leaf Area Index, Fraction of Absorbed PAR (10-day)
- **Dry Matter Productivity (DMP)** — 10-day biomass growth

The **Burnt Area** product is derived from Sentinel-3 SLSTR and Proba-V, updated every 10 days.

## Verdict

⚠️ **Maybe** — CLMS products are **10-day aggregates**, not daily/hourly streaming. Better
suited to batch download + notification events. **EFFIS active fires** (already candidated)
provide better near-real-time fire detection. **Skip** burnt area in favor of EFFIS.

| Criterion | Score |
|-----------|-------|
| Value | 2 |
| Freshness | 1 (10-day cadence) |
| Openness | 3 |
| Schema | 2 |
| Machine-readability | 1 (bulk GeoTIFF) |
| Repo fit | 0 (grid data, 10-day) |

**Total: 9/18**
