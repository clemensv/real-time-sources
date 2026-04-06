# US EPA AirNow

**Country/Region**: United States, Canada, Mexico
**Publisher**: US Environmental Protection Agency (EPA)
**API Endpoint**: `https://www.airnowapi.org/aq/`
**Documentation**: https://docs.airnowapi.org/
**Protocol**: REST
**Auth**: API Key (free registration at airnowapi.org)
**Data Format**: JSON, XML, CSV
**Update Frequency**: Hourly
**License**: US Public Domain (federal government data)

## What It Provides

AirNow provides real-time and forecasted Air Quality Index (AQI) data from over 2,500 monitoring stations across the US, Canada, and Mexico. It covers O₃, PM2.5, PM10, NO₂, SO₂, and CO. Data comes from 150+ local, state, tribal, provincial, and federal agencies. This is the authoritative source for US air quality data.

## API Details

- **Base URL**: `https://www.airnowapi.org/aq/`
- **Key Endpoints**:
  - `GET /observation/zipCode/current/` — current AQI by ZIP code
  - `GET /observation/latLong/current/` — current AQI by lat/lon
  - `GET /forecast/zipCode/` — forecast by ZIP code
  - `GET /forecast/latLong/` — forecast by lat/lon
  - `GET /observation/zipCode/historical/` — historical observations
  - `GET /data/` — monitoring site data by bounding box + date range
- **Output Formats**: `application/json`, `text/csv`, `application/xml`
- **Parameters**: format, zipCode/latitude/longitude, distance, date, API_KEY
- **Rate Limits**: 500 requests/hour per API key
- **Contour Maps**: KML-format contour maps for PM2.5 and O₃

## Freshness Assessment

Observations are updated hourly. Data is preliminary (not fully QA'd) and subject to change. Official regulatory data must come from EPA's AQS system. Forecasts are issued daily for 500+ cities.

## Entity Model

- **Reporting Area** — geographic region with forecast/observation
- **Observation** → AQI value, category, pollutant, date/hour, reporting area
- **Monitoring Site** → lat/lon, parameters measured, agency
- **Forecast** → AQI category, pollutant, date, discussion text

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly observations, daily forecasts |
| Openness | 3 | US Public Domain, free API key |
| Stability | 3 | US federal agency, long-running program |
| Structure | 2 | Simple flat JSON; no nested relationships |
| Identifiers | 2 | ZIP-code and lat/lon based queries; site IDs in bounding box API |
| Additive Value | 2 | US/Canada/Mexico only; already in OpenAQ |
| **Total** | **15/18** | |

## Notes

- AirNow data is already aggregated into OpenAQ, so direct integration is only needed if you want the authoritative US source or forecast data (which OpenAQ does not carry).
- The API key is free but has modest rate limits (500/hr).
- Forecast text includes meteorological discussion useful for context.
- Contour map KML files are unique to AirNow and not available via OpenAQ.
- Data is explicitly preliminary — not for regulatory use.
