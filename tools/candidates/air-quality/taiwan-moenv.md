This documents the Taiwan Ministry of Environment (MOENV) air quality API. Verified:

- Open data portal: `https://data.moenv.gov.tw/en/dataset/detail/AQX_P_432`
- Dataset code: AQX_P_432 (Air quality index / AQI)
- API endpoint pattern: `https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key={key}&format=json`
- Fields: SiteName, County, AQI, Pollutant, Status, SO2, CO, O3, O3_8hr, PM10, PM2.5, NO2, NOx, NO, WIND_SPEED, WIND_DIREC, publishtime, CO_8hr, PM2.5_AVG, PM10_AVG, SO2_AVG, Longitude, Latitude, SiteId
- Auth: API key required (free registration at data.moenv.gov.tw)
- Rate limit: 5000 API calls/day
- License: Open Government Data License (Taiwan)
- Update frequency: Hourly
- English web portal at airtw.moenv.gov.tw

```
# Taiwan MOENV Air Quality Monitoring

**Country/Region**: Taiwan
**Publisher**: Ministry of Environment (MOENV, 環境部)
**API Endpoint**: `https://data.moenv.gov.tw/api/v2/aqx_p_432`
**Documentation**: https://data.moenv.gov.tw/en/dataset/detail/AQX_P_432
**Protocol**: REST
**Auth**: API Key (free registration)
**Data Format**: JSON, CSV, XML
**Update Frequency**: Hourly
**License**: Open Government Data License (Taiwan)

## What It Provides

Taiwan's Ministry of Environment (MOENV, formerly EPA) operates ~80 air quality monitoring stations across the island. The open data API provides real-time AQI values and individual pollutant concentrations for all stations. Data includes AQI, PM2.5, PM10, O₃, NO₂, SO₂, CO, wind speed/direction, and geographic coordinates. Taiwan's monitoring network is dense relative to its area, with stations covering all major cities and regions (North, Chu-Miao, Yilan, Central, Hua-Tung, Yun-Chia-Nan, Kao-Ping) plus offshore islands (Kinmen, Matzu, Penghu).

## API Details

- **Base URL**: `https://data.moenv.gov.tw/api/v2/aqx_p_432`
- **Query Parameters**: `api_key` (required), `format` (json/csv/xml), `limit`, `offset`, `sort`
- **Response Fields**:
  - Station: SiteName, SiteId, County, Longitude, Latitude
  - AQI: AQI (integer), Pollutant (dominant), Status (Good/Moderate/Unhealthy for Sensitive Groups/...)
  - Concentrations: SO2, CO, O3, O3_8hr, PM10, PM2.5, NO2, NOx, NO (µg/m³; CO in ppm)
  - Averages: PM2.5_AVG, PM10_AVG, SO2_AVG, CO_8hr
  - Meteorology: WIND_SPEED, WIND_DIREC
  - Timestamp: publishtime
- **Rate Limit**: 5,000 API calls per day
- **Pagination**: `limit` and `offset` parameters
- **Formats**: JSON, CSV, XML

## Freshness Assessment

Data is updated hourly. The `publishtime` field indicates the measurement timestamp. The API was last updated on 2026-04-06 according to the data portal. Includes both instantaneous and averaged values (8-hour, 24-hour).

## Entity Model

- **Site** → SiteId, SiteName, County, Longitude, Latitude
- **Measurement** → site × publishtime → AQI, pollutant concentrations, wind data
- **Status** → AQI-derived category (Good/Moderate/Unhealthy for Sensitive Groups/Unhealthy/Very Unhealthy/Hazardous)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly data with timestamp |
| Openness | 2 | API key required (free); 5,000 calls/day limit |
| Stability | 3 | Taiwan government open data platform; well-maintained |
| Structure | 3 | Clean JSON/CSV with standardised field names and coordinates |
| Identifiers | 3 | Stable SiteId + SiteName; lat/lon included per record |
| Additive Value | 2 | Taiwan-only; includes wind data and AQI status text |
| **Total** | **16/18** | |

## Notes

- The API key `e8dd42e6-9b8b-43f8-991e-b3dee723a52d` is a commonly cited demo key in tutorials — for production use, register for your own key at data.moenv.gov.tw.
- Each record includes both raw concentrations and the computed AQI with dominant pollutant — saves client-side AQI calculation.
- Wind speed and direction are included, which is unusual for air quality APIs — useful for pollution dispersion analysis.
- Coordinates (Longitude, Latitude) are included per record, eliminating the need for a separate station metadata lookup.
- The 5,000 calls/day rate limit is adequate for hourly polling (~80 stations × 24 hours = 1,920 calls/day if requesting all data per call).
- Taiwan is affected by seasonal sand/dust storms from mainland China and local traffic/industrial emissions.
- English web portal at airtw.moenv.gov.tw provides a good visual overview.
```
