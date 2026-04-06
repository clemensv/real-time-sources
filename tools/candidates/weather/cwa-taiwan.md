# Taiwan CWA (Central Weather Administration) Open Data

**Country/Region**: Taiwan
**Publisher**: CWA (Central Weather Administration, formerly CWB — 交通部中央氣象署)
**API Endpoint**: `https://opendata.cwa.gov.tw/api/v1/rest/datastore/`
**Documentation**: https://opendata.cwa.gov.tw/dist/opendata-swagger.html (Swagger UI)
**Protocol**: REST API (OpenAPI/Swagger)
**Auth**: API Key (free registration required)
**Data Format**: JSON
**Update Frequency**: Real-time (observations), hourly (forecasts), per event (warnings)
**License**: Taiwan Open Government Data License

## What It Provides

CWA (renamed from CWB in 2023) operates Taiwan's comprehensive weather observation and forecast infrastructure, exposed through a well-documented Swagger/OpenAPI interface:

- **Surface Observations** (O-A0001-001, etc.): Real-time automated weather station data from CWA's network of ~700+ stations across Taiwan. Parameters include temperature, humidity, wind, pressure, rainfall.

- **Weather Forecasts**: Multi-day forecasts for 368 townships covering all of Taiwan, including:
  - 36-hour township-level forecasts
  - 7-day general forecasts
  - County/city level forecasts

- **Severe Weather Warnings**: Typhoon warnings (critical for Taiwan), heavy rain, thunderstorm, cold surge, and other hazard alerts.

- **Earthquake Data**: Real-time earthquake reports — Taiwan sits on an active subduction zone and has one of the world's densest seismic networks.

- **Radar Data**: Composite radar imagery for the Taiwan region.

- **Tide and Marine Data**: Tidal predictions and marine weather forecasts.

- **Astronomical Data**: Sunrise/sunset, moonrise/moonset.

- **Climate Statistics**: Historical climate data and normals.

## API Details

The API uses the standard datastore pattern common to Taiwan's open data platform:
```
GET https://opendata.cwa.gov.tw/api/v1/rest/datastore/{dataset-id}?Authorization={API_KEY}&limit=10
```

Dataset IDs follow a classification scheme (e.g., O-A0001-001 for automatic station observations). The Swagger UI at `/dist/opendata-swagger.html` documents all available endpoints.

API key is passed via the `Authorization` query parameter. Registration is free at opendata.cwa.gov.tw — no phone number or special requirements.

Probed endpoint returned HTTP 401 without key — confirms the API is active and requires authentication.

## Freshness Assessment

- Automatic station observations: Real-time (minutes).
- Forecasts: Updated multiple times daily.
- Warnings: Real-time as conditions change.
- Earthquake reports: Within minutes of events.
- Taiwan's position in the western Pacific typhoon belt makes real-time tropical cyclone data especially critical.

## Entity Model

- **Station**: Station ID + name + lat/lon + elevation.
- **Dataset**: Classified by ID (e.g., O-A0001-001) with metadata.
- **Observation**: Multi-parameter readings per station with timestamps.
- **Township**: 368 administrative divisions for forecast granularity.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time observations, real-time warnings, rapid earthquake reports |
| Openness | 2 | Free API key registration, no special requirements |
| Stability | 3 | National weather agency, modern OpenAPI infrastructure |
| Structure | 3 | Swagger/OpenAPI documented, JSON responses, clear dataset classification |
| Identifiers | 3 | Dataset IDs, station IDs, township codes — well-structured |
| Additive Value | 3 | Taiwan/western Pacific coverage, typhoon tracking, dense earthquake network |
| **Total** | **17/18** | |

## Notes

- CWA was renamed from CWB (Central Weather Bureau) in 2023 when it was elevated to administration-level status — the open data platform URLs still use `cwa.gov.tw`.
- The Swagger/OpenAPI documentation makes this one of the more developer-friendly Asian met service APIs.
- Taiwan's ~700 weather stations on a 36,000 km² island provide extremely dense coverage.
- Earthquake data is uniquely valuable — Taiwan's seismic network can locate earthquakes within seconds.
- The typhoon warning system is mission-critical for Taiwan, which is struck by several typhoons annually.
- Registration process is reportedly straightforward and accessible to international users.
- Documentation is primarily in Traditional Chinese, but the Swagger interface makes endpoint discovery feasible even without language skills.
