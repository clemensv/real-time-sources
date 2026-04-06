# AQICN / World Air Quality Index (WAQI)

**Country/Region**: Global
**Publisher**: World Air Quality Index Project (non-profit)
**API Endpoint**: `https://api.waqi.info/`
**Documentation**: https://aqicn.org/api/ and https://aqicn.org/json-api/doc/
**Protocol**: REST
**Auth**: API Key (free token from aqicn.org/data-platform/token/)
**Data Format**: JSON
**Update Frequency**: Hourly to real-time (varies by source)
**License**: Non-commercial use only; attribution required; data cannot be sold or redistributed

## What It Provides

The World Air Quality Index (WAQI) project aggregates AQI data from 11,000+ stations and 1,000+ cities worldwide. It provides a unified AQI calculation (US EPA scale) across all sources, individual pollutant indices (PM2.5, PM10, O₃, NO₂, SO₂, CO), weather conditions, and 3-8 day forecasts. The `aqicn.org` website is one of the most popular air quality portals globally.

## API Details

- **Base URL**: `https://api.waqi.info/`
- **Key Endpoints**:
  - `GET /feed/{city}/?token=xxx` — AQI data for a city (e.g., `/feed/london/`)
  - `GET /feed/geo:{lat};{lng}/?token=xxx` — AQI by coordinates
  - `GET /feed/@{station_id}/?token=xxx` — AQI by station ID
  - `GET /search/?keyword={name}&token=xxx` — search stations by name
  - `GET /map/bounds/?latlng={lat1,lng1,lat2,lng2}&token=xxx` — stations within bounds
- **Response Fields**: aqi, idx (station ID), city (name, geo, url), dominentpol, iaqi (individual pollutant AQIs), time, forecast (daily PM2.5/PM10/O₃/UVI), attributions
- **Map Tile API**: Real-time AQI overlay tiles for web maps
- **Widget API**: Embeddable AQI widgets
- **Rate Limit**: 1,000 requests/second (generous)
- **Sample Response**: `{"status":"ok","data":{"aqi":157,"idx":1437,"city":{"name":"Shanghai"},"iaqi":{"pm25":{"v":157},"pm10":{"v":102},"o3":{"v":88.4},"no2":{"v":14.7}}}}`

## Freshness Assessment

Data freshness varies by upstream source. The `time` field in responses shows the observation timestamp. Most stations update hourly. The `demo` token works for testing but resolves to a default city. Forecasts extend 3-8 days for PM2.5, PM10, O₃, and UV index.

## Entity Model

- **Station** → idx (numeric ID), city name, coordinates, URL, attributions
- **Observation** → AQI (composite), dominant pollutant, individual AQI per pollutant (iaqi)
- **Pollutant** → pm25, pm10, o3, no2, so2, co (AQI-scaled values)
- **Weather** → temperature, humidity, pressure, wind
- **Forecast** → daily avg/min/max for pm25, pm10, o3, uvi

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly, with forecasts |
| Openness | 1 | Non-commercial only; data cannot be sold or redistributed |
| Stability | 2 | Non-profit project, UNEP-backed; but ToS can change without notice |
| Structure | 3 | Clean JSON, simple API, good documentation |
| Identifiers | 2 | Station idx IDs; city-based queries can be ambiguous |
| Additive Value | 2 | Global aggregator like OpenAQ; unique forecast + AQI calculation |
| **Total** | **13/18** | |

## Notes

- The license is restrictive: "data cannot be sold, used in paid applications, or redistributed as cached/archived data." For-profit use requires explicit agreement.
- The `demo` token is for testing only — when used it returns a fixed city (appeared to return Shanghai in testing, not the requested city).
- The unique value of AQICN over OpenAQ is the pre-calculated AQI (US EPA scale), forecasts, and the map tile API.
- Attribution to both WAQI and the originating EPA is mandatory.
- AQICN aggregates from many of the same sources as OpenAQ (EPA, EEA, CPCB, etc.) but adds AQI calculation and forecasting.
