# SMHI Open Data — Weather Observations & Forecasts

**Country/Region**: Sweden
**Publisher**: SMHI (Swedish Meteorological and Hydrological Institute)
**API Endpoint**: `https://opendata-download-metobs.smhi.se/api/` (observations), `https://opendata-download-metfcst.smhi.se/api/` (forecasts)
**Documentation**: https://opendata.smhi.se/apidocs/
**Protocol**: REST (content-negotiated: JSON, XML, Atom)
**Auth**: None (fully open, no API key required)
**Data Format**: JSON, XML, Atom, CSV
**Update Frequency**: Hourly (most observation parameters), 1–10 min for some, model forecasts updated per run
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

## What It Provides

SMHI's open data platform offers several weather-related APIs:

- **Meteorological Observations** (`metobs`): Historical and real-time observations from ~700 Swedish weather stations. Parameters include:
  - Air temperature (instantaneous, min, max, monthly mean)
  - Wind speed and gusts
  - Dew point temperature
  - Global irradiance (solar radiation)
  - Precipitation (multiple aggregation periods)
  - Relative humidity
  - Air pressure
  - Snow depth
  - Cloud cover, visibility, weather phenomena

- **Meteorological Forecasts** (`metfcst`): Point-based forecasts from the PMP3g model, providing hourly data for any coordinate in Sweden and Nordic region.

- **Meteorological Analysis** (`mesan`): Gridded analysis products combining observations and model data (MESAN system).

- **Weather Warnings**: Severe weather warnings for Sweden.

## API Details

The API follows a hierarchical REST pattern:
```
/api/version/{version}/parameter/{parameterId}/station/{stationId}/period/{period}/data.json
```

The version endpoint lists all available parameters with metadata (unit, bounding box, update frequency). Each parameter leads to stations, then to time periods (latest-hour, latest-day, latest-months, corrected-archive).

The forecast API uses:
```
/api/category/pmp3g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json
```

No authentication needed. Content negotiation supports JSON, XML, and Atom.

## Freshness Assessment

- Observations: Most parameters update hourly, with the "latest-hour" period always containing the most recent reading.
- The underlying data has timestamps, and the API `updated` field (Unix epoch ms) indicates last modification.
- Forecasts: The PMP3g model runs every ~6 hours.
- Very responsive API — probed the version endpoint and got immediate JSON response.

## Entity Model

- **Parameter**: Identified by numeric key (e.g., 21 = "Byvind"/gust wind, 39 = dew point, 22 = air temp monthly mean)
- **Station**: Identified by numeric station ID, with lat/lon
- **Observation**: Timestamped value with quality flag
- **Forecast**: Point forecast with hourly time steps, multiple parameters per response

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly observations, frequently updated forecasts |
| Openness | 3 | No authentication required, CC BY 4.0 license |
| Stability | 3 | Government institute, well-maintained API with versioning |
| Structure | 3 | Clean REST with JSON, hierarchical resource model |
| Identifiers | 3 | Stable numeric parameter and station IDs |
| Additive Value | 2 | Sweden-only coverage, but comprehensive; complements Nordic data |
| **Total** | **17/18** | |

## Notes

- One of the most developer-friendly meteorological APIs available — no auth, clean JSON, clear hierarchy.
- The `smhi-hydro` directory in this repo already covers SMHI hydrology; this covers the weather observation/forecast side.
- The MESAN analysis product merges observations with model data for a gridded analysis — useful for spatial interpolation.
- Documentation site uses Docusaurus and renders client-side (hard to scrape), but the API itself is self-documenting via JSON responses.
- Excellent candidate for a low-friction integration.
