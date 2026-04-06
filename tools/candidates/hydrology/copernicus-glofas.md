# Copernicus GloFAS (Global Flood Awareness System)

**Country/Region**: Global
**Publisher**: Copernicus Emergency Management Service (CEMS) / ECMWF
**API Endpoint**: `https://cds.climate.copernicus.eu/api/catalogue/v1/collections` (catalogue), `https://cds.climate.copernicus.eu/api/retrieve/v1/processes` (data retrieval)
**Documentation**: https://www.globalfloods.eu/ , https://confluence.ecmwf.int/display/CEMS/GloFAS
**Protocol**: REST (STAC / OGC Processes)
**Auth**: CDS account + API key (free registration)
**Data Format**: GRIB, NetCDF (via CDS), JSON (catalogue metadata)
**Update Frequency**: Daily (forecasts), Monthly (reanalysis updates)
**Station Count**: Global gridded data (~0.05° resolution); ~2000 calibration gauging stations
**License**: Copernicus licence (free, open, attribution required)

## What It Provides

GloFAS is the global component of CEMS for flood forecasting:
- **30-day ensemble river discharge forecasts** worldwide
- **Seasonal river discharge outlooks** (up to 4 months)
- **Historical reanalysis** of river discharge (1980-present)
- **Flood hazard maps** and return period estimates
- **Snow water equivalent** and soil moisture anomaly maps
- River discharge at 0.05° (~5km) resolution globally

## API Details

### Catalogue browsing (no auth)
```
GET https://cds.climate.copernicus.eu/api/catalogue/v1/collections
```
Returns STAC-compliant collection metadata with dataset IDs, temporal coverage, and spatial extents.

### Relevant dataset collections
Key GloFAS datasets available via CDS:
- `cems-glofas-forecast` — 30-day river discharge forecasts (daily)
- `cems-glofas-seasonal` — Seasonal river discharge forecasts
- `cems-glofas-reforecast` — Historical reforecasts for calibration
- `cems-glofas-historical` — River discharge reanalysis (1980-present)
- `sis-hydrology-variables-derived-seasonal-forecast` — Monthly mean river discharge for Europe

### Data retrieval (requires auth)
Data is accessed via the CDS API using the `cdsapi` Python package:
```python
import cdsapi
client = cdsapi.Client()
client.retrieve('cems-glofas-forecast', {
    'system_version': 'operational',
    'hydrological_model': 'lisflood',
    'variable': 'river_discharge_in_the_last_24_hours',
    'year': '2026',
    'month': '04',
    'day': '06',
    'leadtime_hour': ['24', '48', '72'],
    'format': 'grib'
}, 'glofas_forecast.grib')
```

### Authentication
1. Register at https://cds.climate.copernicus.eu/
2. Obtain API key from user profile
3. Configure `.cdsapirc` file or pass credentials to client

## Freshness Assessment

- Forecast data updated daily with 24-hour latency
- GloFAS v4.0 is operational (2024+) with 0.05° resolution
- Reanalysis data updated monthly, trailing by 2-3 months
- Operational system running continuously at ECMWF

## Entity Model

- **Grid cell**: lat/lon at 0.05° resolution (globally)
- **Forecast**: variable (river discharge), lead time (24h-720h), ensemble member, timestamp
- **Reanalysis**: variable, timestamp (daily since 1980)
- **Return periods**: 1.5y, 2y, 5y, 20y flood levels per grid cell
- Variables: `river_discharge_in_the_last_24_hours`, `snow_depth_water_equivalent`, `soil_wetness_index`

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 2 | STAC catalogue is clean; data retrieval is async batch processing, not streaming REST |
| Data Richness | 3 | Global river discharge forecasts, reanalysis, hazard maps, ensemble probabilities |
| Freshness | 2 | Daily forecasts but with 24h+ latency; not truly real-time gauge readings |
| Station Coverage | 3 | Global gridded data at 5km resolution — covers every river in the world |
| Documentation | 3 | Extensive ECMWF Confluence docs, tutorials, Jupyter notebooks |
| License/Access | 2 | Free registration required; Copernicus licence (open, attribution) |
| **Total** | **15/18** | |

## Notes

- GloFAS is model-derived river discharge, not in-situ gauge readings — fundamentally different from station-based sources
- Ideal as a gap-filler for countries without open gauge data (Africa, parts of Asia, South America)
- GRIB/NetCDF format requires specialized parsing (not simple JSON)
- Async data retrieval: submit request → wait for processing → download — not suitable for real-time polling
- Could complement station-based data by providing forecasts and climatological context
- GloFAS v4.0 uses LISFLOOD hydrological model calibrated at ~2000 gauging stations worldwide
- European EFAS (European Flood Awareness System) provides higher resolution for Europe
- CDS API follows OGC Processes standard — modern but complex
