# PurpleAir

**Country/Region**: Global (concentrated in North America)
**Publisher**: PurpleAir, Inc.
**API Endpoint**: `https://api.purpleair.com/v1/`
**Documentation**: https://develop.purpleair.com/ (PurpleAir Develop portal)
**Protocol**: REST
**Auth**: API Key (free registration at develop.purpleair.com; read and write keys)
**Data Format**: JSON
**Update Frequency**: Real-time (~2 minutes per sensor)
**License**: Proprietary (free for non-commercial use; commercial use requires agreement)

## What It Provides

PurpleAir operates the largest commercial low-cost sensor network for air quality, with 30,000+ sensors worldwide (primarily US, but expanding globally). Each sensor has dual laser particle counters measuring PM1.0, PM2.5, and PM10, plus temperature, humidity, and pressure. The API provides both real-time and historical data access.

## API Details

- **Base URL**: `https://api.purpleair.com/v1/`
- **Key Endpoints**:
  - `GET /sensors` — list sensors (filterable by bounding box, location type, modified since, etc.)
  - `GET /sensors/{sensor_index}` — single sensor data
  - `GET /sensors/{sensor_index}/history` — historical data
  - `GET /groups` — sensor groups
  - `GET /keys` — API key info
- **Query Parameters**: `fields` (select specific fields), `location_type` (outdoor/indoor), `nwlng/nwlat/selng/selat` (bounding box), `modified_since` (Unix timestamp for delta queries)
- **Authentication**: `X-API-Key` header with read or write key
- **Rate Limits**: Based on API key tier; free tier has limits
- **Fields**: Very granular — pm2.5, pm10, pm1.0 (CF=1 and ATM), 0.3/0.5/1.0/2.5/5.0/10.0 µm particle counts, temperature, humidity, pressure, ADC, RSSI, uptime

## Freshness Assessment

Sensors report every ~2 minutes. The `modified_since` parameter enables efficient polling for only changed sensors. Real-time data is the primary use case.

## Entity Model

- **Sensor** → sensor_index, name, lat/lon, location_type (outdoor/indoor), model, firmware
- **Sensor** → has channels A and B (dual laser counters for QA)
- **Reading** → pm1.0, pm2.5, pm10, temperature, humidity, pressure, particle counts
- **History** → timestamp + field values for historical queries
- **Group** → collection of sensors (user-defined)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | ~2 min updates, delta query support |
| Openness | 1 | API key required; non-commercial only; proprietary license |
| Stability | 2 | Commercial company, API has changed before (v1 replaced earlier API) |
| Structure | 3 | Clean JSON, well-documented fields, OpenAPI-like spec |
| Identifiers | 3 | Stable sensor_index, consistent field names |
| Additive Value | 2 | Largest low-cost network; also in OpenAQ |
| **Total** | **14/18** | |

## Notes

- PurpleAir's dual-channel design (A+B lasers) enables data quality assessment — if channels disagree significantly, the sensor may be compromised.
- The `modified_since` parameter is excellent for incremental polling — only returns sensors that reported new data since the given timestamp.
- License is restrictive: free for personal/research/non-commercial use. Commercial use requires explicit agreement with PurpleAir.
- US EPA developed a correction factor for PurpleAir PM2.5 data (the "ALT-CF3" or "US EPA" correction) to align with regulatory monitors.
- Already ingested by OpenAQ, but direct API gives more granular data (particle counts, dual channels, historical).
