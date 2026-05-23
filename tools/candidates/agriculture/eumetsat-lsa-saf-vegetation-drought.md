# EUMETSAT LSA SAF Vegetation Indices and Drought Monitoring

- **Country/Region**: Europe, Africa (MSG disk)
- **Endpoint**: FTP: `landsaf.ipma.pt`, WMS
- **Protocol**: FTP, HDF5/NetCDF, WMS
- **Auth**: Free registration
- **Format**: HDF5, NetCDF-4
- **Freshness**: Daily (NDVI, LAI), 10-day composites
- **Docs**: https://landsaf.ipma.pt/en/products/vegetation/
- **Score**: 8/18

## Overview

LSA SAF produces vegetation and drought monitoring products from MSG SEVIRI:

| Product | Description | Cadence | Resolution |
|---------|-------------|---------|------------|
| **MDVI** | SEVIRI-derived vegetation index | Daily | 3 km |
| **FVC** | Fractional vegetation cover | 10 days | 1 km |
| **LAI** | Leaf area index | 10 days | 1 km |
| **FAPAR** | Fraction absorbed photosynthetically active radiation | 10 days | 1 km |

Applications:
- **Agricultural drought**: Vegetation stress monitoring
- **Crop yield forecasting**: NDVI/LAI correlates with biomass
- **Rangeland management**: Pasture productivity (Africa)
- **Wildfire risk**: Low vegetation moisture increases fire danger

## Why Weak

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 0 | Daily to 10-day composites — **not NRT** |
| **Openness** | 2 | Free registration |
| **Stability** | 3 | Operational LSA SAF |
| **Structure** | 3 | HDF5/NetCDF |
| **Identifiers** | 0 | Gridded field |
| **Additive value** | 0 | Daily/10-day cadence too slow |

## Verdict

**SKIP** (8/18) — Daily to 10-day cadence is **not near-real-time**. Vegetation indices change slowly (days to weeks), so this cadence is scientifically appropriate, but not for sub-hourly streaming.

**Better LSA SAF candidate**: **Fire Radiative Power** (FRP) — 15 minutes, already covered.
