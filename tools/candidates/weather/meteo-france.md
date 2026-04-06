# Météo-France Open Data

**Country/Region**: France
**Publisher**: Météo-France (French national meteorological service)
**API Endpoint**: `https://portail-api.meteofrance.fr/`
**Documentation**: https://confluence-meteofrance.atlassian.net/wiki/spaces/OpenDataMeteoFrance/overview and https://meteo.data.gouv.fr/
**Protocol**: REST API
**Auth**: API Key (free registration on the API portal)
**Data Format**: JSON, CSV, GRIB2, GeoJSON, CAP XML (warnings)
**Update Frequency**: Hourly (observations), per model run (forecasts), real-time (warnings)
**License**: Licence Ouverte / Open Licence v2.0 (Etalab)

## What It Provides

Météo-France has migrated its open data from the legacy `donneespubliques.meteofrance.fr` to two new platforms:

- **API Portal** (`portail-api.meteofrance.fr`): Programmatic REST access to weather data including:
  - Real-time observations from ~600 surface stations across France (temperature, humidity, wind, precipitation, pressure)
  - AROME (1.3 km France), ARPEGE (global ~10 km) model outputs in GRIB2
  - Site-specific forecasts
  - Weather warnings (vigilance météorologique) in CAP XML
  - Radar precipitation composites
  - Climate normals and historical data

- **meteo.data.gouv.fr**: Bulk data download portal on the French government's data infrastructure.

## API Details

The API portal uses OAuth2/API key authentication. After registration, users receive an application ID and secret. REST endpoints return JSON for observations and forecasts, GRIB2 for model grids.

Key API families:
- Observation: Latest observations from synoptic and automatic weather stations
- Forecast: AROME, ARPEGE model data
- Vigilance: Severe weather warnings per department
- Radar: Precipitation radar mosaics (PANTHERE product)
- Climatology: Monthly/daily normals and historical series

## Freshness Assessment

- Observations update hourly (some stations report every 6 minutes).
- AROME model runs 4×/day (00, 06, 12, 18 UTC) with data available ~3h after run time.
- Weather warnings update in real-time when conditions change.
- Radar composites update every 5–15 minutes.

## Entity Model

- **Station**: Identified by station ID, with lat/lon and metadata
- **Observation**: Timestamped readings of multiple parameters per station
- **Forecast**: Grid-based (GRIB2) or point-based (JSON) with temporal steps
- **Warning**: Department-level vigilance with color codes (green/yellow/orange/red)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly obs, frequent model runs, real-time warnings |
| Openness | 2 | Free but requires registration; Licence Ouverte v2 |
| Stability | 3 | National met service with government mandate for open data |
| Structure | 2 | JSON/GRIB2 well-structured, but API migration in progress |
| Identifiers | 3 | Station IDs, department codes for warnings, WMO numbers |
| Additive Value | 3 | AROME 1.3km model is one of the highest-resolution operational NWP products |
| **Total** | **16/18** | |

## Notes

- The open data infrastructure is in active migration (legacy site shutting down, new Confluence docs + API portal).
- Documentation is primarily in French, which may require translation for international developers.
- The AROME 1.3 km model for metropolitan France is exceptionally high-resolution.
- France overseas territories (DOM-TOM) are also covered with specific products.
- Radar mosaics are excellent for precipitation nowcasting.
