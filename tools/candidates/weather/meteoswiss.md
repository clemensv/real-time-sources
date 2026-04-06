# MeteoSwiss Open Data

**Country/Region**: Switzerland
**Publisher**: MeteoSwiss (Federal Office of Meteorology and Climatology)
**API Endpoint**: `https://data.geo.admin.ch/ch.meteoschweiz.messwerte-*` (via Swiss federal geoportal)
**Documentation**: https://www.meteoswiss.admin.ch/services-and-publications/service/open-government-data.html
**Protocol**: HTTP file download (OGD portal), OGC API (via geo.admin.ch)
**Auth**: None (fully open as of 2024/2025 OGD mandate)
**Data Format**: CSV, JSON, NetCDF
**Update Frequency**: 10-minute observations, hourly, daily
**License**: Open Government Data (OGD) — Swiss federal open data policy (free, including commercial use)

## What It Provides

MeteoSwiss transitioned to full open data in 2024 under Switzerland's OGD mandate. Available data includes:

- **Automatic surface observations**: Real-time 10-minute measurements from ~160 SwissMetNet stations. Parameters: temperature, precipitation, wind speed/direction, humidity, pressure, sunshine duration, radiation.

- **Manual climate observations**: Historical climate data from staffed stations.

- **Precipitation radar**: CombiPrecip product (radar + gauge composite) for Switzerland.

- **Warning data**: Natural hazard warnings for weather, including thunderstorms, heavy rain, wind, heat/cold, snow.

- **Climate normals and historical data**: Long-term climate reference values.

- **Model output**: COSMO/ICON-CH limited-area model forecasts for Switzerland and the Alpine region.

Data is published through the Swiss federal geoportal (`geo.admin.ch`) and the opendata.swiss catalog.

## API Details

Data access primarily through the Swiss federal geodata infrastructure:
```
https://data.geo.admin.ch/ch.meteoschweiz.messwerte-lufttemperatur-10min/
```

Files are organized by parameter and temporal resolution. Current measurement data is published as CSV files updated every 10 minutes.

The `opendata.swiss` catalog provides metadata and download links for all MeteoSwiss datasets.

Some datasets are also available through STAC (SpatioTemporal Asset Catalog) endpoints on the federal geoportal.

## Freshness Assessment

- 10-minute SwissMetNet observations are published with minimal delay.
- Radar composites update every 5 minutes.
- Warning data updates in real-time.
- The transition to full OGD is recent (2024), so the infrastructure is still maturing.

## Entity Model

- **Station**: SwissMetNet station ID, with metadata (name, coordinates, elevation)
- **Observation**: Timestamped parameter values at 10-min/hourly/daily resolution
- **Grid product**: Spatial coverage over Switzerland at various resolutions
- **Warning**: Regional natural hazard warnings with severity levels

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-minute observations, 5-minute radar |
| Openness | 3 | Full OGD mandate since 2024, no auth required |
| Stability | 2 | OGD infrastructure is new; still evolving |
| Structure | 2 | CSV file downloads rather than structured REST API; evolving toward OGC APIs |
| Identifiers | 2 | Station IDs stable, but API endpoint patterns still settling |
| Additive Value | 2 | Switzerland-specific; Alpine weather coverage complements Austria/France |
| **Total** | **14/18** | |

## Notes

- MeteoSwiss's transition to open data is relatively recent (2024) — a significant policy shift from their previous commercial data model.
- The Swiss federal geodata infrastructure (`geo.admin.ch`) is well-maintained but MeteoSwiss-specific APIs are still being built out.
- Alpine station coverage is valuable for mountain meteorology research.
- Data is published in multiple languages (German, French, Italian, English) reflecting Switzerland's multilingual nature.
- The COSMO/ICON-CH model output for the Alpine region is high-resolution and scientifically valuable.
- As the OGD mandate matures, expect more structured API access to emerge.
- Worth monitoring for improved API availability.
