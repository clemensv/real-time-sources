# CHIRPS — African Rainfall Estimates

- **Country/Region**: Pan-African (global, but Africa is primary focus)
- **Endpoint**: `https://data.chc.ucsb.edu/products/CHIRPS-2.0/`
- **Protocol**: HTTP (file download)
- **Auth**: None
- **Format**: GeoTIFF, NetCDF, BIL (raster)
- **Freshness**: Dekadal (10-day) preliminary, monthly final
- **Docs**: https://www.chc.ucsb.edu/data/chirps
- **Score**: 12/18

## Overview

Climate Hazards Group InfraRed Precipitation with Station data (CHIRPS) is the gold
standard for satellite-based rainfall estimation in Africa. Developed by UC Santa
Barbara with USAID/FEWS NET funding, CHIRPS provides 40+ years of gridded rainfall
data at 0.05° (~5km) resolution.

CHIRPS is *the* dataset used by FEWS NET, WFP, FAO, and virtually every food security
and drought monitoring system operating in Africa. When you hear "below-average rainfall
in the Sahel," the analysis almost certainly used CHIRPS.

## Endpoint Analysis

Data access:
```
# Dekadal (10-day) data — most recent
https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_dekad/tifs/

# Daily data
https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/

# Monthly data
https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_monthly/tifs/
```

File naming: `chirps-v2.0.{year}.{month}.{dekad}.tif`

Spatial coverage: Africa-specific products at 0.05° resolution.

Also available through:
- **Google Earth Engine**: `ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')`
- **IRI Data Library**: Interactive subset/download
- **THREDDS**: OPeNDAP access for programmatic subsetting

## Integration Notes

- **Raster processing required**: CHIRPS data is in GeoTIFF format. Processing requires
  GDAL, rasterio, or similar libraries — not a simple JSON API.
- **Anomaly computation**: The value isn't raw rainfall but rainfall vs historical normal.
  Compute anomalies (% of average) for meaningful events.
- **Dekadal approach**: 10-day totals match the agricultural reporting cadence in Africa.
  Emit CloudEvents per dekad per administrative region with rainfall amounts and anomalies.
- **FEWS NET complement**: Combine CHIRPS rainfall with FEWS NET food security data
  for a complete early warning pipeline.
- **Google Earth Engine shortcut**: For simpler access, use Earth Engine's JavaScript/Python
  API to extract CHIRPS data for specific regions without downloading full tiles.
- **High value for agriculture**: Rainfall is the single most important variable for
  African rainfed agriculture. CHIRPS + crop calendars = crop monitoring.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Dekadal preliminary, monthly final |
| Openness | 3 | Free, public domain |
| Stability | 3 | USAID/FEWS NET backed, 40+ year record |
| Structure | 1 | GeoTIFF (requires spatial processing) |
| Identifiers | 1 | Filename-based temporal indexing |
| Richness | 2 | High-resolution gridded rainfall |
