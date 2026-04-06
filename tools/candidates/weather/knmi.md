# KNMI Data Platform

**Country/Region**: Netherlands
**Publisher**: KNMI (Royal Netherlands Meteorological Institute)
**API Endpoint**: `https://api.dataplatform.knmi.nl/open-data/v1/`
**Documentation**: https://developer.dataplatform.knmi.nl/open-data-api
**Protocol**: REST (file-based API)
**Auth**: API Key (anonymous key available, registered key recommended)
**Data Format**: NetCDF, GRIB2, HDF5, JSON
**Update Frequency**: 10-minute observations, hourly, daily — depending on dataset
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

## What It Provides

The KNMI Data Platform (KDP) is a file-based API providing access to Dutch meteorological datasets:

- **10-minute in-situ meteorological observations**: Real-time surface observations from ~50 KNMI automatic weather stations across the Netherlands. Parameters: temperature, humidity, wind speed/direction/gust, precipitation, pressure, visibility, cloud cover, solar radiation.
- **Hourly weather observations**: Aggregated hourly values from the same station network.
- **Daily weather observations**: Daily summaries.
- **Radar precipitation data**: Netherlands-wide radar composites.
- **Forecast model data**: HARMONIE-AROME high-resolution NWP model output.
- **Climate datasets**: Historical time series.
- **EDR API**: Environmental Data Retrieval API for OGC-compliant access.
- **WMS API**: Map layer access.
- **Notification service**: Push notifications when new files arrive.

## API Details

The Open Data API is file-oriented:
1. **List files**: `GET /datasets/{datasetName}/versions/{versionId}/files` — returns a paginated list of files in a dataset, sortable by filename or lastModified.
2. **Get download URL**: `GET /datasets/{datasetName}/versions/{versionId}/files/{filename}/url` — returns a temporary download URL.

Example dataset: `10-minute-in-situ-meteorological-observations` version `1.0`.

Three API key tiers:
- **Anonymous**: 50 req/min shared, 3000 req/hour shared (key published on docs page)
- **Registered**: 200 req/sec, 1000 req/hour (personal key via registration)
- **Bulk**: For full dataset downloads, request via email

The `X-KNMI-Deprecation` header signals when datasets/endpoints are being retired.

## Freshness Assessment

- 10-minute observations are published as new files every 10 minutes.
- The file listing API supports `sorting=desc&orderBy=lastModified` to quickly find the most recent file.
- Radar data updates every 5 minutes.
- HARMONIE-AROME forecast data available after each model run (~4×/day).

## Entity Model

- **Dataset**: Named collection with version (e.g., `10-minute-in-situ-meteorological-observations/1.0`)
- **File**: Individual data file within a dataset, identified by filename (typically includes timestamp)
- **Station**: WMO station ID within NetCDF files
- **Observation**: Timestamped parameter values per station

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-minute observation updates, 5-min radar |
| Openness | 2 | Requires API key (anonymous available but rate-limited) |
| Stability | 3 | National met institute, versioned API with deprecation policy |
| Structure | 2 | File-based (NetCDF) requires extra processing; not direct JSON observations |
| Identifiers | 3 | Dataset names versioned, WMO station IDs in files |
| Additive Value | 2 | Netherlands-focused, HARMONIE model shared with Nordics |
| **Total** | **15/18** | |

## Notes

- The file-based approach means you download NetCDF/GRIB2 files rather than querying a parameter API — more suited to batch processing than real-time point queries.
- The anonymous API key is published on the documentation page and rotates periodically (current key valid until July 2026).
- The notification service can push alerts when new data files arrive, enabling event-driven architectures.
- Swagger/OpenAPI documentation available at `https://tyk-cdn.dataplatform.knmi.nl/open-data/index.html`.
- KNMI also offers an EDR API (`/edr-api`) for standards-compliant spatial data queries.
