# GeoSphere Austria (formerly ZAMG)

**Country/Region**: Austria
**Publisher**: GeoSphere Austria (formerly Zentralanstalt für Meteorologie und Geodynamik — ZAMG)
**API Endpoint**: `https://dataset.api.hub.geosphere.at/v1/`
**Documentation**: https://data.hub.geosphere.at/dataset
**Protocol**: REST API, HTTP file download
**Auth**: None (fully open, no registration required)
**Data Format**: JSON (station data), GRIB2/NetCDF (gridded), GeoJSON (warnings)
**Update Frequency**: 10-minute observations, hourly, daily; model forecasts 3-hourly runs
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

## What It Provides

GeoSphere Austria Data Hub offers 96+ datasets covering meteorological, climatological, and geophysical data:

- **TAWES 10-minute observations**: Real-time 10-minute data from Austria's dense automatic weather station network (TAWES). Parameters: pressure, humidity, precipitation, snow, sunshine, radiation, temperature, wind.

- **Hourly/daily/monthly/annual station data**: Comprehensive climate observation datasets spanning historical records to present.

- **INCA Nowcasting Analysis & Forecasts**: The INCA (Integrated Nowcasting through Comprehensive Analysis) system provides:
  - High-resolution analyses (1 km grid) of current weather conditions
  - Short-range forecasts (nowcasts) combining observations, remote sensing, and NWP

- **AROME weather model**: 2.5 km resolution forecasts for the extended Alpine region, run every 3 hours with forecasts out to 60 hours. Parameters: cloud cover, pressure, humidity, thunderstorm indicators, precipitation, radiation, temperature, wind.

- **C-LAEF ensemble**: 2.5 km convection-permitting ensemble system, run twice daily.

- **Gridded climate datasets** (SPARTACUS): Temperature, precipitation, and sunshine at 1 km resolution across Austria since 1961.

- **SNOWGRID**: Snow height and snow water equivalent analysis at 1 km.

- **Weather warnings**: GeoSphere Austria's public warning system with meteorological parameters (wind, precipitation, snow, thunderstorm, heat, cold, icing).

- **Air quality forecasts**: WRF-Chem model output for ozone, PM, NO₂.

## API Details

The Data Hub provides per-dataset API documentation. Station data typically uses:
```
GET https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min?parameters=TL,RF,RR&station_ids=11035
```

Gridded data uses HTTP download of NetCDF/GRIB2 files.

Warning data is available as GeoJSON through a web UI and API.

Each dataset page on `data.hub.geosphere.at/dataset` provides:
- API documentation link
- Web UI for interactive exploration
- Data format and temporal coverage

## Freshness Assessment

- TAWES 10-minute observations: Updated every 10 minutes from ~280 stations.
- INCA nowcasts: Updated every 15 minutes.
- AROME model: New run every 3 hours.
- Warnings: Real-time updates as conditions change.

## Entity Model

- **Station**: Identified by station ID, with metadata (name, lat/lon, elevation)
- **Observation**: Timestamped parameter values per station at 10-min/hourly/daily resolution
- **Grid**: INCA/AROME/SPARTACUS 1–2.5 km resolution grids over Austria/Alpine region
- **Warning**: Regional polygons with severity levels and meteorological parameters

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-minute observations, 15-min INCA nowcasts, 3-hour AROME runs |
| Openness | 3 | No auth required, CC BY 4.0 license |
| Stability | 3 | National agency (merged ZAMG + geological survey), modern API infrastructure |
| Structure | 2 | Mix of JSON (stations) and NetCDF/GRIB2 (grids); 96 datasets to navigate |
| Identifiers | 3 | Station IDs, dataset names with versioning |
| Additive Value | 3 | Alpine-specific models (AROME, INCA), snow/avalanche data, dense mountain stations |
| **Total** | **17/18** | |

## Notes

- GeoSphere Austria was formed in 2023 by merging ZAMG (meteorology) and GBA (geology) — the Data Hub is modern and actively maintained.
- The INCA nowcasting system is particularly strong for Alpine weather, combining radar, satellite, station data, and NWP.
- Austria's mountain terrain makes the dense station network and high-resolution models especially valuable.
- AROME at 2.5 km explicitly resolves convection — important for thunderstorm forecasting in the Alps.
- Documentation is primarily in German.
- The 96 datasets cover an unusually broad range, from basic observations to specialized products (snow, radiation, evapotranspiration indices).
