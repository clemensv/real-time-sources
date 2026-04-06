# NILU Norway (Norwegian Institute for Air Research)

**Country/Region**: Norway
**Publisher**: NILU (Norsk institutt for luftforskning) / Norwegian Environment Agency (Miljødirektoratet)
**API Endpoint**: `https://api.nilu.no/`
**Documentation**: https://api.nilu.no/ (self-documenting root)
**Protocol**: REST
**Auth**: API Key (required)
**Data Format**: JSON
**Update Frequency**: Hourly
**License**: Norwegian Licence for Open Government Data (NLOD)

## What It Provides

NILU operates Norway's national air quality monitoring and data API on behalf of the Norwegian Environment Agency (Miljødirektoratet). The API provides both the Norwegian Air Quality Index and raw measurement data from monitoring stations across Norway. It covers key urban areas (Oslo, Bergen, Trondheim, Stavanger) and background sites. Measured pollutants include PM10, PM2.5, NO₂, O₃, SO₂, and CO. The public-facing portal is luftkvalitet.miljodirektoratet.no.

## API Details

- **Base URL**: `https://api.nilu.no/`
- **Key Endpoints**:
  - `GET /aq/utd` — latest air quality index and measured values (filters: areas, stations, components)
  - `GET /aq/utd/{lat}/{lon}/{radius}` — location-based query (max 20 km radius); method=within for all series
  - `GET /aq/historical/{from}/{to}/{station}` — historical AQI data (max 1-year span; date format: yyyy-mm-dd)
  - `GET /obs/utd` — latest raw observations (same filters)
  - `GET /obs/historical/{from}/{to}/{station}` — historical raw observations
  - `GET /lookup/areas` — list of monitoring areas
  - `GET /lookup/stations` — list of monitoring stations
  - `GET /lookup/components` — list of measured components
- **Filters**: Use semicolons for multiple values: `areas=bergen;trondheim`, `components=pm10;no2`
- **Auth**: API key required (returns 401 without); obtain from NILU
- **Spatial Query**: Supports lat/lon/radius queries — unique feature for location-based apps

## Freshness Assessment

Latest measurement data is available via the `/aq/utd` and `/obs/utd` endpoints. Updates are hourly. Historical queries support date-time precision to the minute (`yyyy-mm-dd hh24:mi`). Data is provided from Norway's national network stations.

## Entity Model

- **Area** → monitoring area (e.g., Oslo, Bergen, Trondheim)
- **Station** → located within an area, with metadata
- **Component** → measured pollutant (PM10, PM2.5, NO₂, O₃, etc.)
- **AQ Index** → station × component × datetime → value + index category
- **Observation** → station × component × datetime → raw measured value

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly latest data |
| Openness | 2 | API key required; NLOD licence |
| Stability | 3 | NILU/government-backed; well-documented self-describing API |
| Structure | 3 | Clean REST with spatial queries; semicolon multi-filters |
| Identifiers | 2 | Area/station names used as filters; lookup endpoints for enumeration |
| Additive Value | 2 | Norway-only; spatial query feature is unique |
| **Total** | **15/18** | |

## Notes

- The API requires authentication (returns HTTP 401 without a key). An API key must be obtained from NILU — check their website or contact them.
- Some lookup endpoints (e.g., `/lookup/areas`) returned HTTP 410 (Gone) during testing, suggesting a possible migration to v2. The main `/aq/utd` endpoints still require auth rather than being removed.
- The spatial query feature (`/aq/utd/{lat}/{lon}/{radius}`) is a standout — most other air quality APIs only offer station-based queries.
- The `method=within` parameter returns all timeseries within a radius, which is ideal for mobile apps.
- The public portal (luftkvalitet.miljodirektoratet.no) is a JavaScript SPA that likely calls this API internally.
- Norway has relatively clean air overall, but Bergen and Oslo can have PM/NO₂ episodes, especially in winter inversions.
