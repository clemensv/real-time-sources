# FMI Open Data — Finnish Meteorological Institute

**Country/Region**: Finland
**Publisher**: Finnish Meteorological Institute (Ilmatieteen laitos / FMI)
**API Endpoint**: `https://opendata.fmi.fi/wfs` (WFS 2.0), `https://opendata.fmi.fi/timeseries`
**Documentation**: https://en.ilmatieteenlaitos.fi/open-data
**Protocol**: OGC WFS 2.0 (primary), REST/timeseries (secondary)
**Auth**: None (fully open, no registration required since 2013)
**Data Format**: GML (via WFS), JSON (via timeseries API), GRIB2/NetCDF (model data)
**Update Frequency**: 10-minute observations, model runs multiple times daily
**License**: Creative Commons Attribution 4.0 (CC BY 4.0) — free for all uses including commercial

## What It Provides

FMI's open data service is one of the most comprehensive national met data platforms:

- **Weather observations**: Real-time and historical data from FMI's station network across Finland. Parameters: temperature, humidity, wind, precipitation, pressure, visibility, cloud cover, snow depth, sunshine duration.

- **Weather forecasts**: HIRLAM/HARMONIE model output for Finland and surrounding region.

- **Radar data**: Precipitation radar composites covering Finland.

- **Marine/ocean data**: Sea level, water temperature, ice conditions from coastal and offshore stations.

- **Air quality observations**: From municipal monitoring networks (integrated).

- **Radiation measurements**: Environmental radiation monitoring (from STUK — Radiation and Nuclear Safety Authority).

- **Road weather observations**: From Fintraffic's road weather station network.

In addition to FMI's own data, the platform integrates data from the Finnish Transport Agency and the Radiation and Nuclear Safety Authority.

## API Details

Primary interface is **OGC WFS 2.0**:
```
https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature
  &storedquery_id=fmi::observations::weather::multipointcoverage
  &place=Helsinki
  &starttime=2026-04-06T00:00:00Z
  &endtime=2026-04-06T12:00:00Z
```

The WFS service supports:
- GetCapabilities: Lists all available stored queries and feature types
- GetFeature: Retrieves data using stored query IDs
- Temporal filtering (starttime/endtime)
- Spatial filtering (place name, FMISID, bbox, lat/lon)

Stored queries provide pre-defined access patterns:
- `fmi::observations::weather::multipointcoverage` — multi-station weather observations
- `fmi::forecast::hirlam::surface::point::multipointcoverage` — forecast data
- `fmi::observations::radiation::multipointcoverage` — radiation measurements
- And many more (dozens of stored queries available)

The timeseries API provides a more REST-friendly JSON interface for time-series data.

## Freshness Assessment

- Observation data: Available at 10-minute resolution, published within minutes.
- The WFS supports temporal queries, so you can always request the latest data.
- Forecast data: Updated per model run (multiple times daily).
- The service has been operational since 2013 with strong uptime.

## Entity Model

- **Station**: Identified by FMISID (FMI station ID), with name, coordinates, WMO number
- **Stored query**: Pre-defined data access pattern with typed parameters
- **Feature**: GML or GeoJSON feature representing observations or forecasts
- **Coverage**: Multi-point coverage for spatial data

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-minute observations, frequent forecast updates |
| Openness | 3 | No auth since 2013, CC BY 4.0, explicitly including commercial use |
| Stability | 3 | Government institute, operational since 2013, well-maintained |
| Structure | 2 | WFS/GML is verbose and complex to parse; timeseries API simpler |
| Identifiers | 3 | FMISID, WMO numbers, stored query IDs all stable |
| Additive Value | 3 | Finland + road weather + radiation + ice data; multi-source integration |
| **Total** | **17/18** | |

## Notes

- FMI was one of the first European met services to open all their data (2013) — a pioneer in meteorological open data.
- The WFS 2.0 interface is standards-compliant but GML is verbose compared to JSON APIs. The timeseries endpoint provides a lighter alternative.
- Road weather observations from Fintraffic and radiation data from STUK are integrated — unique multi-agency data source.
- Ice condition data for the Baltic Sea and Finnish lakes is especially valuable for maritime and inland waterway operations.
- The stored query approach provides good abstraction but requires learning FMI's query naming convention.
- Finnish documentation is excellent, with an English version available.
- Data advisory and consulting services are available for a fee.
