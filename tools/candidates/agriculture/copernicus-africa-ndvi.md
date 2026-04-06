# Copernicus Africa NDVI / Vegetation Health

- **Country/Region**: Pan-African
- **Endpoint**: `https://land.copernicus.eu/global/products/ndvi`
- **Protocol**: HTTP (file download) / WMS
- **Auth**: Free registration for Copernicus Data Store
- **Format**: GeoTIFF, NetCDF
- **Freshness**: Dekadal (10-day composites)
- **Docs**: https://land.copernicus.eu/global/products/ndvi
- **Score**: 12/18

## Overview

The Copernicus Global Land Service provides satellite-derived vegetation indices for
all of Africa at 300m resolution. NDVI (Normalized Difference Vegetation Index) and
related products are the primary tool for monitoring:

- **Crop health**: Green vegetation vigor correlates with crop condition
- **Drought impact**: Declining NDVI signals agricultural drought
- **Rangeland condition**: Critical for pastoralist communities
- **Deforestation**: Persistent NDVI decline indicates land cover change
- **Locust habitat**: Green vegetation in normally arid areas indicates potential
  locust breeding grounds

For African food security monitoring, NDVI is second only to rainfall as a predictor
of harvest outcomes.

## Endpoint Analysis

Copernicus Global Land Service products:
| Product | Resolution | Frequency | Coverage |
|---------|-----------|-----------|----------|
| NDVI | 300m | Dekadal (10-day) | Global |
| LAI (Leaf Area Index) | 300m | Dekadal | Global |
| FAPAR | 300m | Dekadal | Global |
| DMP (Dry Matter Productivity) | 300m | Dekadal | Global |
| Soil Water Index | 1km | Daily | Global |

Access via Copernicus Climate/Land Data Store:
```python
import cdsapi
c = cdsapi.Client()
c.retrieve('satellite-ndvi', {
    'variable': 'ndvi',
    'version': '3.0',
    'year': '2026',
    'month': '03',
    'nominal_day': ['11', '21'],
    'area': [37, -20, -35, 55],  # Africa
    'format': 'zip'
})
```

Also available as WMS map tiles for visualization.

## Integration Notes

- **Raster processing**: Like CHIRPS, this requires spatial data processing. Not a
  simple JSON API call.
- **Anomaly approach**: The key signal is NDVI anomaly (current vs historical average).
  Below-normal NDVI in agricultural zones indicates potential crop failure.
- **Zone statistics**: Pre-compute statistics for administrative regions (districts,
  counties) and emit CloudEvents with per-zone NDVI status.
- **FEWS NET pipeline**: CHIRPS (rainfall) + NDVI (vegetation) + FEWS NET (food security)
  forms the complete early warning chain used by humanitarian agencies in Africa.
- **10-day cadence**: Matches the dekadal reporting cycle used in African agriculture.
- **Soil Water Index**: The daily SWI product could provide a higher-frequency signal
  for near-real-time agricultural monitoring.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Dekadal (10-day) |
| Openness | 2 | Free CDS registration |
| Stability | 3 | EU Copernicus operational |
| Structure | 2 | GeoTIFF/NetCDF (spatial processing required) |
| Identifiers | 1 | Product/date-based |
| Richness | 2 | NDVI, LAI, FAPAR, DMP, SWI |
