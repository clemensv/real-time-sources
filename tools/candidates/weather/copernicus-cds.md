# Copernicus Climate Data Store (CDS)

**Country/Region**: Global
**Publisher**: Copernicus Climate Change Service (C3S), operated by ECMWF
**API Endpoint**: `https://cds.climate.copernicus.eu/api`
**Documentation**: https://cds.climate.copernicus.eu/how-to-api
**Protocol**: REST API + Python client library (`cdsapi`)
**Auth**: Personal access token (free registration required)
**Data Format**: GRIB, NetCDF (via download requests)
**Update Frequency**: Varies — ERA5 reanalysis ~5 days lag, some products near-real-time
**License**: Copernicus License (free for all uses, including commercial)

## What It Provides

The Copernicus Climate Data Store is the EU's flagship climate data service, providing access to the world's most comprehensive collection of climate datasets. While primarily a climate platform, several products approach near-real-time:

- **ERA5 Reanalysis**: The gold standard global atmospheric reanalysis. Hourly data on pressure and single levels, covering 1940–present. 31 km resolution, 137 pressure levels. Parameters: temperature, wind, humidity, pressure, precipitation, radiation, clouds, soil moisture, and hundreds more.

- **ERA5-Land**: Higher-resolution (9 km) land surface reanalysis.

- **Seasonal Forecasts**: Multi-model seasonal prediction ensembles from ECMWF, Météo-France, DWD, CMCC, NCEP, JMA, and UKMO.

- **Climate Projections**: CMIP6 global climate model output.

- **Satellite-Derived Products**: Climate data records from ESA CCI and EUMETSAT.

- **Near-Real-Time Products**:
  - ERA5 Preliminary data (updated daily with ~5 day lag)
  - CAMS (Copernicus Atmosphere Monitoring Service) air quality forecasts
  - Global fire radiative power
  - Sea surface temperature and sea ice

- **Sectoral Climate Indicators**: Pre-computed indicators for energy, agriculture, health, water management.

## API Details

The CDS API uses an asynchronous request-download pattern:

1. **Register** at cds.climate.copernicus.eu and obtain a personal access token.
2. **Configure** `~/.cdsapirc` with URL and key.
3. **Submit** a request specifying dataset, variables, time range, and area.
4. **Wait** for the server to process (can be seconds to hours depending on request size).
5. **Download** the result file (GRIB or NetCDF).

Python client:
```python
import cdsapi
client = cdsapi.Client()
client.retrieve('reanalysis-era5-pressure-levels', {
    'product_type': ['reanalysis'],
    'variable': ['temperature'],
    'year': ['2026'], 'month': ['04'], 'day': ['01'],
    'time': ['12:00'],
    'pressure_level': ['850'],
    'data_format': 'grib',
}, 'download.grib')
```

A newer REST API is available via `ecmwf-datastores-client` package with catalogue browsing and async job management.

Probed root endpoint — received welcome JSON confirming API is active.

## Freshness Assessment

- ERA5 preliminary: ~5-day latency (near-real-time by climate standards).
- CAMS air quality: Daily forecasts, near-real-time analysis.
- Seasonal forecasts: Monthly updates.
- Climate projections: Static datasets, updated per CMIP cycle.
- This is fundamentally a climate data store, not a real-time weather service. Latency is measured in days, not minutes.

## Entity Model

- **Dataset**: Named datasets with versioning (e.g., `reanalysis-era5-pressure-levels`).
- **Variable**: Standardized CF-convention variable names (e.g., `temperature`, `u_component_of_wind`).
- **Grid**: Regular lat/lon grids at varying resolutions (0.25° for ERA5, ~0.1° for ERA5-Land).
- **Time**: Hourly, daily, monthly aggregations depending on product.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | 5-day lag for ERA5; this is climate data, not real-time weather |
| Openness | 2 | Free registration + token, Copernicus License (very permissive) |
| Stability | 3 | EU-funded via ECMWF, operational since 2018, flagship Copernicus service |
| Structure | 2 | GRIB/NetCDF formats require specialized libraries; async download pattern |
| Identifiers | 3 | CF-convention variables, dataset naming, DOIs for datasets |
| Additive Value | 3 | ERA5 is the global reference reanalysis; unique climate monitoring data |
| **Total** | **14/18** | |

## Notes

- ERA5 is the most-cited atmospheric reanalysis dataset in the world. If your use case needs historical weather data or climate monitoring, CDS is the authoritative source.
- The 5-day latency makes this unsuitable for real-time weather applications, but the "Preliminary" product and CAMS forecasts push closer to operational timeliness.
- GRIB and NetCDF formats are standard in meteorology but require libraries like `cfgrib`, `xarray`, or `eccodes` to process.
- The asynchronous request pattern means integration requires job management (submit → poll → download).
- The CDS catalogue contains 200+ datasets — navigating it requires understanding of climate data taxonomy.
- Complements the already-researched ECMWF Open Data candidate (which provides the IFS model output directly in near-real-time GRIB2 files).
- The new `ecmwf-datastores-client` package provides a more modern API with catalogue browsing and async job management.
