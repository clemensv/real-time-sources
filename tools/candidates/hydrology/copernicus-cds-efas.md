# Copernicus CDS River Discharge / EFAS

**Country/Region**: Europe (EFAS), Global (CDS)
**Publisher**: Copernicus Climate Data Store (CDS) / ECMWF
**API Endpoint**: `https://cds.climate.copernicus.eu/api/catalogue/v1/collections`
**Documentation**: https://cds.climate.copernicus.eu/ , https://www.efas.eu/
**Protocol**: REST (STAC catalogue) + OGC Processes (data retrieval)
**Auth**: CDS account + API key (free registration)
**Data Format**: GRIB, NetCDF, CSV (via CDS API)
**Update Frequency**: 6-hourly (EFAS), daily (seasonal forecasts)
**Station Count**: Gridded data (5km Europe, variable global)
**License**: Copernicus licence (open, attribution required)

## What It Provides

The Copernicus Climate Data Store offers multiple river discharge datasets:

### EFAS (European Flood Awareness System)
- 10-day medium-range river discharge forecasts for Europe
- Higher resolution than GloFAS for European rivers
- Flood alert levels and return periods
- Updated every 6 hours

### Seasonal hydrology forecasts
- `sis-hydrology-variables-derived-seasonal-forecast` — monthly mean river discharge for Europe
- Derived from seasonal climate forecasts
- 7-month lead time

### ERA5-Land
- Historical land surface reanalysis including runoff
- Daily/hourly data from 1950 to near-present
- ~9km resolution globally

### CDS API catalogue (confirmed working)
```
GET https://cds.climate.copernicus.eu/api/catalogue/v1/collections
```
Returns STAC collection metadata in JSON. The processes API:
```
GET https://cds.climate.copernicus.eu/api/retrieve/v1/processes
```
Lists available data retrieval processes.

## API Details

### Catalogue browsing (no auth)
```json
{
  "type": "Collection",
  "id": "sis-hydrology-variables-derived-seasonal-forecast",
  "title": "Monthly mean river discharge forecasts for Europe"
}
```

### Data retrieval (auth required)
Uses Python `cdsapi` or direct REST calls with authentication:
```python
import cdsapi
client = cdsapi.Client()
client.retrieve('sis-hydrology-variables-derived-seasonal-forecast', {
    'variable': 'river_discharge',
    'hydrological_model': 'e_hypecatch',
    'year': '2026', 'month': '04'
}, 'output.nc')
```

## Freshness Assessment

- EFAS forecasts updated every 6 hours — near-real-time for Europe
- Seasonal forecasts updated monthly
- ERA5-Land updated with ~5 day latency
- CDS infrastructure is well-maintained and reliable

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 2 | STAC catalogue is clean JSON; data retrieval is batch/async |
| Data Richness | 3 | EFAS, seasonal forecasts, ERA5-Land, multiple models |
| Freshness | 2 | 6-hourly EFAS, but batch retrieval adds latency |
| Station Coverage | 3 | Gridded European and global coverage |
| Documentation | 3 | Excellent CDS documentation with examples |
| License/Access | 2 | Free account required; Copernicus open licence |
| **Total** | **15/18** | |

## Notes

- EFAS provides the best-resolution European river discharge forecasts
- Different from GloFAS (global) — EFAS is Europe-specific with higher resolution
- Data is model-derived, not in-situ gauge readings
- GRIB/NetCDF format requires specialized processing
- Batch retrieval model (submit→wait→download) is not suitable for real-time streaming
- Complements station-based data by providing forecasts and spatial coverage
- Could be valuable for gap-filling in countries without open gauge APIs
